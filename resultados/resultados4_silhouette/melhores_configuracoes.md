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
| 2       | 2 | 4                | 2,3,4,5,6    | 2->2:0.6209;3->2:0.6285;4->2:0.6507;5->2:0.6380;6->2:0.6253 | 60           | 3.5 | 30.0 | 0.4          | 0.6            | 0.05                      | 0.15             | 3    | 50         | 0.6507                  | 0.6539                   | 0.6443188990168992     | 0.3589                    | 0.2918                            |
| 3       | 5 | 6                | 2,3,4,5,6    | 2->3:0.1941;3->5:0.2015;4->4:0.1990;5->5:0.1995;6->5:0.2017 | 60           | 3.5 | 30.0 | 0.4          | 0.6            | 0.05                      | 0.15             | 3    | 50         | 0.2017                  | 0.2121                   | 0.19450272851821346    | 0.222                     | -0.0203                           |
| 4       | 4 | 4                | 2,3,4,5,6    | 2->4:0.5902;3->4:0.5890;4->4:0.5903;5->4:0.5891;6->4:0.5896 | 60           | 3.5 | 30.0 | 0.4          | 0.6            | 0.05                      | 0.15             | 3    | 50         | 0.5903                  | 0.5905                   | 0.5898349141504893     | 0.5866                    | 0.0037                            |
| 5       | 2 | 2                | 2,3,4,5,6    | 2->2:0.6644;3->2:0.6644;4->2:0.6644;5->2:0.6644;6->2:0.6644 | 60           | 3.5 | 30.0 | 0.4          | 0.6            | 0.05                      | 0.15             | 3    | 50         | 0.6644                  | 0.6644                   | 0.6643575754503649     | 0.6644                    | 0.0                               |