# -*- coding: utf-8 -*-
"""
Created on Sat Jun 26 04:36:32 2021

@author: cptw
"""
# -*- coding: UTF-8 -*-

import os

print('transfer...')
for i in range(1, 12):
    command = 'dot pic%d.dot -T png -o pic%d.png' % (i, i)
    os.system(command)
