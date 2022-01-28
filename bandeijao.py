import sys
from collections import deque
from enum import Enum

class Chamada(Enum):
    PAR = 0
    IMPAR = 1

class Planeta:
    def __init__(self, id):
        self.id = id
        self.rotas = []
        # Menor distância entre o planeta terra e um enésimo planeta qualquer, considerando que um deles é 
        # referente a uma quantidade par de planetas passados, e o outro ímpar.
        self.distImpar = sys.maxsize
        self.distPar = sys.maxsize

class Rota:
    def __init__(self, comprimento, planetaDestino):
        self.comprimento = comprimento
        self.planetaDestino = planetaDestino

class Galaxia:
    def __init__(self):
        self.planetas = []

    def criarPlaneta(self, id):
        self.planetas.append(Planeta(id))

    def criarRota(self, comprimento, idPlaneta1, idPlaneta2):
        planeta1 = self._procurarPlaneta(idPlaneta1)
        planeta2 = self._procurarPlaneta(idPlaneta2)
        planeta1.rotas.append(Rota(comprimento, planeta2))
        planeta2.rotas.append(Rota(comprimento, planeta1))

    def _procurarPlaneta(self, id):
        return self.planetas[id]

    def pesquisarMenorCaminho(self, idTerra, idBandeijao):
        terra = self._procurarPlaneta(idTerra)
        terra.distPar = 0
        filaDeExecucao = deque()
        filaDeExecucao.append((terra, Chamada.IMPAR))

        while filaDeExecucao:
            execucaoAtual = filaDeExecucao.popleft()
            planetaAtual = execucaoAtual[0]
            chamadaAtual = execucaoAtual[1]
            rotasAdjacentes = planetaAtual.rotas

            for rota in rotasAdjacentes:
                planetaAdjacente = rota.planetaDestino

                if chamadaAtual == Chamada.PAR:
                    if planetaAtual.distImpar + rota.comprimento < planetaAdjacente.distPar:
                        planetaAdjacente.distPar = planetaAtual.distImpar + rota.comprimento
                        filaDeExecucao.append((planetaAdjacente, Chamada.IMPAR))

                elif chamadaAtual == Chamada.IMPAR:
                    if planetaAtual.distPar + rota.comprimento < planetaAdjacente.distImpar:
                        planetaAdjacente.distImpar = planetaAtual.distPar + rota.comprimento
                        filaDeExecucao.append((planetaAdjacente, Chamada.PAR))

        if self.planetas[idBandeijao].distImpar == sys.maxsize:
            return ":("
        else:
            return self.planetas[idBandeijao].distImpar
        
def main():
    galaxia = Galaxia()

    n, m = input().split(" ")
    n = int(n)
    m = int(m)

    for i in range(n):
        galaxia.criarPlaneta(i+1)

    for i in range(m):
        u, v, w = input().split(" ")
        u = int(u)
        v = int(v)
        w = int(w)

        galaxia.criarRota(w, u-1, v-1)

    resultado = galaxia.pesquisarMenorCaminho(0, n-1)
    print(resultado)

if __name__ == "__main__":
    main()