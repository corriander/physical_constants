from collections import namedtuple

class PhysicalConstant(namedtuple('PhysicalConstant',
							  	  'name, value, uncertainty, units')):
	__slots__ = ()
	def toxml(self):
		s = ('<PhysicalConstant name="{}">'.format(self.name),
		     '    <value>{:g}</value>'.format(self.value),
			 '    <uncertainty>{:e}</uncertainty>'.format(
				 self.uncertainty),
			 '    <units>{}</units>'.format(self.units),
			 '</PhysicalConstant>',
			 ''
			 )

		return '\n'.join(s)

