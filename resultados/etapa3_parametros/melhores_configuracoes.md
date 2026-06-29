# Execucao Configurada do ClonalG

- Fluxo: o ClonalG inicia em cada k candidato e usa mutacao estrutural para adicionar/remover centroides dentro dos limites configurados; o melhor k final do ClonalG e repassado ao k-Means.
- Afinidade interna do ClonalG: indice Silhouette.
- Mutacao: hibrida, com mutacao estrutural de k e mutacao parametrica gaussiana nos centroides existentes.
- Selecao: combina afinidade por Silhouette com recompensa por diversidade entre anticorpos.
- Parametros: N=60, rho=3.5, beta=30.0, replace_rate=0.4, selection_rate=0.6, parametric_mutation_scale=0.05, diversity_weight=0.15
- Candidatos/limites de k: 2,3,4,5,6
- Repeticoes por dataset: 3
- Geracoes por repeticao: 50

## Resultados

| DataSet | k | k_inicial_melhor | k_candidates | k_scores_medios_clonalg                                     | n_antibodies | rho | beta | replace_rate | selection_rate | parametric_mutation_scale | diversity_weight | runs | iterations | ClonalG_Media_Validacao | ClonalG_Melhor_Validacao | ClonalG_Pior_Validacao | KMeans_Silhouette_mesmo_k | Delta_Validacao_vs_KMeans_mesmo_k |
| ------- | - | ---------------- | ------------ | ----------------------------------------------------------- | ------------ | --- | ---- | ------------ | -------------- | ------------------------- | ---------------- | ---- | ---------- | ----------------------- | ------------------------ | ---------------------- | ------------------------- | --------------------------------- |
| 1       | 3 | 2                | 2,3,4,5,6    | 2->3:0.6480;3->3:0.6480;4->3:0.6480;5->3:0.6480;6->3:0.6480 | 60           | 3.5 | 30.0 | 0.4          | 0.6            | 0.05                      | 0.15             | 3    | 50         | 0.648                   | 0.648                    | 0.6479626689290785     | 0.648                     | 0.0                               |
| 2       | 2 | 5                | 2,3,4,5,6    | 2->2:0.6287;3->2:0.6033;4->2:0.6334;5->2:0.6383;6->2:0.5719 | 60           | 3.5 | 30.0 | 0.4          | 0.6            | 0.05                      | 0.15             | 3    | 50         | 0.6383                  | 0.6539                   | 0.6305303233075273     | 0.3589                    | 0.2794                            |
| 3       | 6 | 5                | 2,3,4,5,6    | 2->5:0.1988;3->5:0.2045;4->5:0.2064;5->6:0.2064;6->6:0.2050 | 60           | 3.5 | 30.0 | 0.4          | 0.6            | 0.05                      | 0.15             | 3    | 50         | 0.2064                  | 0.2119                   | 0.2008266518898216     | 0.2221                    | -0.0157                           |
| 4       | 4 | 3                | 2,3,4,5,6    | 2->4:0.5884;3->4:0.5905;4->4:0.5893;5->4:0.5890;6->4:0.5901 | 60           | 3.5 | 30.0 | 0.4          | 0.6            | 0.05                      | 0.15             | 3    | 50         | 0.5905                  | 0.5905                   | 0.5904452094532344     | 0.5866                    | 0.0039                            |
| 5       | 2 | 2                | 2,3,4,5,6    | 2->2:0.6644;3->2:0.6644;4->2:0.6644;5->2:0.6644;6->2:0.6644 | 60           | 3.5 | 30.0 | 0.4          | 0.6            | 0.05                      | 0.15             | 3    | 50         | 0.6644                  | 0.6644                   | 0.6643575754503649     | 0.6644                    | 0.0                               |