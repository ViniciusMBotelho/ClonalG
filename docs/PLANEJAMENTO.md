# Planejamento: Implementação e Avaliação do ClonalG para Agrupamentos

Este documento descreve o plano de ação passo a passo para a implementação do algoritmo de Seleção Clonal (ClonalG) aplicado ao problema de agrupamento de dados (clustering), conforme exigido no Tema 3 do Segundo Trabalho Prático.

## Objetivo
Explorar a capacidade do ClonalG em realizar reconhecimento de padrões e organização de dados, comparando sua eficácia (medida pelo Índice Silhouette) com a abordagem clássica k-Médias (k-Means).

---

## Etapa 1: Preparação e Análise Exploratória dos Dados
**Objetivo:** Compreender a distribuição e escala dos dados antes da aplicação dos algoritmos.
**Arquivos:** `datasets/DataSet1.csv` a `datasets/DataSet5.csv`.

*   **Carregamento:** Ler os 5 arquivos CSV utilizando `pandas`.
*   **Análise Exploratória:**
    *   Verificar a dimensionalidade de cada dataset.
    *   Analisar a distribuição estatística das características (features).
*   **Pré-processamento:**
    *   Normalização ou padronização dos dados (ex: `MinMaxScaler` ou `StandardScaler` do Scikit-Learn), essencial para algoritmos baseados em cálculo de distância.
    *   Plotagem inicial (scatter plots) em 2D ou 3D (usando PCA se necessário) para visualização prévia da distribuição espacial.

---

## Etapa 2: Implementação do Algoritmo ClonalG
**Objetivo:** Desenvolver o Sistema Imunológico Artificial (SIA) contendo os 4 processos obrigatórios.
**Linguagem/Ferramentas:** Python 3, NumPy, SciPy (para cálculo de distâncias).

O algoritmo será estruturado em uma classe `ClonalG_Clustering` com os seguintes passos iterativos:

1.  **Inicialização:**
    *   Gerar uma população inicial de anticorpos. Neste contexto de clustering, cada anticorpo pode representar o centro de um cluster (centroide) ou um conjunto de centroides.
2.  **Reconhecimento (Cálculo de Afinidade):**
    *   Afinidade dos anticorpos com os antígenos (dados).
    *   Métrica base: Distância Euclidiana.
    *   Para avaliar o conjunto de centroides de um anticorpo, a **afinidade interna será guiada pela distância Euclidiana média ao centroide mais próximo** (com sinal invertido para manter maior = melhor).
3.  **Proliferação (Clonagem):**
    *   Selecionar os melhores anticorpos (maior afinidade).
    *   Gerar clones proporcionalmente à afinidade: os melhores produzem mais cópias.
4.  **Variação (Hipermutação Somática):**
    *   Aplicar mutação nos clones.
    *   Regra: Mutação inversamente proporcional à afinidade (clones de anticorpos excelentes sofrem pouca mutação; clones de anticorpos piores sofrem mais mutação para explorar o espaço de busca).
5.  **Seleção e Substituição:**
    *   Calcular a afinidade da população clonada e mutada.
    *   Selecionar os melhores indivíduos entre a população original e os clones para formar a memória explícita (Abm).
    *   Manter o restante como repertório populacional (Abr) e substituir uma porcentagem de indivíduos de baixa afinidade por novos indivíduos gerados aleatoriamente (para manter a diversidade e evitar ótimos locais).

---

## Etapa 3: Experimentos e Ajuste de Parâmetros
**Objetivo:** Encontrar o equilíbrio ótimo entre exploração (exploration) e explotação (exploitation).

*   Implementar uma rotina de testes variando os seguintes parâmetros:
    *   **Tamanho da população de anticorpos** ($N$).
    *   **Taxa de seleção** (percentual de melhores clones mantidos).
    *   **Fator de mutação** (intensidade da busca local / decaimento da mutação).
*   Documentar a evolução do Índice Silhouette para diferentes configurações em cada um dos 5 datasets, mantendo a afinidade interna baseada em distância Euclidiana.

---

## Etapa 4: Descoberta do Número de Clusters ($k$) [CONCLUÍDO]
**Objetivo:** Encontrar o melhor \(k\) com o ClonalG.

*   **Abordagem:** Definir uma lista de candidatos de \(k\) no script de execução e rodar o ClonalG separadamente para cada candidato.
*   **Análise:** Selecionar o \(k\) com melhor Silhouette do ClonalG e repassar esse mesmo \(k\) ao k-Means.

---

## Etapa 5: Avaliação e Comparação com k-Means [CONCLUÍDO]
**Objetivo:** Validar o desempenho do ClonalG contra um algoritmo de referência.

*   Executar o `KMeans` do pacote `sklearn.cluster` nos 5 datasets.
*   Usar no k-Means o melhor \(k\) encontrado pelo ClonalG.
*   Comparar os resultados do ClonalG e k-Means diretamente através do Índice Silhouette final obtido em cada dataset.

---

## Etapa 6: Geração de Entregáveis
**Objetivo:** Preparar os artefatos para a apresentação.

1.  **Gráficos de Evolução:** Gráficos de linha mostrando o crescimento do Índice Silhouette ao longo das gerações (iterações) do ClonalG, evidenciando o ajuste de parâmetros.
2.  **Gráficos de Dispersão (Scatter Plots):**
    *   Visualização final dos grupos formados pelo ClonalG vs. grupos formados pelo k-Means para cada dataset.
3.  **Tabelas de Resultados:** Consolidação da melhor configuração de parâmetros e os valores de Silhouette comparativos.
4.  **Discussão Técnica:** Análise sobre o papel da Memória Imunológica e as situações em que o ClonalG se sobressaiu ou foi superado pelo k-Means.
