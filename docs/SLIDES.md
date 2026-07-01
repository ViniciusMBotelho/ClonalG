# Apresentação: Otimização do Algoritmo ClonalG para Agrupamento de Dados

Este documento sintetiza os slides da apresentação do projeto prático de Computação Natural.

---

## Slide 1: Título e Identificação
*   **Título:** Otimização do Algoritmo ClonalG para Agrupamento de Dados
*   **Subtítulo:** Busca Local Contínua, Diversidade e Mutação Adaptativa
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
    1.  **Afinidade Configurável:** Suporte ao Índice Silhouette e ao Davies-Bouldin.
    2.  **Mutação Estrutural de $k$:** Operações de adição/remoção de centroides para auto-organização do número ideal de clusters.
    3.  **NOVO: Hipermutação Paramétrica:** Busca local no espaço contínuo por perturbação gaussiana dos centroides.
    4.  **NOVO: Decaimento Temporal da Mutação:** Redução gradual da intensidade de mutação ao longo das gerações.
    5.  **NOVO: Seleção por Diversidade na Memória:** Ponderação que recompensa anticorpos que representam soluções distintas no espaço de busca.

---

## Slide 4: Pseudocódigo do ClonalG Otimizado

```text
Entrada: dados X, candidatos de k, tamanho da população N,
         rho, beta, taxa de seleção, taxa de substituição,
         métrica de afinidade, número de iterações

Para cada valor inicial de k:
    Criar população inicial de anticorpos
    Calcular afinidade inicial por Silhouette ou Davies-Bouldin
    Separar memória e repertório

    Para cada iteração:
        Calcular fator de decaimento temporal da mutação
        Selecionar os melhores anticorpos da memória
        Para cada anticorpo selecionado:
            Gerar clones proporcionalmente à afinidade
            Aplicar hipermutação estrutural e paramétrica com decaimento
        Calcular afinidade dos clones
        Combinar memória, repertório e clones
        Manter os melhores na memória usando afinidade + diversidade
        Substituir parte dos piores indivíduos por novos anticorpos
        Guardar o melhor resultado obtido

Comparar o melhor ClonalG com o k-Médias usando o mesmo k final.
```

---

## Slide 5: Solução Adotada - Detalhamento Técnico das Melhorias
1.  **Hipermutação Paramétrica (Busca Local Contínua):**
    *   A cada clone, além da mutação de $k$, aplica-se um ruído gaussiano às coordenadas dos centroides:
        $$C_i \leftarrow C_i + \mathcal{N}(0, \sigma^2)$$
    *   O desvio padrão $\sigma$ é controlado dinamicamente pela afinidade normalizada $A_{\text{norm}}$ e pelo fator temporal $d(t)$:
        $$\sigma = \text{scale} \times d(t) \times e^{-\rho \cdot A_{\text{norm}}}$$
    *   *Intuição:* Centróides ruins sofrem grande variação espacial; centróides excelentes sofrem pequenos ajustes; nas gerações finais a busca estabiliza.

2.  **Davies-Bouldin como Métrica Alternativa de Afinidade:**
    *   O Silhouette continua sendo a métrica principal dos resultados.
    *   O Davies-Bouldin mede a similaridade entre clusters; quanto menor, melhor.
    *   Para manter o ClonalG maximizando afinidade, o código usa:
        $$\text{afinidade} = -DB$$

3.  **Decaimento Temporal da Mutação:**
    *   A intensidade da mutação diminui conforme a iteração avança:
        $$d(t) = \max(0.05, 1 - t/T)$$
    *   Isso favorece exploração no começo e refinamento no fim.

4.  **Seleção Guiada por Diversidade (Preservação de Nichos):**
    *   Evita redundâncias na Memória Imunológica ($A_{bm}$).
    *   Distância entre anticorpos $a$ e $b$ calculada via matching mínimo de centroides:
        $$D(a, b) = \frac{1}{2} \left( \text{mean}_i \min_j d(a_i, b_j) + \text{mean}_j \min_i d(a_i, b_j) \right)$$
    *   Fórmula de seleção de memória combinada:
        $$\text{Score} = A_{\text{norm}} + w_{\text{div}} \times \text{Diversity}_{\text{norm}}$$

---

## Slide 6: Metodologia e Configurações Experimentais
*   **Datasets Utilizados:** 5 conjuntos de dados normalizados (DS1 a DS5), contendo diferentes geometrias e dimensionalidades.
*   **Configurações repetidas da versão antiga:**
    *   C1: $N=15$, $\rho=2.0$, $\beta=15.0$, substituição $0.10$, seleção $0.85$.
    *   C2: $N=15$, $\rho=2.0$, $\beta=5.0$, substituição $0.30$, seleção $0.50$.
    *   C3: $N=30$, $\rho=2.0$, $\beta=15.0$, substituição $0.30$, seleção $0.30$.
    *   C4: $N=60$, $\rho=3.5$, $\beta=30.0$, substituição $0.40$, seleção $0.60$.
*   **Novos componentes mantidos em todas as configurações:** mutação paramétrica com `scale=0.05`, seleção por diversidade com $w_{\text{div}}=0.15$ e decaimento temporal da mutação.
*   **Validação:** 3 runs independentes por dataset, 50 iterações por execução e candidatos de $k \in \{2,3,4,5,6\}$.

---

## Slide 7: Resultados - Algoritmo Antigo vs Algoritmo Novo

| Config. | Média antiga | Média nova | Ganho médio | Maior ganho pontual |
| :---: | ---: | ---: | ---: | :--- |
| C1 | 0.5271 | 0.5389 | +0.0117 | DS2: +0.0491 |
| C2 | 0.5289 | 0.5449 | **+0.0160** | **DS2: +0.0758** |
| C3 | 0.5462 | 0.5475 | +0.0013 | DS3: +0.0075 |
| C4 | 0.5463 | **0.5510** | +0.0047 | DS2: +0.0222 |

*Leitura principal: o algoritmo novo melhorou a média em todas as configurações. A maior média geral foi C4 nova, enquanto o maior ganho pontual ocorreu no DS2 com C2.*

---

## Slide 8: Resultados - Melhor ClonalG Novo vs k-Means

| Dataset | Melhor config. | k final | ClonalG novo | k-Means | Delta |
| :---: | :---: | ---: | ---: | ---: | ---: |
| DS1 | C1-C4 | 3 | 0.6480 | 0.6480 | 0.0000 |
| DS2 | C4 | 2 | **0.6507** | 0.3589 | **+0.2918** |
| DS3 | C3 | 6 | 0.2067 | **0.2221** | -0.0153 |
| DS4 | C4 | 4 | **0.5903** | 0.5866 | **+0.0037** |
| DS5 | C1-C4 | 2 | 0.6644 | 0.6644 | 0.0000 |

*Leitura principal: após comparar antigo vs novo, o melhor ClonalG novo é comparado com o k-Means usando o mesmo k final encontrado pelo ClonalG.*

---

## Slide 9: Resultados - Onde a Melhoria Teve Mais Impacto

| Dataset | Média antiga | Média nova | Ganho | Leitura |
| :---: | ---: | ---: | ---: | :--- |
| DS1 | 0.6480 | 0.6480 | 0.0000 | Estrutura já resolvida pela versão antiga |
| DS2 | 0.5870 | **0.6230** | **+0.0359** | Maior benefício da diversidade e ajuste local |
| DS3 | 0.1990 | 0.2034 | +0.0044 | Reduziu a perda, mas k-Means ainda ficou acima |
| DS4 | 0.5873 | 0.5891 | +0.0018 | Ganho pequeno, porém consistente |
| DS5 | 0.6644 | 0.6644 | 0.0000 | Empate estável nas duas versões |

---

## Slide 10: Discussão dos Resultados
*   **Por que o ClonalG Otimizado superou o k-Means no DS2?**
    *   O k-Means é altamente dependente da inicialização e foi capturado por mínimos locais. A busca global estocástica do ClonalG combinada com o refinamento contínuo da hipermutação paramétrica permitiu encontrar o agrupamento ótimo global.
*   **O papel da seleção por diversidade:**
    *   A diversidade evitou que todos os anticorpos de memória convergissem para a mesma região de busca. Isso permitiu a avaliação simultânea de diferentes estruturas de $k$ durante a busca evolutiva.
*   **O papel da mutação paramétrica:**
    *   Ao adicionar ruído contínuo gaussiano, o ClonalG conseguiu deslocar os centroides de forma suave, permitindo ajustar a posição ideal mesmo quando as amostras originais do dataset não coincidiam exatamente com os centros ideais dos clusters.
*   **O papel do decaimento temporal e do Davies-Bouldin:**
    *   O decaimento temporal controla a busca: exploração maior no início e ajustes menores no fim.
    *   O Davies-Bouldin torna a afinidade configurável, permitindo testar outro critério de qualidade sem alterar o fluxo principal do ClonalG.

---

## Slide 11: Conclusão
*   O ClonalG Otimizado resolve eficientemente a limitação clássica do k-Means (sensibilidade a mínimos locais e necessidade de $k$ fixo).
*   A introdução de busca contínua via mutação gaussiana, decaimento temporal e preservação de nichos via seleção de diversidade melhoraram consideravelmente a robustez do algoritmo imunológico comparado à versão básica.
*   O suporte ao Davies-Bouldin ampliou o algoritmo para trabalhar com mais de um objetivo de qualidade de agrupamento.
*   A abordagem consolida as vantagens de algoritmos evolucionários/imunológicos globais para problemas complexos de aprendizado de máquina não supervisionado.
