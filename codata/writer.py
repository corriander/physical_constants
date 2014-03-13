import csv
import os
import sys

def _file_object(path, opt='w'):
	# Fetch a file object
	if path is None:
		f = sys.stdout
	else:
		if os.path.isfile(path):
			raise IOError("{!s} exists".format(path))
		f = open(path, opt)
	return f

class Writer(object):
	"""Writer for the CODATA physical constants dataset."""

	supported_syntax = ('csv')

	def write(self, syntax, constants, path=None):
		"""Write constants in syntax to STDOUT or path if specified"""
		if syntax not in self.supported_syntax:
			raise ValueError("Unrecognised syntax")
		method = self.__getattribute__("_write_{!s}".format(syntax))
		method(constants, path)

	@staticmethod
	def _write_csv(constants, path):
		# Write dataset to a comma-separated-value format.
		f = _file_object(path, 'wb')
		with f:
			csv_writer = csv.writer(
					f,
					quoting=csv.QUOTE_NONNUMERIC
					)
			csv_writer.writerows(constants)
