import heapq

class No:
    def __init__(self, char=None, freq=0):
        self.dir = [None, 1]
        self.esq = [None, 0]
        self.freq = freq
        self.char = char

class Arvore_Hufflman:
    def __init__(self):
        self.raiz = None
        self.hufflman_trie_binario = ""
        self.tabela_binaria = []
        self.count = 0
        self.string_binaria_entrada = ""
        self.bits_de_enchimento = ""

    def calcular_tamanho_binario_entrada(self, entrada):
        tamTemp = len(entrada)
        stringTempBin = format(tamTemp, "b")
        self.string_binaria_entrada = ("0"*(32-len(stringTempBin)))+stringTempBin

    def montar_arvore(self, fila):
        while True:
            item1 = heapq.heappop(fila)
            item2 = heapq.heappop(fila)
            pai = No()

            pai.esq[0] = item1[2]
            pai.dir[0] = item2[2]

            pai.freq = item1[2].freq + item2[2].freq
            if not fila: break
            self.count+=1
            heapq.heappush(fila, (pai.freq, self.count,pai) )
        self.raiz = pai
    
    def codificacao_de_hufflman(self, no, valor_binario=""):
        if no == None: return
        if no.char != None:
            self.tabela_binaria.append((no.char, valor_binario, no.freq))
            self.hufflman_trie_binario += "1"
            varTemp = format(ord(no.char), 'b')
            varTemp = ("0"*(8-len(varTemp))) + varTemp
            self.hufflman_trie_binario += varTemp
        else:
            self.hufflman_trie_binario += "0"
        
        self.codificacao_de_hufflman(no.esq[0], str(valor_binario)+str(no.esq[1]))
        self.codificacao_de_hufflman(no.dir[0], str(valor_binario)+str(no.dir[1]))


    def calcular_frequencia_de_caracteres(self, caracteres, entrada):
        fila = []
        for i in range(len(entrada)):
            caracteres[ord(entrada[i])] += 1
        for j in range(128):
            if caracteres[j] != 0:
                self.count+=1
                heapq.heappush(fila, (caracteres[j], self.count, No(chr(j), caracteres[j])) )
        return fila

    def contar_bits(self):
        count = 0
        for i in self.tabela_binaria:
            count += len(i[1])*i[2]
        count += len(self.hufflman_trie_binario)+len(self.string_binaria_entrada)
        self._calcular_bits_de_enchimento(count)
        count += len(self.bits_de_enchimento)
        return count

    def _calcular_bits_de_enchimento(self, count):
        resto = count % 8
        multiplicador = 8-resto
        self.bits_de_enchimento = multiplicador*"0"


if __name__ == "__main__":
    caracteres = []
    arvore = Arvore_Hufflman()
    for _ in range(128): caracteres.append(0)
    r = open('example.txt')
    entrada = list(r.read())
    fila = arvore.calcular_frequencia_de_caracteres(caracteres, entrada)
    arvore.montar_arvore(fila)
    arvore.calcular_tamanho_binario_entrada(entrada)
    arvore.codificacao_de_hufflman(arvore.raiz)
    resultado = arvore.contar_bits()
    print(f"{resultado} bits")