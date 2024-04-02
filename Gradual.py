from LOGGENERATORCLASS import Loggenerator
import math
import random


class Gradual(Loggenerator):
    def __init__(self, p):
        Loggenerator.__init__(self, p)
        self.list_gaps_gradual_drifts = None
        self.list_gaps_models = None
        self.list_name_info = None
        self.list_gaps_models = None
        self.current_net = None
        self.current_initial_marking = None
        self.next_net = None
        self.next_initial_marking = None
        self.list_info_name_specific = None
        self.gap = None
        self.dif_final = None
        self.trace_gap = None
        self.current_trace = None
        self.decay_type = None
        self.number_traces_current_model = None
        self.probability_current_model = None
        self.probability_next_model = None
        self.number_of_traces_add_current_model = None
        self.number_of_traces_add_next_model = None
        self.modelo_prox = None
        self.modelo_atual = None
        self.prob_model1 = None
        self.prob_model2 = None

    def probability_gradual(self):

        # O lamb é a probabilidade do último trace ser zero, no entanto, como não existe x para atender a seguinte condição e^x=0
        # portanto, estamos usando 0,01 (1% de probabilidade)
        # O divisor deve ser o intervalo de traces
        # f(x) = e^(-lamb*x)
        # f(x) = probabilidade
        # x = intervalo_traces
        # f(x) = e^(-lamb*intervalo_traces)
        # ln(f(x)) = -lamb*intervalo_traces
        # -ln((f(x))/intervalo_traces = lamb
        # lamb = -ln((f(x))/intervalo_traces
        # pensar se o usuário entrará com a probabilidade

        lamb = -math.log(0.001) / self.trace_gap

        if self.decay_type == 'linear':
            self.probability_current_model = (self.trace_gap - self.current_trace) / self.trace_gap
            self.probability_current_model = str(self.probability_current_model)
            # self.probability_current_model = self.probability_current_model[0:20]
            self.probability_current_model = round(float(self.probability_current_model), 2)
            self.probability_next_model = (1 - self.probability_current_model)

        elif self.decay_type == 'exponencial':
            self.probability_current_model = math.e ** (-self.current_trace * lamb)
            self.probability_current_model = round(self.probability_current_model, 2)
            self.probability_current_model = str(self.probability_current_model)
            # self.probability_current_model = self.probability_current_model[0:20]
            self.probability_current_model = float(self.probability_current_model)

            self.probability_next_model = (1 - self.probability_current_model)
            # print(probabilidade_modelo_atual, probability_next_model)

        else:
            print('ERRO, A STRING INSERIDA PARA O TIPO DE DECAIMENTO É INVÁLIDA')

    def number_of_traced_add(self):
        # print(self.current_trace)
        # print(self.probability_current_model)
        self.number_of_traces_current_model_required = int(self.probability_current_model * self.current_trace)
        self.number_of_traces_add_current_model = self.number_of_traces_current_model_required - self.number_traces_current_model
        if self.number_of_traces_add_current_model < 0:
            self.number_of_traces_add_current_model = 0

        self.number_of_traces_add_next_model = self.split_drift - self.number_of_traces_add_current_model
        # print(f'O valor atual é {numero_traces_adicionar_atual}')
        # print(f'O valor prox é {numero_traces_adicionar_prox}')

    def generates_gradual_logs_according_to_probability(self):
        # print('o num atual  é',add_num_traces_modelo_atual)
        if self.number_of_traces_add_current_model > 0:
            self.log_simulado = self.simulate_petri_nets(self.current_net, self.current_initial_marking,
                                                         self.dif_seconds,
                                                         self.case_id, self.number_of_traces_add_current_model)
            for k in range(0, len(self.log_simulado)):
                self.event_log_empty.append(self.log_simulado[k])
            self.order_trace_timestamp(len(self.log_simulado))
        # print(case_id)

        # adicionar traces do próximo modelo
        # print('o num prox  é',add_num_traces_modelo_prox)
        if self.number_of_traces_add_next_model > 0:
            self.log_simulado = self.simulate_petri_nets(self.next_net, self.next_initial_marking,
                                                         self.dif_seconds,
                                                         self.case_id, self.number_of_traces_add_next_model)

            for k in range(0, len(self.log_simulado)):
                self.event_log_empty.append(self.log_simulado[k])
            # controla timestamp e case_id
            self.order_trace_timestamp(len(self.log_simulado))

    def add_in_list_infor_about_drifts(self, i):
        # print(self.list_gaps_gradual_drifts)
        self.list_gaps_gradual_drifts[0].append(self.gap)
        # print(self.p.list_dict)
        self.list_gaps_gradual_drifts[1].append(self.p.list_dict[i]['tipo decaimento'])
        if self.p.list_dict[i]['divisoes drift'] != None:
            self.list_gaps_gradual_drifts[2].append(int(self.p.list_dict[i]['divisoes drift']))

        self.list_info_name_specific.append(self.p.list_dict[i]['inicio'])
        self.list_info_name_specific.append(self.p.list_dict[i]['fim'])
        self.list_info_name_specific.append(self.p.list_dict[i]['tipo decaimento'])

    def gen_list_gaps_models_and_drifts(self):
        self.list_drift_points = []
        # descobre o gap que o modelo vai existir sozinho
        self.list_gaps_models = []
        # descobre os intervalos entre os drift (tamanho do drift)
        self.list_gaps_gradual_drifts = [[], [], []]
        self.list_name_info = []
        for i in range(0, len(self.p.list_dict)):
            self.list_info_name_specific = []
            # descobre o "comprimento" do drift gradual e adiciona em uma lista
            self.gap = int(self.p.list_dict[i]['fim']) - int(self.p.list_dict[i]['inicio'])
            self.add_in_list_infor_about_drifts(i)
            self.list_name_info.append(self.list_info_name_specific)
            # descobre os gap entre os modelos, sem considerar os drifts para adicionar em uma lista ordenada pelo timestamp
            # em que existe um único modelo
            if i == 0:
                self.gap = int(self.p.list_dict[i]['inicio'])
            # no caso de outros elementos, temos que subtrair a posição do drift atual da posição do drift anterio
            elif i >= 1:
                j = i - 1
                self.gap = int(self.p.list_dict[i]['inicio']) - int(self.p.list_dict[j]['fim'])
            self.list_gaps_models.append(self.gap)
        # o última gap será o tamanho do drift menos o último elemento da lista com os drift points
        self.dif_final = self.p.log_size - int(self.p.list_dict[-1]['fim'])
        # lista com intervalos dos modelos únicos
        self.list_gaps_models.append(self.dif_final)
        # print(self.list_gaps_models)
        # print(self.list_gaps_gradual_drifts)
        # print(list_drift_points)m os drift points
        # print(list_gaps_models)
        # print(list_gaps_gradual_drifts

    def add_trace_accordint_to_probability(self):
        self.probability_gradual()
        self.number_of_traced_add()
        self.number_traces_current_model = self.number_traces_current_model + self.number_of_traces_add_current_model

        self.generates_gradual_logs_according_to_probability()

    def simulates_and_add_control_timestamp_case_id(self):

        if self.modelo_atual == 'Modelo 1':
            self.prob_model1 = 1
            self.prob_model2 = 0

        elif self.modelo_atual == 'Modelo 2':
            self.prob_model2 = 1
            self.prob_model1 = 0

        # adiciona traces anes do drift
        self.simulated_log = self.simulate_petri_nets(self.current_net, self.current_initial_marking,
                                                      self.dif_seconds, self.case_id, self.num_traces_log,
                                                      model=self.modelo_atual, prob_model1=self.prob_model1,
                                                      prob_model2=self.prob_model2)

        for j in range(0, len(self.simulated_log)):
            self.event_log_empty.append(self.simulated_log[j])
            self.simulated_log[j].attributes['modelo'] = self.modelo_atual

        # a função ordena_trace_timestamo deve ser chamada toda vez que forem adicionados no log de eventos para
        # controlar o caseId
        self.order_trace_timestamp(len(self.simulated_log))

    def calculated_probabilities_add_models_and_interchange_models(self, i):

        # primeiro elemento parte do timestamp 1970 e case id=1

        self.simulates_and_add_control_timestamp_case_id()  # adicionas os intervalos sem drift

        if i <= (len(self.list_gaps_gradual_drifts[0]) - 1):
            self.number_traces_current_model = 0
            for j in range(0, self.list_gaps_gradual_drifts[0][i], self.list_gaps_gradual_drifts[2][i]):
                self.trace_gap = self.list_gaps_gradual_drifts[0][i]
                self.current_trace = j
                self.decay_type = self.list_gaps_gradual_drifts[1][i]
                self.split_drift = self.list_gaps_gradual_drifts[2][i]
                self.add_trace_accordint_to_probability()

    def controls_input(self):

        if len(self.p.list_paths_PNMLs) != 2:
            print('ERRO, DEVEM SER PASSADO DOIS MODELOS')

        for i in (0, len(self.p.list_dict)):
            if i < len(self.p.list_dict) and len(self.p.list_dict) > 1:
                if int(self.p.list_dict[i]['inicio']) > int(self.p.list_dict[i + 1]['inicio']):
                    print('ERRO, O DRIFTS DEVEM SER ORDENADOS EM ORDEM CRESCENTE')
                if int(self.p.list_dict[i + 1]['inicio']) < (int(self.p.list_dict[i]['fim']) + 50):
                    print('ERRO, OS DRIFTS DEVEM TER UM ESPAÇAMENTO MÍNIMO')

                if int(self.p.list_dict[i]['inicio']) > self.p.log_size or int(
                        self.p.list_dict[i]['fim']) > self.p.log_size:
                    print('ERRO, OS DRIFTS DEVEM ESTAR DENTRO DO NÚMERO MÁXIMO DE TRACES FORNECIDOS')
                if self.p.list_dict[i]['divisoes drift'] != None:
                    if (int(self.p.list_dict[i]['fim']) - int(self.p.list_dict[i]['fim'])) / (
                    int(self.p.list_dict[i]['divisoes drift'])) != 0:
                        print(
                            'O parâmetro divisões drift deve ser um divisor comum do tamanho do intervalo do drift gradual')
            if i == (len(self.p.list_dict) - 1):
                if int(self.p.list_dict[i]['fim']) > (self.p.log_size - 50):
                    print('O DRIFT GRADUAL DEVE ACABAR ANTES DO ÚLTIMO TRACE')

    def add_probabilist_traces(self, i):
        # print(self.num_traces_log)
        # adiciona traces dos intervalos sem drift
        self.simulates_and_add_control_timestamp_case_id()
        if i <= (len(self.list_gaps_gradual_drifts[0]) - 1):
            # vai de 0 até o último elemento com drift
            for j in range(0, self.list_gaps_gradual_drifts[0][i], 1):
                # calcula probabilidade aleatória de 0 até 1
                random_prob = random.random()
                self.trace_gap = self.list_gaps_gradual_drifts[0][i]
                self.decay_type = self.list_gaps_gradual_drifts[1][i]
                self.current_trace = j
                # calcula a probabilidade do trace
                self.probability_gradual()
                # se a probabilidade aleaória for menor que a probabilidade para o modelo atual-> gera um trace com base no modelo atual
                if self.modelo_atual == 'Modelo 1':
                    self.prob_model1 = self.probability_current_model
                    # print(self.probability_current_model)
                    self.prob_model2 = self.probability_next_model
                    # print(self.probability_next_model)
                elif self.modelo_atual == 'Modelo 2':
                    self.prob_model2 = self.probability_current_model
                    self.prob_model1 = self.probability_next_model

                if random_prob <= self.probability_current_model:
                    self.simulated_log = self.simulate_petri_nets(self.current_net, self.current_initial_marking,
                                                                  self.dif_seconds, self.case_id,
                                                                  1, model=self.modelo_atual,
                                                                  prob_model1=self.prob_model1,
                                                                  prob_model2=self.prob_model2)
                    # marca o modelo no início do traço
                    self.simulated_log[0].attributes['modelo'] = self.modelo_atual
                # se a probabilidade aleatória for maior que a probilidade de existência do modelo atual-> gera um trace com base no próximo modelo
                elif self.probability_current_model < random_prob < 1:
                    self.simulated_log = self.simulate_petri_nets(self.next_net,
                                                                  self.next_initial_marking,
                                                                  self.dif_seconds, self.case_id,
                                                                  1, model=self.modelo_prox,
                                                                  prob_model1=self.prob_model1,
                                                                  prob_model2=self.prob_model2)
                    # marca o modelo no ínicio do traço
                    self.simulated_log[0].attributes['modelo'] = self.modelo_prox

                # adiciona o trace no log
                for k in range(0, len(self.simulated_log)):
                    self.event_log_empty.append(self.simulated_log[k])
                # ordena
                self.order_trace_timestamp(1)

    def apply(self):
        self.empty_log()
        # Pega a lista com os drifts points e descobre os intervalos entre os modelos
        self.generates_list_with_model_info()
        self.gen_list_gaps_models_and_drifts()
        self.controls_input()

        # 2000, o colocar ruído, o tamanho do log será 5%=2000+5%*2000

        self.case_id = 0
        # faz o for na lista com intervalos dos modelos onde serão alternados entre modelo 01 e modelo 02
        for i in range(0, len(self.list_gaps_models)):
            # para o primeiro elemento da lista:
            if i == 0:
                # MODELO ATUAL= MODELO 1
                self.current_net = self.list_petri_nets[0][0]
                self.current_initial_marking = self.list_petri_nets[0][1]
                self.num_traces_log = self.list_gaps_models[i]
                self.modelo_atual = 'Modelo 1'

                # primeiro elemento parte do timestamp 1970 (default) e case id=1
                self.dif_secconds = self.controls_initial_timestamp()

                # MODELO PROX= MODELO 2
                self.next_net = self.list_petri_nets[1][0]
                self.next_initial_marking = self.list_petri_nets[1][1]
                self.modelo_prox = 'Modelo 2'
                print(self.p.gradual_generation_method)
                if self.p.gradual_generation_method == 'Deterministico':
                    self.calculated_probabilities_add_models_and_interchange_models(i)
                elif self.p.gradual_generation_method == 'Probabilistico':
                    self.add_probabilist_traces(i)
            # se for impar (unica coisa que muda é o modelo atual e o proximo que são o contrário do i==0)
            elif i % 2 != 0:
                self.current_net = self.list_petri_nets[1][0]
                self.current_initial_marking = self.list_petri_nets[1][1]
                self.num_traces_log = self.list_gaps_models[i]
                self.modelo_atual = 'Modelo 2'
                self.next_net = self.list_petri_nets[0][0]
                self.next_initial_marking = self.list_petri_nets[0][1]
                self.modelo_prox = 'Modelo 1'
                if self.p.gradual_generation_method == 'Deterministico':
                    self.calculated_probabilities_add_models_and_interchange_models(i)
                elif self.p.gradual_generation_method == 'Probabilistico':
                    self.add_probabilist_traces(i)
            # para os intervalos pares e diferentes de 0, utilizamos o case id e timestamp ordenado de acordo com o traces anteriores. Aqui utilizamos o modelo 01

            elif i % 2 == 0 and not i == 0:
                # MODELO ATUAL= MODELO 1
                self.current_net = self.list_petri_nets[0][0]
                self.current_initial_marking = self.list_petri_nets[0][1]
                self.modelo_atual = 'Modelo 1'
                self.num_traces_log = self.list_gaps_models[i]

                self.next_net = self.list_petri_nets[1][0]
                self.next_initial_marking = self.list_petri_nets[1][1]
                self.modelo_prox = 'Modelo 2'
                if self.p.gradual_generation_method == 'Deterministico':
                    self.calculated_probabilities_add_models_and_interchange_models(i)
                elif self.p.gradual_generation_method == 'Probabilistico':
                    self.add_probabilist_traces(i)



        if self.p.gradual_generation_method == 'Probabilistico':
            self.scatter_plot()
        self.insert_noise()
        self.insert_gold_standard('Gradual')
        self.export_log()