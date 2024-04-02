import datetime
import ast
from LOGGENERATORCLASS import Loggenerator

class Mergelogs(Loggenerator):
    def __init__(self, list_path_logs_to_merge, initial_timestamp, merged_name):
        self.list_path_logs_to_merge = list_path_logs_to_merge
        self.initial_timestamp = initial_timestamp
        self.merged_log = None
        self.event_log_empty = None
        self.merged_name = merged_name
        self.traco = 0
        self.total_real_drifts = ""


    def sum_real_drifts_values(self, log):
        if 'Drift localization' in log.attributes:
            data_str = (log.attributes['Drift localization'])
            data = ast.literal_eval(data_str)
            self.total_real_drifts += " "+str(log.attributes['Drift type'])+': '
            for i in data:
                if isinstance(i, int):
                    i = i + self.traco
                    self.total_real_drifts += ' '+ str(i)
                elif isinstance(i, dict):
                    inicio_int = int(i['inicio'])
                    fim_int = int(i['fim'])
                    inicio_int += self.traco
                    fim_int += self.traco

                    # Atualizando os valores no dicionário
                    i['inicio'] = str(inicio_int)  # Convertendo de volta para string se necessário
                    i['fim'] = str(fim_int)
                    self.total_real_drifts += ' ' + str(i)


    def merge_logs(self):
        # cria variável vazia para o atributo "real drift"
        total_real_drifts_before_merge = ""
        # cria log vazio
        from pm4py.objects.log.importer.xes import importer as xes_importer
        # importa qualquer log para criar um log vazio
        log = xes_importer.apply("C://Users//raduy//Downloads//modelo01_lp.xes")
        # cria log vazio a partir do log importanto (aqui tanto faz o log pois a inteção é gerar um log vazio
        from pm4py.algo.filtering.log.timestamp import timestamp_filter
        filtered_log_events = timestamp_filter.apply_events(log, "1300-03-09 00:00:00", "1300-01-18 23:59:59")
        self.event_log_empty = filtered_log_events
        print(self.event_log_empty)

        x = 0
        # for na lista com os caminho dos logs de eventos
        for i in range(0, len(self.list_path_logs_to_merge)):
            # transforma os caminhos em logs
            self.list_path_logs_to_merge[i] = xes_importer.apply(self.list_path_logs_to_merge[i])
            self.sum_real_drifts_values(self.list_path_logs_to_merge[i])
            self.traco += len(self.list_path_logs_to_merge[i])

            # faz o for no traço dos logs de evetos
            for j in range(0, len(self.list_path_logs_to_merge[i])):
                # adiciona o traço no log de evento
                self.event_log_empty.append(self.list_path_logs_to_merge[i][j])
                # controla o case_id do traço
                self.event_log_empty[x].attributes['concept:name'] = x
                x = x + 1
                # faz o for nos eventos do traço
                for k in range(0, len(self.list_path_logs_to_merge[i][j])):
                    # adiciona um timedelta do último evento
                    self.initial_timestamp = self.initial_timestamp + datetime.timedelta(0.005)
                    # reconfigura o timestamp do evento do traço
                    self.list_path_logs_to_merge[i][j][k]['time:timestamp'] = self.initial_timestamp

        # exporta o log de eventos
        from pm4py.objects.log.exporter.xes import exporter as xes_exporter
        self.event_log_empty.attributes['Drift type and Drift localization'] = self.total_real_drifts
        xes_exporter.apply(self.event_log_empty,

                           "LogsSinteticos\\MergedLogs\\" + self.merged_name + '.xes')

if __name__ == "__main__":
    MergedLog_3 = Mergelogs(list_path_logs_to_merge=['LogsSinteticos/GeneratedLogs/LS3_INCREMENTAL.xes',
                                                     'LogsSinteticos/GeneratedLogs/LS18_GRADUAL.xes'],
                            initial_timestamp=datetime.datetime(
                                2021, 7, 13, 10, 0, 0),
                            merged_name="teste")
    MergedLog_3.merge_logs()