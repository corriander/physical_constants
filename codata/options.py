from argparse import ArgumentParser

class Options(object):
	"""CLI argument processor"""
	def __init__(self):
		desc=('Parse the NIST CODATA database of '
			  'fundamental physical constants')
		self.argparser = ArgumentParser(prog='codata',
							            description=desc)
		self.argparser.add_argument('-f',
									'--format',
									default='csv',
									dest='format',
									help='Output format/syntax')
		self.argparser.add_argument('-s',
									'--search',
									default=None,
									dest='substrings',
									nargs='*',
									help='Search strings')

	def parse(self, args=None):
		"""Parse the CLI options"""
		return self.argparser.parse_args(args)
