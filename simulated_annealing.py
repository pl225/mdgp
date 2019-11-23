from leitor import Instancia
from random import random
from math import exp
import sys
import numpy as np
from timeit import default_timer

def simulated_annealing(instancia, alpha, temperatura_inicial, temperatura_final, s_max):
	
	s = instancia.produzir_solucao()
	s_melhor = s
	t = temperatura_inicial

	print("Solução inicial: {}".format(s))
	
	while t > temperatura_final:
		iter_t = 0
		while iter_t < s_max:
			iter_t += 1
			s_vizinho = instancia.swap(s, 1) if random() < .5 else instancia.relocacao(s, 1)
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
	alpha = 0.9
	temperatura_inicial = 1000#instancia.n * 1000
	temperatura_final = 0.0001
	s_max = 1000#instancia.n * 100

	print("Temperatura inicial: {}, temperatura final: {}, alpha: {}, sMax: {}".format(temperatura_inicial, temperatura_final, alpha, s_max))

	inicio = default_timer()
	simulated_annealing(instancia, alpha, temperatura_inicial, temperatura_final, s_max)
	fim = default_timer()
	print("Tempo total: {}".format(fim - inicio))