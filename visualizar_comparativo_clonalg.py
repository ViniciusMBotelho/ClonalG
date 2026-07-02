import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score, davies_bouldin_score
from clonalg_core import ClonalG

OUTPUT_DIR = 'resultados'
RANDOM_SEED = 42

def safe_metrics(data, labels):
    if len(np.unique(labels)) < 2:
        return -1.0, 999.0
    sil = float(silhouette_score(data, labels))
    db = float(davies_bouldin_score(data, labels))
    return sil, db

def run_clonalg(data, k, params):
    np.random.seed(RANDOM_SEED)
    sia = ClonalG(
        n_antibodies=30,
        k=k,
        k_min=2,
        k_max=6,
        rho=2.0,
        beta=10,
        replace_rate=0.1,
        selection_rate=1.0,
        silhouette_sample_size=300,
        **params
    )
    centroids, history = sia.fit(data, n_iterations=30, verbose=False)
    labels = sia.predict(data, centroids)
    sil, db = safe_metrics(data, labels)
    return centroids, labels, sil, db

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Vamos usar o DataSet 2 onde as melhorias do ClonalG novo fazem diferença clara
    ds_id = 2
    k = 2
    data_path = f'datasets/DataSet{ds_id}_scaled.csv'
    
    if not os.path.exists(data_path):
        print(f"Dataset nao encontrado em {data_path}")
        return
        
    data = pd.read_csv(data_path, header=None).values
    
    # Parâmetros Clássico (Lab 2)
    params_classico = {
        'parametric_mutation_scale': 0.0,
        'diversity_weight': 0.0,
        'affinity_metric': 'silhouette',
        'dynamic_decay': False
    }
    
    # Parâmetros Otimizado (Lab 4)
    params_otimizado = {
        'parametric_mutation_scale': 0.05,
        'diversity_weight': 0.15,
        'affinity_metric': 'silhouette',
        'dynamic_decay': True
    }
    
    print("Executando ClonalG Clássico...")
    cent_c, labels_c, sil_c, db_c = run_clonalg(data, k, params_classico)
    
    print("Executando ClonalG Otimizado (Novo)...")
    cent_o, labels_o, sil_o, db_o = run_clonalg(data, k, params_otimizado)
    
    # Projeção PCA 2D
    pca = PCA(n_components=2, random_state=RANDOM_SEED)
    data_2d = pca.fit_transform(data)
    cent_c_2d = pca.transform(cent_c)
    cent_o_2d = pca.transform(cent_o)
    
    # Plotagem
    fig, axes = plt.subplots(1, 2, figsize=(15, 6.5))
    
    # Plot do Clássico
    sns.scatterplot(
        x=data_2d[:, 0], y=data_2d[:, 1], 
        hue=labels_c, palette='Set2', 
        s=40, alpha=0.7, ax=axes[0], legend=False
    )
    axes[0].scatter(
        cent_c_2d[:, 0], cent_c_2d[:, 1], 
        s=200, c='#d62728', marker='X', edgecolor='black', linewidth=1.5,
        label='Anticorpos (Centróides)'
    )
    axes[0].set_title(f"ClonalG Clássico (Lab 2)\nSilhouette: {sil_c:.4f} | Davies-Bouldin: {db_c:.4f}", fontsize=12, fontweight='bold')
    axes[0].grid(True, alpha=0.2)
    axes[0].legend(loc='best')
    
    # Plot do Otimizado
    sns.scatterplot(
        x=data_2d[:, 0], y=data_2d[:, 1], 
        hue=labels_o, palette='Set2', 
        s=40, alpha=0.7, ax=axes[1], legend=False
    )
    axes[1].scatter(
        cent_o_2d[:, 0], cent_o_2d[:, 1], 
        s=200, c='#2ca02c', marker='D', edgecolor='black', linewidth=1.5,
        label='Anticorpos (Centróides)'
    )
    axes[1].set_title(f"ClonalG Otimizado (Novo - Lab 4)\nSilhouette: {sil_o:.4f} | Davies-Bouldin: {db_o:.4f}", fontsize=12, fontweight='bold')
    axes[1].grid(True, alpha=0.2)
    axes[1].legend(loc='best')
    
    plt.suptitle("Comparação do Resultado de Agrupamento (DataSet 2)", fontsize=14, fontweight='bold', y=0.98)
    plt.tight_layout()
    
    output_path = f'{OUTPUT_DIR}/comparativo_visual_antigo_novo.png'
    plt.savefig(output_path, dpi=180)
    plt.close()
    print(f"Gráfico comparativo gerado com sucesso em: {output_path}")

if __name__ == "__main__":
    main()
