# Execucao Configurada do ClonalG

- Fluxo: o ClonalG inicia em cada k candidato e usa mutacao estrutural para adicionar/remover centroides dentro dos limites configurados; o melhor k final do ClonalG e repassado ao k-Means.
- Afinidade interna do ClonalG: indice Silhouette.
- Mutacao: hibrida, com mutacao estrutural de k e mutacao parametrica gaussiana nos centroides existentes.
- Selecao: combina afinidade por Silhouette com recompensa por diversidade entre anticorpos.
- Parametros: N=30, rho=2.0, beta=15.0, replace_rate=0.3, selection_rate=0.3, parametric_mutation_scale=0.05, diversity_weight=0.15
- Candidatos/limites de k: 2,3,4,5,6
- Repeticoes por dataset: 3
- Geracoes por repeticao: 50

## Resultados

| DataSet | k | k_inicial_melhor | k_candidates | k_scores_medios_clonalg                                     | n_antibodies | rho | beta | replace_rate | selection_rate | parametric_mutation_scale | diversity_weight | runs | iterations | ClonalG_Media_Validacao | ClonalG_Melhor_Validacao | ClonalG_Pior_Validacao | KMeans_Silhouette_mesmo_k | Delta_Validacao_vs_KMeans_mesmo_k |
| ------- | - | ---------------- | ------------ | ----------------------------------------------------------- | ------------ | --- | ---- | ------------ | -------------- | ------------------------- | ---------------- | ---- | ---------- | ----------------------- | ------------------------ | ---------------------- | ------------------------- | --------------------------------- |
| 1       | 3 | 2                | 2,3,4,5,6    | 2->3:0.6480;3->3:0.6480;4->3:0.6480;5->3:0.6480;6->3:0.6480 | 30           | 2.0 | 15.0 | 0.3          | 0.3            | 0.05                      | 0.15             | 3    | 50         | 0.648                   | 0.648                    | 0.6479626689290785     | 0.648                     | 0.0                               |
| 2       | 2 | 6                | 2,3,4,5,6    | 2->2:0.4919;3->4:0.3972;4->2:0.4730;5->2:0.5281;6->2:0.6285 | 30           | 2.0 | 15.0 | 0.3          | 0.3            | 0.05                      | 0.15             | 3    | 50         | 0.6285                  | 0.6539                   | 0.6158135544625102     | 0.3589                    | 0.2696                            |
| 3       | 6 | 4                | 2,3,4,5,6    | 2->4:0.1980;3->4:0.2027;4->6:0.2067;5->5:0.2000;6->5:0.1969 | 30           | 2.0 | 15.0 | 0.3          | 0.3            | 0.05                      | 0.15             | 3    | 50         | 0.2067                  | 0.2111                   | 0.2035868269194311     | 0.2221                    | -0.0153                           |
| 4       | 4 | 5                | 2,3,4,5,6    | 2->4:0.5896;3->4:0.5877;4->4:0.5885;5->4:0.5900;6->4:0.5875 | 30           | 2.0 | 15.0 | 0.3          | 0.3            | 0.05                      | 0.15             | 3    | 50         | 0.59                    | 0.5905                   | 0.5891245282172711     | 0.5866                    | 0.0035                            |
| 5       | 2 | 2                | 2,3,4,5,6    | 2->2:0.6644;3->2:0.6644;4->2:0.6644;5->2:0.6644;6->2:0.6644 | 30           | 2.0 | 15.0 | 0.3          | 0.3            | 0.05                      | 0.15             | 3    | 50         | 0.6644                  | 0.6644                   | 0.6643575754503649     | 0.6644                    | 0.0                               |