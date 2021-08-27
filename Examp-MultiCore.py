#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Examp Multicore"""

import multiprocessing
import time
import numpy as np
import Kraken as kn

#______________________________________#

start_time = time.time()

#______________________________________#

P_Obj = kn.surf()
P_Obj.Rc = 0.0
P_Obj.Thickness = 10
P_Obj.Glass = "AIR"
P_Obj.Diameter = 30.0

#______________________________________#

L1a = kn.surf()
L1a.Rc = 9.284706570002484E+001
L1a.Thickness = 6.0
L1a.Glass = "BK7"
L1a.Diameter = 30.0
L1a.Axicon = 0

#______________________________________#

L1b = kn.surf()
L1b.Rc = -3.071608670000159E+001
L1b.Thickness = 3.0
L1b.Glass = "F2"
L1b.Diameter = 30

#______________________________________#

L1c = kn.surf()
L1c.Rc = -7.819730726078505E+001
L1c.Thickness = 9.737604742910693E+001
L1c.Glass = "AIR"
L1c.Diameter = 30

#______________________________________#

P_Ima = kn.surf()
P_Ima.Rc = 0.0
P_Ima.Thickness = 0.0
P_Ima.Glass = "AIR"
P_Ima.Diameter = 3.0
P_Ima.Name = "Plano imagen"

#______________________________________#

A = [P_Obj, L1a, L1b, L1c, P_Ima]
config_1 = kn.Kraken_setup()

#______________________________________#

Doblete1 = kn.system(A, config_1)


#______________________________________#

def trax1(xyz, lmn, w, q):
    Rayos = kn.raykeeper(Doblete1)
    start_time = time.time()
    for i in range(0, 700):
        Doblete1.Trace(xyz, lmn, w)
        Rayos.push()
    A = Rayos.pick(-1)
    Rayos.clean()
    q.put(A[0])
    print("--- %s seconds ---" % (time.time() - start_time))

#______________________________________#

if __name__ == '__main__':
    start_time = time.time()
    pSource_0 = [1, 0, 0.0]
    dCos = [0.0, np.sin(np.deg2rad(0)), np.cos(np.deg2rad(0))]
    w = 0.5
    q = multiprocessing.Queue()
    p1 = multiprocessing.Process(target=trax1, args=(pSource_0, dCos, w + 0.1, q))
    p2 = multiprocessing.Process(target=trax1, args=(pSource_0, dCos, w + 0.2, q))
    p3 = multiprocessing.Process(target=trax1, args=(pSource_0, dCos, w + 0.3, q))
    p4 = multiprocessing.Process(target=trax1, args=(pSource_0, dCos, w + 0.4, q))
    p5 = multiprocessing.Process(target=trax1, args=(pSource_0, dCos, w + 0.5, q))
    p6 = multiprocessing.Process(target=trax1, args=(pSource_0, dCos, w + 0.6, q))
    p7 = multiprocessing.Process(target=trax1, args=(pSource_0, dCos, w + 0.7, q))
    p8 = multiprocessing.Process(target=trax1, args=(pSource_0, dCos, w + 0.8, q))
    p9 = multiprocessing.Process(target=trax1, args=(pSource_0, dCos, w + 0.1, q))
    p10 = multiprocessing.Process(target=trax1, args=(pSource_0, dCos, w + 0.2, q))

    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p5.start()
    p6.start()
    p7.start()
    p8.start()
    p9.start()
    p10.start()

    p1.join()
    p2.join()
    p3.join()
    p4.join()
    p5.join()
    p6.join()
    p7.join()
    p8.join()
    p9.join()
    p10.join()

    print(".................................................")
    print("Total time :")
    print("--- %s seconds ---" % (time.time() - start_time))

    print("Restart python kernel by hand because at this moment it is hang, it is inevitable until i know")

    # while q:
    for i in range(0,10):
        A = q.get()
        print(len(A))
