from solucao_inicial import Solucao
import numpy as np
import sys
from leitor import Instancia
import time
from fabrica import FabricaSolucao

class Vizinhanca():
	
	def __init__(self, instancia):
		self.instancia = instancia

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
			c_novo = s.f - 2 * (np.sum(self.instancia.distancias[elems_rand_i][:, elems_rest_i]) + np.sum(self.instancia.distancias[elems_rand_j][:, elems_rest_j]))
			# os elementos de i que serão postos no grupo j e os elementos de j que serão postos em i deverão ter suas diversidades calculadas 
			c_novo += 2 * (np.sum(self.instancia.distancias[elems_rand_i][:, elems_rest_j]) + np.sum(self.instancia.distancias[elems_rand_j][:, elems_rest_i]))

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
				c_novo -= 2 * np.sum(self.instancia.distancias[elems_rand_grupo[i]][:, elementos_grupo[i]])

			y_novo = np.copy(s.y) # cópia do vetor y de s
			z_novo = np.copy(s.z) # cópia do vetor z de s

			for i in range(m - 1):
				c_novo += 2 * np.sum(self.instancia.distancias[elems_rand_grupo[i]][:, elementos_grupo[i + 1]])
				y_novo[elems_rand_grupo[i]] = grupos_selecionados[i + 1]

			c_novo += 2 * np.sum(self.instancia.distancias[elems_rand_grupo[-1]][:, elementos_grupo[0]])
			y_novo[elems_rand_grupo[-1]] = grupos_selecionados[0]

			return Solucao(y_novo, z_novo, c_novo) # retorno de uma nova solução
		else:
			return s # retorno da mesma solução, já que não há vizinho viável

	"""
	Retorna um vizinho aleatório da solução s
		n elementos de um grupo i e n elementos de um grupo j são intercambiados
	"""
	def relocacao(self, s, n):
		limSup = self.instancia.limites[:, 1]
		limInf = self.instancia.limites[:, 0]
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
				c_novo = s.f - 2 * np.sum(self.instancia.distancias[elems_rand_i][:, elems_rest_i]) # retirada dos custos relacionados aos elementos que não estão mais em i
				c_novo += 2 * np.sum(self.instancia.distancias[elems_rand_i][:, elems_grupo_j]) # adição dos custos dos elementos de i que irão para o grupo j

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

	def rvns(self, s, vizinhancas, kmax):
		k = 1
		s_melhor = s
		while k <= kmax:
			s_vizinho = vizinhancas(s_melhor, k)
			if s_vizinho.f > s_melhor.f:
				s_melhor = s_vizinho
				k = 1
			else:
				k += 1
		return s_melhor

	def rvns_relocacao(self, s, n):
		return self.rvns(s, self.relocacao, n)

	def rvns_swap(self, s, n):
		return self.rvns(s, self.swap, n)

	def rvns_swap_generico(self, s, m, n):
		def swap_m(ss, k):
			return self.swap_generico(ss, m, k)
		return self.rvns(s, swap_m, n)

if __name__ == '__main__':
	instancia = Instancia.ler_arquivo(sys.argv[1])
	vizinhanca = Vizinhanca(instancia)
	fabrica = FabricaSolucao(instancia)
	s = fabrica.produzir_solucao()

	print(s)
	start = time.time()
	ss = vizinhanca.rvns_swap_generico(s, 4, 3)
	print(time.time() - start)
	print(ss)