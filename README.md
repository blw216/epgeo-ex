
# Developer Exercise

Please improve this stub project to calculate nearest neighbor values faster
than the naive example given in nearest_neighbor_index.py.

Nearest neighbor is a well studied problem and you should be able to find a
number of different approaches to solving this problem. We would like to see
approximately a 3-fold improvement in speed after you're done optimizing.

While in the "real world" we expect you will import scikit, numpy or similar to
index and query the data, we want to see how you code. So, please avoid using
any of these pre-canned solutions. That being said, be creative, there are many
ways to solve this problem.

The code here is for your convenience, but nothing here is sacred. Change the
interfaces, rename functions/files, link to code in another language, whatever.
Change as much or little as you like. That being said, your hypothetical end
user knowns Python so if your implementation is in COBOL, you should have a good
reason.

# Getting Started

From Linux or anaconda, using Python 3.6 or higher, do this to run the existing
unit tests:

```
python -m pip install .
python -m unittest
```

This should create a result similar to:

```
$ python -m unittest
.slow time: 2.40sec
new time: 2.33sec
speedup: 1.03x
.
----------------------------------------------------------------------
Ran 2 tests in 4.741s

OK
```

Note that the exact times may be different on your computer, we're just worried
about the speedup value.

# Tasks

## Improve the Index Performance

Your goal is to get the speedup value to about 3 or higher.

## Impress Us with Code

In addition to getting a speedup over the existing implementation, we will be
looking for the following in your code:

* Code clarity
* Code efficiency
* Test coverage
  - The existing test coverage is intentionally poor

## Document for the End User

Your end user is a data scientist that would like to take advantage of this
nearest neighbor implementation. Please create an example in 
`examples/simple_example.py` that explains how to use the code and improve the
comments in `pynn/nearest_neighbor_index.py` as reference documentation.

## Post your Code to GitHub

Create a repo and post your code and send us the URL. Please note the MIT
license. This code is yours, show it to your Aunt Hilda, use it in another
interview, whatever.
