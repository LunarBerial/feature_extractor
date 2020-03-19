#coding:utf-8

import re, codecs

import multiprocessing
import time

def worker_1(rootpath):
    from extract_n import gen_cmp
    c = gen_cmp()
    c.get_normed_cmp(rootpath)


if __name__ == "__main__":
    root = '/home/mdisk/data/'
    roots = ['liangjiahe/wav_ns_ljh/out/', 'cartoonjing/wav_ns_cartoonjing/out/']
    p1 = multiprocessing.Process(target = worker_1, args = (root + roots[0],))
    p2 = multiprocessing.Process(target = worker_1, args = (root + roots[1],))
    #p3 = multiprocessing.Process(target = worker_1, args = (root + roots[2],))
    #p4 = multiprocessing.Process(target = worker_1, args = (root + roots[3],))


    p1.start()
    p2.start()
    #p3.start()
    #p4.start()
    print("The number of CPU is:" + str(multiprocessing.cpu_count()))
    for p in multiprocessing.active_children():
        print("child   p.name:" + p.name + "\tp.id" + str(p.pid))
