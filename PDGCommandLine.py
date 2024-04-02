"""
Exemplo de comando:
python CommandLine.py -driftType gradual -logSize 1000 -outputPath "C:\\Users\\raduy\\D
ocuments\\Research\\Codigo\\ConjuntoLS_QUALI\\teste.xes" -listDict "[{'tipo decaimento': 'linear', 'inicio': 300, 'fim': 500, 'divisoes drift': None}, {'ti
po decaimento': 'exponencial', 'inicio': 800, 'fim': 1200, 'divisoes drift': None}]" -gradualMethod Probabilistico -listPathsPNMLs "C:\\Users\\raduy\\Downloads\\ModelosIncrementais\\base.pnml" "C:\\Users\\raduy\\Downloads\\ModelosIncrementais\\I.pnml"





"""
import argparse
import datetime
from Parametro import Parametro
from Contexto import Contexto


def validar_list_dict(list_dict_str):
    if not list_dict_str.strip():
        return []
    try:
        list_dict = eval(list_dict_str)
        for item in list_dict:
            assert item['tipo decaimento'] in ['linear', 'exponencial'], "Tipo de decaimento inválido."
            assert isinstance(item['inicio'], int) and item[
                'inicio'] > 0, "'inicio' deve ser um valor inteiro positivo."
            assert isinstance(item['fim'], int) and item['fim'] > item['inicio'], "'fim' deve ser maior que 'inicio'."
            if item.get('divisoes drift') is not None:
                assert isinstance(item['divisoes drift'], int) and item[
                    'divisoes drift'] > 0, "'divisoes drift' deve ser o valor None ou um valor inteiro positivo."
        return list_dict
    except (AssertionError, SyntaxError, ValueError) as e:
        raise argparse.ArgumentTypeError(f"Erro ao validar listDict: {e}")


class Commandline():
    @staticmethod
    def main():
        parser = argparse.ArgumentParser(description="PDG VIA LINHA DE COMANDO")

        # Definição dos argumentos
        parser.add_argument("-driftType", type=str, choices=['abrupto', 'gradual', 'incremental', 'recurring'],
                            required=True, help="Tipo de drift para simulação.")
        parser.add_argument("-logSize", type=int, required=True, help="Número de traços do log simulado.")
        parser.add_argument("-outputPath", type=str, required=True, help="Caminho para o arquivo de saída.")
        parser.add_argument("-listDriftPoints", nargs='*', type=int, default=[],
                            help="Lista de pontos de drift para tipos abrupto, incremental ou recorrente.")
        parser.add_argument("-initialTimestamp", type=lambda s: datetime.datetime.strptime(s, '%Y-%m-%d %H:%M:%S'),
                            default=datetime.datetime(2021, 7, 13, 10, 0, 0),
                            help="Timestamp inicial no formato AAAA-MM-DD HH:MM:SS.")
        parser.add_argument("-listDict", type=validar_list_dict, default="[]",
                            help="Lista de dicionários para configuração de drifts graduais.")
        parser.add_argument("-gradualMethod", type=str, choices=['Deterministico', 'Probabilistico'],
                            help="Método de geração gradual (Deterministico ou Probabilistico).")
        parser.add_argument("-listPathsPNMLs", nargs='+', type=str, default=[],
                            help="Lista de caminhos para arquivos PNML.")

        args = parser.parse_args()

        # Verificações específicas com base no tipo de drift
        if args.driftType == 'gradual':
            if not args.listDict or not args.gradualMethod:
                parser.error("Para driftType 'gradual', -listDict e -gradualMethod são obrigatórios.")
        elif args.driftType in ['abrupto', 'incremental', 'recorrente']:
            if not args.listDriftPoints:
                parser.error(f"Para driftType '{args.driftType}', -listDriftPoints é obrigatório.")

        parametro = Parametro(
            list_dict=args.listDict,
            list_drift_points=args.listDriftPoints,
            output_final_path=args.outputPath,
            list_paths_PNMLs=args.listPathsPNMLs,
            initial_timestamp=args.initialTimestamp,
            log_size=args.logSize,
            gradual_generation_method=args.gradualMethod if args.driftType == 'gradual' else None
        )

        contexto = Contexto(parametro)


        if hasattr(contexto, args.driftType):
            getattr(contexto, args.driftType)()
        else:
            print(f"Tipo de drift '{args.driftType}' não suportado.")


if __name__ == '__main__':
    Commandline.main()
