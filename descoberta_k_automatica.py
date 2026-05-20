import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from clonalg_core import ClonalG
from sklearn.decomposition import PCA
from markdown_utils import dataframe_to_markdown
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
        sia = ClonalG(n_antibodies=15, k_range=(2, 8), rho=2.0, beta=10, selection_rate=0.85)
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
        if data.shape[1] > 2:
            pca = PCA(n_components=2, random_state=42)
            data_plot = pca.fit_transform(data)
            antibody_plot = pca.transform(best_antibody)
            explained = pca.explained_variance_ratio_.sum() * 100
            subtitle = f'PCA 2D ({explained:.1f}% variancia)'
        else:
            data_plot = data[:, :2]
            antibody_plot = best_antibody[:, :2]
            subtitle = 'atributos originais'
        sns.scatterplot(x=data_plot[:, 0], y=data_plot[:, 1], hue=labels, palette='tab10', legend='full', s=34, alpha=0.82)
        plt.scatter(antibody_plot[:, 0], antibody_plot[:, 1], s=160, c='#d62728', marker='X', edgecolor='white', linewidth=1.2, label='Anticorpos')
        plt.title(f'DS{i} - k autonomo: {best_k} | Sil: {best_score:.3f} | {subtitle}')
        plt.xlabel('Componente 1')
        plt.ylabel('Componente 2')
        plt.grid(alpha=0.25)
        plt.legend()
        plt.tight_layout()
        plt.savefig(f'{output_dir}/descoberta_ds{i}.png', dpi=170)
        plt.close()

    # Salvar Resumo em Markdown
    df_res = pd.DataFrame(resultados)
    open(os.path.join(output_dir, 'resumo_k_automatico.md'), 'w').write(dataframe_to_markdown(df_res, index=False))
    print(f"\n[SUCESSO] Resultados salvos em '{output_dir}/'")

if __name__ == "__main__":
    main()
