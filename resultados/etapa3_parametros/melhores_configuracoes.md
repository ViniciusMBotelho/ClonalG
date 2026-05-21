# Execucao Configurada do ClonalG

- Fluxo: o ClonalG inicia em cada k candidato e usa mutacao estrutural para adicionar/remover centroides dentro dos limites configurados; o melhor k final do ClonalG e repassado ao k-Means.
- Afinidade interna do ClonalG: distancia Euclidiana media ao centroide mais proximo, com sinal invertido.
- Silhouette: usado para registrar a evolucao, escolher o melhor k do ClonalG e comparar com k-Means.
- Parametros: N=100, rho=1.0, beta=15.0, replace_rate=0.1, selection_rate=0.85
- Candidatos/limites de k: 2,3,4,5,6
- Repeticoes por dataset: 3
- Geracoes por repeticao: 100

## Resultados

| DataSet | k | k_inicial_melhor | k_candidates | k_scores_medios_clonalg                                     | n_antibodies | rho | beta | replace_rate | selection_rate | runs | iterations | ClonalG_Media_Validacao | ClonalG_Melhor_Validacao | ClonalG_Pior_Validacao | KMeans_Silhouette_mesmo_k | Delta_Validacao_vs_KMeans_mesmo_k |
| ------- | - | ---------------- | ------------ | ----------------------------------------------------------- | ------------ | --- | ---- | ------------ | -------------- | ---- | ---------- | ----------------------- | ------------------------ | ---------------------- | ------------------------- | --------------------------------- |
| 1       | 6 | 5                | 2,3,4,5,6    | 2->6:0.3180;3->6:0.3204;4->6:0.3366;5->6:0.3806;6->6:0.3441 | 100          | 1.0 | 15.0 | 0.1          | 0.85           | 3    | 100        | 0.3806                  | 0.4518                   | 0.33852817735333546    | 0.3791                    | 0.0015                            |
| 2       | 6 | 4                | 2,3,4,5,6    | 2->6:0.3382;3->6:0.3443;4->6:0.3497;5->6:0.3444;6->6:0.3492 | 100          | 1.0 | 15.0 | 0.1          | 0.85           | 3    | 100        | 0.3497                  | 0.3555                   | 0.34571604318589866    | 0.3961                    | -0.0463                           |
| 3       | 6 | 6                | 2,3,4,5,6    | 2->6:0.2008;3->6:0.1975;4->6:0.1978;5->6:0.1960;6->6:0.2066 | 100          | 1.0 | 15.0 | 0.1          | 0.85           | 3    | 100        | 0.2066                  | 0.2116                   | 0.2038263622382543     | 0.2215                    | -0.0148                           |
| 4       | 6 | 6                | 2,3,4,5,6    | 2->6:0.4862;3->6:0.4768;4->6:0.4956;5->6:0.4855;6->6:0.5025 | 100          | 1.0 | 15.0 | 0.1          | 0.85           | 3    | 100        | 0.5025                  | 0.5064                   | 0.5000468408824853     | 0.4915                    | 0.0111                            |
| 5       | 6 | 2                | 2,3,4,5,6    | 2->6:0.1044;3->6:0.0910;4->6:0.0891;5->6:0.0918;6->6:0.1020 | 100          | 1.0 | 15.0 | 0.1          | 0.85           | 3    | 100        | 0.1044                  | 0.114                    | 0.08812914346841555    | 0.1368                    | -0.0324                           |