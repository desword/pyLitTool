from distutils.core import setup
import py2exe

#modify the input file name into your own python file.
setup(console=['delTab.py'])

#then run the following command.
#--python setup.py py2exe