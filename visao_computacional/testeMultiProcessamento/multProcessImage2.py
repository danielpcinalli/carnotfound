#encoding: utf-8
import multiprocessing as mp
import numpy as np
import time

"""
Tentativa de criar três processos que esperam entradas do código principal em uma fila, processam as entradas e as armazenam em outra fila
"""

def rotate(inputs,outputs): #função escolhida para teste
    while(True):
        #enquanto fila de inputs estiver vazia, faz nada
        if(inputs.empty()):
            continue
            
        #tenta ler de inputs e processar, caso ocorra erro, faz nada
        try:
            mat = inputs.get()        
            outputs.put(np.rot90(mat,k=1))
        except KeyboardInterrupt:
            break
        except:
            continue
    print('processo terminado')
    
if __name__=='__main__':
    qtdeProcessos = 3
    inputs = mp.Queue(qtdeProcessos) #cria uma fila para armazenar entradas
    outputs = mp.Queue(qtdeProcessos) #cria uma fila para armazenar resultados
    

    #cria um processo para cada core
    processes = [mp.Process(target=rotate, args=(inputs, outputs)) for i in range(qtdeProcessos)]

    #inicia cada processo
    for p in processes:
        p.start()

    #continuamente cria novas entradas, as coloca em uma fila, que é lida pelos processos, e espera 
    while(True):
        try:
            width = 640
            height = 480

            #gera matriz aleatória
            mat = np.random.randint(low= 0, high = 9, size=(height,width))

            #gera as 3 matrizes à partir da original
            cut1 = height//3
            cut2 = 2*cut1

            mat1 = mat[0:cut1,:]
            mat2 = mat[cut1:cut2,:]
            mat3 = mat[cut2:height,:]

            #insere matrizes na fila de entradas
            inputs.put(mat1)
            inputs.put(mat2)
            inputs.put(mat3)

            #espera fila de saídas estar cheia
            while(not outputs.full()):
                continue    
            
                
            #pega resultados da fila, que não estão necessariamente na mesma ordem que os das entradas
            results = [outputs.get() for p in processes]
            
            print('__________________')
            print(mat)
            print(results)
        
        except KeyboardInterrupt:
            print('main terminado')
            for p in processes:
                p.join()
            break
    
print('TERMINADO')
