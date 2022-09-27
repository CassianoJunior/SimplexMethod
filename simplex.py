from operator import le

class Simplex:
    
    def __init__(self):
        self.table = [] #inicialização da tabela vazia

    def def_func_objet(self, func_obj: list): #função para definir a função objetiva
        self.table.append(func_obj) #a primeira linha da tabela sempre será a função objetiva

    def add_restricoes(self, restricoes: list): #adição dalista de restrições
        self.table.append(restricoes)

    def coluna_de_entrada(self) -> int: #a coluna que terá os pivores da linha, as variaveis que entram na base
        pivot_coluna = min(self.table[0]) #linha da função objetiva; O menor valor que é o indice, vai representar a coluna dos pivores
        index = self.table[0].index(pivot_coluna) 

        return index #retorna então a coluna de pivoteamento das linhas

    def linha_de_saida(self, coluna_entrada: int) -> int: #retorna o inidice da linha que devera sair
        result = {} #as linhas que são diferentes da linha da função objetiva, fazemos a divisão do ultimo inteiro da linha
                    #vai ser dividio pelo pivor da propria linha, o menor valor dessa divisão vai decidir a linha que vai esta saindo
        for line in range(len(self.table)): #percorrer cada linha
            if line > 0: #se não for a linha da função objetiva
                if self.table[line][coluna_entrada] > 0: #se o pivor for maior que zero, o calculo é possivel
                    divisao = self.table[line][-1] / self.table[line][coluna_entrada] #ultimo elemento da linha dividido pelo elemento pivor
                    result[line] = divisao #armazena na linha em questão
        
        index = min(result, key = result.get) #o menor valor de divisão que contem na linha

        return index #retorna esse menor valor referente a linha