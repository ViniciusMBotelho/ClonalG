"""Ponto de entrada principal do projeto.

Os parametros do ClonalG ficam nas constantes no topo de
experimentos_parametros.py. Execute este arquivo para rodar o fluxo atual:
o ClonalG testa os candidatos de k definidos em experimentos_parametros.py,
repassa o melhor k ao k-Means, e os resultados sao salvos.
"""

from experimentos_parametros import main


if __name__ == '__main__':
    main()
