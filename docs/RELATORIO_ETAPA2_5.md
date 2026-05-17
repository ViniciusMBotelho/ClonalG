# Relatório de Execução - Etapas 2, 3 e 5: Implementação e Comparação

Este relatório detalha os resultados obtidos após a implementação do algoritmo ClonalG e sua comparação direta com o algoritmo k-Means.

## 1. Implementação do ClonalG (Etapa 2)
O algoritmo foi implementado seguindo os princípios de Seleção Clonal:
*   **Afinidade:** Medida pelo Índice Silhouette (faixa de -1 a 1).
*   **Clonagem:** Proporcional à afinidade.
*   **Hipermutação Somática:** Taxa de mutação exponencialmente inversa à afinidade ($ \alpha = e^{-\rho \cdot af} $).
*   **Diversidade:** Substituição de 10% da população por novos anticorpos aleatórios a cada geração.

## 2. Resultados Comparativos (Etapa 5)
Abaixo, a tabela consolidada dos scores de Silhouette obtidos nos 5 datasets, utilizando o número de clusters ($k$) sugerido pela análise visual inicial.

| DataSet | k | ClonalG (Silhouette) | k-Means (Silhouette) | Vantagem |
| :--- | :---: | :---: | :---: | :--- |
| **DataSet 1** | 3 | 0.6307 | 0.6307 | Empate |
| **DataSet 2** | 3 | 0.2494 | 0.2487 | ClonalG (+0.3%) |
| **DataSet 3** | 4 | 0.1814 | 0.1620 | ClonalG (+11.9%) |
| **DataSet 4** | 3 | 0.5741 | 0.5741 | Empate |
| **DataSet 5** | 3 | **0.6656** | 0.3656 | **ClonalG (+82.0%)** |

## 3. Análise dos Resultados
*   **Robustez:** O ClonalG mostrou-se superior ou igual ao k-Means em todos os testes.
*   **O Caso do DataSet 5:** Este foi o resultado mais expressivo. Enquanto o k-Means ficou preso em um mínimo local (score 0.36), o ClonalG conseguiu explorar o espaço de busca e encontrar uma configuração globalmente superior (score 0.66). Isso demonstra que o processo de hipermutação somática é eficaz para "escapar" de agrupamentos sub-ótimos.
*   **Complexidade:** O ClonalG exige mais poder computacional devido ao cálculo repetido do Silhouette para cada clone, mas o ganho em qualidade de agrupamento justifica o custo em datasets mais ruidosos.

---
**Próximo Passo:** Implementar a Etapa 4 para permitir que o algoritmo determine o valor de $k$ de forma autônoma.
