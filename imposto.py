class Carruagem:
    def __init__(self, capacidade):
        self.ouro = 0
        self.estaCheio = False
        self.capacidade = capacidade
        self.distanciaPercorrida = 0

    def encher(self, ouro):
        self.ouro += ouro
        if self.ouro > self.capacidade:
            diferença = self.ouro - self.capacidade
            self.ouro -= diferença
            self.estaCheio = True
            return diferença
        elif self.ouro == self.capacidade:
            self.estaCheio = True
            return 0
        else:
            return 0

    def esvaziar(self):
        self.ouro = 0
        self.estaCheio = False

class Cidade:
    def __init__(self, id=-1, ouro=0):
        self.id = id
        self.cofre = ouro
        self.vizinhancas = []
        self.distanciaDaCapital = 0
        self.cidadeVisitada = (None, 0) # Cidade visitada mais distância referente a ela.

    def cofreEstaVazio(self):
        return self.cofre == 0

class Estrada:
    def __init__(self, comprimento, cidade1, cidade2):
        self.comprimento = comprimento
        self.cidade1 = cidade1
        self.cidade2 = cidade2

class Reino:
    def __init__(self):
        self.cidades = []
        self.estrads = []
        self.cobrandoImpostos = True

    def construirCidade(self, id, ouro):
        self.cidades.append(Cidade(id, ouro))

    def construirEstrada(self, comprimento, idCidade1, idCidade2):
        cidade1 = self._buscarCidade(idCidade1)
        cidade2 = self._buscarCidade(idCidade2)
        estrada = Estrada(comprimento, cidade1, cidade2)
        cidade1.vizinhancas.append((cidade2, estrada))
        cidade2.vizinhancas.append((cidade1, estrada))
        self.estrads.append(estrada)

    def _buscarCidade(self, id):
        return self.cidades[id-1]

    def coletarImposto(self, carruagem):
        # Busca por profundidade usando pilha iterativa ao invés de recursão.

        pilha = []
        capital = self._buscarCidade(1)
        pilha.append(capital)
        retornando = False

        while self.cobrandoImpostos:
            encontrouVizinho = False
            cidadeVisitada = Cidade()
            cidadeAtual = pilha[len(pilha)-1]
            carruagem.distanciaPercorrida += cidadeAtual.distanciaDaCapital * 2
            carruagem.esvaziar()

            while pilha:
                cidadeAtual = pilha[len(pilha)-1]

                if cidadeAtual.cidadeVisitada[0] != None and not cidadeVisitada.cidadeVisitada[0] == cidadeAtual and not retornando: carruagem.distanciaPercorrida += cidadeAtual.cidadeVisitada[1] * 2
                cidadeVisitada = cidadeAtual

                for vizinhanca in cidadeAtual.vizinhancas:
                    if not vizinhanca[0].cofreEstaVazio() and not vizinhanca[0] == cidadeAtual.cidadeVisitada[0]:
                        pilha.append(vizinhanca[0])
                        vizinhanca[0].cidadeVisitada = (cidadeAtual, vizinhanca[1].comprimento)
                        vizinhanca[0].distanciaDaCapital = cidadeAtual.distanciaDaCapital + vizinhanca[1].comprimento
                        encontrouVizinho = True

                if not encontrouVizinho:
                    if cidadeAtual == capital: 
                        self.cobrandoImpostos = False
                        break
                    diferença = carruagem.encher(cidadeAtual.cofre)
                    cidadeAtual.cofre = diferença
                    pilha.pop()

                retornando = False
                encontrouVizinho = False
                if carruagem.estaCheio: break
            retornando = True

        self.cobrandoImpostos = True

def main():
    n, c = input().split(" ")
    n = int(n)
    c = int(c)
    reino = Reino()
    carruagem = Carruagem(c)
    impostos = input()
    impostos = impostos.split(" ")
    for i in range(len(impostos)):
        reino.construirCidade(i+1, int(impostos[i]))

    for i in range(n-1):
        a, b, c = input().split(" ")
        a = int(a)
        b = int(b)
        c = int(c)
        reino.construirEstrada(c, a, b)
    
    reino.coletarImposto(carruagem)
    print(carruagem.distanciaPercorrida)

if __name__ == "__main__":
    main()