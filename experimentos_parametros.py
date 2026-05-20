"""
Busca de parametros do ClonalG e comparacao com k-Means.

Fluxo atual:
1. Carrega os 5 datasets pre-processados.
2. Executa uma busca em grade do ClonalG com k variavel em K_RANGE.
3. Registra o k descoberto pelo melhor anticorpo de cada configuracao.
4. Executa k-Means usando exatamente o k descoberto pelo ClonalG.
5. Revalida as melhores configuracoes e gera CSVs, tabelas Markdown e graficos.
"""

import itertools
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
os.makedirs(OUTPUT_DIR, exist_ok=True)

K_RANGE = range(2, 7)
SEARCH_RUNS = 1
VALIDATION_RUNS = 3
N_ITERATIONS = 18
RANDOM_SEED = 42

PARAM_GRID = {
    'n_antibodies': [10, 20],
    'rho': [1.0, 2.5],
    'beta': [10],
    'replace_rate': [0.05, 0.20],
    'selection_rate': [0.50, 0.85],
}


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


def evaluate_kmeans_for_k(data, k):
    model = KMeans(n_clusters=int(k), n_init=30, random_state=RANDOM_SEED)
    labels = model.fit_predict(data)
    return safe_silhouette(data, labels)


def iter_param_grid():
    keys = list(PARAM_GRID.keys())
    for values in itertools.product(*(PARAM_GRID[key] for key in keys)):
        yield dict(zip(keys, values))


def run_clonalg_once(data, params, seed):
    np.random.seed(seed)
    sia = ClonalG(
        n_antibodies=int(params['n_antibodies']),
        k_range=(min(K_RANGE), max(K_RANGE)),
        rho=float(params['rho']),
        beta=float(params['beta']),
        replace_rate=float(params['replace_rate']),
        selection_rate=float(params['selection_rate']),
    )
    best_ab, history = sia.fit(data, n_iterations=N_ITERATIONS, verbose=False)
    labels = sia.predict(data, best_ab)
    score = safe_silhouette(data, labels)
    return score, len(best_ab), history


def summarize_runs(data, params, n_runs, seed_offset=0):
    scores = []
    discovered_ks = []
    best_history = None
    best_score = -2.0
    best_k = None

    for run in range(n_runs):
        seed = RANDOM_SEED + seed_offset + run
        score, discovered_k, history = run_clonalg_once(data, params, seed)
        scores.append(score)
        discovered_ks.append(discovered_k)
        if score > best_score:
            best_score = score
            best_k = discovered_k
            best_history = history

    return {
        'ClonalG_Media': float(np.mean(scores)),
        'ClonalG_Desvio': float(np.std(scores)),
        'ClonalG_Melhor': float(np.max(scores)),
        'ClonalG_Pior': float(np.min(scores)),
        'k_descoberto_melhor': int(best_k),
        'k_descoberto_moda': int(pd.Series(discovered_ks).mode().iloc[0]),
        'ks_descobertos': ','.join(str(k) for k in discovered_ks),
        'Historico_Melhor': best_history,
    }


def search_dataset(data, ds_id):
    print(f'\nDS{ds_id}: ClonalG buscando k em {min(K_RANGE)}..{max(K_RANGE)}', flush=True)
    rows = []
    configs = list(iter_param_grid())

    for idx, params in enumerate(configs, start=1):
        summary = summarize_runs(data, params, SEARCH_RUNS, seed_offset=idx * 100)
        k_clonalg = summary['k_descoberto_melhor']
        kmeans_score = evaluate_kmeans_for_k(data, k_clonalg)
        row = {
            'DataSet': ds_id,
            'k_descoberto_clonalg': k_clonalg,
            'k_descoberto_moda': summary['k_descoberto_moda'],
            'ks_descobertos': summary['ks_descobertos'],
            **params,
            'KMeans_Silhouette_mesmo_k': kmeans_score,
            'ClonalG_Media': summary['ClonalG_Media'],
            'ClonalG_Desvio': summary['ClonalG_Desvio'],
            'ClonalG_Melhor': summary['ClonalG_Melhor'],
            'ClonalG_Pior': summary['ClonalG_Pior'],
        }
        row['Delta_Media_vs_KMeans_mesmo_k'] = row['ClonalG_Media'] - row['KMeans_Silhouette_mesmo_k']
        rows.append(row)

        if idx % 8 == 0 or idx == len(configs):
            print(f'  {idx:>3}/{len(configs)} configs avaliadas', flush=True)

    df = pd.DataFrame(rows).sort_values('ClonalG_Media', ascending=False)
    return df


def validate_best_configs(datasets, search_df):
    rows = []

    for ds_id, data in datasets.items():
        top_configs = search_df[search_df['DataSet'] == ds_id].head(2)
        for rank, (_, cfg) in enumerate(top_configs.iterrows(), start=1):
            params = {
                'n_antibodies': int(cfg['n_antibodies']),
                'rho': float(cfg['rho']),
                'beta': float(cfg['beta']),
                'replace_rate': float(cfg['replace_rate']),
                'selection_rate': float(cfg['selection_rate']),
            }
            summary = summarize_runs(data, params, VALIDATION_RUNS, seed_offset=9000 + ds_id * 100 + rank * 10)
            k_clonalg = summary['k_descoberto_melhor']
            kmeans_score = evaluate_kmeans_for_k(data, k_clonalg)
            row = {
                'DataSet': ds_id,
                'RankBusca': rank,
                'k_descoberto_clonalg': k_clonalg,
                'k_descoberto_moda': summary['k_descoberto_moda'],
                'ks_descobertos': summary['ks_descobertos'],
                **params,
                'ClonalG_Media_Validacao': summary['ClonalG_Media'],
                'ClonalG_Desvio_Validacao': summary['ClonalG_Desvio'],
                'ClonalG_Melhor_Validacao': summary['ClonalG_Melhor'],
                'ClonalG_Pior_Validacao': summary['ClonalG_Pior'],
                'KMeans_Silhouette_mesmo_k': kmeans_score,
            }
            row['Delta_Validacao_vs_KMeans_mesmo_k'] = row['ClonalG_Media_Validacao'] - row['KMeans_Silhouette_mesmo_k']
            rows.append(row)

    return pd.DataFrame(rows)


def plot_rankings(search_df):
    for ds_id in sorted(search_df['DataSet'].unique()):
        top = search_df[search_df['DataSet'] == ds_id].head(12).copy()
        top['Config'] = [f"#{i}" for i in range(1, len(top) + 1)]

        fig, ax = plt.subplots(figsize=(11, 5.5))
        sns.barplot(data=top, x='Config', y='ClonalG_Media', hue='k_descoberto_clonalg', palette='viridis', ax=ax)
        ax.scatter(top['Config'], top['KMeans_Silhouette_mesmo_k'], color='#333333', marker='D', s=52, label='k-Means no k do ClonalG')
        ax.set_title(f'DS{ds_id} - Top configuracoes ClonalG (k descoberto pelo ClonalG)')
        ax.set_xlabel('Ranking da busca')
        ax.set_ylabel('Silhouette media')
        ax.grid(axis='y', alpha=0.25)
        ax.legend(title='k ClonalG')
        plt.tight_layout()
        plt.savefig(f'{OUTPUT_DIR}/ranking_ds{ds_id}.png', dpi=160)
        plt.close()


def plot_parameter_impact(search_df):
    params = ['k_descoberto_clonalg', 'n_antibodies', 'rho', 'beta', 'replace_rate', 'selection_rate']
    fig, axes = plt.subplots(2, 3, figsize=(16, 9))
    axes = axes.ravel()

    for ax, param in zip(axes, params):
        grouped = search_df.groupby(param, as_index=False)['ClonalG_Media'].mean()
        sns.lineplot(data=grouped, x=param, y='ClonalG_Media', marker='o', ax=ax, color='#2f6f73')
        ax.set_title(f'Impacto medio: {param}')
        ax.set_xlabel(param)
        ax.set_ylabel('Silhouette media')
        ax.grid(alpha=0.25)

    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/impacto_parametros_grid.png', dpi=160)
    plt.close()


def plot_final_comparison(best_df):
    fig, ax = plt.subplots(figsize=(10, 5.5))
    plot_df = best_df.melt(
        id_vars=['DataSet'],
        value_vars=['ClonalG_Media_Validacao', 'KMeans_Silhouette_mesmo_k'],
        var_name='Algoritmo',
        value_name='Silhouette',
    )
    plot_df['Algoritmo'] = plot_df['Algoritmo'].replace({
        'ClonalG_Media_Validacao': 'ClonalG',
        'KMeans_Silhouette_mesmo_k': 'k-Means no k do ClonalG',
    })
    sns.barplot(data=plot_df, x='DataSet', y='Silhouette', hue='Algoritmo', palette=['#2f6f73', '#6b6f76'], ax=ax)
    ax.set_title('ClonalG validado vs k-Means usando k descoberto pelo ClonalG')
    ax.set_xlabel('DataSet')
    ax.set_ylabel('Silhouette')
    ax.grid(axis='y', alpha=0.25)
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/comparativo_melhores_vs_kmeans.png', dpi=160)
    plt.close()


def write_markdown_report(best_df, search_df):
    lines = [
        '# Busca de Parametros do ClonalG\n',
        '- Fluxo: ClonalG descobre k; k-Means e executado com o k descoberto pelo ClonalG.',
        f'- Repeticoes na busca: {SEARCH_RUNS}',
        f'- Repeticoes na validacao das melhores configuracoes: {VALIDATION_RUNS}',
        f'- Iteracoes por execucao ClonalG: {N_ITERATIONS}',
        f'- Faixa de k pesquisada pelo ClonalG: {min(K_RANGE)} a {max(K_RANGE)}',
        '',
        '## Melhores configuracoes validadas\n',
    ]

    display_cols = [
        'DataSet', 'k_descoberto_clonalg', 'k_descoberto_moda', 'ks_descobertos',
        'n_antibodies', 'rho', 'beta', 'replace_rate', 'selection_rate',
        'ClonalG_Media_Validacao', 'ClonalG_Desvio_Validacao', 'KMeans_Silhouette_mesmo_k',
        'Delta_Validacao_vs_KMeans_mesmo_k',
    ]
    best_display = best_df[display_cols].copy()
    for col in ['ClonalG_Media_Validacao', 'ClonalG_Desvio_Validacao', 'KMeans_Silhouette_mesmo_k', 'Delta_Validacao_vs_KMeans_mesmo_k']:
        best_display[col] = best_display[col].round(4)
    lines.append(dataframe_to_markdown(best_display, index=False))

    lines.extend(['', '## Todas as configuracoes da busca\n'])
    search_display = search_df.copy()
    for col in ['ClonalG_Media', 'ClonalG_Desvio', 'KMeans_Silhouette_mesmo_k', 'Delta_Media_vs_KMeans_mesmo_k']:
        search_display[col] = search_display[col].round(4)
    lines.append(dataframe_to_markdown(search_display, index=False))

    Path = __import__('pathlib').Path
    Path(f'{OUTPUT_DIR}/melhores_configuracoes.md').write_text('\n'.join(lines))


def main():
    print('=' * 70, flush=True)
    print('BUSCA DE PARAMETROS: CLONALG DESCOBRE K, K-MEANS USA ESSE K', flush=True)
    print('=' * 70, flush=True)

    datasets = load_datasets()
    if not datasets:
        print('Nenhum dataset pre-processado encontrado. Execute preprocessamento.py primeiro.')
        return

    search_tables = []
    for ds_id, data in datasets.items():
        search_tables.append(search_dataset(data, ds_id))

    search_full = pd.concat(search_tables, ignore_index=True)
    validation_df = validate_best_configs(datasets, search_full)
    best_validated = (
        validation_df.sort_values(['DataSet', 'ClonalG_Media_Validacao'], ascending=[True, False])
        .groupby('DataSet', as_index=False)
        .head(1)
        .reset_index(drop=True)
    )

    search_full.to_csv(f'{OUTPUT_DIR}/resultados_busca_clonalg.csv', index=False)
    search_full.to_csv(f'{OUTPUT_DIR}/resultados_sweep.csv', index=False)
    validation_df.to_csv(f'{OUTPUT_DIR}/validacao_top_configs.csv', index=False)
    best_validated.to_csv(f'{OUTPUT_DIR}/melhores_configuracoes.csv', index=False)

    # Mantem um CSV de compatibilidade com o nome antigo, agora contendo o k escolhido pelo ClonalG.
    best_validated[['DataSet', 'k_descoberto_clonalg', 'KMeans_Silhouette_mesmo_k']].rename(
        columns={'k_descoberto_clonalg': 'k', 'KMeans_Silhouette_mesmo_k': 'KMeans_Silhouette'}
    ).to_csv(f'{OUTPUT_DIR}/kmeans_por_k.csv', index=False)

    plot_rankings(search_full)
    plot_parameter_impact(search_full)
    plot_final_comparison(best_validated)
    write_markdown_report(best_validated, search_full)

    print('\nMelhores configuracoes validadas:', flush=True)
    cols = [
        'DataSet', 'k_descoberto_clonalg', 'k_descoberto_moda', 'ks_descobertos',
        'n_antibodies', 'rho', 'beta', 'replace_rate', 'selection_rate',
        'ClonalG_Media_Validacao', 'KMeans_Silhouette_mesmo_k',
    ]
    print(best_validated[cols].to_string(index=False))
    print(f'\nResultados salvos em {OUTPUT_DIR}/')


if __name__ == '__main__':
    main()
