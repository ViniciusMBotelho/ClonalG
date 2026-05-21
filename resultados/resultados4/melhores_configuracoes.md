# Execucao Configurada do ClonalG

- Fluxo: o ClonalG inicia em cada k candidato e usa mutacao estrutural para adicionar/remover centroides dentro dos limites configurados; o melhor k final do ClonalG e repassado ao k-Means.
- Afinidade interna do ClonalG: indice Silhouette.
- Mutacao: estrutural, adicionando/removendo centroides dentro dos limites configurados; sem ruido gaussiano.
- Parametros: N=60, rho=3.5, beta=30.0, replace_rate=0.4, selection_rate=0.6
- Candidatos/limites de k: 2,3,4,5,6
- Repeticoes por dataset: 3
- Geracoes por repeticao: 50

## Resultados

| DataSet | k | k_inicial_melhor | k_candidates | k_scores_medios_clonalg                                     | n_antibodies | rho | beta | replace_rate | selection_rate | runs | iterations | ClonalG_Media_Validacao | ClonalG_Melhor_Validacao | ClonalG_Pior_Validacao | KMeans_Silhouette_mesmo_k | Delta_Validacao_vs_KMeans_mesmo_k |
| ------- | - | ---------------- | ------------ | ----------------------------------------------------------- | ------------ | --- | ---- | ------------ | -------------- | ---- | ---------- | ----------------------- | ------------------------ | ---------------------- | ------------------------- | --------------------------------- |
| 1       | 3 | 2                | 2,3,4,5,6    | 2->3:0.6480;3->3:0.6480;4->3:0.6480;5->4:0.6480;6->3:0.6480 | 60           | 3.5 | 30.0 | 0.4          | 0.6            | 3    | 50         | 0.648                   | 0.648                    | 0.6479626689290785     | 0.648                     | 0.0                               |
| 2       | 2 | 6                | 2,3,4,5,6    | 2->2:0.6207;3->2:0.6174;4->2:0.5428;5->2:0.6253;6->2:0.6285 | 60           | 3.5 | 30.0 | 0.4          | 0.6            | 3    | 50         | 0.6285                  | 0.6539                   | 0.6158135544625102     | 0.3589                    | 0.2696                            |
| 3       | 6 | 2                | 2,3,4,5,6    | 2->6:0.2006;3->4:0.1990;4->6:0.1962;5->5:0.1990;6->6:0.1976 | 60           | 3.5 | 30.0 | 0.4          | 0.6            | 3    | 50         | 0.2006                  | 0.2066                   | 0.19261456961449297    | 0.2221                    | -0.0215                           |
| 4       | 4 | 4                | 2,3,4,5,6    | 2->4:0.5871;3->4:0.5894;4->4:0.5902;5->4:0.5890;6->5:0.5900 | 60           | 3.5 | 30.0 | 0.4          | 0.6            | 3    | 50         | 0.5902                  | 0.5905                   | 0.5895471111021305     | 0.5866                    | 0.0036                            |
| 5       | 2 | 2                | 2,3,4,5,6    | 2->2:0.6644;3->2:0.6644;4->2:0.6644;5->2:0.6644;6->2:0.6644 | 60           | 3.5 | 30.0 | 0.4          | 0.6            | 3    | 50         | 0.6644                  | 0.6644                   | 0.6643575754503649     | 0.6644                    | 0.0                               |