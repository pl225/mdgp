from solucao_inicial import Solucao
from random import randint
import numpy as np

class FabricaSolucao():
	
	def __init__(self, instancia):
		self.instancia = instancia

	def produzir_solucao(self):
		nums = np.arange(self.instancia.n) # preenchimento de lista de 0 a n - 1 elementos
		y = np.full(self.instancia.n, -1, dtype = int) # todos os elementos não estão associados a grupos no começo
		z = np.zeros(self.instancia.g, dtype = int) # os grupos começam vazios

		for i in range(self.instancia.g):
			indices = np.random.choice(nums.size, self.instancia.limites[i][0], False) # escolha aleatória de a_g elementos para o grupo g
			y[nums[indices]] = i # todos os elementos selecionados são associados ao grupo i
			z[i] = self.instancia.limites[i][0] # o número a de elementos para i foi selecionado
			nums = np.delete(nums, indices) # exclusão dos elementos selecionados

		limSup = self.instancia.limites[:, 1]

		while nums.size > 0: # seleção dos elementos restantes
			indice = randint(0, nums.size - 1) # seleção de um elemento
			grupos_nao_cheios = np.where(z < limSup) # seleção dos grupos com menos que b elementos
			grupo = np.random.choice(grupos_nao_cheios[0], 1) # escolha aleatória do grupo
			y[nums[indice]] = grupo # associação do elemento ao grupo
			z[grupo] += 1 # incrementando a quantidade de elementos do grupo
			nums = np.delete(nums, indice) # exclusão do elemento associado

		custo = 0

		for i in range(self.instancia.g): # cálculo do custo da solução
			elems_grupo_i = np.where(y == i)[0] # quais elementos são do grupo i
			custo += np.sum(self.instancia.distancias[elems_grupo_i][:, elems_grupo_i]) # soma das distancias entre os elementos do grupo i

		return Solucao(y, z, custo)