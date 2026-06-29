import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.metrics import silhouette_score, davies_bouldin_score
from clonalg_core import ClonalG

OUTPUT_DIR = 'resultados/comparativo_trabalhos_futuros'
N_RUNS = 3
N_ITERATIONS = 25
RANDOM_SEED = 42

DEFAULT_K_VALUES = {1: 3, 2: 3, 3: 4, 4: 3, 5: 3}

def safe_metrics(data, labels):
    if len(np.unique(labels)) < 2:
        return -1.0, 999.0
    sil = float(silhouette_score(data, labels))
    db = float(davies_bouldin_score(data, labels))
    return sil, db

def run_experiment(data, k, variant_name, params):
    scores_sil = []
    scores_db = []
    histories = []
    
    for run in range(N_RUNS):
        np.random.seed(RANDOM_SEED + run)
        sia = ClonalG(
            n_antibodies=60,
            k=k,
            k_min=2,
            k_max=6,
            rho=3.5,
            beta=30,
            replace_rate=0.4,
            selection_rate=0.6,
            silhouette_sample_size=300,
            **params
        )
        centroids, history = sia.fit(data, n_iterations=N_ITERATIONS, verbose=False)
        labels = sia.predict(data, centroids)
        sil, db = safe_metrics(data, labels)
        scores_sil.append(sil)
        scores_db.append(db)
        histories.append(history)
        
    return {
        'mean_sil': np.mean(scores_sil),
        'best_sil': np.max(scores_sil),
        'mean_db': np.mean(scores_db),
        'best_db': np.min(scores_db),
        'histories': histories
    }

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    results = []
    
    variants = {
        'ClonalG_Classico_Lab2': {
            'parametric_mutation_scale': 0.0,
            'diversity_weight': 0.0,
            'affinity_metric': 'silhouette',
            'dynamic_decay': False
        },
        'ClonalG_Otimizado_Lab4': {
            'parametric_mutation_scale': 0.05,
            'diversity_weight': 0.15,
            'affinity_metric': 'silhouette',
            'dynamic_decay': False
        },
        'ClonalG_Decay_Sil_Futuro': {
            'parametric_mutation_scale': 0.05,
            'diversity_weight': 0.15,
            'affinity_metric': 'silhouette',
            'dynamic_decay': True
        },
        'ClonalG_Decay_DB_Futuro': {
            'parametric_mutation_scale': 0.05,
            'diversity_weight': 0.15,
            'affinity_metric': 'davies_bouldin',
            'dynamic_decay': True
        }
    }
    
    print("Iniciando Experimento dos Trabalhos Futuros...", flush=True)
    
    for ds_id in range(1, 6):
        path = f'datasets/DataSet{ds_id}_scaled.csv'
        if not os.path.exists(path):
            print(f"Dataset {ds_id} nao encontrado em {path}", flush=True)
            continue
            
        data = pd.read_csv(path, header=None).values
        k = DEFAULT_K_VALUES[ds_id]
        
        print(f"\n--- DataSet {ds_id} (k={k}) ---", flush=True)
        ds_histories = {}
        
        for name, params in variants.items():
            res = run_experiment(data, k, name, params)
            print(f"[{name}] Sil-Mean: {res['mean_sil']:.4f} | DB-Mean: {res['mean_db']:.4f}", flush=True)
            
            results.append({
                'DataSet': ds_id,
                'Variant': name,
                'Mean_Silhouette': res['mean_sil'],
                'Best_Silhouette': res['best_sil'],
                'Mean_DaviesBouldin': res['mean_db'],
                'Best_DaviesBouldin': res['best_db']
            })
            ds_histories[name] = res['histories'][0] # Salvar primeira execucao para historico de evolucao
            
        # Plot de evolucao para este dataset
        plt.figure(figsize=(10, 6))
        for name, history in ds_histories.items():
            # Se for DB, a afinidade eh negativa, entao mostramos o valor positivo de DB para comparar se o usuario desejar
            # Mas para termos o mesmo grafico, plotamos o valor direto da afinidade que o algoritmo maximizou
            plt.plot(history, label=name, linewidth=2)
        plt.title(f'Evolucao da Afinidade no DataSet {ds_id}')
        plt.xlabel('Geracao')
        plt.ylabel('Afinidade (Score de Fitness)')
        plt.legend()
        plt.grid(alpha=0.25)
        plt.tight_layout()
        plt.savefig(f'{OUTPUT_DIR}/evolucao_ds{ds_id}.png', dpi=170)
        plt.close()
        
    df = pd.DataFrame(results)
    df.to_csv(f'{OUTPUT_DIR}/tabela_comparativo_futuro.csv', index=False)
    
    # Salvar tabela formatada em Markdown
    with open(f'{OUTPUT_DIR}/tabela_comparativo_futuro.md', 'w') as f:
        f.write("# Tabela Comparativa de Trabalhos Futuros\n\n")
        f.write(df.to_markdown(index=False))
        
    print(f"\nExperimentos concluidos com sucesso! Resultados salvos em {OUTPUT_DIR}/", flush=True)

if __name__ == "__main__":
    main()
