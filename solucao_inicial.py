class Solucao():
	def __init__(self, y, z, f):
		self.y = y
		self.z = z
		self.f = f

	def __str__(self):
		return "y={0}, z={1}, f={2:.3f}".format(self.y, self.z, self.f)
		