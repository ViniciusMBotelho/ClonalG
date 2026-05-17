# Relatório de Execução - Etapa 1: Preparação e Análise Exploratória

Este relatório detalha os procedimentos realizados na Etapa 1 do planejamento para implementação do algoritmo ClonalG.

## O que foi feito

1. **Criação do Script de Análise (`etapa1_analise.py`):** Desenvolvemos um script em Python utilizando bibliotecas consolidadas para análise de dados e machine learning (`pandas`, `scikit-learn`, `matplotlib`, `seaborn`).
2. **Leitura e Extração de Dimensões:** Carregamos os 5 arquivos de dados localizados na pasta `datasets/` para avaliar sua estrutura e complexidade:
    * **DataSet 1:** 301 amostras, 3 atributos (features).
    * **DataSet 2:** 1011 amostras, 3 atributos.
    * **DataSet 3:** 301 amostras, 5 atributos.
    * **DataSet 4:** 231 amostras, 3 atributos.
    * **DataSet 5:** 441 amostras, 7 atributos.
3. **Tratamento de Dados Ausentes (Imputação):** Durante a primeira execução, detectamos que todos os 5 datasets possuíam 1 valor ausente (`NaN`). O script foi atualizado com a técnica `SimpleImputer` (estratégia de média) para substituir os valores ausentes pela média de suas respectivas colunas.
4. **Padronização dos Dados:** Todos os datasets passaram por padronização utilizando o `StandardScaler` (Z-score normalization). O resultado final padronizado foi salvo de volta na pasta `datasets/` com o sufixo `_scaled.csv` (ex: `DataSet1_scaled.csv`).
5. **Visualização Inicial (Gráficos Dispersão e PCA):** Foram gerados gráficos de dispersão 2D para todos os datasets na pasta `resultados/etapa1/`. Para os datasets com mais de 2 dimensões (3 a 7 features), utilizamos a técnica de Análise de Componentes Principais (PCA) para reduzir os dados a 2 dimensões principais, permitindo assim sua visualização humana em gráficos 2D.

---

## Por que foi feito

* **Leitura e Verificação Dimensional:** É obrigatório compreender a escala e formato dos dados antes de qualquer passo. Saber quantas *features* cada dataset possui impacta diretamente o tempo de execução do cálculo de distâncias. 
* **Tratamento de `NaN` (Missing Values):** Funções matemáticas do ClonalG e do k-Means falharão imediatamente se depararem com um valor ausente. Substituir os `NaN` pela média da coluna permite não descartarmos a amostra, mantendo a integridade estatística dos dados em quantidades tão pequenas.
* **Padronização (`StandardScaler`):** Esta é **a etapa mais crucial**. Os algoritmos de agrupamento baseados em distância (como a Distância Euclidiana, exigida pelo pdf para o reconhecimento no ClonalG e também inerente ao k-Means) são muito sensíveis a diferentes escalas. Se a Feature A varia de 0 a 1000 e a Feature B de 0 a 1, a Distância Euclidiana será quase 100% influenciada pela Feature A. O `StandardScaler` coloca todas as colunas em uma mesma escala (média 0 e variância 1), garantindo que todos os atributos tenham peso igual durante o agrupamento.
* **Visualização via PCA:** Gráficos foram gerados pois a distribuição espacial ajuda no entendimento humano. O PCA foi indispensável porque não é possível plotar gráficos compreensíveis de dispersão com 3, 5 ou 7 dimensões nativamente. Ao forçar a visualização em 2D, podemos criar um "senso de intuição" sobre quão fácil ou difícil será agrupar cada dataset.

Todos os dados tratados, bem como os gráficos gerados, encontram-se nas pastas `datasets/` e `resultados/etapa1/` respectivamente, prontos para serem ingeridos pela classe principal do ClonalG na Etapa 2.