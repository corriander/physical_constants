import unittest
import re
from codata.parser import Parser

class TestParser(unittest.TestCase):

	def setUp(self):
		versions = (2002, 2006, 2010)
		self.parsers = {
				version : Parser(version)
				for version in versions
				}
		self.re_unit = re.compile(
				 r"""
				 ( 						# BEGIN optional group
				 (ohm|GeV|mol|MeV|E_h|  # List of possible units
				 Hz|Wb|MHz|eV|A|C|C_90|
				 F|K|J|N|S|T|W|V|fm|c|
				 kg|sr|m|s|Pa|u|
				 \(GeV/c\^2\)|MeV/c)    #   Special cases
				 (\^-?\d+)?				# exponent (optional)
				 \s? 					# space (optional)
				 )*                     # END optional group
				 $						# End of string
				 """, re.VERBOSE)
		self.re_num = re.compile(
				r"""
				(-?(\d+[.\s]?)+(\.{3})?\s?(e-?\d+)?)
				|
				(\(exact\))
				""", re.VERBOSE)
	
	def test_parser_reads_all_records(self):
		# Dumb check to ensure parser reads from each version
		# properly.
		nrecords = {2002 : 309, 2006 : 326, 2010 : 335}
		for version, parser in self.parsers.items():
			returned_list = parser.read()
			self.assertTrue(len(returned_list), nrecords[version]) 
	
	def test_parser_records_match_regex(self):
		# Make sure the parser parses each table with no obvious 
		# errors (i.e. it splits each row into 4) and cols 2-4 match
		# the regex
		for version, parser in self.parsers.items():
			returned_list = parser.records
			for record in returned_list:
				self.assertTrue(len(record) == 4)
				self.assertTrue(self.re_unit.match(record.units))
				self.assertTrue(self.re_num.match(record.value))
				self.assertTrue(self.re_num.match(record.uncertainty))

if __name__ == '__main__':
	unittest.main()
