import os
import warnings

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, davies_bouldin_score

from clonalg_core import ClonalG
from markdown_utils import dataframe_to_markdown

warnings.filterwarnings('ignore')

OUTPUT_DIR = 'resultados/etapa3_parametros'
RANDOM_SEED = 42

N_ANTIBODIES = 60
RHO = 3.5
BETA = 30.0
REPLACE_RATE = 0.40
SELECTION_RATE = 0.60
PARAMETRIC_MUTATION_SCALE = 0.05
DIVERSITY_WEIGHT = 0.15
K_CANDIDATES = [2, 3, 4, 5, 6]
RUNS = 3
ITERATIONS = 50
SILHOUETTE_SAMPLE_SIZE = 300
AFFINITY_METRIC = 'silhouette'


CONFIG = {
    'n_antibodies': N_ANTIBODIES,
    'rho': RHO,
    'beta': BETA,
    'replace_rate': REPLACE_RATE,
    'selection_rate': SELECTION_RATE,
    'parametric_mutation_scale': PARAMETRIC_MUTATION_SCALE,
    'diversity_weight': DIVERSITY_WEIGHT,
    'k_candidates': K_CANDIDATES,
    'runs': RUNS,
    'iterations': ITERATIONS,
    'seed': RANDOM_SEED,
    'silhouette_sample_size': SILHOUETTE_SAMPLE_SIZE,
    'affinity_metric': AFFINITY_METRIC,
}


def validate_config(config):
    if config['n_antibodies'] <= 0:
        raise ValueError('n_antibodies deve ser maior que zero.')
    if not config['k_candidates']:
        raise ValueError('k_candidates deve conter pelo menos um valor.')
    if any(k < 2 for k in config['k_candidates']):
        raise ValueError('todos os valores em k_candidates devem ser pelo menos 2 para permitir Silhouette.')
    if not 0 <= config['replace_rate'] <= 1:
        raise ValueError('replace_rate deve estar entre 0 e 1.')
    if not 0 < config['selection_rate'] <= 1:
        raise ValueError('selection_rate deve estar no intervalo (0, 1].')
    if config['parametric_mutation_scale'] < 0:
        raise ValueError('parametric_mutation_scale deve ser maior ou igual a zero.')
    if config['diversity_weight'] < 0:
        raise ValueError('diversity_weight deve ser maior ou igual a zero.')
    if config['runs'] <= 0:
        raise ValueError('runs deve ser maior que zero.')
    if config['iterations'] <= 0:
        raise ValueError('iterations deve ser maior que zero.')
    if config.get('affinity_metric', 'silhouette') not in {'silhouette', 'davies_bouldin'}:
        raise ValueError("affinity_metric deve ser 'silhouette' ou 'davies_bouldin'.")


def k_bounds(config):
    return min(config['k_candidates']), max(config['k_candidates'])


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


def safe_davies_bouldin(data, labels):
    if len(np.unique(labels)) < 2:
        return 999.0
    return davies_bouldin_score(data, labels)


def run_clonalg_once(data, config, ds_id, run, k):
    np.random.seed(config['seed'] + ds_id * 1000 + k * 100 + run)
    k_min, k_max = k_bounds(config)
    sia = ClonalG(
        n_antibodies=config['n_antibodies'],
        k=k,
        k_min=k_min,
        k_max=k_max,
        rho=config['rho'],
        beta=config['beta'],
        replace_rate=config['replace_rate'],
        selection_rate=config['selection_rate'],
        silhouette_sample_size=config['silhouette_sample_size'],
        parametric_mutation_scale=config['parametric_mutation_scale'],
        diversity_weight=config['diversity_weight'],
        affinity_metric=config.get('affinity_metric', 'silhouette'),
    )
    best_ab, history = sia.fit(data, n_iterations=config['iterations'], verbose=False)
    labels = sia.predict(data, best_ab)
    silhouette = safe_silhouette(data, labels)
    davies_bouldin = safe_davies_bouldin(data, labels)
    return {
        'score': silhouette,
        'silhouette': silhouette,
        'davies_bouldin': davies_bouldin,
        'k': len(best_ab),
        'k_inicial': k,
        'history': history,
    }


def evaluate_dataset(data, ds_id, config):
    candidates = []
    use_db_objective = config.get('affinity_metric', 'silhouette') == 'davies_bouldin'
    for k in config['k_candidates']:
        runs = [run_clonalg_once(data, config, ds_id, run, k) for run in range(config['runs'])]
        scores = [run['silhouette'] for run in runs]
        db_scores = [run['davies_bouldin'] for run in runs]
        best_run = min(runs, key=lambda run: run['davies_bouldin']) if use_db_objective else max(runs, key=lambda run: run['silhouette'])
        candidates.append({
            'k_inicial': k,
            'k': best_run['k'],
            'runs': runs,
            'mean': float(np.mean(scores)),
            'best': float(np.max(scores)),
            'worst': float(np.min(scores)),
            'mean_db': float(np.mean(db_scores)),
            'best_db': float(np.min(db_scores)),
            'worst_db': float(np.max(db_scores)),
        })

    best_candidate = min(candidates, key=lambda item: item['mean_db']) if use_db_objective else max(candidates, key=lambda item: item['mean'])
    runs = best_candidate['runs']
    scores = [run['silhouette'] for run in runs]
    db_scores = [run['davies_bouldin'] for run in runs]
    k = best_candidate['k']

    kmeans = KMeans(n_clusters=k, n_init=30, random_state=config['seed'])
    labels_km = kmeans.fit_predict(data)
    kmeans_score = safe_silhouette(data, labels_km)
    kmeans_db = safe_davies_bouldin(data, labels_km)

    iteration_records = []
    run_records = []
    for candidate in candidates:
        candidate_k_inicial = candidate['k_inicial']
        is_best_k = candidate is best_candidate
        for run_idx, run_result in enumerate(candidate['runs'], start=1):
            run_records.append({
                'DataSet': ds_id,
                'Run': run_idx,
                'k_inicial': candidate_k_inicial,
                'k_final': run_result['k'],
                'Melhor_k_ClonalG': is_best_k,
                'n_antibodies': config['n_antibodies'],
                'rho': config['rho'],
                'beta': config['beta'],
                'replace_rate': config['replace_rate'],
                'selection_rate': config['selection_rate'],
                'parametric_mutation_scale': config['parametric_mutation_scale'],
                'diversity_weight': config['diversity_weight'],
                'affinity_metric': config.get('affinity_metric', 'silhouette'),
                'Silhouette_Final': run_result['silhouette'],
                'DaviesBouldin_Final': run_result['davies_bouldin'],
            })
            for iteration, affinity in enumerate(run_result['history'], start=1):
                iteration_records.append({
                    'DataSet': ds_id,
                    'Run': run_idx,
                    'Iteracao': iteration,
                    'k_inicial': candidate_k_inicial,
                    'k_final': run_result['k'],
                    'Melhor_k_ClonalG': is_best_k,
                    'n_antibodies': config['n_antibodies'],
                    'rho': config['rho'],
                    'beta': config['beta'],
                    'replace_rate': config['replace_rate'],
                    'selection_rate': config['selection_rate'],
                    'parametric_mutation_scale': config['parametric_mutation_scale'],
                    'diversity_weight': config['diversity_weight'],
                    'affinity_metric': config.get('affinity_metric', 'silhouette'),
                    'Afinidade': affinity,
                })

    result = {
        'DataSet': ds_id,
        'k': k,
        'k_inicial_melhor': best_candidate['k_inicial'],
        'k_candidates': ','.join(str(candidate['k_inicial']) for candidate in candidates),
        'k_scores_medios_clonalg': ';'.join(f"{candidate['k_inicial']}->{candidate['k']}:{candidate['mean']:.4f}" for candidate in candidates),
        'n_antibodies': config['n_antibodies'],
        'rho': config['rho'],
        'beta': config['beta'],
        'replace_rate': config['replace_rate'],
        'selection_rate': config['selection_rate'],
        'parametric_mutation_scale': config['parametric_mutation_scale'],
        'diversity_weight': config['diversity_weight'],
        'affinity_metric': config.get('affinity_metric', 'silhouette'),
        'runs': config['runs'],
        'iterations': config['iterations'],
        'ClonalG_Media_Validacao': float(np.mean(scores)),
        'ClonalG_Melhor_Validacao': float(np.max(scores)),
        'ClonalG_Pior_Validacao': float(np.min(scores)),
        'ClonalG_DB_Medio_Validacao': float(np.mean(db_scores)),
        'ClonalG_DB_Melhor_Validacao': float(np.min(db_scores)),
        'ClonalG_DB_Pior_Validacao': float(np.max(db_scores)),
        'KMeans_Silhouette_mesmo_k': float(kmeans_score),
        'Delta_Validacao_vs_KMeans_mesmo_k': float(np.mean(scores) - kmeans_score),
        'KMeans_DB_mesmo_k': float(kmeans_db),
        'Delta_DB_vs_KMeans_mesmo_k': float(np.mean(db_scores) - kmeans_db),
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
    ax.set_title('ClonalG configurado vs k-Means usando k encontrado pelo ClonalG')
    ax.set_xlabel('DataSet')
    ax.set_ylabel('Silhouette')
    ax.grid(axis='y', alpha=0.25)
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/comparativo_melhores_vs_kmeans.png', dpi=160)
    plt.close()


def write_markdown_report(df, config):
    lines = [
        '# Execucao Configurada do ClonalG\n',
        '- Fluxo: o ClonalG inicia em cada k candidato e usa mutacao estrutural para adicionar/remover centroides dentro dos limites configurados; o melhor k final do ClonalG e repassado ao k-Means.',
        f'- Afinidade interna do ClonalG: {config.get("affinity_metric", "silhouette")}.',
        '- Mutacao: hibrida, com mutacao estrutural de k e mutacao parametrica gaussiana nos centroides existentes.',
        '- Selecao: combina afinidade por Silhouette com recompensa por diversidade entre anticorpos.',
        f'- Parametros: N={config["n_antibodies"]}, rho={config["rho"]}, beta={config["beta"]}, '
        f'replace_rate={config["replace_rate"]}, selection_rate={config["selection_rate"]}, '
        f'parametric_mutation_scale={config["parametric_mutation_scale"]}, diversity_weight={config["diversity_weight"]}',
        f'- Candidatos/limites de k: {",".join(str(k) for k in config["k_candidates"])}',
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
        'ClonalG_DB_Medio_Validacao',
        'ClonalG_DB_Melhor_Validacao',
        'KMeans_DB_mesmo_k',
        'Delta_DB_vs_KMeans_mesmo_k',
    ]:
        if col in display.columns:
            display[col] = display[col].round(4)
    lines.append(dataframe_to_markdown(display, index=False))
    open(f'{OUTPUT_DIR}/melhores_configuracoes.md', 'w').write('\n'.join(lines))


def write_iteration_output(iteration_df, run_df, config):
    lines = [
        '# Output por Iteracao do ClonalG\n',
        '## Parametros\n',
        f'- k_candidates: {",".join(str(k) for k in config["k_candidates"])}',
        f'- k_min: {min(config["k_candidates"])}',
        f'- k_max: {max(config["k_candidates"])}',
        f'- n_antibodies: {config["n_antibodies"]}',
        f'- rho: {config["rho"]}',
        f'- beta: {config["beta"]}',
        f'- replace_rate: {config["replace_rate"]}',
        f'- selection_rate: {config["selection_rate"]}',
        f'- parametric_mutation_scale: {config["parametric_mutation_scale"]}',
        f'- diversity_weight: {config["diversity_weight"]}',
        f'- affinity_metric: {config.get("affinity_metric", "silhouette")}',
        f'- runs: {config["runs"]}',
        f'- iterations: {config["iterations"]}',
        '',
        '## Saida final por run\n',
    ]

    run_display = run_df.copy()
    if not run_display.empty:
        run_display['Silhouette_Final'] = run_display['Silhouette_Final'].round(4)
        if 'DaviesBouldin_Final' in run_display.columns:
            run_display['DaviesBouldin_Final'] = run_display['DaviesBouldin_Final'].round(4)
    lines.append(dataframe_to_markdown(run_display, index=False))

    lines.extend(['', '## Silhouette por iteracao\n'])
    iteration_display = iteration_df.copy()
    if not iteration_display.empty:
        if 'Afinidade' in iteration_display.columns:
            iteration_display['Afinidade'] = iteration_display['Afinidade'].round(6)
    lines.append(dataframe_to_markdown(iteration_display, index=False))

    open(f'{OUTPUT_DIR}/output_iteracoes.md', 'w').write('\n'.join(lines))


def save_outputs(df, config, iteration_df, run_df):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    df.to_csv(f'{OUTPUT_DIR}/execucao_configurada.csv', index=False)
    df.to_csv(f'{OUTPUT_DIR}/melhores_configuracoes.csv', index=False)
    df.to_csv(f'{OUTPUT_DIR}/validacao_top_configs.csv', index=False)
    df.to_csv(f'{OUTPUT_DIR}/resultados_sweep.csv', index=False)

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
