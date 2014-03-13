Physical Constants
==================

A language-independent, customisable library of fundamental physical
constants sourced from [NIST](http://physics.nist.gov/cuu/Constants/).

This is a little bit wheel-reinventy, there are libraries/packages out
there that process the very same data I'm going to. However, one
reason I wish to do this is to de-couple physical constants data from
both specific languages *and* specific software modules dealing with
other operations (such as units of measure and quantities). Aside from
the obvious portability, one benefit of this is to allow tighter
control over what is ultimately an input dataset within a given 
project:

  - *If* the dataset changes (improved accuracy, updated standard
	values, bug fixes etc.) this is a change occurring under the
	auspice of the project and its revision control system, not in the
	background.
  - It may be desirable to maintain references to a specific dataset
    in a revision-controlled codebase, something less easy to do if
	the dataset is managed as an external package.

Dependencies
------------

None, standard library only.

Usage
-----

The following assuumes `bin/codata` is in the system `PATH`.

The utility currently writes to `STDOUT`, so for now it's for use with
pipes and redirection:

	codata > /path/to/output/file

Search constants database for substrings. This is not intelligent, so
if you want a specific constant it's best to make sure the substring
is unique to it via quotation (note the usual shell behaviour of
unpreserved spaces, so if the substring has spaces, it requires
quote-delimiting).

	codata -s light standard 'molar mass constant'

Different output formats can be selected, currently CSV and XML:

	codata -f xml 'standard-state pressure'
	codata -f csv 'standard-state pressure'

CSV is the default at the moment, but will be replaced by a plain text
representation at Some Point(tm). The XML is rough and ready but
should be enough for now.

TODO
----

This is going to start simple and be extended incrementally as and
when I find a personal need.

  - Subset categories.
  - Subset specification.
  - More data format choices.


