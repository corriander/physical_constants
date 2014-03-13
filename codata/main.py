from writer import Writer
from parser import Parser
from collections import namedtuple
from itertools import chain

PhysicalConstant = namedtuple('PhysicalConstant',
							  'name, value, uncertainty, units')
class CODATA(dict):
	"""NIST CODATA physical constants with dict-like access"""

	def __init__(self, version=2010):
		self.parser = Parser(version)
		self._list = map(self._convert, self.parser.records)
		for constant in self._list:
			self[constant.name] = constant
		# self.writer = Writer(self._constants)

	def find_strings(self, strings):
		"""Constants with one of many specified strings in name"""
		matches = tuple(self.find_string(s) for s in strings)
		return tuple(set(chain.from_iterable(matches)))
	
	def find_string(self, string):
		"""Constants with a specified string in name"""
		return tuple(obj 
					 for name, obj in self.items() 
					 if string in name
					 )
	
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
	for constant in sorted(
			codata.values(),
			key=lambda c: c.name.lower().replace('{', '')
			):
		print constant
