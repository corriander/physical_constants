import csv
import os
import sys
from xml.etree import ElementTree as etree

def _file_object(path, opt='w'):
	# Fetch a file object
	if path is None:
		f = sys.stdout
	else:
		if os.path.isfile(path):
			raise IOError("{!s} exists".format(path))
		f = open(path, opt)
	return f

def _indentxml(elem, level=0):
	# Indent XML string representation of elements;
	# http://effbot.org/zone/element-lib.htm#prettyprint
	indent = "    "
	i = "\n" +level*indent
	if len(elem):
		if not elem.text or not elem.text.strip():
			elem.text = i + indent
		if not elem.tail or not elem.tail.strip():
			elem.tail = i
		for elem in elem:
			_indentxml(elem, level+1)
		if not elem.tail or not elem.tail.strip():
			elem.tail = i
	else:
		if level and (not elem.tail or not elem.tail.strip()):
			elem.tail = i

class Writer(object):
	"""Writer for the CODATA physical constants dataset."""

	supported_syntax = ('csv', 'xml', 'xmle')

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

	@staticmethod
	def _write_xml(constants, path):
		# Write dataset to xml format.
		f = _file_object(path)
		root = etree.Element('PhysicalConstantSet')
		for constant in constants:
			croot = etree.SubElement(root, 
									 'PhysicalConstant',
									 attrib={'name' : constant.name})
			for attr in constant._fields[1:]:
				element = etree.SubElement(croot, attr)
				element.text = str(getattr(constant, attr))
		_indentxml(root)
		with f:
			etree.ElementTree(root).write(f,
										  xml_declaration=True,
										  encoding='utf-8',
										  method='xml')
	
	@staticmethod
	def _write_xmle(constants, path):
		# Write dataset as XML elements sequence (no root/declaration)
		f = _file_object(path, 'w+')
		with f:	map(lambda c: f.write(c.toxml()), constants)
