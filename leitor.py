import sys

class Instancia():
	
	def __init__(self, n, g, limites, distancias):
		self.n = n
		self.g = g
		self.limites = limites
		self.distancias = distancias

	@staticmethod
	def ler_arquivo(filename):
		file = open(filename, "r")
		info = file.readline().split()
		n = int(info[0])
		g = int(info[1])

		limites = []
		distancias = [[0] * n for _ in range(n)]

		if (info[2] == 'ds'):
			for i in range(3, len(info), 2):
				limites.append((int(info[i]), int(info[i + 1])))
		else:
			limites = [(int(info[3]), int(info[4])) for _ in range(g)]

		for linha in file:
			linha = linha.split()
			i, j, d = int(linha[0]), int(linha[1]), float(linha[2])
			distancias[i][j] = distancias[j][i] = d

		file.close()

		return Instancia(n, g, limites, distancias)


if __name__ == '__main__':
	instancia = Instancia.ler_arquivo(sys.argv[1])
	print(instancia.n)
	print(instancia.g)
	print(instancia.limites)
	print(instancia.distancias)
