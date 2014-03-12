from writer import Writer
from parser import Parser
from collections import namedtuple

PhysicalConstant = namedtuple('PhysicalConstant',
							  'name, value, uncertainty, units')
class CODATA(object):
	"""Parse NIST CODATA ASCII table"""

	def __init__(self, version=2010):
		self.parser = Parser(version)
		self._constants = map(self._convert, self.parser.records)
		self.writer = Writer(self._constants)

	@property
	def constants(self):
		"""CODATA fundamental physical constants.

		CODATA internally recommended values of the fundamental
		physical constants represented as appropriate data types.
		Pretty-printed numerical strings have been turned into valid
		floats with non-numerical components removed/replaced.

		"""
		return self._constants

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

if __name__ == '__main__':
	codata = CODATA()
	print codata.constants
