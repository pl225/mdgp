from solucao_inicial import Solucao
from random import randint
import numpy as np
import os
from leitor import Instancia
import time
import sys

class FabricaSolucao():
	
	def __init__(self, instancia):
		self.instancia = instancia
		self.limInf = self.instancia.limites[:, 0]
		self.limSup = self.instancia.limites[:, 1]

	def custo(self, y):
		custo = 0

		for i in range(self.instancia.g): # cálculo do custo da solução
			elems_grupo_i = np.where(y == i)[0] # quais elementos são do grupo i
			custo += np.sum(self.instancia.distancias[elems_grupo_i][:, elems_grupo_i]) # soma das distancias entre os elementos do grupo i

		return custo

	def produzir_solucao(self):
		nums = np.arange(self.instancia.n) # preenchimento de lista de 0 a n - 1 elementos
		y = np.full(self.instancia.n, -1, dtype = int) # todos os elementos não estão associados a grupos no começo
		z = np.zeros(self.instancia.g, dtype = int) # os grupos começam vazios

		for i in range(self.instancia.g):
			indices = np.random.choice(nums.size, self.instancia.limites[i][0], False) # escolha aleatória de a_g elementos para o grupo g
			y[nums[indices]] = i # todos os elementos selecionados são associados ao grupo i
			z[i] = self.instancia.limites[i][0] # o número a de elementos para i foi selecionado
			nums = np.delete(nums, indices) # exclusão dos elementos selecionados

		while nums.size > 0: # seleção dos elementos restantes
			indice = randint(0, nums.size - 1) # seleção de um elemento
			grupos_nao_cheios = np.where(z < self.limSup) # seleção dos grupos com menos que b elementos
			grupo = np.random.choice(grupos_nao_cheios[0], 1) # escolha aleatória do grupo
			y[nums[indice]] = grupo # associação do elemento ao grupo
			z[grupo] += 1 # incrementando a quantidade de elementos do grupo
			nums = np.delete(nums, indice) # exclusão do elemento associado

		return Solucao(y, z, self.custo(y))

	def escolher_elemento_grasp(self, elementos_grupo, elems, grupos, alpha, y, z, lim):
		
		n_possibilidades = elems.size * grupos.size # número máximo de candidatos
		cands_aleatorio = np.random.choice(n_possibilidades, min(n_possibilidades, 1500 // self.instancia.g), False) # seleção aleatória dos candidatos
		score = np.array(
			[np.sum(self.instancia.distancias[c // grupos.size][elementos_grupo[c % grupos.size]]) / len(elementos_grupo[c % grupos.size]) 
				for c in cands_aleatorio]
		) # calculo da diversidade do de um elemento para todos os grupos

		mini, maxi = np.min(score), np.max(score) # cálculo dos extremos da pontuação
		LRC = np.where(score >= maxi - alpha * (maxi - mini))[0] # construção da LRC
		e = np.random.choice(LRC) # escolha do elemento
		i, j = cands_aleatorio[e] // grupos.size, cands_aleatorio[e] % grupos.size

		y[elems[i]] = grupos[j]
		z[grupos[j]] += 1
		elementos_grupo[j].append(elems[i])

		elems = np.delete(elems, i)
		if z[grupos[j]] == lim[grupos[j]]:
			grupos = np.delete(grupos, j)

		return elems, grupos

	def grasp(self, alpha):
		y = np.full(self.instancia.n, -1, dtype = int) # todos os elementos não estão associados a grupos no começo
		z = np.zeros(self.instancia.g, dtype = int) # os grupos começam vazios
		
		# fase 1
		elems_ordenados_distancia = np.argsort(np.sum(self.instancia.distancias, axis = 1)) # elementos ordenados de acordo com a soma para todos os outros
		melhores = elems_ordenados_distancia[-self.instancia.g:] # seleção dos g últimos elementos (ordem crescente)
		np.random.shuffle(melhores) # embaralhamento dos melhores
		y[melhores] = np.arange(self.instancia.g, dtype = int) # cada um deles é atribuído a um grupo
		z += 1 # um elemento foi atribuído a cada grupo
		
		elems_ordenados_distancia = elems_ordenados_distancia[:-self.instancia.g] # apenas os elementos não atribuídos são candidatos agora

		grupos_abaixo_minimo = np.where(z < self.limInf)[0] # grupos que ainda não têm o número mínimo de elementos
		elementos_grupo = [[m] for m in melhores]

		while grupos_abaixo_minimo.size > 0:
			elems_ordenados_distancia, grupos_abaixo_minimo = self.escolher_elemento_grasp(elementos_grupo, elems_ordenados_distancia, grupos_abaixo_minimo, alpha, y, z, self.limInf)

		grupos_abaixo_maximo = np.where(z < self.limSup)[0]

		while elems_ordenados_distancia.size > 0:
			elems_ordenados_distancia, grupos_abaixo_maximo = self.escolher_elemento_grasp(elementos_grupo, elems_ordenados_distancia, grupos_abaixo_maximo, alpha, y, z, self.limSup)

		return Solucao(y, z, self.custo(y))

	def wj(self):
		nums = np.arange(self.instancia.n) # preenchimento de lista de 0 a n - 1 elementos
		y = np.full(self.instancia.n, -1, dtype = int) # todos os elementos não estão associados a grupos no começo
		z = np.zeros(self.instancia.g, dtype = int) # os grupos começam vazios

		i = np.random.choice(nums.size)
		e = nums[i]
		y[e] = 0
		z[0] = 1 
		nums = np.delete(nums, i)

		g = 1
		while nums.size > 0:
			if z[g] < self.limSup[g]:
				e_similar_indice = np.argmin(self.instancia.distancias[e][nums])
				e = nums[e_similar_indice]
				y[e] = g
				z[g] += 1
				nums = np.delete(nums, e_similar_indice)

			g += 1
			if g >= self.instancia.g:
				g = 0

		return Solucao(y, z, self.custo(y))

def executarTestes(resultados, tipo, arquivos):
	resultados.write('\n\n############################' + tipo + '############################\n\n')
	for arq in arquivos:
		instancia = Instancia.ler_arquivo(arq)
		fabrica = FabricaSolucao(instancia)
		alpha = None
		if tipo == 'Aleatório':
			construcao = fabrica.produzir_solucao
		elif tipo == 'GRASP':
			construcao = fabrica.grasp
			alpha = .5
		else:
			construcao = fabrica.wj
		custo = np.array([])
		tempo = np.array([])
		for _ in range(5):
			start = time.time()
			custo = np.append(custo, construcao().f if not alpha else construcao(alpha).f)
			tempo = np.append(tempo, time.time() - start)
		resultados.write("{0}\t{1:.2f}\t\t{2:.3f}\t{3:.3f}\t\t{4:.3f}\t{5:.3f}\n".
			format(arq.split('/')[2], np.max(custo), np.average(custo), np.std(custo), np.average(tempo), np.std(tempo)))


if __name__ == '__main__':
	caminho = 'mdgplib/'
	arquivos = []
	for r, d, f in os.walk(caminho):
		for file in f:
			if 'resultados_construcao.txt' != file:
				arquivos.append(os.path.join(r, file))
	arquivos.sort()
	resultados = open('resultados_construcao.txt', 'w')
	resultados.write('Instância\tmelhor custo\tmédia custo\t\tstd custo\tmédia tempo\t\tstd tempo\n')
	executarTestes(resultados, 'Aleatório', arquivos)
	print('Acabou o aleatório')
	executarTestes(resultados, 'GRASP', arquivos)
	print('Acabou o GRASP')
	executarTestes(resultados, 'WJ', arquivos)
	print('Acabou o WJ');
	resultados.close()