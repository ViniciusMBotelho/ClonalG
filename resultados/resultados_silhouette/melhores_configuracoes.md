# Execucao Configurada do ClonalG

- Fluxo: o ClonalG inicia em cada k candidato e usa mutacao estrutural para adicionar/remover centroides dentro dos limites configurados; o melhor k final do ClonalG e repassado ao k-Means.
- Afinidade interna do ClonalG: indice Silhouette.
- Mutacao: hibrida, com mutacao estrutural de k e mutacao parametrica gaussiana nos centroides existentes.
- Selecao: combina afinidade por Silhouette com recompensa por diversidade entre anticorpos.
- Parametros: N=15, rho=2.0, beta=15.0, replace_rate=0.1, selection_rate=0.85, parametric_mutation_scale=0.05, diversity_weight=0.15
- Candidatos/limites de k: 2,3,4,5,6
- Repeticoes por dataset: 3
- Geracoes por repeticao: 50

## Resultados

| DataSet | k | k_inicial_melhor | k_candidates | k_scores_medios_clonalg                                     | n_antibodies | rho | beta | replace_rate | selection_rate | parametric_mutation_scale | diversity_weight | runs | iterations | ClonalG_Media_Validacao | ClonalG_Melhor_Validacao | ClonalG_Pior_Validacao | KMeans_Silhouette_mesmo_k | Delta_Validacao_vs_KMeans_mesmo_k |
| ------- | - | ---------------- | ------------ | ----------------------------------------------------------- | ------------ | --- | ---- | ------------ | -------------- | ------------------------- | ---------------- | ---- | ---------- | ----------------------- | ------------------------ | ---------------------- | ------------------------- | --------------------------------- |
| 1       | 3 | 2                | 2,3,4,5,6    | 2->3:0.6480;3->3:0.6480;4->3:0.6480;5->3:0.6480;6->3:0.6480 | 15           | 2.0 | 15.0 | 0.1          | 0.85           | 0.05                      | 0.15             | 3    | 50         | 0.648                   | 0.648                    | 0.6479626689290785     | 0.648                     | 0.0                               |
| 2       | 2 | 2                | 2,3,4,5,6    | 2->2:0.5908;3->4:0.3979;4->4:0.3892;5->4:0.3951;6->4:0.3851 | 15           | 2.0 | 15.0 | 0.1          | 0.85           | 0.05                      | 0.15             | 3    | 50         | 0.5908                  | 0.6158                   | 0.5782895886086112     | 0.3589                    | 0.2319                            |
| 3       | 5 | 5                | 2,3,4,5,6    | 2->3:0.1917;3->6:0.2030;4->6:0.1997;5->5:0.2044;6->5:0.1959 | 15           | 2.0 | 15.0 | 0.1          | 0.85           | 0.05                      | 0.15             | 3    | 50         | 0.2044                  | 0.2062                   | 0.20312001729524767    | 0.222                     | -0.0176                           |
| 4       | 4 | 3                | 2,3,4,5,6    | 2->4:0.5812;3->4:0.5869;4->4:0.5864;5->4:0.5806;6->4:0.5746 | 15           | 2.0 | 15.0 | 0.1          | 0.85           | 0.05                      | 0.15             | 3    | 50         | 0.5869                  | 0.5887                   | 0.5832019340200274     | 0.5866                    | 0.0003                            |
| 5       | 2 | 2                | 2,3,4,5,6    | 2->2:0.6644;3->2:0.6644;4->2:0.6644;5->2:0.6644;6->2:0.6644 | 15           | 2.0 | 15.0 | 0.1          | 0.85           | 0.05                      | 0.15             | 3    | 50         | 0.6644                  | 0.6644                   | 0.6643575754503649     | 0.6644                    | 0.0                               |