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
		info = file.readline().split()
		n = int(info[0])
		g = int(info[1])

		limites = []
		distancias = np.array([[0.] * n for _ in range(n)])

		if (info[2] == 'ds'):
			for i in range(3, len(info), 2):
				limites.append((int(info[i]), int(info[i + 1])))
		else:
			limites = [(int(info[3]), int(info[4])) for _ in range(g)]

		limites = np.array(limites)

		for linha in file:
			linha = linha.split()
			i, j, d = int(linha[0]), int(linha[1]), float(linha[2])
			distancias[i][j] = distancias[j][i] = d

		file.close()

		return Instancia(n, g, limites, distancias)

	def produzir_solucao(self):
		nums = np.arange(self.n)
		y = np.full(self.n, -1, dtype = int)
		z = np.zeros(self.g, dtype = int)

		for i in range(self.g):
			indices = np.random.choice(nums.size, self.limites[i][0], False)
			y[nums[indices]] = i
			z[i] = self.limites[i][0]
			nums = np.delete(nums, indices)

		limSup = self.limites[:, 1]

		while nums.size > 0:
			indice = randint(0, nums.size - 1)
			grupos_nao_cheios = np.where(z < limSup)
			grupo = np.random.choice(grupos_nao_cheios[0], 1)
			y[nums[indice]] = grupo
			z[grupo] += 1
			nums = np.delete(nums, indice)

		custo = 0

		for i in range(self.g):
			elems_grupo_i = np.where(y == i)[0]
			custo += np.sum(self.distancias[elems_grupo_i][:, elems_grupo_i])

		return Solucao(y, z, custo)


if __name__ == '__main__':
	instancia = Instancia.ler_arquivo(sys.argv[1])
	print(instancia.n)
	print(instancia.g)
	print(instancia.limites)
	print(instancia.distancias)
	s = instancia.produzir_solucao()
	print(s.y, s.z, s.f)