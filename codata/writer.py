import csv
import os
from codata.parser import Parser

class Writer(object):
	"""Writer for the CODATA physical constants dataset."""
	def __init__(self, version=2010):
		self.parser = Parser(version)
	
	def write_csv(self, path):
		"""Write dataset to a comma-separated-value data file."""
		if os.path.isfile(path):
			raise IOError("File exists")
		with open(path, 'wb') as csvfile:
			csv_writer = csv.writer(
					csvfile,
					quoting=csv.QUOTE_NONNUMERIC
					)
			csv_writer.writerows(self.parser.constants)
