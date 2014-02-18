class Parser(object):
	"""Parse NIST CODATA ASCII table"""

	path = 'codata/data/2002CODATA.txt'

	def read(self):
		"""Return records from CODATA table as a list."""
		with open(self.path, 'r') as dat:
			in_table = False
			while not in_table:
				line = dat.readline()
				if line.startswith('-----'):
					in_table = True
			return dat.readlines()
