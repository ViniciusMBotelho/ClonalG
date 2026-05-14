import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from preprocessamento import main as run_preprocess
from clonalg_core import ClonalG
import os
import numpy as np

def main():
    # 1. Garante que os dados estão prontos
    print("--- 1/3 Iniciando Pré-processamento ---")
    run_preprocess()
    
    # 2. Configurações para o Experimento Inicial (DataSet 1)
    dataset_path = 'datasets/DataSet1_scaled.csv'
    if not os.path.exists(dataset_path):
        print(f"Erro: {dataset_path} não encontrado!")
        return
        
    data = pd.read_csv(dataset_path, header=None).values
    
    print(f"\n--- 2/3 Iniciando ClonalG no {dataset_path} ---")
    
    # Parâmetros: N=10 anticorpos, k=3 clusters, rho=2.0, beta=10
    sia = ClonalG(n_antibodies=10, n_clusters=3, rho=2.0, beta=10)
    
    # Treinamento por 50 gerações
    best_centroids, history = sia.fit(data, n_iterations=50)
    
    # 3. Visualização dos Resultados
    print("\n--- 3/3 Gerando Visualizações Finais ---")
    plt.figure(figsize=(12, 5))
    
    # Gráfico de Evolução
    plt.subplot(1, 2, 1)
    plt.plot(history, color='#2ca02c', linewidth=2)
    plt.title('Evolução da Afinidade (Silhouette)')
    plt.xlabel('Geração')
    plt.ylabel('Score')
    plt.grid(True, alpha=0.3)
    
    # Gráfico de Clusters Final
    plt.subplot(1, 2, 2)
    labels = sia.predict(data, best_centroids)
    sns.scatterplot(x=data[:, 0], y=data[:, 1], hue=labels, palette='viridis')
    plt.scatter(best_centroids[:, 0], best_centroids[:, 1], s=200, c='red', marker='X', label='Centroides')
    plt.title('Clusters Identificados pelo ClonalG')
    plt.legend()
    
    plt.tight_layout()
    plt.savefig('resultados/resultado_clonalg_ds1.png')
    
    print(f"\n[SUCESSO] Melhor Silhouette: {max(history):.4f}")
    print("Resultado salvo em: resultados/resultado_clonalg_ds1.png")

if __name__ == "__main__":
    main()
