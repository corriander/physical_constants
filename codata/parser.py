import re

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
	
	def _parse_columns(self):
		# Split table into columns via regex
		regex = re.compile(r'\s{2,}')    # Contiguous whitespace
		l = []
		for row in self.read():
			l.append(tuple(regex.split(row)))
		return l    # List of tuples
