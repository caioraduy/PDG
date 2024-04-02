import os
from LOGGENERATORCLASS import Loggenerator

class Abrupto(Loggenerator):
    def __init__(self, p):
        self.list_gaps = None
        self.net1 = None
        self.initial_marking1 = None
        self.net2 = None
        self.initial_marking2 = None
        self.net3 = None
        self.initial_marking3 = None
        self.list_gaps = None
        Loggenerator.__init__(self, p)

    def apply(self):
        self.event_log_empty = self.empty_log()
        print('----', self.event_log_empty)
        # Pega a lista com os drifts points e descobre os intervalos entre os modelos
        self.p.list_drift_points.sort()
        self.finds_list_gaps_based_on_the_drifts_points()
        self.generates_list_with_model_info()
        # descobre os intervalos entre os drift
        # print(self.list_gaps)
        print(self.list_gaps)
        self.case_id = 0
        for i in range(1, len(self.list_gaps) + 1):
            # print(self.p.case_id)
            # print(lista_intervalos[i])
            # para o primeiro intervalo (i=0), o case id deve partir de zero e o timestamp deve ser o primeiro
            if i == 1 or i % 3 == 1:
                self.controls_initial_timestamp()
                self.net1 = self.list_petri_nets[0][0]
                self.initial_marking1 = self.list_petri_nets[0][1]
                if i == 1:
                    self.simulated_log = self.simulate_petri_nets(self.net1, self.initial_marking1, self.dif_seconds, 1,
                                                                  self.list_gaps[i - 1])
                else:
                    self.order_trace_timestamp(self.list_gaps[i - 2])
                    print("i == 1 or i % 3 == 1",self.case_id)
                    self.simulated_log = self.simulate_petri_nets(self.net1, self.initial_marking1, self.dif_seconds,
                                                                  self.case_id,
                                                                  self.list_gaps[i - 1])
                # não podemos tirar essa adição pois causa problema nos indices do log de eventos criado
            # para os intervalos impares, utilizamos o case id e timestamp ordenado de acordo com o traces anteriores. Aqui utilizamos o modelo 02
            elif i == 2 or i % 3 == 2:
                # importa o event log e extrai o modelo1
                self.net2 = self.list_petri_nets[1][0]
                self.initial_marking2 = self.list_petri_nets[1][1]
                print(self.list_gaps[i-1])
                self.order_trace_timestamp(self.list_gaps[i - 2])                # print(self.case_id)
                print("i==2 e i %3==2", self.case_id)
                self.simulated_log = self.simulate_petri_nets(self.net2, self.initial_marking2,
                                                              self.dif_seconds, self.case_id, self.list_gaps[i - 1])
            # para os intervalos pares e diferentes de 0, utilizamos o case id e timestamp ordenado de acordo com o traces anteriores. Aqui utilizamos o modelo 01
            elif i % 3 == 0:
                self.net3 = self.list_petri_nets[2][0]
                self.initial_marking3 = self.list_petri_nets[2][1]
                self.order_trace_timestamp(self.list_gaps[i - 2])
                print("i %3==0",self.case_id)
                self.simulated_log = self.simulate_petri_nets(self.net3, self.initial_marking3, self.dif_seconds,
                                                              self.case_id, self.list_gaps[i - 1])
            # print(self.simulated_log)
            # print('teste',self.simulated_log)
            for j in range(0, len(self.simulated_log)):
                # print(self.simulated_log[j])
                self.event_log_empty.append(self.simulated_log[j])

        self.insert_gold_standard('Abrupto')
        self.export_log()


    def finds_list_gaps_based_on_the_drifts_points(self):
        self.list_gaps = []
        for i in range(0, len(self.p.list_drift_points)):
            # para o primeiro elemento a o intervalo é a própria posição do drift
            if i == 0:
                gap = self.p.list_drift_points[i]
            # no caso de outros elementos, temos que subtrair a posição do drift atual da posição do drift anterio
            elif i >= 1:
                j = i - 1
                gap = self.p.list_drift_points[i] - self.p.list_drift_points[j]
            self.list_gaps.append(gap)
        # o última intervalo será o tamanho do drift menos o último elemento da lista com os drift points
        dif_final = self.p.log_size - self.p.list_drift_points[-1]
        self.list_gaps.append(dif_final)

    def name_files_generator_sudden_drift_points(self):
        path_output = 'C:/Users/raduy/Documents/Research/Codigo/LogsGerados/'
        path_output_join = os.path.join(path_output,
                                        'drift_abrupto' + '_' + str(log_size / 1000) + 'k_' + str(
                                            len(list_drift_points)) + 'Drifts_')

        empty_string = ''
        for i in range(0, len(self.p.list_drift_points)):
            if i == (len(list_drift_points) - 1):
                empty_string = empty_string + str(self.p.list_drift_points[i]) + '.xes'
            else:
                empty_string = empty_string + str(self.list_drift_points[i]) + '_'

        self.p.output_final_path = path_output_join + empty_string


