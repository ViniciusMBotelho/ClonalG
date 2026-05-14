import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.impute import SimpleImputer
import os

def main():
    # Garantir que o diretório de resultados exista
    output_dir = 'resultados/etapa1'
    os.makedirs(output_dir, exist_ok=True)

    relatorio_texto = "# Resumo Estatístico - Etapa 1\n\n"

    for i in range(1, 6):
        file_path = f'datasets/DataSet{i}.csv'
        print(f"Processando {file_path}...")
        
        try:
            # Tentar carregar sem cabeçalho e com cabeçalho
            df = pd.read_csv(file_path)
            
            # Se a primeira linha parecer dado (todos números), recarregar sem cabeçalho
            if all(df.iloc[0].apply(lambda x: isinstance(x, (int, float)))):
                 df = pd.read_csv(file_path, header=None)

            shape = df.shape
            missing = df.isnull().sum().sum()
            
            relatorio_texto += f"## DataSet {i}\n"
            relatorio_texto += f"- **Dimensões:** {shape[0]} amostras, {shape[1]} features\n"
            relatorio_texto += f"- **Valores ausentes:** {missing}\n\n"
            
            # Tratamento de valores ausentes (Imputação com a média)
            imputer = SimpleImputer(strategy='mean')
            df_imputed = imputer.fit_transform(df)
            
            # Normalização / Padronização
            scaler = StandardScaler()
            df_scaled = scaler.fit_transform(df_imputed)
            
            # Salvando os dados padronizados para uso nos próximos algoritmos
            df_scaled_pd = pd.DataFrame(df_scaled)
            df_scaled_pd.to_csv(f'datasets/DataSet{i}_scaled.csv', index=False, header=False)
            
            # Visualização
            plt.figure(figsize=(8, 6))
            if shape[1] > 2:
                # Usa PCA para reduzir a 2 dimensões se tiver mais de 2 features
                pca = PCA(n_components=2)
                df_pca = pca.fit_transform(df_scaled)
                sns.scatterplot(x=df_pca[:, 0], y=df_pca[:, 1], alpha=0.7, color='#1f77b4')
                plt.title(f'DataSet {i} - PCA 2D (Padronizado)')
                plt.xlabel('Componente Principal 1')
                plt.ylabel('Componente Principal 2')
            else:
                # Plotagem direta se tiver 2 features
                sns.scatterplot(x=df_scaled[:, 0], y=df_scaled[:, 1], alpha=0.7, color='#ff7f0e')
                plt.title(f'DataSet {i} - 2D (Padronizado)')
                plt.xlabel('Feature 1')
                plt.ylabel('Feature 2')
                
            plt.grid(True, linestyle='--', alpha=0.5)
            plot_path = os.path.join(output_dir, f'dataset{i}_plot.png')
            plt.savefig(plot_path)
            plt.close()
            
        except Exception as e:
            print(f"Erro no dataset {i}: {e}")
            relatorio_texto += f"Erro ao processar DataSet {i}: {e}\n\n"

    with open(os.path.join(output_dir, 'resumo_estatistico.md'), 'w') as f:
        f.write(relatorio_texto)
        
    print("Processamento concluído com sucesso!")

if __name__ == "__main__":
    main()
