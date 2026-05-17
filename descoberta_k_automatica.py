import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from clonalg_core import ClonalG
import os

def main():
    output_dir = 'resultados/etapa4_descoberta_k'
    os.makedirs(output_dir, exist_ok=True)
    
    print("Iniciando Etapa 4: Descoberta Automática de Clusters (k)\n")
    print(f"{'DataSet':<12} | {'k Descoberto':<12} | {'Melhor Silhouette':<15}")
    print("-" * 45)

    resultados = []

    for i in range(1, 6):
        dataset_path = f'datasets/DataSet{i}_scaled.csv'
        if not os.path.exists(dataset_path):
            continue
            
        data = pd.read_csv(dataset_path, header=None).values
        
        # Instancia ClonalG com k_range de 2 a 8
        # Aumentamos o número de gerações para dar tempo de estabilizar o k
        sia = ClonalG(n_antibodies=15, k_range=(2, 8), rho=2.0, beta=10)
        best_antibody, history = sia.fit(data, n_iterations=100, verbose=False)
        
        best_k = len(best_antibody)
        best_score = max(history)
        
        print(f"DataSet {i:<4} | {best_k:<12} | {best_score:<15.4f}")
        
        resultados.append({
            'DataSet': i,
            'k_descoberto': best_k,
            'silhouette': best_score
        })
        
        # Plot do Agrupamento Descoberto
        plt.figure(figsize=(8, 6))
        labels = sia.predict(data, best_antibody)
        sns.scatterplot(x=data[:, 0], y=data[:, 1], hue=labels, palette='viridis', legend='full')
        plt.scatter(best_antibody[:, 0], best_antibody[:, 1], s=150, c='red', marker='X', label='Centroides')
        plt.title(f'DS{i} - k Autônomo: {best_k} (Sil: {best_score:.3f})')
        plt.legend()
        plt.tight_layout()
        plt.savefig(f'{output_dir}/descoberta_ds{i}.png')
        plt.close()

    # Salvar Resumo em Markdown
    df_res = pd.DataFrame(resultados)
    df_res.to_markdown(os.path.join(output_dir, 'resumo_k_automatico.md'), index=False)
    print(f"\n[SUCESSO] Resultados salvos em '{output_dir}/'")

if __name__ == "__main__":
    main()
