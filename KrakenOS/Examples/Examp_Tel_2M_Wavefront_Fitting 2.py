# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Examp Tel 2M Wavefront Fitting"""

import os
import sys
import matplotlib.pyplot as plt
import numpy as np
import KrakenOS as Kos

# ______________________________________#

currentDirectory = os.getcwd()
sys.path.insert(1, currentDirectory + '/library')

# ______________________________________#

P_Obj = Kos.surf()
P_Obj.Rc = 0
P_Obj.Thickness = 1000 + 3.452200000000000E+003
P_Obj.Glass = "AIR"
P_Obj.Diameter = 1.059E+003 * 2.0

# ______________________________________#

Thickness = 3.452200000000000E+003
M1 = Kos.surf()
M1.Rc = -9.638000000004009E+003
M1.Thickness = -Thickness
M1.k = -1.077310000000000E+000
M1.Glass = "MIRROR"
M1.Diameter = 1.059E+003 * 2.0
M1.InDiameter = 250 * 2.0
M1.TiltY = 0.0
M1.TiltX = 0.0
M1.AxisMove = 0
# ______________________________________#

M2 = Kos.surf()
M2.Rc = -3.93E+003
M2.Thickness = Thickness + 1037.525880
M2.k = -4.328100000000000E+000
M2.Glass = "MIRROR"
M2.Diameter = 3.365E+002 * 2.0
M2.TiltY = 0.0
M2.TiltX = 0.0
M2.DespY = 0.0
""" Se inclina el secundario """
M2.DespX = 0.4
M2.AxisMove = 0

# ______________________________________#

P_Ima = Kos.surf()
P_Ima.Diameter = 300.0
P_Ima.Glass = "AIR"
P_Ima.Name = "Plano imagen"

# ______________________________________#

A = [P_Obj, M1, M2, P_Ima]
configuracion_1 = Kos.Setup()
Telescopio = Kos.system(A, configuracion_1)

# ______________________________________#
"""Vamos a definir los parámetros de la pupila del sistema,
definiremos esta pupila en la superficie 1, esta corresponde al
espejo primario"""
Surf = 1

"""Definimos la longitud de onda en micras"""
W = 0.5016
"""Dindicamos que la apertura del sistema definirá la pupila"""
AperType = "STOP"

""" Definimos el Diametro de la apertura del sistema"""
AperVal = 2000.
Pupil = Kos.PupilCalc(Telescopio, Surf, W, AperType, AperVal)

""" Para los calculos internos de la fase del frente de onda indicamos que
la pupila tendrá un arreglo exapolar con 10 anillos"""

Pupil.Samp = 10
Pupil.Ptype = "hexapolar"
"""Indicamos que los campos son tel tipo angulo, como en el caso de los telescopios
con luz desde el infinito, para diseños con objeto certano este parametro es la altura
 del objeto"""

Pupil.FieldType = "angle"
""" Definimos que el campo es 0 en x y cero en y, es decir, está en el eje óptico"""

Pupil.FieldY = 0.0
Pupil.FieldX = 0.0

""" Ahora calculamos la fase del frente de onda en la pupila, las coordenadas X, Y
son las coordendas en la pupila, el valor de Z es la fase en cada punto X, Y y P2V
es el valor pico a valle."""

X, Y, Z, P2V = Kos.Phase(Pupil)
print("Peak to valley: ", P2V)


"""Indicamos el grado de expanción para los polinomios de Zernike"""
NC = 38

"""Generamos un arreglo numpy conlas mismas dimensiones de la expanción definida"""
A = np.ones(NC)

"""Calculamos los polinomios de Zernike con la fase calculada y el numero de
 elementos deseados en la expanción, Zcoef son los coeficientes en longitudes de
 onda, Mat es la expreción matematica de Zeidel para dicho coeficiente,
 esto con fines ilustrativos, w_rms es el error del ajuste"""

Zcoef, Mat, w_rms = Kos.Zernike_Fitting(X, Y, Z, A)

""""Se despliegan los resultados"""
for i in range(0, NC):
    print("z", i + 1, "  ", "{0:.6f}".format(float(Zcoef[i])), ":", Mat[i])
# ______________________________________#


"""Se genera un contenedor de rayos"""

RR = Kos.raykeeper(Telescopio)

""" Se generan rayos que pasan por la pupila con la configuración realizada antes"""
x, y, z, L, M, N = Pupil.Pattern2Field()

# ______________________________________#

""" Se trazan esos rayos y se almacenan"""

for i in range(0, len(x)):
    pSource_0 = [x[i], y[i], z[i]]
    dCos = [L[i], M[i], N[i]]
    Telescopio.Trace(pSource_0, dCos, W)
    RR.push()

# ______________________________________#

""" Se grafica el telescopio con los rayos almacenados"""

Kos.display3d(Telescopio, RR, 2)
X, Y, Z, L, M, N = RR.pick(-1)

# ______________________________________#

""" Se grafica el diagrama de manchas """

plt.plot(X, Y, 'x')
plt.xlabel('numbers')
plt.ylabel('values')
plt.title('spot Diagram')
plt.axis('square')
plt.show()

""" Se prepara una imagen con los coeficientes de 400x400"""
ima = Kos.WavefrontData2Image(Zcoef, 400)



""" Se grafica el interferograma """
Type = "interferogram"
Kos.ZernikeDataImage2Plot(ima, Type)


""" Se calculan las sumas de Seidel """
AB = Kos.Seidel(Pupil)

print("--------------------------------------")
print(AB.SCW_AN)
print(AB.SCW_NM)
print(AB.SCW_TOTAL)
