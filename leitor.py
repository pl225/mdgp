import sys
import numpy as np
from random import randint
from solucao_inicial import Solucao

class Instancia():
	
	def __init__(self, n, g, limites, distancias):
		self.n = n
		self.g = g
		self.limites = limites
		self.distancias = distancias

	@staticmethod
	def ler_arquivo(filename):
		file = open(filename, "r")
		info = file.readline().split() # divide a palavra inteira em uma lista de palavras conforme espaços em branco
		n = int(info[0]) # quantidade de elementos
		g = int(info[1]) # quantidade de grupos

		limites = []
		distancias = np.array([[0.] * n for _ in range(n)]) # iniciando todas as distancias entre pares de elementos como zero

		# definição dos limites a e b para cada grupo
		if (info[2] == 'ds'): # se os grupos têm tamanhos diferentes
			for i in range(3, len(info), 2):
				limites.append((int(info[i]), int(info[i + 1])))
		else: # os grupos têm tamanhos iguais
			limites = [(int(info[3]), int(info[4])) for _ in range(g)]

		limites = np.array(limites)

		for linha in file: # preenchendo as distancias entre cada par de elemento
			linha = linha.split()
			i, j, d = int(linha[0]), int(linha[1]), float(linha[2])
			distancias[i][j] = distancias[j][i] = d

		file.close()

		return Instancia(n, g, limites, distancias)

if __name__ == '__main__':
	#np.random.seed(0)
	instancia = Instancia.ler_arquivo(sys.argv[1])
	print(instancia.n)
	print(instancia.g)
	print(instancia.limites)
	print(instancia.distancias)