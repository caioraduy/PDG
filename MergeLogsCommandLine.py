# merge_logs_cli.py
import argparse
import datetime
from MergeLogs import Mergelogs

def main():
    parser = argparse.ArgumentParser(description="MergedLogs via linha de cmando")
    parser.add_argument("-listPaths", nargs='+', required=True,
                        help="Lista de caminhos para os logs de eventos que sofreram a fusão")
    parser.add_argument("-initialTimestamp", type=lambda s: datetime.datetime.strptime(s, '%Y-%m-%d %H:%M:%S'),
                        required=True, help="Timestamp inicial para a fusão no formato AAAA-MM-DD HH:MM:SS.")
    parser.add_argument("-mergedName", required=True, help="Nome do arquivo de saída para o merge log")

    args = parser.parse_args()

    merger = Mergelogs(list_path_logs_to_merge=args.listPaths,
                       initial_timestamp=args.initialTimestamp,
                       merged_name=args.mergedName)


    merger.merge_logs()

    print(f"Fusão dos logs foi feira e o arquivo de saída é {args.mergedName}")

if __name__ == "__main__":
    main()
