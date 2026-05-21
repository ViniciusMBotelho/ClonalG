import os

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score

from clonalg_core import ClonalG
from markdown_utils import dataframe_to_markdown

OUTPUT_DIR = 'resultados/comparativo_final'
BEST_CONFIG_PATH = 'resultados/etapa3_parametros/melhores_configuracoes.csv'
N_RUNS = 3
N_ITERATIONS = 25
RANDOM_SEED = 42
SILHOUETTE_SAMPLE_SIZE = 300
DEFAULT_K_VALUES = {1: 3, 2: 3, 3: 4, 4: 3, 5: 3}


def safe_silhouette(data, labels):
    if len(np.unique(labels)) < 2:
        return -1.0
    return silhouette_score(data, labels)


def default_configs():
    configs = {}
    for ds_id, k in DEFAULT_K_VALUES.items():
        configs[ds_id] = {
            'DataSet': ds_id,
            'k': k,
            'n_antibodies': 15,
            'rho': 2.0,
            'beta': 10,
            'replace_rate': 0.10,
            'selection_rate': 1.0,
            'k_min': min(DEFAULT_K_VALUES.values()),
            'k_max': max(DEFAULT_K_VALUES.values()),
        }
    return configs


def load_best_configs():
    if os.path.exists(BEST_CONFIG_PATH):
        df = pd.read_csv(BEST_CONFIG_PATH)
        if 'k' not in df.columns:
            return default_configs()
        return {int(row['DataSet']): row.to_dict() for _, row in df.iterrows()}

    return default_configs()


def get_config_k(cfg):
    return int(cfg['k'])


def get_k_bounds(cfg):
    if 'k_candidates' in cfg and isinstance(cfg['k_candidates'], str):
        candidates = [int(value) for value in cfg['k_candidates'].split(',') if value]
        return min(candidates), max(candidates)
    if 'k_min' in cfg and 'k_max' in cfg and not pd.isna(cfg['k_min']) and not pd.isna(cfg['k_max']):
        return int(cfg['k_min']), int(cfg['k_max'])
    k = get_config_k(cfg)
    return k, k


def project_2d(data, *centers):
    if data.shape[1] <= 2:
        projected = data[:, :2]
        projected_centers = [center[:, :2] for center in centers]
        subtitle = 'atributos originais'
    else:
        pca = PCA(n_components=2, random_state=RANDOM_SEED)
        projected = pca.fit_transform(data)
        projected_centers = [pca.transform(center) for center in centers]
        explained = pca.explained_variance_ratio_.sum() * 100
        subtitle = f'PCA 2D ({explained:.1f}% variancia)'
    return projected, projected_centers, subtitle


def run_clonalg(data, cfg, ds_id):
    scores = []
    histories = []
    best = {'score': -2.0, 'centroids': None, 'labels': None, 'history': None}

    k = get_config_k(cfg)
    k_min, k_max = get_k_bounds(cfg)

    for run in range(N_RUNS):
        np.random.seed(RANDOM_SEED + ds_id * 100 + run)
        sia = ClonalG(
            n_antibodies=int(cfg['n_antibodies']),
            k=k,
            k_min=k_min,
            k_max=k_max,
            rho=float(cfg['rho']),
            beta=float(cfg['beta']),
            replace_rate=float(cfg['replace_rate']),
            selection_rate=float(cfg.get('selection_rate', 1.0)),
            silhouette_sample_size=SILHOUETTE_SAMPLE_SIZE,
        )
        centroids, history = sia.fit(data, n_iterations=N_ITERATIONS, verbose=False)
        labels = sia.predict(data, centroids)
        score = safe_silhouette(data, labels)
        scores.append(score)
        histories.append(history)
        if score > best['score']:
            best = {'score': score, 'centroids': centroids, 'labels': labels, 'history': history}

    return {
        'scores': scores,
        'mean': float(np.mean(scores)),
        'best': best,
        'histories': histories,
    }


def plot_comparison(ds_id, data, clonalg_result, kmeans, labels_km, score_km):
    best = clonalg_result['best']
    data_2d, centers_2d, subtitle = project_2d(data, best['centroids'], kmeans.cluster_centers_)
    centers_sia_2d, centers_km_2d = centers_2d

    fig, axes = plt.subplots(1, 2, figsize=(15, 6), sharex=True, sharey=True)

    sns.scatterplot(x=data_2d[:, 0], y=data_2d[:, 1], hue=best['labels'], palette='tab10', s=34, alpha=0.82, ax=axes[0], legend=False)
    axes[0].scatter(centers_sia_2d[:, 0], centers_sia_2d[:, 1], s=190, c='#d62728', marker='X', edgecolor='white', linewidth=1.2, label='Anticorpos')
    axes[0].set_title(f"ClonalG | melhor={best['score']:.3f} media={clonalg_result['mean']:.3f}")
    axes[0].legend(loc='best')

    sns.scatterplot(x=data_2d[:, 0], y=data_2d[:, 1], hue=labels_km, palette='tab10', s=34, alpha=0.82, ax=axes[1], legend=False)
    axes[1].scatter(centers_km_2d[:, 0], centers_km_2d[:, 1], s=160, c='#1f77b4', marker='o', edgecolor='white', linewidth=1.2, label='Centroides')
    axes[1].set_title(f'k-Means | silhouette={score_km:.3f}')
    axes[1].legend(loc='best')

    for ax in axes:
        ax.set_xlabel('Componente 1')
        ax.set_ylabel('Componente 2')
        ax.grid(alpha=0.25)

    fig.suptitle(f'DataSet {ds_id} - comparacao visual ({subtitle})', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/comparacao_ds{ds_id}.png', dpi=170)
    plt.close()

    fig, ax = plt.subplots(figsize=(8, 4.8))
    ax.plot(best['history'], color='#2f6f73', linewidth=2)
    ax.set_title(f'DS{ds_id} - evolucao do Silhouette do ClonalG')
    ax.set_xlabel('Geracao')
    ax.set_ylabel('Silhouette')
    ax.grid(alpha=0.25)
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/evolucao_clonalg_ds{ds_id}.png', dpi=170)
    plt.close()


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    configs = load_best_configs()
    rows = []

    print('Comparativo Final: ClonalG vs k-Means', flush=True)
    print(f'Repeticoes ClonalG por dataset: {N_RUNS}\n', flush=True)

    for ds_id in range(1, 6):
        path = f'datasets/DataSet{ds_id}_scaled.csv'
        if not os.path.exists(path):
            continue

        data = pd.read_csv(path, header=None).values
        cfg = configs[ds_id]
        k = get_config_k(cfg)

        clonalg_result = run_clonalg(data, cfg, ds_id)

        kmeans = KMeans(n_clusters=k, n_init=30, random_state=RANDOM_SEED)
        labels_km = kmeans.fit_predict(data)
        score_km = safe_silhouette(data, labels_km)

        rows.append({
            'DataSet': ds_id,
            'k': k,
            'n_antibodies': int(cfg['n_antibodies']),
            'rho': float(cfg['rho']),
            'beta': float(cfg['beta']),
            'replace_rate': float(cfg['replace_rate']),
            'selection_rate': float(cfg.get('selection_rate', 1.0)),
            'ClonalG_media': clonalg_result['mean'],
            'ClonalG_melhor': clonalg_result['best']['score'],
            'KMeans': score_km,
            'Delta_media': clonalg_result['mean'] - score_km,
        })

        print(f"DS{ds_id}: k={k} ClonalG={clonalg_result['mean']:.4f} | k-Means={score_km:.4f}", flush=True)
        plot_comparison(ds_id, data, clonalg_result, kmeans, labels_km, score_km)

    df = pd.DataFrame(rows)
    df.to_csv(f'{OUTPUT_DIR}/tabela_resultados.csv', index=False)

    md = df.copy()
    for col in ['ClonalG_media', 'ClonalG_melhor', 'KMeans', 'Delta_media']:
        md[col] = md[col].round(4)
    open(f'{OUTPUT_DIR}/tabela_resultados.md', 'w').write(dataframe_to_markdown(md, index=False))
    print(f'\nResultados salvos em {OUTPUT_DIR}/')


if __name__ == '__main__':
    main()
