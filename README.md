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

TODO
----

This is going to start simple and be extended iteratively as and when
I find a personal need.

  - Subset categories.
  - Subset specification.
  - More data format choices.


