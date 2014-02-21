import re
from collections import namedtuple

CODATARecord = namedtuple(
	'CODATARecord',
	'name, value, uncertainty, units'
	)

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

	@property
	def records(self):
		"""Table records as a list of CODATARecord named tuples.
		
		Simply splits each row by contiguous whitespace into fields
		and stores them as an immutable object. The records are
		composed of the original, unmodified strings.
		
		"""
		regex = re.compile(r'\s{2,}')    # Contiguous whitespace
		return map(CODATARecord._make, map(regex.split, self.read()))
