import re
import os
import sys

inputfile = sys.argv[1]
f = open(inputfile, 'r')
all_text = f.read()
open(sys.argv[1],'w').write(re.sub('\t', '    ', all_text))

