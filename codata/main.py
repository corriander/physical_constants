import sys 
from writer import Writer
from parser import Parser
from options import Options
from constant import PhysicalConstant
from collections import namedtuple
from collections import Sequence as SeqABC
from itertools import chain

class CODATA(dict):
	"""NIST CODATA physical constants with dict-like access"""

	def __init__(self, version=2010):
		self.parser = Parser(version)
		for constant in map(self._convert, self.parser.records):
			self[constant.name] = constant
		self.writer = Writer()

	@property
	def subset(self):
		"""Subset of physical constants"""
		return self._subset
	@subset.setter
	def subset(self, seq):
		if not isinstance(seq, SeqABC):
			raise ValueError("subset must be a sequence")
		for item in seq:
			if not isinstance(item, PhysicalConstant):
				raise ValueError("subset sequence must contain "
								 "objects exclusively of type "
								 "<codata.main.PhysicalConstant>")
		self._subset = seq

	def find_strings(self, strings):
		"""Constants with one of many specified strings in name"""
		matches = tuple(self._find_string(s) for s in strings)
		self.subset = tuple(set(chain.from_iterable(matches)))
	
	def _find_string(self, string):
		"""Constants with a specified string in name"""
		return tuple(obj 
					 for name, obj in self.items() 
					 if string in name
					 )
	
	def write(self, syntax):
		"""Write constants subset to STDOUT in syntax"""
		self.writer.write(syntax, self.subset)

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
	options = Options().parse(sys.argv[1:])
	c = CODATA(options.codataversion)
	if options.substrings:
		c.find_strings(options.substrings)
	else:
		c.subset = sorted(
				c.values(),
				key=lambda c: c.name.lower().replace('{', '')
				)
	c.write(options.format)
