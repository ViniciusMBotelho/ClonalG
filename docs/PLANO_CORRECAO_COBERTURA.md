# Plano de Correcao e Cobertura do Enunciado

## 1. Dados e pre-processamento
- Remover colunas de indice exportadas nos CSVs antes da normalizacao.
- Regenerar todos os `DataSet*_scaled.csv` com apenas atributos reais.
- Atualizar a analise exploratoria com dimensoes corretas, valores ausentes e scatter/PCA.

## 2. Ajuste de parametros
- Executar uma busca em grade para `k`, tamanho da populacao, `rho`, `beta` e `replace_rate`.
- Repetir cada configuracao varias vezes para reduzir ruido estocastico.
- Registrar media, melhor e pior Silhouette por configuracao.
- Comparar cada melhor configuracao do ClonalG com k-Means usando o mesmo `k`.
- Salvar CSV detalhado, tabela Markdown com melhores parametros e graficos de ranking/impacto.

## 3. Comparacao final
- Trocar resultado unico por media de multiplas execucoes do ClonalG.
- Usar k-Means como baseline deterministico com `n_init` alto e `random_state` fixo.
- Apresentar vantagem/desvantagem do ClonalG por dataset com base na media.

## 4. Visualizacao
- Para datasets com mais de 2 atributos, projetar dados, centroides e centros via PCA ajustado no proprio dataset.
- Manter escalas, legenda, grade leve e titulos com Silhouette para facilitar leitura.
- Gerar graficos lado a lado ClonalG vs k-Means e graficos de evolucao do Silhouette.

## 5. Relatorio final
- Incorporar pseudocodigo do ClonalG.
- Explicitar quais parametros foram testados, quantas repeticoes foram usadas e os melhores parametros por dataset.
- Discutir memoria imunologica como populacao/anticorpos sobreviventes e quando ela ajudou ou nao contra k-Means.
