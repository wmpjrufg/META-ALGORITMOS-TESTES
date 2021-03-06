# $$\      $$\ $$$$$$$$\ $$$$$$$$\  $$$$$$\        $$$$$$$$\  $$$$$$\   $$$$$$\  $$\       $$$$$$$\   $$$$$$\  $$\   $$\ 
# $$$\    $$$ |$$  _____|\__$$  __|$$  __$$\       \__$$  __|$$  __$$\ $$  __$$\ $$ |      $$  __$$\ $$  __$$\ $$ |  $$ |
# $$$$\  $$$$ |$$ |         $$ |   $$ /  $$ |         $$ |   $$ /  $$ |$$ /  $$ |$$ |      $$ |  $$ |$$ /  $$ |\$$\ $$  |
# $$\$$\$$ $$ |$$$$$\       $$ |   $$$$$$$$ |         $$ |   $$ |  $$ |$$ |  $$ |$$ |      $$$$$$$\ |$$ |  $$ | \$$$$  / 
# $$ \$$$  $$ |$$  __|      $$ |   $$  __$$ |         $$ |   $$ |  $$ |$$ |  $$ |$$ |      $$  __$$\ $$ |  $$ | $$  $$<  
# $$ |\$  /$$ |$$ |         $$ |   $$ |  $$ |         $$ |   $$ |  $$ |$$ |  $$ |$$ |      $$ |  $$ |$$ |  $$ |$$  /\$$\ 
# $$ | \_/ $$ |$$$$$$$$\    $$ |   $$ |  $$ |         $$ |    $$$$$$  | $$$$$$  |$$$$$$$$\ $$$$$$$  | $$$$$$  |$$ /  $$ |
# \__|     \__|\________|   \__|   \__|  \__|         \__|    \______/  \______/ \________|\_______/  \______/ \__|  \__|

################################################################################
# UNIVERSIDADE FEDERAL DE CATALÃO (UFCAT)
# WANDERLEI MALAQUIAS PEREIRA JUNIOR,                  ENG. CIVIL / PROF (UFCAT)
# JOÃO V. COELHO ESTRELA,                                     ENG. MINAS (UFCAT)
################################################################################

################################################################################
# DESCRIÇÃO ALGORITMO:
# BIBLIOTECA DE FUNÇÕES COMUNS DA PLATAFORMA "META OPTIMIZATION TOOLBOX" DESEN-
# VOLVIDA PELO GRUPO DE PESQUISAS E ESTUDOS EM ENGENHARIA (GPEE)
################################################################################

################################################################################
# BIBLIOTECAS NATIVAS PYTHON
import numpy as np
import pandas as pd

################################################################################
# BIBLIOTECAS DESENVOLVEDORES GPEE

# CRIAÇÃO DA POP. INICIAL
def INITIAL_POPULATION(N_POP, D, X, X_L, X_U):
    """ 
    This function initializes the population randomically between 
    the limits X_L and X_U.

    Input:
    N_POP  | Number of population          | Integer
    D      | Problem dimension             | Integer
    X_L    | Lower limit design variables  | Py list[D]
    X_U    | Upper limit design variables  | Py list[D]
    X      | Empty design variables        | Py Numpy array[N_POP x D]
        
    Output:
    X      | Initial design variables      | Py Numpy array[N_POP x D]
    """
    for I_COUNT in range(N_POP):
        for J_COUNT in range(D):
            RANDON_NUMBER = np.random.random()
            X[I_COUNT, J_COUNT] = X_L[J_COUNT] + (X_U[J_COUNT] - X_L[J_COUNT]) * RANDON_NUMBER
    return X

# AVALIAÇÃO DA APTIDÃO DE UMA ÚNICA PARTÍCULA
def FIT_VALUE(OF_VALUEI):
    """ 
    This function calculates the fitness of a value of the 
    objective function.

    Input:
    OF_VALUEI   | Objective function I particle value  | Float

    Output:
    FIT_VALUEI  | Fitness I particle value             | Float
    """
    if OF_VALUEI >= 0:
        FIT_VALUEI = 1 / (1 + OF_VALUEI)
    elif OF_VALUEI < 0:
        FIT_VALUEI = 1 + abs(OF_VALUEI)
    return FIT_VALUEI

# CHECAGEM DOS LIMITES DAS VARIÁVEIS DE PROJETO DE UMA ÚNICA PARTÍCULA
def CHECK_INTERVAL(X_T0I, X_L, X_U):
    """
    This function checks if a variable is out of the limits established X_L and X_U.

    Input:
    X_T0I  | Design variable I particle before check  | Py list[D]
    X_L    | Lower limit design variables             | Py list[D]
    X_U    | Upper limit design variables             | Py list[D]

    Output:
    X_T1I  | Design variable I particle after check   | Py list[D]
    """
    X_T1I = np.clip(X_T0I, X_L, X_U)
    return X_T1I

# VERIFICAÇÃO DA MELHOR PARTÍCULA, PIOR E VALOR MÉDIO
def BEST_VALUES(X, OF, FIT, N_POP):
    """ 
    This function determines the best and worst particle. 
    It also determines the average value (OF and FIT) of the population

    Input:
    X               | Design variables                        | Py Numpy array[N_POP x D]
    OF              | All objective function values           | Py Numpy array[N_POP x 1]
    FIT             | All fitness values                      | Py Numpy array[N_POP x 1] 
    N_POP           | Number of population                    | Integer

    Output:
    BEST_POSITION   | ID best position                         | Integer
    WORST_POSITION  | ID worst position                        | Integer
    X_BEST          | Design variables best particle           | Py list[D]
    X_WORST         | Design variables worst particle          | Py list[D]
    OF_BEST         | Objective function best particle value   | Float
    OF_WORST        | Objective function worst particle value  | Float
    FIT_BEST        | Fitness best particle value              | Float
    FIT_WORST       | Fitness worst particle value             | Float
    OF_AVERAGE      | Average Objective function value         | Float
    FIT_AVERAGE     | Average Fitness value                    | Float
    """
    # BEST AND WORST POSITION IN POPULATION
    SORT_POSITIONS = np.argsort(OF.T)
    BEST_POSITION = SORT_POSITIONS[0, 0]
    WORST_POSITION = SORT_POSITIONS[0, N_POP - 1]
    # GLOBAL BEST VALUES
    X_BEST = X[BEST_POSITION, :]
    OF_BEST = OF[BEST_POSITION, 0]
    FIT_BEST = FIT[BEST_POSITION, 0]
    # WORST BEST VALUES
    X_WORST = X[WORST_POSITION, :]
    OF_WORST = OF[WORST_POSITION, 0]
    FIT_WORST = FIT[WORST_POSITION, 0]
    # AVERAGE VALUES
    OF_AVERAGE = np.mean(OF)
    FIT_AVERAGE = np.mean(FIT)
    return BEST_POSITION, WORST_POSITION, X_BEST, X_WORST, OF_BEST, OF_WORST, FIT_BEST, FIT_WORST, OF_AVERAGE, FIT_AVERAGE

# VERIFICAÇÃO DA MELHOR RESPOSTA NO BEST_REPEAT
def SUMMARY_ANALYSIS(BEST_REP, N_REP, N_ITER):
    """ 
    This function presents a written summary of the best simulation. 

    Input:
    BEST_REP         | Best population results by repetition                            | Py dictionary
                     |   Dictionary tags                                                |
                     |     'X_POSITION'    = Design variables by iteration              | Py Numpy array[N_ITER + 1 x D]
                     |     'OF'            = Obj function value by iteration            | Py Numpy array[N_ITER + 1 x 1]
                     |     'FIT'           = Fitness value by iteration                 | Py Numpy array[N_ITER + 1 x 1]
                     |     'SA_PARAMETERS' = Temperature by iteration                   | Py Numpy array[N_ITER + 1 x 1]
                     |     'NEOF'          = Number of objective function evaluations   | Py Numpy array[N_ITER + 1 x 1]
                     |     'ID_PARTICLE'   = ID best particle by iteration              | Integer 
    N_REP            | Number of repetitions                                            | Integer
    N_ITER           | Number of iterations                                             | Integer

    Output:
    STATUS_PROCEDURE | Process repetition ID - from lowest OF value to highest OF value | Py list[N_REP]
    """ 
    # Start reserved space for repetitions
    OF_MINVALUES = []
    # Checking which is the best process 
    for I_COUNT in range(N_REP):
        ID = I_COUNT
        OF_MIN = BEST_REP[ID]['OF'][N_ITER]
        OF_MINVALUES.append(OF_MIN)
    STATUS_PROCEDURE = np.argsort(OF_MINVALUES)    
    return STATUS_PROCEDURE

# PLOTAGEM DA BARRA DE PROGRESSO
def PROGRESSBAR(I_COUNT, TOTAL, PREFIX = 'Progress:', SUFFIX = 'Complete', DECIMALS = 1, LENGTH = 50, FILL = '█', PRINT_END = "\r"):
    """
    This function create terminal progress bar
    
    Input:
    I_COUNT    | Current iteration (required)                     | Integer
    TOTAL      | Total iterations (required)                      | Integer
    PREFIX     | Prefix string                                    | String
    SUFFIX     | Suffix string                                    | String
    DECIMALS   | Positive number of decimals in percent complete  | Integer
    LENGTH     | Character length of bar                          | Integer
    FILL       | Bar fill character                               | String
    PRINT_END  | End character (e.g. "\r", "\r\n")                | String
    
    Output:
    N/A
    """
    PERCENT = ("{0:." + str(DECIMALS) + "f}").format(100 * (I_COUNT / float(TOTAL)))
    FILLED_LENGTH = int(LENGTH * I_COUNT // TOTAL)
    BAR = FILL * FILLED_LENGTH + '-' * (LENGTH - FILLED_LENGTH)
    print(f'\r{PREFIX} |{BAR}| {PERCENT}% {SUFFIX}', end = PRINT_END)
    # Print New Line on Complete
    if I_COUNT == TOTAL: 
        print()

# SALVA ARQUIVO EM EXCEL
def EXCEL_WRITER_ITERATION(NAME, D, DATASET):
    """
    This function create output Excel files by iteration.
    
    Input:
    NAME       | Filename                                         | String
    D          | Problem dimension                                | Integer
    DATASET    | Best results I repetition                        | Py Numpy array
    
    Output:
    Save xls file in current directory
    """
    # Individual results
    X = DATASET['X_POSITION']
    COLUMNS = []
    for I_COUNT in range(D):
        COLUMNS_X = 'X_' + str(I_COUNT)
        COLUMNS.append(COLUMNS_X)
    DATA1 = pd.DataFrame(X, columns = COLUMNS)
    OF = DATASET['OF']
    DATA2 = pd.DataFrame(OF, columns = ['OF'])
    FIT = DATASET['FIT']
    DATA3 = pd.DataFrame(FIT, columns = ['FIT'])
    NEOF = DATASET['NEOF']
    DATA4 = pd.DataFrame(NEOF, columns = ['NEOF'])
    FRAME = [DATA1, DATA2, DATA3, DATA4]
    DATA = pd.concat(FRAME, axis = 1)
    NAME += '.xlsx' 
    print(NAME)
    WRITER = pd.ExcelWriter(NAME, engine = 'xlsxwriter')
    DATA.to_excel(WRITER, sheet_name = 'Sheet1')
    WRITER.save()

# RESUMO DOS DADOS EM EXCEL
def EXCEL_PROCESS_RESUME(NAME, D, DATASET, N_ITER, N_REP):
    """
    This function create output Excel files complete process.

    Input:
    NAME       | Filename                                         | String
    D          | Problem dimension                                | Integer
    DATASET    | Best results I repetition                        | Py Numpy array
    N_REP      | Number of repetitions                            | Integer
    N_ITER     | Number of iterations                             | Integer

    Output:
    Save xls file in current directory
    """
    # Resume process in arrays
    X = np.zeros((N_REP, D))
    OF = np.zeros((N_REP, 1))
    FIT = np.zeros((N_REP, 1))
    NEOF = np.zeros((N_REP, 1))
    for I_COUNT in range(N_REP):
        X_I = DATASET[I_COUNT]['X_POSITION'][N_ITER]
        X[I_COUNT, :] = X_I
        OF[I_COUNT, :] = DATASET[I_COUNT]['OF'][N_ITER]
        FIT[I_COUNT, :] = DATASET[I_COUNT]['FIT'][N_ITER]
        NEOF[I_COUNT, :] = DATASET[I_COUNT]['NEOF'][N_ITER]
    # Excel save
    COLUMNS = []
    for I_COUNT in range(D):
        COLUMNS_X = 'X_' + str(I_COUNT)
        COLUMNS.append(COLUMNS_X)
    DATA1 = pd.DataFrame(X, columns = COLUMNS)
    DATA2 = pd.DataFrame(OF, columns = ['OF'])
    DATA3 = pd.DataFrame(FIT, columns = ['FIT'])
    DATA4 = pd.DataFrame(NEOF, columns = ['NEOF'])
    FRAME = [DATA1, DATA2, DATA3, DATA4]
    DATA = pd.concat(FRAME, axis = 1)
    NAME += '.xlsx' 
    print(NAME)
    WRITER = pd.ExcelWriter(NAME, engine = 'xlsxwriter')
    DATA.to_excel(WRITER, sheet_name = 'Sheet1')
    WRITER.save()

#   /$$$$$$  /$$$$$$$  /$$$$$$$$ /$$$$$$$$       /$$$$$$$$ /$$$$$$$$  /$$$$$$  /$$   /$$ /$$   /$$  /$$$$$$  /$$        /$$$$$$   /$$$$$$  /$$$$$$ /$$$$$$$$  /$$$$$$ 
#  /$$__  $$| $$__  $$| $$_____/| $$_____/      |__  $$__/| $$_____/ /$$__  $$| $$  | $$| $$$ | $$ /$$__  $$| $$       /$$__  $$ /$$__  $$|_  $$_/| $$_____/ /$$__  $$
# | $$  \__/| $$  \ $$| $$      | $$               | $$   | $$      | $$  \__/| $$  | $$| $$$$| $$| $$  \ $$| $$      | $$  \ $$| $$  \__/  | $$  | $$      | $$  \__/
# | $$ /$$$$| $$$$$$$/| $$$$$   | $$$$$            | $$   | $$$$$   | $$      | $$$$$$$$| $$ $$ $$| $$  | $$| $$      | $$  | $$| $$ /$$$$  | $$  | $$$$$   |  $$$$$$ 
# | $$|_  $$| $$____/ | $$__/   | $$__/            | $$   | $$__/   | $$      | $$__  $$| $$  $$$$| $$  | $$| $$      | $$  | $$| $$|_  $$  | $$  | $$__/    \____  $$
# | $$  \ $$| $$      | $$      | $$               | $$   | $$      | $$    $$| $$  | $$| $$\  $$$| $$  | $$| $$      | $$  | $$| $$  \ $$  | $$  | $$       /$$  \ $$
# |  $$$$$$/| $$      | $$$$$$$$| $$$$$$$$         | $$   | $$$$$$$$|  $$$$$$/| $$  | $$| $$ \  $$|  $$$$$$/| $$$$$$$$|  $$$$$$/|  $$$$$$/ /$$$$$$| $$$$$$$$|  $$$$$$/
#  \______/ |__/      |________/|________/         |__/   |________/ \______/ |__/  |__/|__/  \__/ \______/ |________/ \______/  \______/ |______/|________/ \______/ 