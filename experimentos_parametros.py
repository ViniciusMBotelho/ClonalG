"""
Execucao configurada do ClonalG e comparacao com k-Means.

Este script nao faz mais busca em grade. A cada execucao, os parametros do
ClonalG sao definidos nas constantes no topo deste arquivo. O k e fixo em toda
a execucao.
"""

import os
import warnings

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

from clonalg_core import ClonalG
from markdown_utils import dataframe_to_markdown

warnings.filterwarnings('ignore')

OUTPUT_DIR = 'resultados/etapa3_parametros'
RANDOM_SEED = 42

# Edite estes valores para controlar a proxima execucao.
N_ANTIBODIES = 50
RHO = 2.0
BETA = 10.0
REPLACE_RATE = 0.10
SELECTION_RATE = 0.85
K = 3
RUNS = 3
ITERATIONS = 50


CONFIG = {
    'n_antibodies': N_ANTIBODIES,
    'rho': RHO,
    'beta': BETA,
    'replace_rate': REPLACE_RATE,
    'selection_rate': SELECTION_RATE,
    'k': K,
    'runs': RUNS,
    'iterations': ITERATIONS,
    'seed': RANDOM_SEED,
}


def validate_config(config):
    if config['n_antibodies'] <= 0:
        raise ValueError('n_antibodies deve ser maior que zero.')
    if config['k'] < 2:
        raise ValueError('k deve ser pelo menos 2 para permitir Silhouette.')
    if not 0 <= config['replace_rate'] <= 1:
        raise ValueError('replace_rate deve estar entre 0 e 1.')
    if not 0 < config['selection_rate'] <= 1:
        raise ValueError('selection_rate deve estar no intervalo (0, 1].')
    if config['runs'] <= 0:
        raise ValueError('runs deve ser maior que zero.')
    if config['iterations'] <= 0:
        raise ValueError('iterations deve ser maior que zero.')


def load_datasets():
    datasets = {}
    for i in range(1, 6):
        path = f'datasets/DataSet{i}_scaled.csv'
        if os.path.exists(path):
            datasets[i] = pd.read_csv(path, header=None).values
            print(f'DataSet {i}: {datasets[i].shape}', flush=True)
    return datasets


def safe_silhouette(data, labels):
    if len(np.unique(labels)) < 2:
        return -1.0
    return silhouette_score(data, labels)


def run_clonalg_once(data, config, ds_id, run):
    np.random.seed(config['seed'] + ds_id * 100 + run)
    sia = ClonalG(
        n_antibodies=config['n_antibodies'],
        k=config['k'],
        rho=config['rho'],
        beta=config['beta'],
        replace_rate=config['replace_rate'],
        selection_rate=config['selection_rate'],
    )
    best_ab, history = sia.fit(data, n_iterations=config['iterations'], verbose=False)
    labels = sia.predict(data, best_ab)
    score = safe_silhouette(data, labels)
    return {
        'score': score,
        'k': len(best_ab),
        'history': history,
    }


def evaluate_dataset(data, ds_id, config):
    runs = [run_clonalg_once(data, config, ds_id, run) for run in range(config['runs'])]
    scores = [run['score'] for run in runs]
    k = config['k']

    kmeans = KMeans(n_clusters=k, n_init=30, random_state=config['seed'])
    labels_km = kmeans.fit_predict(data)
    kmeans_score = safe_silhouette(data, labels_km)

    iteration_records = []
    run_records = []
    for run_idx, run_result in enumerate(runs, start=1):
        run_records.append({
            'DataSet': ds_id,
            'Run': run_idx,
            'k': k,
            'n_antibodies': config['n_antibodies'],
            'rho': config['rho'],
            'beta': config['beta'],
            'replace_rate': config['replace_rate'],
            'selection_rate': config['selection_rate'],
            'Silhouette_Final': run_result['score'],
        })
        for iteration, affinity in enumerate(run_result['history'], start=1):
            iteration_records.append({
                'DataSet': ds_id,
                'Run': run_idx,
                'Iteracao': iteration,
                'k': k,
                'n_antibodies': config['n_antibodies'],
                'rho': config['rho'],
                'beta': config['beta'],
                'replace_rate': config['replace_rate'],
                'selection_rate': config['selection_rate'],
                'Afinidade_Euclidiana': affinity,
            })

    result = {
        'DataSet': ds_id,
        'k': k,
        'n_antibodies': config['n_antibodies'],
        'rho': config['rho'],
        'beta': config['beta'],
        'replace_rate': config['replace_rate'],
        'selection_rate': config['selection_rate'],
        'runs': config['runs'],
        'iterations': config['iterations'],
        'ClonalG_Media_Validacao': float(np.mean(scores)),
        'ClonalG_Melhor_Validacao': float(np.max(scores)),
        'ClonalG_Pior_Validacao': float(np.min(scores)),
        'KMeans_Silhouette_mesmo_k': float(kmeans_score),
        'Delta_Validacao_vs_KMeans_mesmo_k': float(np.mean(scores) - kmeans_score),
    }
    return result, iteration_records, run_records


def plot_final_comparison(df):
    fig, ax = plt.subplots(figsize=(10, 5.5))
    plot_df = df.melt(
        id_vars=['DataSet'],
        value_vars=['ClonalG_Media_Validacao', 'KMeans_Silhouette_mesmo_k'],
        var_name='Algoritmo',
        value_name='Silhouette',
    )
    plot_df['Algoritmo'] = plot_df['Algoritmo'].replace({
        'ClonalG_Media_Validacao': 'ClonalG',
        'KMeans_Silhouette_mesmo_k': 'k-Means no mesmo k',
    })
    sns.barplot(data=plot_df, x='DataSet', y='Silhouette', hue='Algoritmo', palette=['#2f6f73', '#6b6f76'], ax=ax)
    ax.set_title('ClonalG configurado vs k-Means usando k fixo')
    ax.set_xlabel('DataSet')
    ax.set_ylabel('Silhouette')
    ax.grid(axis='y', alpha=0.25)
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/comparativo_melhores_vs_kmeans.png', dpi=160)
    plt.close()


def write_markdown_report(df, config):
    lines = [
        '# Execucao Configurada do ClonalG\n',
        '- Fluxo: os parametros sao definidos nas constantes do script; o ClonalG usa k fixo.',
        '- Afinidade interna do ClonalG: distancia Euclidiana media ao centroide mais proximo, com sinal invertido.',
        '- Silhouette: usado apenas na validacao final das execucoes e na comparacao com k-Means.',
        f'- Parametros: N={config["n_antibodies"]}, rho={config["rho"]}, beta={config["beta"]}, '
        f'replace_rate={config["replace_rate"]}, selection_rate={config["selection_rate"]}, k={config["k"]}',
        f'- Repeticoes por dataset: {config["runs"]}',
        f'- Geracoes por repeticao: {config["iterations"]}',
        '',
        '## Resultados\n',
    ]

    display = df.copy()
    for col in [
        'ClonalG_Media_Validacao',
        'ClonalG_Melhor_Validacao',
        'KMeans_Silhouette_mesmo_k',
        'Delta_Validacao_vs_KMeans_mesmo_k',
    ]:
        display[col] = display[col].round(4)
    lines.append(dataframe_to_markdown(display, index=False))
    open(f'{OUTPUT_DIR}/melhores_configuracoes.md', 'w').write('\n'.join(lines))


def write_iteration_output(iteration_df, run_df, config):
    lines = [
        '# Output por Iteracao do ClonalG\n',
        '## Parametros\n',
        f'- k: {config["k"]}',
        f'- n_antibodies: {config["n_antibodies"]}',
        f'- rho: {config["rho"]}',
        f'- beta: {config["beta"]}',
        f'- replace_rate: {config["replace_rate"]}',
        f'- selection_rate: {config["selection_rate"]}',
        f'- runs: {config["runs"]}',
        f'- iterations: {config["iterations"]}',
        '',
        '## Saida final por run\n',
    ]

    run_display = run_df.copy()
    if not run_display.empty:
        run_display['Silhouette_Final'] = run_display['Silhouette_Final'].round(4)
    lines.append(dataframe_to_markdown(run_display, index=False))

    lines.extend(['', '## Afinidade interna por iteracao\n'])
    iteration_display = iteration_df.copy()
    if not iteration_display.empty:
        iteration_display['Afinidade_Euclidiana'] = iteration_display['Afinidade_Euclidiana'].round(6)
    lines.append(dataframe_to_markdown(iteration_display, index=False))

    open(f'{OUTPUT_DIR}/output_iteracoes.md', 'w').write('\n'.join(lines))


def save_outputs(df, config, iteration_df, run_df):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    df.to_csv(f'{OUTPUT_DIR}/execucao_configurada.csv', index=False)
    df.to_csv(f'{OUTPUT_DIR}/melhores_configuracoes.csv', index=False)
    df.to_csv(f'{OUTPUT_DIR}/validacao_top_configs.csv', index=False)
    df.to_csv(f'{OUTPUT_DIR}/resultados_sweep.csv', index=False)

    # Nome mantido por compatibilidade com scripts e relatorios antigos.
    df[['DataSet', 'k', 'KMeans_Silhouette_mesmo_k']].rename(
        columns={'KMeans_Silhouette_mesmo_k': 'KMeans_Silhouette'}
    ).to_csv(f'{OUTPUT_DIR}/kmeans_por_k.csv', index=False)

    plot_final_comparison(df)
    write_markdown_report(df, config)
    write_iteration_output(iteration_df, run_df, config)


def remove_grid_artifacts():
    old_files = [
        'resultados_busca_clonalg.csv',
        'impacto_parametros_grid.png',
        'impacto_n_antibodies.png',
        'impacto_replace_rate.png',
        'impacto_rho.png',
    ]
    old_files.extend(f'ranking_ds{i}.png' for i in range(1, 6))

    for filename in old_files:
        path = os.path.join(OUTPUT_DIR, filename)
        if os.path.exists(path):
            os.remove(path)


def main():
    config = dict(CONFIG)
    validate_config(config)

    print('\nExecucao configurada do ClonalG')
    print(f'Parametros: {config}\n', flush=True)

    datasets = load_datasets()
    if not datasets:
        print('Nenhum dataset pre-processado encontrado. Execute preprocessamento.py primeiro.')
        return

    rows = []
    iteration_records = []
    run_records = []
    for ds_id, data in datasets.items():
        result, ds_iteration_records, ds_run_records = evaluate_dataset(data, ds_id, config)
        rows.append(result)
        iteration_records.extend(ds_iteration_records)
        run_records.extend(ds_run_records)
        print(
            f"DS{ds_id}: k={result['k']} "
            f"ClonalG={result['ClonalG_Media_Validacao']:.4f} "
            f"| k-Means={result['KMeans_Silhouette_mesmo_k']:.4f}",
            flush=True,
        )

    df = pd.DataFrame(rows)
    iteration_df = pd.DataFrame(iteration_records)
    run_df = pd.DataFrame(run_records)
    remove_grid_artifacts()
    save_outputs(df, config, iteration_df, run_df)
    print(f'\nResultados salvos em {OUTPUT_DIR}/')


if __name__ == '__main__':
    main()
