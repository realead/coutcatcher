# coutcatcher

Catches things printed to c-stdout/stderr and makes it available to python. Works on Linux,macOS and Windows. 

## Installation:

To install via `pip`, run:

    pip install https://github.com/realead/coutcatcher/zipball/master

It is possible to uninstall it afterwards via

   pip uninstall coutcatcher

You can also install using the `setup.py` file from the root directory of the project:

   python setup.py install

or 

   pip install .

For installation, a C-compiler is needed.


## Usage:

To catch output to C-stdout/stderr use:

    from coutcatcher import capture
    with capture() as c:
        # do here stuff which prints to c-stdout/stderr

    print("Printed to C-stdout:", c.cout)
    print("Printed to C-stderr:", c.cerr)


There is also a lazy variant:

    from coutcatcher import capture
    with capture(as_streams=True) as c:
        # do here stuff which prints to c-stdout/stderr

    print("Printed to C-stdout:", c.cout.read())  # data is read only now, cerr isn't read at all
    c.close()                                     # it is our responsibility to close streams now

Postponing reading of the data until it is really needed (if it is needed).

### IPython

Use following magic-command to redirect the output to notebook:

    %load_ext coutcatcher

to switch it off again:

   %unload_ext coutcatcher

## Testing for development:

For testing of the local version run:

    sh test_install.sh p3

in the `tests` subfolder.

For testing of the version from github run:

    sh test_install.sh p3 from-github

For keeping the the virtual enviroment after the tests:

    sh test_install.sh p3 local keep

Or 

    sh test_in_active_env.sh

to install and to test in the currently active environment.

## Trivia:

Inspired by:
  
  * `wurlitzer` (https://github.com/minrk/wurlitzer) which doesn't work for Windows.
  * this article (https://eli.thegreenplace.net/2015/redirecting-all-kinds-of-stdout-in-python/) of Eli Bendersky
  * this SO-question: https://stackoverflow.com/questions/63112945/c-extensions-how-to-redirect-printf-to-a-python-logger

## History

#### Release 1.0.1 (??.??.2020):
  
  * ToDo
    
