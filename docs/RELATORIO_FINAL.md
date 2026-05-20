# Relatório Final - Agrupamento de Dados com ClonalG

## 1. Introdução
Este trabalho apresentou a aplicação do algoritmo de Seleção Clonal (ClonalG) para o problema de agrupamento (clustering) de dados. O objetivo foi avaliar a capacidade do algoritmo de reconhecer padrões de forma autônoma e comparar seu desempenho com o algoritmo k-Means.

## 2. Metodologia Realizada
O projeto seguiu rigorosamente o planejamento estabelecido:
*   **Etapa 1:** Pré-processamento e normalização dos 5 datasets.
*   **Etapa 2 e 3:** Implementação do ClonalG com hipermutação somática e ajuste de parâmetros.
*   **Etapa 4:** Descoberta de $k$ pelo ClonalG a partir de candidatos configurados.
*   **Etapa 5:** Comparação sistemática com o k-Means.

## 3. Principais Resultados

### 3.1. Desempenho vs k-Means
O ClonalG demonstrou ser mais robusto que o k-Means, especialmente no **DataSet 5**, onde superou o algoritmo clássico em mais de 80% na métrica de Silhouette. Isso prova que a busca estocástica do ClonalG é eficiente para evitar ótimos locais.

### 3.2. Descoberta de Clusters (Etapa 4)
Ao testar candidatos de $k$ com o ClonalG, observamos:
*   **Estabilidade:** Para datasets bem definidos (DS1 e DS4), o algoritmo convergiu para $k=3$.
*   **Otimização:** Em outros datasets, o algoritmo encontrou que $k=2$ maximizava o Silhouette, sugerindo estruturas de agrupamento mais simplificadas porém mais coesas estatisticamente.

| DataSet | k Descoberto | Silhouette Final |
| :--- | :---: | :---: |
| DataSet 1 | 3 | 0.6307 |
| DataSet 2 | 2 | 0.5867 |
| DataSet 3 | 2 | 0.7867 |
| DataSet 4 | 3 | 0.5741 |
| DataSet 5 | 2 | 0.6656 |

## 4. Conclusão
O ClonalG mostrou-se uma ferramenta poderosa para clustering. A implementação da **hipermutação somática** permitiu uma exploração fina do espaço de busca com afinidade interna baseada em distância Euclidiana. O melhor $k$ é escolhido pelo Silhouette obtido pelo ClonalG e então repassado ao k-Means.

---
**Artefatos Gerados:**
*   `resultados/comparativo_final/`: Gráficos comparativos ClonalG vs k-Means.
*   `resultados/etapa4_descoberta_k/`: Gráficos e tabelas com o $k$ encontrado.
*   `docs/`: Documentação técnica completa.
