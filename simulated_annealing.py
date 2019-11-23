from leitor import Instancia
from fabrica import FabricaSolucao
from vizinhanca import Vizinhanca
from random import random
from math import exp
import sys
from timeit import default_timer

class SimulatedAnnealing():

	def __init__(self, fabrica, vizinhanca):
		self.fabrica = fabrica
		self.vizinhanca = vizinhanca


	def executar(self, alpha, temperatura_inicial, temperatura_final, s_max):
		
		s = self.fabrica.produzir_solucao()
		s_melhor = s
		t = temperatura_inicial

		print("Solução inicial: {}".format(s))
		
		while t > temperatura_final:
			iter_t = 0
			while iter_t < s_max:
				iter_t += 1
				s_vizinho = self.vizinhanca.swap(s, 1) if random() < .5 else self.vizinhanca.relocacao(s, 1)
				delta = s_vizinho.f - s.f
				if delta > 0:
					s = s_vizinho
					if s_vizinho.f > s_melhor.f:
						s_melhor = s_vizinho
				else:
					x = random()
					if x < exp(delta / t):
						s = s_vizinho
			t *= alpha

		print("Melhor solução encontrada: {}".format(s_melhor))

if __name__ == '__main__':
	instancia = Instancia.ler_arquivo(sys.argv[1])
	fabrica = FabricaSolucao(instancia)
	vizinhanca = Vizinhanca(instancia)
	simulated_annealing = SimulatedAnnealing(fabrica, vizinhanca)
	
	alpha = 0.9
	temperatura_inicial = (instancia.n * 10) // 2 #1000
	temperatura_final = 0.001 #0.0001
	s_max = (instancia.n * 10) // 2 #1000

	print("Temperatura inicial: {}, temperatura final: {}, alpha: {}, sMax: {}".format(temperatura_inicial, temperatura_final, alpha, s_max))

	inicio = default_timer()
	simulated_annealing.executar(alpha, temperatura_inicial, temperatura_final, s_max)
	fim = default_timer()
	print("Tempo total: {}".format(fim - inicio))