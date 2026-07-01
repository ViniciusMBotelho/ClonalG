# Execucao Configurada do ClonalG

- Fluxo: o ClonalG inicia em cada k candidato e usa mutacao estrutural para adicionar/remover centroides dentro dos limites configurados; o melhor k final do ClonalG e repassado ao k-Means.
- Afinidade interna do ClonalG: indice Silhouette.
- Mutacao: hibrida, com mutacao estrutural de k e mutacao parametrica gaussiana nos centroides existentes.
- Selecao: combina afinidade por Silhouette com recompensa por diversidade entre anticorpos.
- Parametros: N=15, rho=2.0, beta=5.0, replace_rate=0.3, selection_rate=0.5, parametric_mutation_scale=0.05, diversity_weight=0.15
- Candidatos/limites de k: 2,3,4,5,6
- Repeticoes por dataset: 3
- Geracoes por repeticao: 50

## Resultados

| DataSet | k | k_inicial_melhor | k_candidates | k_scores_medios_clonalg                                     | n_antibodies | rho | beta | replace_rate | selection_rate | parametric_mutation_scale | diversity_weight | runs | iterations | ClonalG_Media_Validacao | ClonalG_Melhor_Validacao | ClonalG_Pior_Validacao | KMeans_Silhouette_mesmo_k | Delta_Validacao_vs_KMeans_mesmo_k |
| ------- | - | ---------------- | ------------ | ----------------------------------------------------------- | ------------ | --- | ---- | ------------ | -------------- | ------------------------- | ---------------- | ---- | ---------- | ----------------------- | ------------------------ | ---------------------- | ------------------------- | --------------------------------- |
| 1       | 3 | 2                | 2,3,4,5,6    | 2->3:0.6480;3->3:0.6480;4->3:0.6473;5->3:0.6480;6->3:0.6473 | 15           | 2.0 | 5.0  | 0.3          | 0.5            | 0.05                      | 0.15             | 3    | 50         | 0.648                   | 0.648                    | 0.6479626689290785     | 0.648                     | 0.0                               |
| 2       | 2 | 2                | 2,3,4,5,6    | 2->2:0.6220;3->4:0.3950;4->2:0.4843;5->2:0.4612;6->2:0.4670 | 15           | 2.0 | 5.0  | 0.3          | 0.5            | 0.05                      | 0.15             | 3    | 50         | 0.622                   | 0.6539                   | 0.5961586340522335     | 0.3589                    | 0.263                             |
| 3       | 5 | 5                | 2,3,4,5,6    | 2->2:0.1876;3->2:0.1933;4->2:0.1892;5->5:0.2009;6->2:0.1909 | 15           | 2.0 | 5.0  | 0.3          | 0.5            | 0.05                      | 0.15             | 3    | 50         | 0.2009                  | 0.2067                   | 0.19685045200605852    | 0.222                     | -0.0211                           |
| 4       | 4 | 5                | 2,3,4,5,6    | 2->4:0.5872;3->4:0.5848;4->4:0.5859;5->4:0.5893;6->4:0.5888 | 15           | 2.0 | 5.0  | 0.3          | 0.5            | 0.05                      | 0.15             | 3    | 50         | 0.5893                  | 0.5905                   | 0.586802438216917      | 0.5866                    | 0.0027                            |
| 5       | 2 | 2                | 2,3,4,5,6    | 2->2:0.6644;3->2:0.6644;4->2:0.6644;5->2:0.6644;6->2:0.6644 | 15           | 2.0 | 5.0  | 0.3          | 0.5            | 0.05                      | 0.15             | 3    | 50         | 0.6644                  | 0.6644                   | 0.6643575754503649     | 0.6644                    | 0.0                               |