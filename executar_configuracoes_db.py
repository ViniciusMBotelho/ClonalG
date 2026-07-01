import pandas as pd

import experimentos_parametros as exp


CONFIGURACOES = [
    {
        'nome': 'C1',
        'pasta': 'resultados/resultados_db',
        'n_antibodies': 15,
        'rho': 2.0,
        'beta': 15.0,
        'replace_rate': 0.10,
        'selection_rate': 0.85,
    },
    {
        'nome': 'C2',
        'pasta': 'resultados/resultados2_db',
        'n_antibodies': 15,
        'rho': 2.0,
        'beta': 5.0,
        'replace_rate': 0.30,
        'selection_rate': 0.50,
    },
    {
        'nome': 'C3',
        'pasta': 'resultados/resultados3_db',
        'n_antibodies': 30,
        'rho': 2.0,
        'beta': 15.0,
        'replace_rate': 0.30,
        'selection_rate': 0.30,
    },
    {
        'nome': 'C4',
        'pasta': 'resultados/resultados4_db',
        'n_antibodies': 60,
        'rho': 3.5,
        'beta': 30.0,
        'replace_rate': 0.40,
        'selection_rate': 0.60,
    },
]


def executar_configuracao(item, datasets):
    config = dict(exp.CONFIG)
    config.update({
        'n_antibodies': item['n_antibodies'],
        'rho': item['rho'],
        'beta': item['beta'],
        'replace_rate': item['replace_rate'],
        'selection_rate': item['selection_rate'],
        'affinity_metric': 'davies_bouldin',
    })
    exp.validate_config(config)
    exp.OUTPUT_DIR = item['pasta']

    print(f"\n{item['nome']} DB -> {item['pasta']}")
    print(f"Parametros: {config}", flush=True)

    rows = []
    iteration_records = []
    run_records = []
    for ds_id, data in datasets.items():
        result, ds_iteration_records, ds_run_records = exp.evaluate_dataset(data, ds_id, config)
        rows.append(result)
        iteration_records.extend(ds_iteration_records)
        run_records.extend(ds_run_records)
        print(
            f"{item['nome']} DS{ds_id}: k={result['k']} "
            f"DB={result['ClonalG_DB_Medio_Validacao']:.4f} "
            f"| Silhouette={result['ClonalG_Media_Validacao']:.4f} "
            f"| k-Means DB={result['KMeans_DB_mesmo_k']:.4f}",
            flush=True,
        )

    df = pd.DataFrame(rows)
    iteration_df = pd.DataFrame(iteration_records)
    run_df = pd.DataFrame(run_records)
    exp.remove_grid_artifacts()
    exp.save_outputs(df, config, iteration_df, run_df)
    print(f"Resultados salvos em {exp.OUTPUT_DIR}/", flush=True)


def main():
    datasets = exp.load_datasets()
    if not datasets:
        print('Nenhum dataset pre-processado encontrado. Execute preprocessamento.py primeiro.')
        return

    for item in CONFIGURACOES:
        executar_configuracao(item, datasets)


if __name__ == '__main__':
    main()
