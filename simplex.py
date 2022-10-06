from operator import le

class Simplex:
    
    def __init__(self):
        self.table = [] #inicialização da tabela vazia

    def def_func_objet(self, func_obj: list): #função para definir a função objetiva
        self.table.append(func_obj) #a primeira linha da tabela sempre será a função objetiva

    def adiciona_restricoes(self, restricoes: list): #adição dalista de restrições
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

    def calcula_nova_linha_pivo(self, coluna_entrada: int, linha_saida: int) -> list:
        linha = self.table[linha_saida]

        pivo = linha[coluna_entrada]

        nova_linha_pivo = [valor / pivo for valor in linha]

        return nova_linha_pivo

    def nova_linha(self, linha: list, coluna_entrada: int, linha_pivo: list) -> list:
        pivo = linha[coluna_entrada] * -1

        resultado_linha = [valor * pivo for valor in linha_pivo]

        nova_linha = []

        for i in range(len(resultado_linha)):
            soma_element_linha = resultado_linha[i] + linha[i]
            nova_linha.append(soma_element_linha)

        return nova_linha

    def eh_negativo(self) -> bool:
        negativos = list(filter(lambda x: x < 0, self.table[0]))

        return True if len(negativos) > 0 else False

    def mostrar_tabela(self):
        variaveis_basicas = []
        for i in range(len(self.table)):
            for j in range(len(self.table[0])):
                if self.table[i][j] == 1.0:
                    variaveis_basicas.append(self.table[i][-1])
                print(f'{self.table[i][j]}\t\t\t', end = "")
            print()
        variaveis_basicas.pop(0) #remove o 1 da função objetiva
        print()
        print("Variaveis Basicas: ", variaveis_basicas)

    def calcula(self):
        coluna_entrada = self.coluna_de_entrada()

        primeira_linha_saida = self.linha_de_saida(coluna_entrada)

        linha_pivo = self.calcula_nova_linha_pivo(coluna_entrada, primeira_linha_saida)

        self.table[primeira_linha_saida] = linha_pivo

        copia_table = self.table.copy()

        index = 0

        while index < len(self.table):
            if index != primeira_linha_saida:
                linha = copia_table[index]
                nova_linha = self.nova_linha(linha, coluna_entrada, linha_pivo)
                self.table[index] = nova_linha
            index += 1

    def resolver(self):
        self.calcula()

        while self.eh_negativo():
            self.calcula()
        
        self.mostrar_tabela()

if __name__ == "__main__":

    """
    z = 5x1 + 2x2 -> MAX
    sa:
        2x1 + x2 <= 6
        10x1 + 12x2 <= 60
        x, y <= 0

    fp:
        z - 5x1 - 2x2 = 0

        2x1 + x2 + f1 = 6
        10x1 + 12x2 + f2 = 60
    """

    funcao_obj = [1, -5, -2, 0, 0, 0] #z, x1, x2, f1, f2, =0

    restricoes_1 = [0, 2, 1, 1, 0, 6] #z, x1, x2, f1, f2, =6
    restricoes_2 = [0, 10, 12, 0, 1, 60] #z, x1, x2, f1, f2, =60

    simplex = Simplex()
    simplex.def_func_objet(funcao_obj)
    simplex.adiciona_restricoes(restricoes_1)
    simplex.adiciona_restricoes(restricoes_2)

    simplex.resolver()