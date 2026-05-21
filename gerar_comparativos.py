import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.impute import SimpleImputer
from preprocessamento import carregar_dataset_limpo
import os

def main():
    output_dir = 'resultados/comparativo_normalizacao'
    os.makedirs(output_dir, exist_ok=True)
    
    for i in range(1, 6):
        file_path = f'datasets/DataSet{i}.csv'
        try:
            df = carregar_dataset_limpo(file_path)
            
            imputer = SimpleImputer(strategy='mean')
            data_raw = imputer.fit_transform(df)
            
            plt.figure(figsize=(12, 5))
            
            plt.subplot(1, 2, 1)
            if data_raw.shape[1] > 2:
                pca = PCA(n_components=2)
                viz_data = pca.fit_transform(data_raw)
                plt.title(f'DS {i} - SEM Normalização (PCA)')
            else:
                viz_data = data_raw
                plt.title(f'DS {i} - SEM Normalização')
            
            sns.scatterplot(x=viz_data[:, 0], y=viz_data[:, 1], color='red', alpha=0.6)
            plt.grid(True, alpha=0.3)
            
            plt.subplot(1, 2, 2)
            data_scaled = pd.read_csv(f'datasets/DataSet{i}_scaled.csv', header=None).values
            if data_scaled.shape[1] > 2:
                pca = PCA(n_components=2)
                viz_scaled = pca.fit_transform(data_scaled)
                plt.title(f'DS {i} - COM Normalização (PCA)')
            else:
                viz_scaled = data_scaled
                plt.title(f'DS {i} - COM Normalização')
                
            sns.scatterplot(x=viz_scaled[:, 0], y=viz_scaled[:, 1], color='green', alpha=0.6)
            plt.grid(True, alpha=0.3)
            
            plt.tight_layout()
            plt.savefig(f'{output_dir}/comparacao_ds{i}.png')
            plt.close()
            print(f"Comparativo do DataSet {i} gerado.")
            
        except Exception as e:
            print(f"Erro no DS {i}: {e}")

if __name__ == "__main__":
    main()
