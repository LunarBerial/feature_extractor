import os

import sys
models=sys.argv[1]
models=models.split(',')
os.system("rm wav/*")


for model in models:
    if os.path.exists("wav"):
        os.system("rm -r wav")
        os.system("mkdir wav")
    else:
        os.system("mkdir wav")
    if os.path.exists(model):
        os.system("rm -r "+model)
    os.system("cp ../synth_1/"+model+"/*.cmp wav")
    os.system("python2 generate.py loop.conf jietong")
    print "mv wav "+model
    os.system("mv wav "+model)

