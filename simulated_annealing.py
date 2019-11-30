from leitor import Instancia
from fabrica import FabricaSolucao
from vizinhanca import Vizinhanca
from random import random
from math import exp
import sys
import time
import os
import numpy as np

class SimulatedAnnealing():

	def __init__(self, fabrica, vizinhanca):
		self.fabrica = fabrica
		self.vizinhanca = vizinhanca


	def executar(self, alpha, temperatura_inicial, temperatura_final, s_max, tipo):
		
		s = self.fabrica.produzir_solucao() if tipo == 'Aleatório' else self.fabrica.wj()
		s_melhor = s
		t = temperatura_inicial

		#print("Solução inicial: {}".format(s))
		
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

		#print("Melhor solução encontrada: {}".format(s_melhor))
		return s_melhor

def executarTestes(resultados, tipo, arquivos):
	resultados.write('\n\n############################' + tipo + '############################\n\n')
	for arq in arquivos:
		instancia = Instancia.ler_arquivo(arq)
		fabrica = FabricaSolucao(instancia)
		vizinhanca = Vizinhanca(instancia)
		simulated_annealing = SimulatedAnnealing(fabrica, vizinhanca)
		alpha = 0.9
		temperatura_inicial = (instancia.n * 2) #// 2 #1000
		temperatura_final = 0.001 #0.0001
		s_max = (instancia.n * 2) #// 2 #1000
		custo = np.array([])
		tempo = np.array([])
		for _ in range(5):
			start = time.time()
			custo = np.append(custo, simulated_annealing.executar(alpha, temperatura_inicial, temperatura_final, s_max, tipo).f)
			tempo = np.append(tempo, time.time() - start)
		resultados.write("{0}\t{1:.2f}\t\t{2:.3f}\t{3:.3f}\t\t{4:.3f}\t{5:.3f}\n".
			format(arq.split('/')[2], np.max(custo), np.average(custo), np.std(custo), np.average(tempo), np.std(tempo)))

if __name__ == '__main__':
	caminho = 'mdgplib/'
	arquivos = []
	for r, d, f in os.walk(caminho):
		for file in f:
			if 'resultados_heuristica.txt' != file and any(i in file for i in ['120', '240', '480', '960']):
				arquivos.append(os.path.join(r, file))
	arquivos.sort()
	resultados = open('resultados_heuristica_simples.txt', 'w')
	resultados.write('Instância\tmelhor custo\tmédia custo\t\tstd custo\tmédia tempo\t\tstd tempo\n')
	executarTestes(resultados, 'Aleatório', arquivos)
	print('Acabou o aleatório')
	#executarTestes(resultados, 'GRASP', arquivos)
	#print('Acabou o GRASP')
	executarTestes(resultados, 'WJ', arquivos)
	print('Acabou o WJ');
	resultados.close()