from Parametro import Parametro
from Contexto import Contexto
import datetime
if __name__ == '__main__':
    # incrementais
    LS3 = Parametro(list_drift_points=[300, 500], log_size=1000, list_paths_PNMLs=[
        "C:\\Users\\raduy\\Downloads\\ModelosIncrementais\\base.pnml",
        'C:\\Users\\raduy\\Downloads\\ModelosIncrementais\\I.pnml',
        'C:\\Users\\raduy\\Downloads\\ModelosIncrementais\\IO.pnml'],
                    output_final_path="LS3_INCREMENTAL",
                    initial_timestamp=datetime.datetime(
                        2021, 7, 13, 10, 0, 0))
    contexto = Contexto(LS3)
    contexto.incremental()

    LS18 = Parametro(list_dict=[{'tipo decaimento': 'linear', 'inicio': '300', 'fim': '600', 'divisoes drift': None}
                                ],

                     log_size=900,
                     list_paths_PNMLs=["C:\\Users\\raduy\\Downloads\\ModelosIncrementais\\base.pnml",
        'C:\\Users\\raduy\\Downloads\\ModelosIncrementais\\I.pnml'],
                     output_final_path="teste_GRADUAL",
                     initial_timestamp=datetime.datetime(2021, 7, 13, 10, 0, 0),
                     noise=None, gradual_generation_method='Probabilistico')
    contexto = Contexto(LS18)
    contexto.gradual()

