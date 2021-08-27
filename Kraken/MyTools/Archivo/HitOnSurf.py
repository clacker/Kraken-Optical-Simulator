# -*- coding: utf-8 -*-
"""
Editor de Spyder

Este es un archivo temporal.
"""
import numpy as np
from .Surf_tools import surface_tools as SUT


class Hit_Solver:
    def __init__(self, SurfData):
        self.SDT = SurfData
        self.n = len(self.SDT)
        self.SuTo = SUT(SurfData)
        self.vj = 0
        self.vevaX = 0
        self.vevaY = 0

        self.NP_x1 = 0
        self.NP_y1 = 0
        self.NP_z1 = 0
        self.MN = 0
        self.LN = 0

        self.SuTo.ErrSurfCase = 0

    def __Fxyz(self, x, y, z):
        VF = self.SuTo.SurfaceShape(x, y, self.vj) - z
        return VF

    def SurfDer(self, x, y, z):
        delta = 0.0001  # Never chage from 0.00001

        vx = np.asarray([x + delta, x, x, x - delta, x, x])
        vy = np.asarray([y, y + delta, y, y, y - delta, y])
        vz = np.asarray([z, z, z + delta, z, z, z - delta])

        V = (self.__Fxyz(vx, vy, vz))

        Dx = (V[0] - V[3]) / (2.0 * delta)
        Dy = (V[1] - V[4]) / (2.0 * delta)
        Dz = (V[2] - V[5]) / (2.0 * delta)

        Dr = np.sqrt((Dx ** 2) + (Dy ** 2) + (Dz ** 2))
        return Dx / Dr, Dy / Dr, Dz / Dr

    def __lineCurve(self, vz):
        PX = ((vz - self.NP_z1) * self.LN) + self.NP_x1
        PY = ((vz - self.NP_z1) * self.MN) + self.NP_y1
        self.vevaX = PX
        self.vevaY = PY
        Vzf = self.SuTo.SurfaceShape(PX, PY, self.vj) - vz
        return Vzf

    def __DerLineCurve(self, gf):
        delta = 0.0000000000001  # Never chage from 0.0001 or 0.00001 or 0.0000000000001, jeje
        Dz = (self.__lineCurve(gf + delta) - self.__lineCurve(gf - delta)) / (2.0 * delta)

        return Dz

    def SolveHit(self, Px1, Py1, Pz1, L, M, N, j):

        if len(self.SDT[j].Error_map) != 0:
            self.SuTo.ErrSurfCase = 1
        if len(self.SDT[j].Error_map) == 0:
            self.SuTo.ErrSurfCase = 0

        self.vevaX = 0
        self.vevaY = 0
        self.vj = j
        cnt = 0
        PP_z2 = Pz1
        P_z2 = Pz1

        self.NP_x1 = Px1
        self.NP_y1 = Py1
        self.NP_z1 = Pz1
        self.MN = M / N
        self.LN = L / N

        while True:
            FdeX = self.__lineCurve(PP_z2)
            DerFdeX = self.__DerLineCurve(PP_z2)
            PP_z2 = PP_z2 - (FdeX / DerFdeX)

            if np.abs(PP_z2 - P_z2) < 0.00001:  # si la distancia entre raiz y funcion es de 0.001micras
                break
            else:
                # print(cnt)
                P_z2 = PP_z2

            if cnt == 30:
                break
            cnt = cnt + 1

        P_z2 = PP_z2
        P_x2 = ((P_z2 - self.NP_z1) * self.LN) + self.NP_x1
        P_y2 = ((P_z2 - self.NP_z1) * self.MN) + self.NP_y1

        self.SuTo.ErrSurfCase = 0

        if len(self.SDT[j].Error_map) != 0:
            PP_z2 = P_z2
            cnt = 0
            while True:
                FdeX = self.__lineCurve(PP_z2)
                DerFdeX = self.__DerLineCurve(PP_z2)
                PP_z2 = PP_z2 - (FdeX / DerFdeX)

                if np.abs(PP_z2 - P_z2) < 0.00001:  # si la distancia entre raiz y funcion es de 0.001micras
                    break
                else:
                    P_z2 = PP_z2

                if cnt == 3:
                    break
                cnt = cnt + 1

            P_z2 = PP_z2
            P_x2 = ((P_z2 - self.NP_z1) * self.LN) + self.NP_x1
            P_y2 = ((P_z2 - self.NP_z1) * self.MN) + self.NP_y1

        return P_x2, P_y2, P_z2
