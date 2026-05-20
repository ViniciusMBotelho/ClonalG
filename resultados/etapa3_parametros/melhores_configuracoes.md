# Execucao Configurada do ClonalG

- Fluxo: os parametros sao definidos nas constantes do script; o ClonalG usa k fixo.
- Afinidade interna do ClonalG: distancia Euclidiana media ao centroide mais proximo, com sinal invertido.
- Silhouette: usado apenas na validacao final das execucoes e na comparacao com k-Means.
- Parametros: N=50, rho=2.0, beta=10.0, replace_rate=0.1, selection_rate=0.85, k=3
- Repeticoes por dataset: 3
- Geracoes por repeticao: 50

## Resultados

| DataSet | k   | n_antibodies | rho | beta | replace_rate | selection_rate | runs | iterations | ClonalG_Media_Validacao | ClonalG_Melhor_Validacao | ClonalG_Pior_Validacao | KMeans_Silhouette_mesmo_k | Delta_Validacao_vs_KMeans_mesmo_k |
| ------- | --- | ------------ | --- | ---- | ------------ | -------------- | ---- | ---------- | ----------------------- | ------------------------ | ---------------------- | ------------------------- | --------------------------------- |
| 1.0     | 3.0 | 50.0         | 2.0 | 10.0 | 0.1          | 0.85           | 3.0  | 50.0       | 0.648                   | 0.648                    | 0.6479626689290785     | 0.648                     | 0.0                               |
| 2.0     | 3.0 | 50.0         | 2.0 | 10.0 | 0.1          | 0.85           | 3.0  | 50.0       | 0.38                    | 0.3805                   | 0.3796642388953492     | 0.3807                    | -0.0007                           |
| 3.0     | 3.0 | 50.0         | 2.0 | 10.0 | 0.1          | 0.85           | 3.0  | 50.0       | 0.1929                  | 0.1973                   | 0.18971155604208878    | 0.1977                    | -0.0048                           |
| 4.0     | 3.0 | 50.0         | 2.0 | 10.0 | 0.1          | 0.85           | 3.0  | 50.0       | 0.5483                  | 0.5483                   | 0.5483211956419075     | 0.5483                    | 0.0                               |
| 5.0     | 3.0 | 50.0         | 2.0 | 10.0 | 0.1          | 0.85           | 3.0  | 50.0       | 0.3642                  | 0.3685                   | 0.35769588749363446    | 0.3724                    | -0.0082                           |