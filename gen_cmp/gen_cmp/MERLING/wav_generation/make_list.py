import os

f = os.listdir ('./wav')

f = [item.split ('.')[0] for item in f if '.cmp' in item]

g = open ('list', 'w')

g.writelines ([item + '\n' for item in f])

g.close ()







