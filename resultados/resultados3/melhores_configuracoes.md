# Execucao Configurada do ClonalG

- Fluxo: o ClonalG inicia em cada k candidato e usa mutacao estrutural para adicionar/remover centroides dentro dos limites configurados; o melhor k final do ClonalG e repassado ao k-Means.
- Afinidade interna do ClonalG: indice Silhouette.
- Mutacao: estrutural, adicionando/removendo centroides dentro dos limites configurados; sem ruido gaussiano.
- Parametros: N=30, rho=2.0, beta=15.0, replace_rate=0.3, selection_rate=0.3
- Candidatos/limites de k: 2,3,4,5,6
- Repeticoes por dataset: 3
- Geracoes por repeticao: 50

## Resultados

| DataSet | k | k_inicial_melhor | k_candidates | k_scores_medios_clonalg                                     | n_antibodies | rho | beta | replace_rate | selection_rate | runs | iterations | ClonalG_Media_Validacao | ClonalG_Melhor_Validacao | ClonalG_Pior_Validacao | KMeans_Silhouette_mesmo_k | Delta_Validacao_vs_KMeans_mesmo_k |
| ------- | - | ---------------- | ------------ | ----------------------------------------------------------- | ------------ | --- | ---- | ------------ | -------------- | ---- | ---------- | ----------------------- | ------------------------ | ---------------------- | ------------------------- | --------------------------------- |
| 1       | 3 | 2                | 2,3,4,5,6    | 2->3:0.6480;3->3:0.6480;4->3:0.6480;5->3:0.6480;6->3:0.6480 | 30           | 2.0 | 15.0 | 0.3          | 0.3            | 3    | 50         | 0.648                   | 0.648                    | 0.6479626689290785     | 0.648                     | 0.0                               |
| 2       | 2 | 5                | 2,3,4,5,6    | 2->2:0.4947;3->2:0.5491;4->2:0.5388;5->2:0.6318;6->2:0.4818 | 30           | 2.0 | 15.0 | 0.3          | 0.3            | 3    | 50         | 0.6318                  | 0.6637                   | 0.6158135544625102     | 0.3589                    | 0.2729                            |
| 3       | 5 | 3                | 2,3,4,5,6    | 2->6:0.1927;3->5:0.1992;4->4:0.1936;5->5:0.1952;6->2:0.1934 | 30           | 2.0 | 15.0 | 0.3          | 0.3            | 3    | 50         | 0.1992                  | 0.2048                   | 0.19135694329410413    | 0.222                     | -0.0229                           |
| 4       | 4 | 6                | 2,3,4,5,6    | 2->4:0.5826;3->4:0.5874;4->4:0.5853;5->4:0.5863;6->4:0.5877 | 30           | 2.0 | 15.0 | 0.3          | 0.3            | 3    | 50         | 0.5877                  | 0.5894                   | 0.5867775587285363     | 0.5866                    | 0.0011                            |
| 5       | 2 | 2                | 2,3,4,5,6    | 2->2:0.6644;3->2:0.6644;4->2:0.6644;5->2:0.6644;6->2:0.6644 | 30           | 2.0 | 15.0 | 0.3          | 0.3            | 3    | 50         | 0.6644                  | 0.6644                   | 0.6643575754503649     | 0.6644                    | 0.0                               |