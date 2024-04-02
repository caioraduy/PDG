from Abrupto import Abrupto
import os


class Incremental(Abrupto):
    def __init__(self, p):
        Abrupto.__init__(self, p)

    def name_log_incremental_drift(self):
        path_output = 'C:/Users/raduy/Documents/Research/Codigo/LogsGerados/'
        path_output_join = os.path.join(path_output,
                                        'drift_incremental' + '_' + str(log_size) + 'k_' + str(
                                            len(list_pathss_PNMLs) - 1) + 'Drifts_')

        empty_string = ''
        for i in range(0, len(self.p.list_paths_PNMLs)):
            model = self.p.list_paths_PNMLs[i]
            model = model.split('/')
            model = model[-1]
            model = model[0:-5]

            if i == (len(self.p.list_paths_PNMLs) - 1):
                empty_string = empty_string + 'modelo_' + str(model) + '_' + str(self.list_gaps[i]) + 'traces.xes'
            else:
                empty_string = empty_string + 'modelo_' + str(model) + '_' + str(self.list_gaps[i]) + 'traces_'

        self.p.output_final_path = path_output_join + empty_string

    def condition_incremental(self):
        # pré-condição
        if len(self.p.list_paths_PNMLs) < (len(self.p.list_drift_points) + 1):
            print('ERRO, o número de modelos passados não pode ser inferior ao número de de drifts points+1')

    def apply(self):
        self.empty_log()
        # Pega a lista com os drifts points e descobre os intervalos entre os modelos
        self.condition_incremental()
        self.p.list_drift_points.sort()
        self.generates_list_with_model_info()
        self.finds_list_gaps_based_on_the_drifts_points()

        for i in self.list_gaps:
            if i < 150:
                print('Erro, o log de eventos não pode ter intervalos inferiores a 150 traces para que o ruído'
                      ' seja inserido da maneira apropriada')
        self.case_id = 0

        for i in range(0, len(self.list_gaps)):
            # print(list_gaps[i])
            # para o primeiro intervalo (i=0), o case id deve partir de zero e o timestamp deve ser o primeiro
            if i == 0:
                # primeiro elemento parte do timestamp 1970 e case id=1
                self.difference_between_timestamp_calculator(self.p.initial_timestamp)
                self.simulated_log = self.simulate_petri_nets(self.list_petri_nets[i][0], self.list_petri_nets[i][1],
                                                              self.dif_seconds, 1,
                                                              self.list_gaps[i])
                self.add_traces_in_the_log()
                # a função ordena_trace_timestamp deve ser chamada toda vez que forem adicionados no log de eventos para
                # controlar o caseId
                self.order_trace_timestamp(len(self.simulated_log))

            # para os intervalos impares, utilizamos o case id e timestamp ordenado de acordo com o traces anteriores. Aqui utilizamos o modelo 02
            else:
                self.simulated_log = self.simulate_petri_nets(self.list_petri_nets[i][0], self.list_petri_nets[i][1],
                                                              self.dif_seconds,
                                                              self.case_id, self.list_gaps[i])
                self.add_traces_in_the_log()
                self.order_trace_timestamp(self.list_gaps[i - 1])

        self.insert_noise()
        if self.p.output_final_path == None:
            self.name_log_incremental_drift()
        self.insert_gold_standard('Incremental')
        self.export_log()
