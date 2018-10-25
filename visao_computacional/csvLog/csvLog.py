#encoding: utf-8
import time
def writeRow(csvfile,*args):
    """Escreve uma linha no arquivo csv"""
    row = ''
    #x,y,z
    for arg in args[:-1]:
        #para cada valor menos o último, adiciona vírgula
        row += str(arg) + ','
    #para o último valor, adiciona quebra de linha
    row += str(args[len(args)-1]) + '\n'

    #escreve no arquivo
    csvfile.write(row)

#abre arquivo(sobrescreve o último arquivo criado)
csvfile = open('teste.csv','w')
writeRow(csvfile,'X','Y','Z')#cabeçalho
x=0
y=0
z=0.0
while(True):
    try:
        #escreve separando valores por vígula
        writeRow(csvfile,x,y,z)
        x+=1
        y=2*x
        z=x/2.0
        time.sleep(0.1)
    except KeyboardInterrupt:
        csvfile.close()#fecha arquivo ao sair do loop
        break
