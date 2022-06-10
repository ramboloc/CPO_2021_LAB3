import os

print('transfer...')
for i in range(1, 12):
    command = 'dot pic%d.dot -T png -o pic%d.png' % (i, i)
    os.system(command)
