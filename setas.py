from enum import Enum
from collections import deque
import sys

class Seta:
    def __init__(self, circuloOrigem, circuloDestino):
        self.circuloOrigem = circuloOrigem
        self.circuloDestino = circuloDestino

class Sentido(Enum):
    NORMAL = 0
    OPOSTO = 1

class Circulo:
    def __init__(self, id):
        self.id = id
        self.setasInvertidas = sys.maxsize
        self.adjacentes = []
        self.sentidosDasSetas = []
        self.setas = []

class Desenho:
    def __init__(self):
        self.circulos = []
        self.setas = []

    def desenharCirculo(self, id):
        self.circulos.append(Circulo(id))

    def desenharSeta(self, idCirculoOrigem, idCirculoDestino):
        circuloOrigem = self._procurarCirculo(idCirculoOrigem)
        circuloDestino = self._procurarCirculo(idCirculoDestino)
        seta = Seta(circuloOrigem, circuloDestino)

        # Adicionando a seta ao desenho e ligando aos círculos.
        self.setas.append(seta)
        circuloOrigem.setas.append(seta)
        circuloDestino.setas.append(seta)

        # Adicionando o sentido da seta em relação aos círculos.
        circuloOrigem.sentidosDasSetas.append(Sentido.NORMAL)
        circuloDestino.sentidosDasSetas.append(Sentido.OPOSTO)

        # Criando a relação de um círculo com o outro por meio da seta.
        circuloOrigem.adjacentes.append(circuloDestino)
        circuloDestino.adjacentes.append(circuloOrigem)

    def _procurarCirculo(self, idCirculo):
        return self.circulos[idCirculo-1]

    def checarResposta(self, idCirculoA, idCirculoB):
        a = self._procurarCirculo(idCirculoA)
        b = self._procurarCirculo(idCirculoB)
        a.setasInvertidas = 0
        filaDeExecucao = deque()
        filaDeExecucao.append(a)

        while filaDeExecucao:
            circuloAtual = filaDeExecucao.popleft()
            adjacentesDoAtual = circuloAtual.adjacentes
            i = 0

            while i < len(adjacentesDoAtual):
                adjacente = adjacentesDoAtual[i]
                circuloAtual.setasInvertidas += circuloAtual.sentidosDasSetas[i].value

                if circuloAtual.setasInvertidas < adjacente.setasInvertidas:
                    adjacente.setasInvertidas = circuloAtual.setasInvertidas
                    filaDeExecucao.append(adjacente)

                circuloAtual.setasInvertidas -= circuloAtual.sentidosDasSetas[i].value
                i += 1
        
        return b.setasInvertidas

    def reiniciarJogo(self):
        for circulo in self.circulos:
            circulo.setasInvertidas = sys.maxsize      

def main():
    instrutor = Desenho()
    bibiResposta = 0
    bibikaResposta = 0

    c, s, a, b = input().split(" ")
    c = int(c)
    s = int(s)
    a = int(a)
    b = int(b)

    for i in range(c):
        instrutor.desenharCirculo(i+1)

    for i in range(s):
        c1, c2 = input().split(" ")
        c1 = int(c1)
        c2 = int(c2)
        instrutor.desenharSeta(c1, c2)

    bibiResposta = instrutor.checarResposta(a, b)
    instrutor.reiniciarJogo()
    bibikaResposta = instrutor.checarResposta(b, a)

    if bibiResposta == bibikaResposta:
        print("Bibibibika")
    elif bibiResposta > bibikaResposta:
        print(f"Bibika: {bibikaResposta}")
    elif bibikaResposta > bibiResposta:
        print(f"Bibi: {bibiResposta}")

if __name__ == "__main__":
    main()