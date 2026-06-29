# Apresentação: Validação de Trabalhos Futuros no ClonalG

Este documento sintetiza os slides da apresentação dos experimentos com as melhorias propostas nos trabalhos futuros.

---

## Slide 1: Título e Identificação
*   **Título:** Validação de Trabalhos Futuros no ClonalG
*   **Subtítulo:** Decaimento Dinâmico de Mutação e Métrica Davies-Bouldin
*   **Equipe:** Marcos Daniel e Vinicius Macedo
*   **Instituição:** Instituto Federal do Norte de Minas Gerais (IFNMG)
*   **Disciplina:** Computação Natural
*   **Prazo de Entrega:** 02/07/2026

---

## Slide 2: Introdução
*   **Contextualização:**
    *   As melhorias anteriores (busca espacial contínua e diversidade) elevaram o desempenho, mas restaram gargalos:
        1.  *Instabilidade de convergência final:* Parâmetros de mutação estáticos causavam oscilação nas coordenadas dos centroides no fim da busca.
        2.  *Custo computacional:* O Índice Silhouette é quadrático $O(N^2)$, tornando-se proibitivo para grandes volumes de dados.
*   **Objetivo:**
    *   Implementar e validar duas frentes de Trabalhos Futuros: decaimento dinâmico de mutação e o índice Davies-Bouldin como métrica de afinidade.

---

## Slide 3: O Algoritmo ClonalG (Resumo)
*   **Princípio de Seleção Clonal:**
    *   **Anticorpos:** Conjuntos de centroides candidatos que se auto-organizam no espaço de busca.
    *   **Afinidade:** Métrica de qualidade do agrupamento (Silhouette ou Davies-Bouldin).
    *   **Clonagem:** Proporcional à afinidade (soluções boas multiplicam-se mais).
    *   **Hipermutação Somática:** Inversamente proporcional à afinidade (promove ajuste fino local em boas soluções e exploração em soluções piores).
    *   **Memória Imunológica:** Preservação estrita das melhores conformações e substituição dos piores anticorpos para manter diversidade.

---

## Slide 4: Proposta de Melhoria 1: Decaimento Dinâmico de Mutação
*   **O Mecanismo:**
    *   Fator de decaimento decresce linearmente conforme a geração atual $it$ sobre o total de iterações:
        $$\text{decay} = \max\left(0.05, 1.0 - \frac{it}{n\_iterations}\right)$$
*   **Aplicações Práticas no Algoritmo:**
    1.  *Mutação Estrutural:* Reduz a probabilidade de adicionar/remover centroides ao longo do tempo ($\alpha_{\text{novo}} = \alpha \times \text{decay}$), estabilizando o valor de $k$ descoberto.
    2.  *Hipermutação Paramétrica (Espacial):* Reduz o desvio padrão do ruído gaussiano aplicado nas coordenadas ($\sigma_{\text{novo}} = \sigma \times \text{decay}$).
*   **Benefício:** Comportamento clássico de *annealing* (alta exploração inicial e ajuste refinado/explotação no final).

---

## Slide 5: Proposta de Melhoria 2: Afinidade via Davies-Bouldin (DB)
*   **Métrica Davies-Bouldin:**
    *   Avalia a similaridade entre clusters analisando a razão da dispersão interna pela distância inter-cluster.
    *   Como é uma métrica de minimização, definimos a afinidade imunológica a ser maximizada como:
        $$A = -DB = - \frac{1}{k} \sum_{i=1}^{k} \max_{j \neq i} \left( \frac{S_i + S_j}{d(c_i, c_j)} \right)$$
*   **Vantagem Crítica:** Complexidade linear $O(N)$ em relação ao número de amostras, pois evita o cálculo da distância de todos os pares exigida pelo Silhouette. Ideal para Big Data.

---

## Slide 6: Comparação de Resultados - Silhouette Médio
Desempenho de Silhouette nas 4 variantes em 3 execuções:

| Variante / Algoritmo | DS1 | DS2 | DS3 | DS4 | DS5 |
| :--- | :---: | :---: | :---: | :---: | :---: |
| ClonalG Clássico (Lab 2) | 0.6480 | 0.6285 | 0.1979 | 0.5875 | 0.6644 |
| ClonalG Otimizado (Lab 4) | 0.6480 | 0.6158 | **0.2032** | **0.5902** | 0.6644 |
| **ClonalG com Decaimento (Sil)** | 0.6480 | **0.6539** | 0.1972 | **0.5902** | 0.6644 |
| ClonalG com Decaimento (DB) | 0.6480 | 0.6253 | 0.1650 | 0.5790 | 0.6644 |

*Nota: No DataSet 2, a inclusão do decaimento dinâmico de mutação permitiu estabilizar as coordenadas no ótimo exato, elevando a média para **0.6539**.*

---

## Slide 7: Comparação de Resultados - Davies-Bouldin Médio
Desempenho de dispersão interna (Davies-Bouldin - menor é melhor):

| Variante / Algoritmo | DS1 | DS2 | DS3 | DS4 | DS5 |
| :--- | :---: | :---: | :---: | :---: | :---: |
| ClonalG Clássico (Lab 2) | 0.4837 | 0.4949 | 1.5833 | 0.5397 | 0.5046 |
| ClonalG Otimizado (Lab 4) | 0.4837 | 0.5454 | 1.3903 | 0.5323 | 0.5046 |
| ClonalG com Decaimento (Sil) | 0.4837 | **0.3939** | 1.4307 | 0.5347 | 0.5046 |
| **ClonalG com Decaimento (DB)** | 0.4837 | 0.5161 | **1.3039** | **0.5312** | 0.5046 |

*Nota: Quando o algoritmo foi guiado pela métrica Davies-Bouldin, obteve com sucesso os melhores índices DB nos datasets 3 e 4, provando a eficácia da otimização orientada a essa métrica.*

---

## Slide 8: Comportamento de Convergência da Afinidade (Curvas)
*   **Evolução da Afinidade (Silhouette/DB):**
    *   *Visualização Gráfica:* O gráfico `evolucao_ds2.png` demonstra que o decaimento estabiliza a curva de Silhouette rapidamente, evitando as perturbações violentas observadas no Lab 4 sem decaimento.
    *   *Orientação à Afinidade:* O ClonalG com Davies-Bouldin exibe curva distinta por maximizar uma métrica de geometria diferente (DB), convergindo de forma extremamente célere no início.

---

## Slide 9: Conclusão
*   **Decaimento de Mutação:** O controle dinâmico da mutação de grande a pequena escala mitigou ruídos e assegurou ótimo refinamento espacial.
*   **Afinidade via Davies-Bouldin:** Validou-se como métrica viável, permitindo um tempo de computação reduzido enquanto gera agrupamentos coerentes sob uma formulação matemática de baixíssimo custo ($O(N)$).
*   **Balanço Geral:** As propostas de Trabalhos Futuros integraram com sucesso o SIA e a busca contínua, atingindo alto desempenho.
