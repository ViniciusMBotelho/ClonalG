import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.impute import SimpleImputer
import os


def carregar_dataset_limpo(file_path):
    df = pd.read_csv(file_path)

    first_col = df.columns[0]
    first_values = pd.to_numeric(df.iloc[:, 0], errors='coerce')
    looks_like_index = (
        str(first_col).startswith('Unnamed')
        or (
            first_values.notna().all()
            and np.array_equal(first_values.astype(int).to_numpy(), np.arange(len(df)))
        )
    )

    if looks_like_index:
        df = df.iloc[:, 1:]

    return df.apply(pd.to_numeric, errors='coerce')


def main():
    output_dir = 'resultados/etapa1'
    os.makedirs(output_dir, exist_ok=True)

    relatorio_texto = "# Resumo Estatístico - Etapa 1\n\n"

    for i in range(1, 6):
        file_path = f'datasets/DataSet{i}.csv'
        print(f"Processando {file_path}...")
        
        try:
            df = carregar_dataset_limpo(file_path)

            shape = df.shape
            missing = df.isnull().sum().sum()
            
            relatorio_texto += f"## DataSet {i}\n"
            relatorio_texto += f"- **Dimensões:** {shape[0]} amostras, {shape[1]} features\n"
            relatorio_texto += f"- **Valores ausentes:** {missing}\n\n"
            
            imputer = SimpleImputer(strategy='mean')
            df_imputed = imputer.fit_transform(df)
            
            scaler = StandardScaler()
            df_scaled = scaler.fit_transform(df_imputed)
            
            df_scaled_pd = pd.DataFrame(df_scaled)
            df_scaled_pd.to_csv(f'datasets/DataSet{i}_scaled.csv', index=False, header=False)
            
            plt.figure(figsize=(8, 6))
            if shape[1] > 2:
                pca = PCA(n_components=2)
                df_pca = pca.fit_transform(df_scaled)
                sns.scatterplot(x=df_pca[:, 0], y=df_pca[:, 1], alpha=0.7)
                plt.title(f'DataSet {i} - PCA 2D (Padronizado)')
            else:
                sns.scatterplot(x=df_scaled[:, 0], y=df_scaled[:, 1], alpha=0.7)
                plt.title(f'DataSet {i} - 2D (Padronizado)')
                
            plt.grid(True, linestyle='--', alpha=0.5)
            plt.savefig(os.path.join(output_dir, f'dataset{i}_plot.png'))
            plt.close()
            
        except Exception as e:
            print(f"Erro no dataset {i}: {e}")

    with open(os.path.join(output_dir, 'resumo_estatistico.md'), 'w') as f:
        f.write(relatorio_texto)
    print("Pré-processamento concluído.")

if __name__ == "__main__":
    main()
