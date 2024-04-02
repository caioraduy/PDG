WELCOME TO PDG (PROCESS LOG GENERATOR)

O PDG É UM GERADOR DE LOG DE EVENTOS COM DRIFT DESENVOLVIDO NO PPGIA PELO CAIO RADUY, PELA DENISE SATO E PELO EDSON SCALABRIN 

o PDG É INTERAMENTE EM PYTHON E UTILIZA O PM4PY

Como rodar o PDG via linha de comando ??
Entre na pasta em que o programada CommandLine.py está presente e em seguida execute o comando python CommandLine.py com os seguintes atributos especificados 

-driftType (Obrigatório): Especifica o tipo de drift a ser simulado. Os valores possíveis são:
    
    abrupto
    gradual
    incremental
    recurring

-logSize (Obrigatório): Define o número total de traços que o log simulado deverá ter. É um inteiro que especifica o tamanho do log.

-outputPath (Obrigatório): Caminho do arquivo onde o log simulado será salvo. Deve ser fornecido pelo usuário para indicar onde o arquivo de saída será criado. 

-listDriftPoints (Obrigatório para abrupto, incremental, recorrente): Uma lista de inteiros que especifica os pontos no log onde os drifts ocorrerão. Esse argumento é obrigatório para os tipos de drift abrupto, incremental e recorrente, pois define os pontos específicos no log em que as mudanças ocorrem. 
Para gradual, este argumento não é utilizado, já que a configuração dos drifts é feita de forma diferente.

-initialTimestamp (Opcional): O timestamp inicial para o log simulado, no formato AAAA-MM-DD HH:MM:SS. O valor padrão é 2021-07-13 10:00:00. Esse argumento define o ponto de partida temporal para a simulação dos eventos no log.

-listDict (Obrigatório para gradual): Uma lista de dicionários que especifica a configuração de cada drift gradual. Cada dicionário deve conter chaves para "tipo de decaimento" (linear ou exponencial), "inicio", "fim" e "divisoes drift" (que pode ser None ou um inteiro positivo). 

-gradualMethod (Obrigatório para gradual): Especifica o método de geração para drifts graduais. Pode ser Deterministico ou Probabilistico. Este argumento é essencial para definir como a mudança gradual será aplicada ao longo do intervalo especificado.

-listPathsPNMLs (Obrigatório): Lista de caminhos para os arquivos PNML que serão usados na simulação. Este argumento é necessário para indicar os modelos de processo que serão utilizados para gerar os logs de eventos simulados.

Exemplo para gerar um log de eventos com drift graduais:

    python PDGCommandLine.py -driftType gradual -logSize 1000 -outputPath "C:\\Users\\raduy\\Documents\\Research\\Codigo\\ConjuntoLS_QUALI\\teste.xes" -listDict "[{'tipo decaimento': 'linear', 'inicio': 300, 'fim': 500, 'divisoes drift': None}, {'ti
    po decaimento': 'exponencial', 'inicio': 700, 'fim': 900, 'divisoes drift': None}]" -gradualMethod Probabilistico -listPathsPNMLs "C:\\Users\\raduy\\Downloads\\ModelosIncrementais\\base.pnml" "C:\\Users\\raduy\\Downloads\\ModelosIncrementais\\I.pnml"

Exemplo para gerar um log de eventos com drifts abruptos:

    python PDGCommandLine.py -driftType abrupto -logSize 1000 -outputPath "teste.xes" -listDriftPoints 300 500 -listPathsPNMLs "C:\\Users\\raduy\\Downloads\\ModelosIncrementais\\base.pnml" "C:\\Users\\raduy\\Downloads\\ModelosIncrementais\\I.pnml" "C:\\Users\\raduy\\Downloads\\ModelosIncrementais\\IO.pnml"

Como rodar o Merge Logs via linha de comando??

Após gerar logs de eventos com o PGG também é possível juntar eles em apenas um log. Nesse caso, todos os argumentos abaixo devem ser fornecidos via
linha de comando

-listPaths
    
    Descrição: Lista de caminhos para os logs de eventos que serão mesclados.
    
    Como Passar: Este argumento deve ser seguido por um ou mais caminhos de arquivo, cada um representando um log de eventos que você deseja mesclar. Os caminhos devem ser separados por espaços.
    
    Exemplo: -listPaths "PATH1" "PATH2"

-initialTimestamp:

    Descrição: O timestamp inicial para a mesclagem, usado para ajustar os timestamps dos eventos nos logs mesclados.
    
    Como Passar: Este argumento deve ser fornecido no formato AAAA-MM-DD HH:MM:SS.
    
    Exemplo: -initialTimestamp "2021-01-01 00:00:00"

-mergedName:

    Descrição: Nome do arquivo de saída para o log mesclado. Este nome será usado para criar o arquivo final que contém todos os logs de eventos mesclados.

    Como Passar: Este argumento deve ser seguido pelo nome desejado para o arquivo de saída. O caminho pode ser absoluto ou relativo ao diretório de trabalho atual.
    
    Exemplo: -mergedName "MERGEDlog.xes"

Exemplo de como rodar:
