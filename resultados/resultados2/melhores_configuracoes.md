# Execucao Configurada do ClonalG

- Fluxo: o ClonalG inicia em cada k candidato e usa mutacao estrutural para adicionar/remover centroides dentro dos limites configurados; o melhor k final do ClonalG e repassado ao k-Means.
- Afinidade interna do ClonalG: indice Silhouette.
- Mutacao: estrutural, adicionando/removendo centroides dentro dos limites configurados; sem ruido gaussiano.
- Parametros: N=15, rho=2.0, beta=5.0, replace_rate=0.3, selection_rate=0.5
- Candidatos/limites de k: 2,3,4,5,6
- Repeticoes por dataset: 3
- Geracoes por repeticao: 50

## Resultados

| DataSet | k | k_inicial_melhor | k_candidates | k_scores_medios_clonalg                                     | n_antibodies | rho | beta | replace_rate | selection_rate | runs | iterations | ClonalG_Media_Validacao | ClonalG_Melhor_Validacao | ClonalG_Pior_Validacao | KMeans_Silhouette_mesmo_k | Delta_Validacao_vs_KMeans_mesmo_k |
| ------- | - | ---------------- | ------------ | ----------------------------------------------------------- | ------------ | --- | ---- | ------------ | -------------- | ---- | ---------- | ----------------------- | ------------------------ | ---------------------- | ------------------------- | --------------------------------- |
| 1       | 3 | 3                | 2,3,4,5,6    | 2->3:0.6473;3->3:0.6480;4->3:0.6480;5->3:0.6480;6->3:0.6473 | 15           | 2.0 | 5.0  | 0.3          | 0.5            | 3    | 50         | 0.648                   | 0.648                    | 0.6479626689290785     | 0.648                     | 0.0                               |
| 2       | 2 | 5                | 2,3,4,5,6    | 2->2:0.4838;3->2:0.4622;4->2:0.4610;5->2:0.5462;6->2:0.4397 | 15           | 2.0 | 5.0  | 0.3          | 0.5            | 3    | 50         | 0.5462                  | 0.6158                   | 0.406858445601303      | 0.3589                    | 0.1872                            |
| 3       | 5 | 3                | 2,3,4,5,6    | 2->4:0.1950;3->5:0.1995;4->4:0.1891;5->6:0.1925;6->5:0.1948 | 15           | 2.0 | 5.0  | 0.3          | 0.5            | 3    | 50         | 0.1995                  | 0.2078                   | 0.19091375616177467    | 0.222                     | -0.0225                           |
| 4       | 4 | 3                | 2,3,4,5,6    | 2->4:0.5720;3->4:0.5865;4->4:0.5841;5->4:0.5859;6->4:0.5684 | 15           | 2.0 | 5.0  | 0.3          | 0.5            | 3    | 50         | 0.5865                  | 0.5904                   | 0.579032517736098      | 0.5866                    | -0.0001                           |
| 5       | 2 | 2                | 2,3,4,5,6    | 2->2:0.6644;3->2:0.6644;4->2:0.6644;5->2:0.6644;6->2:0.6644 | 15           | 2.0 | 5.0  | 0.3          | 0.5            | 3    | 50         | 0.6644                  | 0.6644                   | 0.6643575754503649     | 0.6644                    | 0.0                               |