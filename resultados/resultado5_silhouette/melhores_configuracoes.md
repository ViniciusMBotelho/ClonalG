# Execucao Configurada do ClonalG

- Fluxo: o ClonalG inicia em cada k candidato e usa mutacao estrutural para adicionar/remover centroides dentro dos limites configurados; o melhor k final do ClonalG e repassado ao k-Means.
- Afinidade interna do ClonalG: silhouette.
- Mutacao: hibrida, com mutacao estrutural de k e mutacao parametrica gaussiana nos centroides existentes.
- Selecao: combina afinidade por Silhouette com recompensa por diversidade entre anticorpos.
- Parametros: N=80, rho=1.2, beta=25.0, replace_rate=0.55, selection_rate=0.4, parametric_mutation_scale=0.12, diversity_weight=0.25
- Candidatos/limites de k: 2,3,4,5,6
- Repeticoes por dataset: 3
- Geracoes por repeticao: 150

## Resultados

| DataSet | k | k_inicial_melhor | k_candidates | k_scores_medios_clonalg                                     | n_antibodies | rho | beta | replace_rate | selection_rate | parametric_mutation_scale | diversity_weight | affinity_metric | runs | iterations | ClonalG_Media_Validacao | ClonalG_Melhor_Validacao | ClonalG_Pior_Validacao | ClonalG_DB_Medio_Validacao | ClonalG_DB_Melhor_Validacao | ClonalG_DB_Pior_Validacao | KMeans_Silhouette_mesmo_k | Delta_Validacao_vs_KMeans_mesmo_k | KMeans_DB_mesmo_k | Delta_DB_vs_KMeans_mesmo_k |
| ------- | - | ---------------- | ------------ | ----------------------------------------------------------- | ------------ | --- | ---- | ------------ | -------------- | ------------------------- | ---------------- | --------------- | ---- | ---------- | ----------------------- | ------------------------ | ---------------------- | -------------------------- | --------------------------- | ------------------------- | ------------------------- | --------------------------------- | ----------------- | -------------------------- |
| 3       | 6 | 4                | 2,3,4,5,6    | 2->6:0.2153;3->6:0.2150;4->6:0.2235;5->6:0.2179;6->6:0.2174 | 80           | 1.2 | 25.0 | 0.55         | 0.4            | 0.12                      | 0.25             | silhouette      | 3    | 150        | 0.2235                  | 0.2301                   | 0.2140984398278399     | 1.2363                     | 1.2195                      | 1.2455348686093228        | 0.2221                    | 0.0014                            | 1.2582            | -0.022                     |