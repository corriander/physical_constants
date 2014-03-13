import re
import os
from collections import namedtuple
from constant import PhysicalConstant 

Record = namedtuple('CODATARecord', PhysicalConstant._fields)

class Parser(object):
	"""Parse NIST CODATA ASCII table"""

	def __init__(self, version=2010):
		self.path = 'codata/data/%sCODATA.txt' % version
		if not os.path.isfile(self.path): 
			raise ValueError(
				"%s is not a recognised CODATA version." % version)

	def read(self):
		"""Return records from CODATA table as a list."""
		with open(self.path, 'r') as dat:
			in_table = False
			while not in_table:
				line = dat.readline()
				if line.startswith('-----'):
					in_table = True
			return [line.rstrip('\n') for line in dat.readlines()]

	@property
	def records(self):
		"""Table records as a list of CODATARecord named tuples.
		
		Simply splits each row by contiguous whitespace into fields
		and stores them as an immutable object. The records are
		composed of the original, unmodified strings.
		
		"""
		regex = re.compile(r'\s{2,}')    # Contiguous whitespace
		return map(Record._make, map(regex.split, self.read()))
