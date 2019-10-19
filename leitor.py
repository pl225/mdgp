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

	def produzir_solucao(self):
		nums = np.arange(self.n) # preenchimento de lista de 0 a n - 1 elementos
		y = np.full(self.n, -1, dtype = int) # todos os elementos não estão associados a grupos no começo
		z = np.zeros(self.g, dtype = int) # os grupos começam vazios

		for i in range(self.g):
			indices = np.random.choice(nums.size, self.limites[i][0], False) # escolha aleatória de a_g elementos para o grupo g
			y[nums[indices]] = i # todos os elementos selecionados são associados ao grupo i
			z[i] = self.limites[i][0] # o número a de elementos para i foi selecionado
			nums = np.delete(nums, indices) # exclusão dos elementos selecionados

		limSup = self.limites[:, 1]

		while nums.size > 0: # seleção dos elementos restantes
			indice = randint(0, nums.size - 1) # seleção de um elemento
			grupos_nao_cheios = np.where(z < limSup) # seleção dos grupos com menos que b elementos
			grupo = np.random.choice(grupos_nao_cheios[0], 1) # escolha aleatória do grupo
			y[nums[indice]] = grupo # associação do elemento ao grupo
			z[grupo] += 1 # incrementando a quantidade de elementos do grupo
			nums = np.delete(nums, indice) # exclusão do elemento associado

		custo = 0

		for i in range(self.g): # cálculo do custo da solução
			elems_grupo_i = np.where(y == i)[0] # quais elementos são do grupo i
			custo += np.sum(self.distancias[elems_grupo_i][:, elems_grupo_i]) # soma das distancias entre os elementos do grupo i

		return Solucao(y, z, custo)


if __name__ == '__main__':
	instancia = Instancia.ler_arquivo(sys.argv[1])
	print(instancia.n)
	print(instancia.g)
	print(instancia.limites)
	print(instancia.distancias)
	s = instancia.produzir_solucao()
	print(s.y, s.z, s.f)