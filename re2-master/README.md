**Brief introduction below, unfortunately there're wrongs within the code files, that make compilling and testing failed, which I'm currently working on.**
**Aaron Chung**
___
This is the source code repository for RE2, a regular expression library. I modified it for building static DFA and dynamic DFAs.
getDFA.ccp can accept one argument for Static DFA or two arguments for Dynamic DFA.
To compile getDFA use the following command:
g++ -v getDFA.cpp -g -o getDFA -std=c++11 -pthread -I/home/peipei/re2/ -I/usr/local/include -O3 -L/home/peipei/re2/obj -Lre2

For documentation about how to install and use RE2,
visit https://github.com/google/re2/.

The short version is:

make
make test
make install
make testinstall

There is a fair amount of documentation (including code snippets) in
the re2.h header file.

More information can be found on the wiki:
https://github.com/google/re2/wiki

Issue tracker:
https://github.com/google/re2/issues

Mailing list:
https://groups.google.com/group/re2-dev

Unless otherwise noted, the RE2 source files are distributed
under the BSD-style license found in the LICENSE file.

RE2's native language is C++.

A C wrapper is at https://github.com/marcomaggi/cre2/.
An Erlang wrapper is at https://github.com/tuncer/re2/.
An Inferno wrapper is at https://github.com/powerman/inferno-re2/.
A Node.js wrapper is at https://github.com/uhop/node-re2/ and on NPM.
An OCaml wrapper is at https://github.com/janestreet/re2/ and on OPAM.
A Perl wrapper is at https://github.com/dgl/re-engine-RE2/ and on CPAN.
A Python wrapper is at https://github.com/facebook/pyre2/.
An R wrapper is at https://github.com/qinwf/re2r/.
A Ruby wrapper is at https://github.com/mudge/re2/.
