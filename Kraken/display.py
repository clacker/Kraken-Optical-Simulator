# -*- coding: utf-8 -*-
"""
Created on Sun Feb 14 21:41:31 2021

@author: JOELHERRERAVAZQUEZ
"""
import numpy as np
import pyvista as pv
import matplotlib.pyplot as plt


def wavelength_to_rgb(wavelength, gamma=1.0):
    ##http://www.noah.org/wiki/Wavelength_to_RGB_in_Python
    """This converts a given wavelength of light to an
    approximate RGB color value. The wavelength must be given
    in nanometers in the range from 380 nm through 750 nm
    (789 THz through 400 THz).

    Based on code by Dan Bruton
    http://www.physics.sfasu.edu/astro/color/spectra.html
    """

    wavelength = float(wavelength)
    if 380 <= wavelength <= 440:
        attenuation = 0.3 + 0.7 * (wavelength - 380) / (440 - 380)
        R = ((-(wavelength - 440) / (440 - 380)) * attenuation) ** gamma
        G = 0.0
        B = (1.0 * attenuation) ** gamma
    elif 440 <= wavelength <= 490:
        R = 0.0
        G = ((wavelength - 440) / (490 - 440)) ** gamma
        B = 1.0
    elif 490 <= wavelength <= 510:
        R = 0.0
        G = 1.0
        B = (-(wavelength - 510) / (510 - 490)) ** gamma
    elif 510 <= wavelength <= 580:
        R = ((wavelength - 510) / (580 - 510)) ** gamma
        G = 1.0
        B = 0.0
    elif 580 <= wavelength <= 645:
        R = 1.0
        G = (-(wavelength - 645) / (645 - 580)) ** gamma
        B = 0.0
    elif 645 <= wavelength <= 750:
        attenuation = 0.3 + 0.7 * (750 - wavelength) / (750 - 645)
        R = (1.0 * attenuation) ** gamma
        G = 0.0
        B = 0.0
    else:
        R = 0.0
        G = 0.0
        B = 0.0
    R *= 255
    G *= 255
    B *= 255
    return [int(R) / 255.0, int(G) / 255.0, int(B) / 255.0]


def display3d(SYSTEM, RAYS, view=0):
    """display3d.

    :param SYSTEM:
    :param RAYS:
    :param view:
    """
    # System_stat_at_this_time=SYSTEM.prerequisites_status()
    # SEST=SYSTEM.System_stat-System_stat_at_this_time

    # if np.any(SEST!=0)==True:
    #     SYSTEM.System_stat=System_stat_at_this_time
    #     SYSTEM.non_secuential_status_change()

    p = pv.Plotter(shape=(1, 1), notebook=False)  # Con notebook=False se abre la ventana de ploter 3D
    # self.p.enable_eye_dome_lighting()
    # self.p.enable_depth_peeling(number_of_peels=0, occlusion_ratio=0.5)

    Absorb_color = np.array([10 / 256, 23 / 256, 24 / 256])
    Mirror_color = np.array([189 / 256, 189 / 256, 189 / 256])
    Glass_color = np.array([12 / 256, 238 / 256, 246 / 256])  # [0,2,3]

    recorte = view
    NN = SYSTEM.AAA.n_blocks
    if SYSTEM.SDT[0].Drawing == 0:
        points2 = np.c_[0, 0, 0]
        c = pv.PolyData(points2)
        cc = pv.PolyData(points2)

    if SYSTEM.SDT[0].Drawing == 1:
        c = SYSTEM.AAA[0]
        cc = SYSTEM.AAA[0]

    for n in range(1, NN):
        if SYSTEM.SDT[n].Drawing == 1:
            AAAA = SYSTEM.AAA[n]
            if SYSTEM.SDT[n].Glass != "NULL":
                if SYSTEM.SDT[n].Color == [0, 0, 0]:
                    if SYSTEM.SDT[n].Glass == "MIRROR":
                        color = Mirror_color
                    else:
                        color = Glass_color
                    if SYSTEM.SDT[n].Glass == "ABSORB":
                        color = Absorb_color
                else:
                    color = SYSTEM.SDT[n].Color

                cc = cc.merge(AAAA)

                if recorte == 1:
                    clippedx = AAAA.clip((1, 0, 0), invert=False)
                    clippedy = clippedx.clip((0, 1, 0), invert=False)
                    c = c.merge(clippedy)
                    clippedx = AAAA.clip((-1, 0, 0), invert=False)
                    clippedy = clippedx.clip((0, -1, 0), invert=False)
                    c = c.merge(clippedy)
                    clippedx = AAAA.clip((1, 0, 0), invert=False)
                    clippedy = clippedx.clip((0, -1, 0), invert=False)
                    c = c.merge(clippedy)
                if recorte == 0:
                    No_clipped = AAAA

                    c = c.merge(No_clipped)
                if recorte == 2:
                    clippedx = AAAA.clip((1, 0, 0), invert=False)
                    c = c.merge(clippedx)

                p.add_mesh(c, color, opacity=0.95, specular=1, specular_power=15, smooth_shading=True, show_edges=False)
                # p.add_mesh(c,color,opacity=0.85)

                edges = c.extract_feature_edges(boundary_edges=True,
                                                feature_edges=True,
                                                manifold_edges=False)

                p.add_mesh(edges, "red", )

                points2 = np.c_[0, 0, 0]
                c = pv.PolyData(points2)

    p.add_mesh(SYSTEM.DDD, color=[5, 5, 5], opacity=0.95, show_edges=None)

    NN = SYSTEM.AAA.n_blocks
    n = 0
    for g in SYSTEM.side_number:
        if SYSTEM.SDT[g].Drawing == 1:
            if SYSTEM.SDT[g].Color == [0, 0, 0]:
                if SYSTEM.SDT[g].Glass == "MIRROR":
                    LL_color = Mirror_color
                else:
                    LL_color = Glass_color

                if SYSTEM.SDT[g].Glass == "ABSORB":
                    LL_color = Absorb_color

                color = LL_color

            else:
                color = SYSTEM.SDT[g].Color

            if recorte == 1:
                clippedx = SYSTEM.BBB[n].clip('x', invert=False)
                p.add_mesh(clippedx, color, smooth_shading=True, show_edges=None)
                clippedy = SYSTEM.BBB[n].clip('-y', invert=False)
                p.add_mesh(clippedy, color, smooth_shading=True, show_edges=None)
            if recorte == 0:
                No_clipped = SYSTEM.BBB[n]
                p.add_mesh(No_clipped, color, smooth_shading=False, show_edges=None)

            if recorte == 2:
                BBBB = SYSTEM.BBB[n]
                clippedx = BBBB.clip((1, 0, 0), invert=False)
                p.add_mesh(clippedx, color, smooth_shading=True, show_edges=None)

        n = n + 1
    if len(RAYS.RayWave) != 0:
        RW = np.asarray(RAYS.RayWave)
        for i in range(0, np.shape(RW)[0]):
            RGB = wavelength_to_rgb(RW[i] * 1000.0)
            p.add_mesh(RAYS.CCC[i], color=RGB, opacity=0.95, smooth_shading=True, line_width=1.0, show_edges=None)

    p.add_axes()
    p.set_focus([0, 0, 0])  # Punto de enfoque de la camara
    p.set_position([-1000, 0, 0])  # Posicion de la camara
    p.set_viewup([0, 1, 0])
    p.enable_anti_aliasing()  # ERROR macos big sur
    p.disable_anti_aliasing()
    p.enable_eye_dome_lighting()  # ERROR macos big sur
    p.disable_eye_dome_lighting()
    p.set_background("white", top="royalblue")
    p.add_text("Kraken - Optical Simulator")
    p.show_grid(font_size=4)
    p.show(auto_close=False, interactive=True, interactive_update=False)
    #p.save_graphic('test.svg', raster=True)



def display2d(SYSTEM, RAYS, view=0):
    """display2d.

    :param SYSTEM:
    :param RAYS:
    :param view:
    """
    # System_stat_at_this_time=SYSTEM.prerequisites_status()
    # SEST=SYSTEM.System_stat-System_stat_at_this_time

    # if np.any(SEST!=0)==True:
    #     SYSTEM.System_stat=System_stat_at_this_time
    #     SYSTEM.non_secuential_status_change()

    plt.figure()

    plt.rcParams["font.family"] = "Times New Roman"

    L_color = [0, 2, 3]
    recorte = view
    NN = SYSTEM.AAA.n_blocks
    if SYSTEM.SDT[0].Drawing == 0:
        points2 = np.c_[0, 0, 0]
        c = pv.PolyData(points2)

    if SYSTEM.SDT[0].Drawing == 1:
        c = SYSTEM.AAA[0]

    for n in range(0, NN):
        if SYSTEM.SDT[n].Drawing == 1:
            AAAA = SYSTEM.AAA[n]
            if SYSTEM.SDT[n].Glass != "NULL":

                (PosX, PosY) = SYSTEM.SDT[n].Nm_Poss
                s = SYSTEM.SDT[n].Name
                ss = SYSTEM.Object_Num[n]

                if view == 0:
                    LT = ''
                    ax, ay, az = edge_3d(AAAA, 1, 0, 0)
                    az, ay = filter_face_2dplot(az, ay)
                    plt.plot(az, ay, LT, c="black", linewidth=0.5)

                    ax, ay, az = edge_3d(AAAA, -1, 0, 0)
                    az, ay = filter_face_2dplot(az, ay)
                    plt.plot(az, ay, LT, c="black", linewidth=0.5)

                    # plt.plot([az[0],az[-1]],[ay[0],ay[-1]],'-.',c="black",linewidth=0.5)

                    plt.text(np.max(az) + PosX + 1, np.max(ay) + PosY - 1, s, fontsize=7)
                    delta = (np.max(ay) - np.min(ay)) / 10
                    plt.text(az[np.argmin(ay * ay)], np.min(ay) - 1.5 * delta, "[" + str(ss) + "]", fontsize=7)
                    plt.plot([az[np.argmin(ay * ay)], az[np.argmin(ay * ay)]], [0, np.min(ay) - delta], '-.', c="red",
                             linewidth=0.5)

                    if PosX != 0 or PosY != 0:
                        plt.arrow(np.max(az) + PosX, np.max(ay) + PosY, -PosX, -PosY, head_width=0.5, head_length=1.0,
                                  fc='k', ec='k', length_includes_head=True)

                if view == 1:
                    LT = ''
                    ax, ay, az = edge_3d(AAAA, 0, 1, 0)
                    az, ax = filter_face_2dplot(az, ax)
                    plt.plot(az, ax, LT, c="black", linewidth=0.5)

                    ax, ay, az = edge_3d(AAAA, 0, -1, 0)
                    az, ax = filter_face_2dplot(az, ax)
                    plt.plot(az, ax, LT, c="black", linewidth=0.5)

                    # plt.plot([az[0],az[-1]],[ax[0],ax[-1]],'-.',c="black",linewidth=0.5)
                    delta = (np.max(ax) - np.min(ax)) / 20
                    plt.text(np.max(az) + PosX + 1, np.max(ax) + PosY - 1, s, fontsize=10)
                    plt.text(az[np.argmin(ax * ax)], np.min(ax) - 1.5 * delta, "[" + str(ss) + "]", fontsize=7)

                    plt.plot([az[np.argmin(ax * ax)], az[np.argmin(ax * ax)]], [0, np.min(ax) - delta], '-.', c="red",
                             linewidth=0.5)

                    if PosX != 0 or PosY != 0:
                        plt.arrow(np.max(az) + PosX, np.max(ax) + PosY, -PosX, -PosY, head_width=0.5, head_length=1.0,
                                  fc='k', ec='k', length_includes_head=True)

    # Ploting sides
    NN = SYSTEM.BBB.n_blocks
    for n in range(0, NN):
        TT = SYSTEM.BBB[n]

        sim = '-.'

        if view == 0:
            ax, ay, az = edge_3d(TT, 1, 0, 0)
            plt.plot(az, ay, sim, c="black", linewidth=0.5)

            ax, ay, az = edge_3d(AAAA, -1, 0, 0)
            plt.plot(az, ay, sim, c="black", linewidth=0.5)

        if view == 1:
            ax, ay, az = edge_3d(TT, 0, 1, 0)
            plt.plot(az, ax, sim, c="black", linewidth=0.5)

            ax, ay, az = edge_3d(AAAA, 0, -1, 0)
            plt.plot(az, ax, sim, c="black", linewidth=0.5)

    # Ploting rays

    if len(RAYS.RayWave) != 0:
        RW = np.asarray(RAYS.RayWave)
        for i in range(0, np.shape(RW)[0]):
            RGB = wavelength_to_rgb(RW[i] * 1000.0)
            RRR = RAYS.CCC[i]
            Ax = RRR.points[:, 0]
            Ay = RRR.points[:, 1]
            Az = RRR.points[:, 2]

            if view == 0:
                plt.plot(Az, Ay, color=RGB, linewidth=0.5)

            if view == 1:
                plt.plot(Az, Ax, color=RGB, linewidth=0.5)

    plt.title('System Plot')
    plt.xlabel('Z')
    if view == 0:
        plt.ylabel('Y')
    if view == 1:
        plt.ylabel('X')

    plt.axis('equal')
    plt.show()


def edge_3d(MeshObject, cx, cy, xz):
    """edge_3d.

    :param MeshObject:
    :param cx:
    :param cy:
    :param xz:
    """
    c = MeshObject.clip((cx, cy, xz), invert=False)
    edges = c.extract_feature_edges(boundary_edges=True, feature_edges=False, manifold_edges=False)

    Ax = edges.points[:, 0]
    Ay = edges.points[:, 1]
    Az = edges.points[:, 2]

    Ax = np.asarray(Ax)
    Ay = np.asarray(Ay)
    Az = np.asarray(Az)

    Xe = []
    Ye = []
    Ze = []

    if cx == 1:
        i = np.argmin(Ax)
    if cx == -1:
        i = np.argmax(Ax)
    if cy == 1:
        i = np.argmin(Ay)
    if cy == -1:
        i = np.argmax(Ay)

    x0 = Ax[i]
    y0 = Ay[i]
    z0 = Az[i]

    for j in range(0, np.shape(Ax)[0] - 1):
        AAx = Ax[i]
        AAy = Ay[i]
        AAz = Az[i]

        Xe.append(AAx)
        Ye.append(AAy)
        Ze.append(AAz)

        Ax = np.delete(Ax, i)
        Ay = np.delete(Ay, i)
        Az = np.delete(Az, i)

        X = Ax - AAx
        Y = Ay - AAy
        Z = Az - AAz
        R = np.sqrt((X * X) + (Y * Y) + (Z * Z))

        i = np.argmin(R)

    Xe.append(x0)
    Ye.append(y0)
    Ze.append(z0)

    Xe = np.asarray(Xe)
    Ye = np.asarray(Ye)
    Ze = np.asarray(Ze)
    return Xe, Ye, Ze


def filter_face_2dplot(v1, v2):
    """filter_face_2dplot.

    :param v1:
    :param v2:
    """
    av1 = np.copy(v1)
    av2 = np.copy(v2)
    av1 = np.roll(av1, -1)
    av2 = np.roll(av2, -1)
    yy = v1 - av1
    zz = v2 - av2
    R = np.sqrt((yy * yy) + (zz * zz))
    M = (np.mean(R))

    AW = np.argwhere(R < M)

    v1 = v1[AW]
    v2 = v2[AW]
    av1 = np.copy(v1)
    av2 = np.copy(v2)
    av1 = np.roll(av1, 1)
    av2 = np.roll(av2, 1)
    yy = v1 - av1
    zz = v2 - av2
    R = np.sqrt((yy * yy) + (zz * zz))
    AW = np.argmax(R)

    v1 = np.roll(v1, -AW)
    v2 = np.roll(v2, -AW)

    return v1, v2

##############################################################
