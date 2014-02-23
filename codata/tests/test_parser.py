import unittest
from codata.parser import Parser

class TestParser(unittest.TestCase):

	def setUp(self):
		versions = (2002, 2006, 2010)
		self.parsers = {
				version : Parser(version)
				for version in versions
				}
		regex_units = { 'start' : re.compile('[a-zA-Z()]') }
		regex_uncer = { 'start' : re.compile('0\.\d|\(exact\)') }
		regex_num = { 'full' : re.compile(
							'[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?'
							) }
		self.regex = {
				'units' : regex_units,
				'uncertainty' : regex_uncer,
				'value' : regex_num
				}
	
	def test_parser_read(self):
		# Dumb check to ensure parser reads from each version
		# properly.
		nrecords = {2002 : 309, 2006 : 326, 2010 : 335}
		for version, parser in self.parsers.items():
			returned_list = parser.read()
			self.assertIsInstance(returned_list, list)
			self.assertTrue(len(returned_list), nrecords[version]) 
	
	def test_parser_records(self):
		# Make sure the parser parses each table with no obvious 
		# errors (i.e. it splits each row into 4) and cols 2-4 match
		# the regex
		re_unit = re.compile(
				r'((ohm|GeV|mol|MeV|E_h|Hz|Wb|MHz|eV|A|C|'
		         'C_90|F|K|J|N|S|T|W|V|fm|c|kg|sr|m|s|Pa|u)'
				 '( |^-?\d+)*)*$'
				 )
		re_num = re.compile(r'-?(\d+[. ]?)+(\.{3})? ?(e-?\d+)?')
		for version, parser in self.parsers.items():
			returned_list = parser.parse()
			self.assertIsInstance(returned_dict, list)
			for record in returned_list:
				self.assertTrue(len(record) == 4)
				self.assertTrue(re_unit.match(record.units))
				self.assertTrue(re_num.match(record.value))
				self.assertTrue(re_num.match(record.uncertainty))
