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

	"""
	Retorna um vizinho aleatório da solução s
		n elementos de um grupo i e n elementos de um grupo j são intercambiados
	"""
	def swap(self, s, n):
		grupos_n_elementos = np.where(s.z >= n)[0] # separação dos grupos que tenham ao menos n elementos

		if grupos_n_elementos.size >= 2: # se houver pelo menos dois conjuntos com pelos menos n elementos
			grupo_i, grupo_j = np.random.choice(grupos_n_elementos, 2, False) # escolha aleatória dos grupos i e j
			elems_grupo_i = np.where(s.y == grupo_i)[0] # aquisição de todos os elementos do grupo i
			elems_grupo_j = np.where(s.y == grupo_j)[0] # aquisição de todos os elementos do grupo j

			elems_rand_i_index = np.random.choice(elems_grupo_i.size, n, False) # escolha aleatória de n índices, ou seja, as posições dos elementos que serão tirados do grupo i
			elems_rand_j_index = np.random.choice(elems_grupo_j.size, n, False) # escolha aleatória de n índices, ou seja, as posições dos elementos que serão tirados do grupo j
			elems_rand_i = elems_grupo_i[elems_rand_i_index] # seleção dos elementos de acordo com os índices escolhidos aleatoriamente do grupo i
			elems_rand_j = elems_grupo_j[elems_rand_j_index] # seleção dos elementos de acordo com os índices escolhidos aleatoriamente do grupo j

			y_novo = np.copy(s.y) # cópia do vetor y de s
			z_novo = np.copy(s.z) # cópia do vetor z de s
			elems_rest_i = np.delete(elems_grupo_i, elems_rand_i_index) # separação dos elementos que continuarão do grupo i
			elems_rest_j = np.delete(elems_grupo_j, elems_rand_j_index) # separação dos elementos que continuarão do grupo j
			
			# os elementos de i que não farão mais dele e os elementos de j que não farão mais parte dele deverão ter suas diversidades retiradas
			c_novo = s.f - 2 * (np.sum(self.distancias[elems_rand_i][:, elems_rest_i]) + np.sum(self.distancias[elems_rand_j][:, elems_rest_j]))
			# os elementos de i que serão postos no grupo j e os elementos de j que serão postos em i deverão ter suas diversidades calculadas 
			c_novo += 2 * (np.sum(self.distancias[elems_rand_i][:, elems_rest_j]) + np.sum(self.distancias[elems_rand_j][:, elems_rest_i]))

			y_novo[elems_rand_i] = grupo_j # troca de grupos
			y_novo[elems_rand_j] = grupo_i # troca de grupos

			return Solucao(y_novo, z_novo, c_novo) # retorno de uma nova solução
		else:
			return s # retorno da mesma solução, já que não há vizinho viável

	"""
	Retorna um vizinho aleatório da solução s
		n elementos de um grupo m são intercambiados
	"""
	def swap_generico(self, s, m, n):
		grupos_n_elementos = np.where(s.z >= n)[0] # separação dos grupos que tenham ao menos n elementos

		if grupos_n_elementos.size >= m: # se houver pelo menos dois conjuntos com pelos menos n elementos
			grupos_selecionados = np.random.choice(grupos_n_elementos, m, False) # escolha aleatória dos grupos i e j
			
			elementos_grupo = []
			elems_rand_grupo = []
			c_novo = s.f
			for i in range(m):
				elementos_grupo.append(np.where(s.y == grupos_selecionados[i])[0]) # aquisição de todos os elementos do grupo g
				indexes = np.random.choice(elementos_grupo[i].size, n, False)
				elems_rand_grupo.append(elementos_grupo[i][indexes])
				elementos_grupo[i] = np.delete(elementos_grupo[i], indexes)
				c_novo -= 2 * np.sum(self.distancias[elems_rand_grupo[i]][:, elementos_grupo[i]])

			y_novo = np.copy(s.y) # cópia do vetor y de s
			z_novo = np.copy(s.z) # cópia do vetor z de s

			for i in range(m - 1):
				c_novo += 2 * np.sum(self.distancias[elems_rand_grupo[i]][:, elementos_grupo[i + 1]])
				y_novo[elems_rand_grupo[i]] = grupos_selecionados[i + 1]

			c_novo += 2 * np.sum(self.distancias[elems_rand_grupo[-1]][:, elementos_grupo[0]])
			y_novo[elems_rand_grupo[-1]] = grupos_selecionados[0]

			return Solucao(y_novo, z_novo, c_novo) # retorno de uma nova solução
		else:
			return s # retorno da mesma solução, já que não há vizinho viável

	"""
	Retorna um vizinho aleatório da solução s
		n elementos de um grupo i e n elementos de um grupo j são intercambiados
	"""
	def relocacao(self, s, n):
		limSup = self.limites[:, 1]
		limInf = self.limites[:, 0]
		grupos_inf = np.where(s.z >= limInf + n)[0] # grupos com o limite inferior mais n elementos satisfeito
		grupos_sup = np.where(s.z <= limSup - n)[0] # grupos com o limite superior menos n elementos satisfeito

		if grupos_inf.size > 0 and grupos_sup.size > 0: # se houver pelo menos dois conjuntos com mais de um elemento
			
			grupo_i = np.random.choice(grupos_inf, 1) # escolha aleatória do grupo i que perderá elementos
			grupos_sup = np.delete(grupos_sup, np.argwhere(grupos_sup == grupo_i)) # exclusão do grupo i escolhido dos outros candidatos
			
			if grupos_sup.size > 0: # se ainda há mais de um elemento após a possível exclusão do grupo i
				grupo_j = np.random.choice(grupos_sup, 1) # escolha aleatória do grupo j que receberá elementos
				elems_grupo_i = np.where(s.y == grupo_i)[0] # aquisição de todos os elementos do grupo i
				elems_grupo_j = np.where(s.y == grupo_j)[0] # aquisição de todos os elementos do grupo j

				elems_rand_i_index = np.random.choice(elems_grupo_i.size, n, False) # escolha aleatória de n índices, ou seja, as posições dos elementos que serão tirados do grupo i
				elems_rand_i = elems_grupo_i[elems_rand_i_index] # seleção dos elementos de acordo com os índices escolhidos aleatoriamente do grupo i

				elems_rest_i = np.delete(elems_grupo_i, elems_rand_i_index) # separação dos elementos que continuarão no grupo i
				c_novo = s.f - 2 * np.sum(self.distancias[elems_rand_i][:, elems_rest_i]) # retirada dos custos relacionados aos elementos que não estão mais em i
				c_novo += 2 * np.sum(self.distancias[elems_rand_i][:, elems_grupo_j]) # adição dos custos dos elementos de i que irão para o grupo j

				y_novo = np.copy(s.y) # cópia do vetor y de s
				z_novo = np.copy(s.z) # cópia do vetor z de s
				
				y_novo[elems_rand_i] = grupo_j # atribuição dos elementos retirados de i ao grupo j
				z_novo[grupo_i] -= n # decréscimo de n elementos do grupo i
				z_novo[grupo_j] += n # acréscimo de n elementos ao grupo j

				return Solucao(y_novo, z_novo, c_novo)
                                
			else:
				return s # retorno da mesma solução, já que não há vizinho viável
		
		else:
			return s # retorno da mesma solução, já que não há vizinho viável


if __name__ == '__main__':
	#np.random.seed(0)
	instancia = Instancia.ler_arquivo(sys.argv[1])
	print(instancia.n)
	print(instancia.g)
	print(instancia.limites)
	print(instancia.distancias)
	s = instancia.produzir_solucao()
	print(s)
	print(instancia.swap_generico(s, 3, 2))