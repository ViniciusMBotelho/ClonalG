import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from clonalg_core import ClonalG
import os

def main():
    # Configurações de saída
    output_dir = 'resultados/comparativo_final'
    os.makedirs(output_dir, exist_ok=True)
    
    # Parâmetros sugeridos para o ClonalG (baseados no nosso teste anterior)
    # k_values define o número de clusters que esperamos encontrar em cada dataset
    # (Pode ser ajustado após ver os gráficos iniciais)
    k_values = {1: 3, 2: 3, 3: 4, 4: 3, 5: 3} 
    
    resultados = []

    print("Iniciando Comparativo Final: ClonalG vs k-Means\n")
    print(f"{'DataSet':<12} | {'k':<3} | {'ClonalG (Sil.)':<15} | {'k-Means (Sil.)':<15}")
    print("-" * 55)

    for i in range(1, 6):
        dataset_path = f'datasets/DataSet{i}_scaled.csv'
        if not os.path.exists(dataset_path):
            continue
            
        data = pd.read_csv(dataset_path, header=None).values
        k = k_values[i]
        
        # --- 1. Rodar ClonalG ---
        # Usando a fórmula alpha = exp(-rho * af)
        sia = ClonalG(n_antibodies=15, k_range=(k, k), rho=2.0, beta=10)
        best_centroids_sia, history = sia.fit(data, n_iterations=50, verbose=False)
        labels_sia = sia.predict(data, best_centroids_sia)
        score_sia = silhouette_score(data, labels_sia)
        
        # --- 2. Rodar k-Means ---
        kmeans = KMeans(n_clusters=k, n_init=10, random_state=42)
        labels_km = kmeans.fit_predict(data)
        score_km = silhouette_score(data, labels_km)
        
        # Armazenar resultados
        resultados.append({
            'DataSet': i,
            'k': k,
            'ClonalG': score_sia,
            'k-Means': score_km
        })
        
        print(f"DataSet {i:<4} | {k:<3} | {score_sia:<15.4f} | {score_km:<15.4f}")
        
        # --- 3. Geração de Gráficos Lado a Lado ---
        plt.figure(figsize=(15, 6))
        
        # Plot ClonalG
        plt.subplot(1, 2, 1)
        sns.scatterplot(x=data[:, 0], y=data[:, 1], hue=labels_sia, palette='viridis', legend=None)
        plt.scatter(best_centroids_sia[:, 0], best_centroids_sia[:, 1], s=150, c='red', marker='X', label='Anticorpos')
        plt.title(f'ClonalG - DS{i} (Sil: {score_sia:.3f})')
        plt.legend()
        
        # Plot k-Means
        plt.subplot(1, 2, 2)
        sns.scatterplot(x=data[:, 0], y=data[:, 1], hue=labels_km, palette='viridis', legend=None)
        plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], s=150, c='blue', marker='o', label='Centroides')
        plt.title(f'k-Means - DS{i} (Sil: {score_km:.3f})')
        plt.legend()
        
        plt.tight_layout()
        plt.savefig(f'{output_dir}/comparacao_ds{i}.png')
        plt.close()

    # Salvar Tabela de Resultados em Markdown
    df_res = pd.DataFrame(resultados)
    df_res.to_markdown(os.path.join(output_dir, 'tabela_resultados.md'), index=False)
    print(f"\n[SUCESSO] Tabela e gráficos salvos em '{output_dir}/'")

if __name__ == "__main__":
    main()
