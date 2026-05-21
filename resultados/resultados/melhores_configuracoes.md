# Execucao Configurada do ClonalG

- Fluxo: o ClonalG inicia em cada k candidato e usa mutacao estrutural para adicionar/remover centroides dentro dos limites configurados; o melhor k final do ClonalG e repassado ao k-Means.
- Afinidade interna do ClonalG: indice Silhouette.
- Mutacao: estrutural, adicionando/removendo centroides dentro dos limites configurados; sem ruido gaussiano.
- Parametros: N=15, rho=2.0, beta=15.0, replace_rate=0.1, selection_rate=0.85
- Candidatos/limites de k: 2,3,4,5,6
- Repeticoes por dataset: 3
- Geracoes por repeticao: 50

## Resultados

| DataSet | k | k_inicial_melhor | k_candidates | k_scores_medios_clonalg                                     | n_antibodies | rho | beta | replace_rate | selection_rate | runs | iterations | ClonalG_Media_Validacao | ClonalG_Melhor_Validacao | ClonalG_Pior_Validacao | KMeans_Silhouette_mesmo_k | Delta_Validacao_vs_KMeans_mesmo_k |
| ------- | - | ---------------- | ------------ | ----------------------------------------------------------- | ------------ | --- | ---- | ------------ | -------------- | ---- | ---------- | ----------------------- | ------------------------ | ---------------------- | ------------------------- | --------------------------------- |
| 1       | 3 | 2                | 2,3,4,5,6    | 2->3:0.6480;3->3:0.6480;4->3:0.6480;5->3:0.6430;6->3:0.6401 | 15           | 2.0 | 15.0 | 0.1          | 0.85           | 3    | 50         | 0.648                   | 0.648                    | 0.6479626689290785     | 0.648                     | 0.0                               |
| 2       | 2 | 4                | 2,3,4,5,6    | 2->2:0.4314;3->5:0.3939;4->2:0.5417;5->2:0.4593;6->5:0.3871 | 15           | 2.0 | 15.0 | 0.1          | 0.85           | 3    | 50         | 0.5417                  | 0.6158                   | 0.3933269282771896     | 0.3589                    | 0.1827                            |
| 3       | 6 | 4                | 2,3,4,5,6    | 2->2:0.1852;3->4:0.1937;4->6:0.1969;5->4:0.1916;6->4:0.1912 | 15           | 2.0 | 15.0 | 0.1          | 0.85           | 3    | 50         | 0.1969                  | 0.2041                   | 0.18815307806701034    | 0.2221                    | -0.0252                           |
| 4       | 4 | 4                | 2,3,4,5,6    | 2->4:0.5826;3->4:0.5696;4->4:0.5847;5->4:0.5845;6->4:0.5815 | 15           | 2.0 | 15.0 | 0.1          | 0.85           | 3    | 50         | 0.5847                  | 0.5898                   | 0.5769282165375607     | 0.5866                    | -0.0018                           |
| 5       | 2 | 2                | 2,3,4,5,6    | 2->2:0.6644;3->2:0.6644;4->2:0.6644;5->2:0.6644;6->2:0.6644 | 15           | 2.0 | 15.0 | 0.1          | 0.85           | 3    | 50         | 0.6644                  | 0.6644                   | 0.6643575754503649     | 0.6644                    | 0.0                               |