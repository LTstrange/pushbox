#!/user/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'LTstrange'

import multiprocessing as mp

q = mp.Queue()

q.put(12)
print(q.get())
q.put(12)
q = mp.Queue()

print(q.get(False))



