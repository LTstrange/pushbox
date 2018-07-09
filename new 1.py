#!/user/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'LTstrange'

import multiprocessing as mp
import time
import os

def info(title):
    print(title)
    print("module proces:",os.getppid())
    print("process id:",os.getpid())


def f(name):
    info('function f')
    print('hello',name)

if __name__ == '__main__':
    info('main line')
    p = mp.Process(target=f,args=('bob',))
    p.start()
    p.join()


