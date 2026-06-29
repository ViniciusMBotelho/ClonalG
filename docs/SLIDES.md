# Apresentação: Otimização do Algoritmo ClonalG para Agrupamento de Dados

Este documento sintetiza os slides da apresentação do projeto prático de Computação Natural.

---

## Slide 1: Título e Identificação
*   **Título:** Otimização do Algoritmo ClonalG para Agrupamento de Dados
*   **Subtítulo:** Busca Local Contínua e Seleção por Diversidade para Clustering Autônomo
*   **Equipe:** Marcos Daniel e Vinicius Macedo
*   **Instituição:** Instituto Federal do Norte de Minas Gerais (IFNMG)
*   **Disciplina:** Computação Natural
*   **Prazo de Entrega:** 02/07/2026

---

## Slide 2: O Problema (Contextualização)
*   **O que é Agrupamento de Dados (Clustering)?**
    *   Particionamento de dados multidimensionais em grupos homogêneos sem supervisão (rótulos).
*   **Limitações dos Métodos Tradicionais (k-Means):**
    *   Necessidade de definir o número de grupos ($k$) previamente.
    *   Sensibilidade à inicialização dos centroides, levando a convergência em mínimos locais.
*   **O Desafio do ClonalG Básico (Lab 2):**
    *   *Mutação Rígida:* Centróides limitados estritamente a pontos existentes do dataset (apenas adição/remoção estrutural de $k$). Sem ajuste local fino das coordenadas.
    *   *Perda de Diversidade:* Pressão seletiva gananciosa baseada puramente no Índice Silhouette, resultando em convergência prematura para soluções subótimas redundantes.

---

## Slide 3: A Solução Proposta - Visão Geral
*   **Objetivo:** Introduzir mecanismos híbridos de busca contínua e diversidade genética ao ClonalG tradicional.
*   **Arquitetura do ClonalG Otimizado:**
    1.  **Afinidade Baseada no Índice Silhouette:** Mede a coesão interna e separação dos clusters.
    2.  **Mutação Estrutural de $k$:** Operações de adição/remoção de centroides para auto-organização do número ideal de clusters.
    3.  **NOVO: Hipermutação Paramétrica:** Busca local no espaço contínuo por perturbação gaussiana dos centroides.
    4.  **NOVO: Seleção por Diversidade na Memória:** Ponderação que recompensa anticorpos que representam soluções distintas no espaço de busca.

---

## Slide 4: Solução Adotada - Detalhamento Técnico das Melhorias
1.  **Hipermutação Paramétrica (Busca Local Contínua):**
    *   A cada clone, além da mutação de $k$, aplica-se um ruído gaussiano às coordenadas dos centroides:
        $$C_i \leftarrow C_i + \mathcal{N}(0, \sigma^2)$$
    *   O desvio padrão $\sigma$ é controlado dinamicamente pela afinidade normalizada $A_{\text{norm}}$ do anticorpo:
        $$\sigma = \text{scale} \times e^{-\rho \cdot A_{\text{norm}}}$$
    *   *Intuição:* Centróides ruins sofrem grande variação espacial (exploração); centróides excelentes sofrem pequenos ajustes finos locais (explotação).

2.  **Seleção Guiada por Diversidade (Preservação de Nichos):**
    *   Evita redundâncias na Memória Imunológica ($A_{bm}$).
    *   Distância entre anticorpos $a$ e $b$ calculada via matching mínimo de centroides:
        $$D(a, b) = \frac{1}{2} \left( \text{mean}_i \min_j d(a_i, b_j) + \text{mean}_j \min_i d(a_i, b_j) \right)$$
    *   Fórmula de seleção de memória combinada:
        $$\text{Score} = A_{\text{norm}} + w_{\text{div}} \times \text{Diversity}_{\text{norm}}$$

---

## Slide 5: Metodologia e Configurações Experimentais
*   **Datasets Utilizados:** 5 conjuntos de dados normalizados (DS1 a DS5), contendo diferentes geometrias e dimensionalidades.
*   **Parâmetros do ClonalG Otimizado:**
    *   Tamanho da População ($N$): 60 anticorpos.
    *   Taxa de Clonagem ($\beta$): 30.
    *   Substituição Populacional (Replace Rate): 40% das piores soluções por novas aleatórias a cada geração.
    *   Escala da Mutação Contínua ($\text{scale}$): 0.05.
    *   Peso da Diversidade ($w_{\text{div}}$): 0.15.
*   **Validação:** Execução de 3 runs independentes por dataset para calcular Silhouette médio e Silhouette melhor. Comparação direta com o k-Means (usando o melhor $k$ descoberto pelo ClonalG).

---

## Slide 6: Resultados - Tabela Comparativa (Silhouette)
O ClonalG otimizado demonstrou alta estabilidade e capacidade de encontrar soluções superiores:

| DataSet | k Descoberto | ClonalG (Melhor) | ClonalG (Média) | k-Means | Delta (Média) |
| :---: | :---: | :---: | :---: | :---: | :---: |
| **DS1** | 3 | **0.6480** | 0.6480 | 0.6480 | 0.0000 |
| **DS2** | 2 | **0.6539** | **0.6220** | 0.3589 | **+0.2631** |
| **DS3** | 6 | 0.2143 | 0.2045 | **0.2221** | -0.0176 |
| **DS4** | 4 | **0.5905** | **0.5903** | 0.5866 | **+0.0037** |
| **DS5** | 2 | **0.6644** | 0.6644 | 0.6644 | 0.0000 |

*Nota: No DataSet 2, o k-Means convergiu em um mínimo local subótimo devido à complexidade da distribuição, enquanto o ClonalG otimizado escapou do mínimo local e obteve melhora significativa de **+0.2631**.*

---

## Slide 7: Discussão dos Resultados
*   **Por que o ClonalG Otimizado superou o k-Means no DS2?**
    *   O k-Means é altamente dependente da inicialização e foi capturado por mínimos locais. A busca global estocástica do ClonalG combinada com o refinamento contínuo da hipermutação paramétrica permitiu encontrar o agrupamento ótimo global.
*   **O papel da seleção por diversidade:**
    *   A diversidade evitou que todos os anticorpos de memória convergissem para a mesma região de busca. Isso permitiu a avaliação simultânea de diferentes estruturas de $k$ durante a busca evolutiva.
*   **O papel da mutação paramétrica:**
    *   Ao adicionar ruído contínuo gaussiano, o ClonalG conseguiu deslocar os centroides de forma suave, permitindo ajustar a posição ideal mesmo quando as amostras originais do dataset não coincidiam exatamente com os centros ideais dos clusters.

---

## Slide 8: Conclusão
*   O ClonalG Otimizado resolve eficientemente a limitação clássica do k-Means (sensibilidade a mínimos locais e necessidade de $k$ fixo).
*   A introdução de busca contínua via mutação gaussiana e a preservação de nichos via seleção de diversidade melhoraram consideravelmente a robustez do algoritmo imunológico comparado à versão básica.
*   A abordagem consolida as vantagens de algoritmos evolucionários/imunológicos globais para problemas complexos de aprendizado de máquina não supervisionado.
