Commit Entropy
==============

Commit Entropy is a tool that can be used to calculate the entropy of
changes in a source code repository. Entropy for code changes is a
measure of how specific each commit was in relation to the entire code
base. Very specific commits only affect a small set of files, and thus
have a low entropy. Commits that touch a large number of files are much
less specific and have a higher entropy as a result.

The term Entropy in this context is a simplified application of `Shannon
Entropy <https://en.wikipedia.org/wiki/Entropy_%28information_theory%29>`__
to commits in a source repository. It's simplified since we only look at
the number of files changed each commit, with each file having an equal
probability.

Installation
------------

Commit Entropy currently supports `Python
3.x <https://www.python.org/downloads/>`__. It can be installed using
`pip <https://pip.pypa.io/en/latest/>`__.

::

    pip install commit-entropy

This will install the ``commit-entropy`` executable on your path.

If you don't have pip, you can install it manually by cloning the code
and running the install script:

::

    git clone git@github.com:GripQA/commit-entropy.git
    cd commit-ntropy
    python setup.py install

Usage
-----

Currently we support a single operation: exporting a csv file with the
average entropy per day and a 30-day rolling average. From within a git
repo:

::

    commit-entropy csv

This will output a ``entropy.csv`` file in the current directory with
the average entropy values.

Support
-------

If you have any questions, problems, or suggestions, please submit an
`issue </GripQA/commit-entropy/issues>`__ or contact us at
support@grip.qa.
