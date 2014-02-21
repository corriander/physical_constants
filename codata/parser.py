import re
from collections import namedtuple

Record = namedtuple('CODATARecord', 'name, value, uncertainty, units')
PhysicalConstant = namedtuple('PhysicalConstant', Record._fields)

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
		return map(Record._make, map(regex.split, self.read()))

	@property
	def constants(self):
		"""CODATA fundamental physical constants.

		CODATA internally recommended values of the fundamental
		physical constants represented as appropriate data types.
		Pretty-printed numerical strings have been turned into valid
		floats with non-numerical components removed/replaced.

		"""
		return map(self._convert, self.records)

	@staticmethod
	def _convert(record):
		# Convert Record --> PhysicalConstant.
		#
		# Performs some string substitutions and changes type.
		kwargs = {
			'name' : record.name,
			# Value strings have inter-digit spacing and ellipses in
			# the case of irrational numbers.
			'value' : float(record.value.replace(' ', '').\
					replace('...', '')),
			# Uncertainties have inter-digit spacing and exact values
			# are denoted by (exact), this can be changed to 0
			'uncertainty' : float(record.uncertainty.replace(' ', '').\
					replace('(exact)', '0')),
			'units' : record.units
			}

		return PhysicalConstant(**kwargs)
