import pm4py
import datetime
import matplotlib.pyplot as plt


class Loggenerator:

    def __init__(self, p):
        self.p = p
        self.net = None
        self.initial_marking = None
        self.final_marking = None
        self.list_petri_nets = None
        self.dif_seconds = None
        self.simulated_log = None
        self.generated_log = None
        self.event_log_empty = None
        self.previous_timestamp = None
        self.case_id = None
        self.output_final_path = None
        self.log_with_noise = None
        self.scatter_x = []
        self.scatter_y = []
        self.scatter_y_prob_model1 = []
        self.scatter_y_prob_model2 = []

    def apply(self, p):
        pass

    def scatter_plot(self):
        area = 0.5  # 0 to 10 point radii
        colors = ['#1f77b4', '#2ca02c']
        colors_list = []
        marker_list = []
        for i in range(0, len(self.scatter_y)):
            # print(self.scatter_y[i])
            if self.scatter_y[i] == "Modelo 1":
                c1 = colors[0]
                colors_list.append(c1)
            elif self.scatter_y[i] == "Modelo 2":
                c2 = colors[1]
                colors_list.append(c2)

        # print(colors_list)
        plt.figure(figsize=(6, 2))
        plt.scatter(self.scatter_x, self.scatter_y, s=area, c=colors_list)
        plt.show()

        area = 0.01  # 0 to 10 point radii

        plt.plot(self.scatter_x, self.scatter_y_prob_model1, c='#1f77b4', label='Modelo 1')
        plt.plot(self.scatter_x, self.scatter_y_prob_model2, c='#2ca02c', label='Modelo 2', markersize=3)
        plt.legend(title='Modelo')
        plt.show()

    def difference_between_timestamp_calculator(self, previous_timestamp):
        self.previous_timestamp = previous_timestamp
        datetime1970 = datetime.datetime(1969, 12, 31, 21, 0, 0)
        # print('--------------timestamp inicial---------')
        # print(timestamp_anterior)
        # print('----------datetime1970-----------------')
        # print(datetime1970)

        dif_time = previous_timestamp - datetime1970
        self.dif_seconds = dif_time.total_seconds()
        # print(timestamp_anterior.second)
        # print(timestamp_anterior.minute)
        # print(timestamp_anterior.now())
        # print(dir(timestamp_anterior.date)
        return self.dif_seconds

    def add_traces_in_the_log(self):
        for j in range(0, len(self.simulated_log)):
            self.event_log_empty.append(self.simulated_log[j])

    def empty_log(self):
        from pm4py.objects.log.importer.xes import importer as xes_importer
        # importa qualquer log para criar um log vazio
        log = xes_importer.apply("C:/Users/raduy/Downloads/modelo01_lp.xes")
        # cria log vazio a partir do log importanto (aqui tanto faz o log pois a inteção é gerar um log vazio
        from pm4py.algo.filtering.log.timestamp import timestamp_filter
        filtered_log_events = timestamp_filter.apply_events(log, "1300-03-09 00:00:00", "1300-01-18 23:59:59")
        self.event_log_empty = filtered_log_events
        return self.event_log_empty

    def generates_list_with_model_info(self):
        self.list_petri_nets = []
        # Parsa a lista com os caminho das PNMLs e adicona em uma lista
        # list_petri_nets=[[net, initial_marking,final_marking], [net, initial_marking, final_marking], [net, initial_marking, final_marking],...]
        for i in range(0, len(self.p.list_paths_PNMLs)):
            self.net, self.initial_marking, self.final_marking = pm4py.read_pnml(self.p.list_paths_PNMLs[i])
            empty_list = []
            empty_list.append(self.net)
            empty_list.append(self.initial_marking)
            empty_list.append(self.final_marking)
            self.list_petri_nets.append(empty_list)

        # aqui vou pegar self.list_petri_nets

    def simulate_petri_nets(self, net, initial_marking, previous_timestamp, case_id, num_traces_log,
                            model=None, prob_model1=None, prob_model2=None, modelo_xes=None):
        self.case_id = case_id
        self.net = net
        self.initial_marking = initial_marking
        self.previous_timestamp = previous_timestamp
        self.num_traces_log = num_traces_log
        from pm4py.algo.simulation.playout.petri_net import algorithm as simulator

        print(modelo_xes)

        if self.previous_timestamp != None and modelo_xes == None:
            self.simulated_log = simulator.apply(self.net, self.initial_marking,
                                                 variant=simulator.Variants.BASIC_PLAYOUT,
                                                 parameters={
                                                     simulator.Variants.BASIC_PLAYOUT.value.Parameters.NO_TRACES: num_traces_log,
                                                     simulator.Variants.BASIC_PLAYOUT.value.Parameters.INITIAL_TIMESTAMP: previous_timestamp,
                                                    simulator.Variants.BASIC_PLAYOUT.value.Parameters.INITIAL_CASE_ID: case_id})

        elif self.previous_timestamp == None and modelo_xes == None:

            self.simulated_log = simulator.apply(self.net, self.initial_marking,
                                                 variant=simulator.Variants.BASIC_PLAYOUT,
                                                 parameters={
                                                     simulator.Variants.BASIC_PLAYOUT.value.Parameters.NO_TRACES: num_traces_log,
                                                     simulator.Variants.BASIC_PLAYOUT.value.Parameters.INITIAL_CASE_ID: case_id
                                                 })
        elif self.previous_timestamp != None and modelo_xes != None:
            log_do_modelo_replicado = pm4py.read_xes(modelo_xes)
            print("STOCASTICO--------------")
            print(case_id)
            print(self.net)
            self.simulated_log = simulator.apply(self.net, self.initial_marking,
                                                 variant=simulator.Variants.STOCHASTIC_PLAYOUT,
                                                 parameters={
                                                     simulator.Variants.STOCHASTIC_PLAYOUT.value.Parameters.NO_TRACES: num_traces_log,
                                                     simulator.Variants.STOCHASTIC_PLAYOUT.value.Parameters.INITIAL_TIMESTAMP: previous_timestamp,
                                                     simulator.Variants.STOCHASTIC_PLAYOUT.value.Parameters.INITIAL_CASE_ID: case_id,
                                                     simulator.Variants.STOCHASTIC_PLAYOUT.value.Parameters.LOG: log_do_modelo_replicado})

        elif self.previous_timestamp == None and modelo_xes != None:
            log_do_modelo_replicado = pm4py.read_xes(modelo_xes)
            print("STOCASTICO")
            print(case_id)
            print(self.previous_timestamp)
            self.simulated_log = simulator.apply(self.net, self.initial_marking,
                                                 variant=simulator.Variants.STOCHASTIC_PLAYOUT,
                                                 parameters={
                                                     simulator.Variants.STOCHASTIC_PLAYOUT.value.Parameters.NO_TRACES: num_traces_log,
                                                     simulator.Variants.STOCHASTIC_PLAYOUT.value.Parameters.INITIAL_CASE_ID: case_id,
                                                     simulator.Variants.STOCHASTIC_PLAYOUT.value.Parameters.LOG: log_do_modelo_replicado})

        for i in range(case_id, case_id + num_traces_log):
            self.scatter_x.append(i)
            self.scatter_y.append(model)
            self.scatter_y_prob_model1.append(prob_model1)
            self.scatter_y_prob_model2.append(prob_model2)
        print(self.simulated_log)
        return self.simulated_log

    def export_log(self):
        self.p.output_final_path = 'LogsSinteticos\\GeneratedLogs\\' + self.p.output_final_path +".xes"
        from pm4py.objects.log.exporter.xes import exporter as xes_exporter
        xes_exporter.apply(self.event_log_empty,
                           self.p.output_final_path)

    def controls_initial_timestamp(self):
        if self.p.initial_timestamp == None:
            self.dif_seconds = 0
        # caso a pessoa entre com o timestamp inicial
        else:
            self.dif_seconds = self.difference_between_timestamp_calculator(self.p.initial_timestamp)

    def insert_noise(self):
        if self.p.noise != None:
            num_noise_traces = int(self.p.noise * self.p.log_size / 100)
            num_noise_traces_partial = int(num_noise_traces / 10)
            # divide o log
            for i in range(0, len(self.event_log_empty), int(len(self.event_log_empty) / 10)):
                index_final = i + num_noise_traces_partial
                # acha o intervalo e partir dele retira os eventos dos traces
                for j in range(i, index_final):
                    # for k in range(0,len(self.event_log_empty[j])):
                    # print(self.event_log_empty[j][k]['Activity'])
                    # print('-----------')
                    # print(j)
                    # remove o primeiro evento do trace
                    self.event_log_empty[j].remove(0)
                    # for k in range(0,len(self.event_log_empty[j])):
                    # print(self.event_log_empty[j][k]['Activity'])
                    # print('-----------')

    def order_trace_timestamp(self, gap):

        timestamp_previous_log = self.event_log_empty[-1][-1]['time:timestamp']
        self.dif_seconds = self.difference_between_timestamp_calculator(timestamp_previous_log)
        self.case_id = self.case_id + gap

    def insert_gold_standard(self, drifttytpe):
        # Adicionar o novo atributo no nível global (log)
        if self.p.list_drift_points != None:
            new_attribute_value = self.p.list_drift_points

        else:
            new_attribute_value = self.p.list_dict

        self.event_log_empty.attributes['Drift localization'] = new_attribute_value
        self.event_log_empty.attributes['Drift type'] = drifttytpe
