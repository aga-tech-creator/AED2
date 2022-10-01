class Consulta:
    def __init__(self):
        self.cor = 0
        self.cores = []
        self.consultasEmConflito = []
        self.horarioInicio = 0
        self.horarioTermino = 0

class Agenda:
    def __init__(self):
        self.consultas = []
        self.gruposInconflitantes = []
        self.consultasSelecionadas = []
        self.coresUsadas = []

    def exemplo(self):
        for i in self.consultas:
            for j in self.consultas:
                if self._definirConflito(i, j):
                    i.consultasEmConflito.append(j)

    def agendarConsulta(self, horarioInicio, horarioTermino):
        novaConsulta = Consulta()
        novaConsulta.horarioInicio = horarioInicio
        novaConsulta.horarioTermino = horarioTermino
        self.consultas.append(novaConsulta)

    def ordenarConsultas(self):
        self.consultas.sort(key=lambda consulta: len(consulta.consultasEmConflito), reverse=True)

    def _definirConflito(self, consulta1, consulta2):
        if(consulta2.horarioTermino > consulta1.horarioInicio > consulta2.horarioInicio) or (consulta2.horarioInicio < consulta1.horarioTermino < consulta2.horarioTermino) or (consulta2.horarioInicio > consulta1.horarioInicio and consulta2.horarioTermino < consulta1.horarioTermino):
            return True
        else:
            return False

    def definirCores(self):
        for consulta in self.consultas:
            for i in range(len(self.consultas[0].consultasEmConflito)):
                consulta.cores.append(i+1)
        for i in range(len(self.consultas[0].consultasEmConflito)):
            self.coresUsadas.append(0)


    def contarCores(self):
        for consulta in self.consultas:
            self.coresUsadas[consulta.cor - 1] += 1

    def validarConsulta(self):
        for consulta in self.consultas:
            for vizinho in consulta.consultasEmConflito:
                if not vizinho.cor == 0:
                    consulta.cores[vizinho.cor - 1] = 0

            for cor in consulta.cores:
                if not cor == 0:
                    consulta.cor = cor
                    break

def main():
    agenda = Agenda()
    n = int(input())

    for i in range(n):
        x, y = input().split(" ")
        x = int(x)
        y = int(y)
        agenda.agendarConsulta(x, y)

    agenda.exemplo()
    agenda.ordenarConsultas()
    agenda.definirCores()
    agenda.validarConsulta()
    agenda.contarCores()
    maiorCor = 0
    for cor in agenda.coresUsadas:
        if cor > maiorCor:
            maiorCor = cor

    print(maiorCor)

if __name__ == "__main__":
    main()