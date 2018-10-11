#encoding: utf-8
import multiprocessing as mp
import numpy as np
import timeit
"""
Gera uma matriz aleatória, divide em três matrizes, e manda cada uma para cada uma core diferente para ser processada.

Também compara com tempo que leva para realizar mesmo processamento sem multiprocessamento
"""
TIMES_TO_RUN = 100 #qtde de vezes que cada código irá rodar
mats = [] #matrizes que serão processadas, global por causa de como timeit funciona

def rotate(mat,outputs): #função escolhida para teste
    outputs.put(np.rot90(mat,k=1))

def multiProcMats():
    """Realiza operação com multiprocessamento"""
    
    outputs = mp.Queue() #cria uma fila para armazenar resultados
    
    #cria um processo para cada matriz
    processes = [mp.Process(target=rotate, args=(mats[i], outputs)) for i in range(len(mats))]
    
    #inicia cada processo
    for p in processes:
        p.start()

    #termina cada processo
    for p in processes:
        p.join()

    #pega resultados da fila
    results = [outputs.get() for p in processes]
    
    return results

def uniProcMats():
    """Realiza operação sem multiprocessamento"""
    results = []
    for mat in mats:
        results.append(np.rot90(mat,k=1))
        
    return results
    
if __name__=='__main__':
    width = 30
    height = 30
    
    #gera matriz aleatória
    mat = np.random.uniform(size=(height,width))

    #gera as 3 matrizes à partir da original
    cut1 = height//3
    cut2 = 2*cut1
    
    mat1 = mat[0:cut1,:]
    mat2 = mat[cut1:cut2,:]
    mat3 = mat[cut2:height,:]

    mats = [mat1,mat2,mat3]
    
    #compara os dois tipos de processamento
    timeMulti = timeit.timeit(multiProcMats,number = TIMES_TO_RUN)
    print('Com multiprocessamento: ' + str(timeMulti))

    timeUni = timeit.timeit(uniProcMats,number = TIMES_TO_RUN)
    print('Sem multiprocessamento: ' + str(timeUni))
    
    print('Multiprocessamento é ' + str(timeUni/timeMulti) + ' vezes mais rápido')
