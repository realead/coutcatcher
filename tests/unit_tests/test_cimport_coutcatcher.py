import pyximport;
pyximport.install(setup_args = {"script_args" : ["--force"]},
                  language_level=3)

from cytest_cimport_coutcatcher import *
