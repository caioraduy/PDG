import os
from Abrupto import Abrupto

class Recurring(Abrupto):
    def __init__(self, p):
        Abrupto.__init__(self, p)

    def name_files_generator_recurring_drift_points(self):
        path_output = 'C:/Users/raduy/Documents/Research/Codigo/LogsGerados/'
        path_output_join = os.path.join(path_output,
                                        'drift_recorrente' + '_' + str(log_size / 1000) + 'k_' + str(
                                            len(list_drift_points)) + 'Drifts_')

        empty_string = ''
        for i in range(0, len(self.p.list_drift_points)):
            if i == (len(self.p.list_drift_points) - 1):
                empty_string = empty_string + str(self.p.list_drift_points[i]) + '.xes'
            else:
                empty_string = empty_string + str(self.p.list_drift_points[i]) + '_'

        self.p.output_final_path = path_output_join + empty_string

    def replica_base_apromore5k(self, i):
        if self.p.replicate == True:
            nome_do_log_replicado = self.p.list_paths_PNMLs[1][-8:-5]
            if "/" in nome_do_log_replicado:
                nome_do_log_replicado = nome_do_log_replicado[1:]
            if nome_do_log_replicado == 'lp' or nome_do_log_replicado == 're':
                modelo_xes = "modelo0" + str(i + 1) + '_' + nome_do_log_replicado + "2.5k.xes"
            else:
                modelo_xes = "modelo0" + str(i + 1) + '_' + nome_do_log_replicado + "5k.xes"
            modelo_xes = "G:\\Meu Drive\\Pesquisa\\Codigo\\LogsDeEventos\\" + modelo_xes
        else:
            modelo_xes = None
        return modelo_xes

    def apply(self):
        self.empty_log()
        # Pega a lista com os drifts points e descobre os intervalos entre os modelos
        self.p.list_drift_points.sort()
        self.generates_list_with_model_info()
        # descobre os intervalos entre os drift
        self.finds_list_gaps_based_on_the_drifts_points()

        print(self.list_gaps)

        self.case_id = 0
        for i in range(0, len(self.list_gaps)):
            modelo_xes = self.replica_base_apromore5k(i)
            #print('OS INTERVALOS SÃO')
            print(self.list_gaps)
            # print(lista_intervalos[i])
            # para o primeiro intervalo (i=0), o case id deve partir de zero e o timestamp deve ser o primeiro
            if i == 0:
                self.dif_seconds = self.controls_initial_timestamp()
                self.net1 = self.list_petri_nets[0][0]
                self.initial_marking1 = self.list_petri_nets[0][1]
                self.final_marking1 = self.list_petri_nets[0][2]
                # pm4py.view_petri_net(self.net1, self.initial_marking1, self.final_marking1)
                self.simulated_log = self.simulate_petri_nets(self.net1, self.initial_marking1,
                                                              self.dif_seconds, 1, self.list_gaps[i],
                                                              modelo_xes=modelo_xes)
                # não podemos tirar essa adição pois causa problema nos indices do log de eventos criado
                #self.case_id = self.case_id + 1

            # para os intervalos impares, utilizamos o case id e timestamp ordenado de acordo com o traces anteriores. Aqui utilizamos o modelo 02
            elif i % 2 != 0:
                # importa o event log e extrai o modelo1
                self.net2 = self.list_petri_nets[1][0]
                self.initial_marking2 = self.list_petri_nets[1][1]
                self.final_marking2 = self.list_petri_nets[1][2]
                # pm4py.view_petri_net(self.net2, self.initial_marking2, self.final_marking2)
                self.order_trace_timestamp(self.list_gaps[i - 1])
                self.simulated_log = self.simulate_petri_nets(self.net2, self.initial_marking2, self.dif_seconds,
                                                              self.case_id, self.list_gaps[i], modelo_xes=modelo_xes)

            # para os intervalos pares e diferentes de 0, utilizamos o case id e timestamp ordenado de acordo com o traces anteriores. Aqui utilizamos o modelo 01
            elif i % 2 == 0 and not i == 0:
                self.net1 = self.list_petri_nets[0][0]
                self.initial_marking1 = self.list_petri_nets[0][1]
                self.order_trace_timestamp(self.list_gaps[i - 1])
                print(self.case_id)
                self.simulated_log = self.simulate_petri_nets(self.net1, self.initial_marking1, self.dif_seconds,
                                                              self.case_id, self.list_gaps[i], modelo_xes=modelo_xes)

            for j in range(0, len(self.simulated_log)):
                self.event_log_empty.append(self.simulated_log[j])
        print('----------------------')
        #for l  in self.event_log_empty:
            #print(l)
        self.insert_noise()
        self.insert_gold_standard("Recorrente")
        self.export_log()

