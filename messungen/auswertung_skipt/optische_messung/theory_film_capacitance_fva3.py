# -*- coding: utf-8 -*-
"""
Calculate the theory film thickness and
the theory capacitace in the ehl contact
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

#pgf_with_latex = {                      # setup matplotlib to use latex for output# {{{
#    "pgf.texsystem": "pdflatex",        # change this if using xetex or lautex
#    "text.usetex": True,                # use LaTeX to write all text
#    "font.family": "serif",
#    "font.serif": [],                   # blank entries should cause plots 
#    "font.sans-serif": [],              # to inherit fonts from the document
#    "font.monospace": [],
#    "axes.labelsize": 12,               # LaTeX default is 10pt font.
#    "font.size": 12,
#    "legend.fontsize": 10,               # Make the legend/label fonts 
#    "xtick.labelsize": 10,               # a little smaller
#    "ytick.labelsize": 10,
#    "pgf.preamble": [
#        r"\usepackage[utf8x]{inputenc}",    # use utf8 fonts 
#        r"\usepackage[T1]{fontenc}",        # plots will be generated
#        r"\usepackage[detect-all,locale=DE]{siunitx}",
#        ]                                   # using this preamble
#    }
## }}}
#
# plt.rcParams.update(pgf_with_latex) # update the setting for matplotlib


def getCapacitance(a_hertz, h0, e0=8.85e-15, er=2.07):
    """
    Calculate the capacitace in a ehl contact

    Input:
        a_hertz (float): ehl contact area
        e0 (float): electric field constant in vacum
        er (float): relativ dielectric field constant
        h (float): film thickness

    Output:
        c (float): capacitace of the ehl contact
    """
    return e0 * er * a_hertz / h0


def getSpeeds(start_speed, speed_step, number):
    """
    Create a array of speeds when using with the PCS test rig

    Input:
        start_speed (float) [m/s]: start speed at first test
        speed_step (float) [%]: a step to increase speed
        number (int): number of speed value

    Output:
        speeds (list): array of speeds
    """
    speeds = [start_speed]
    for i in range(1, number):
        temp = speeds[-1] * (100 + speed_step) / 100
        speeds.append(temp)

    return speeds


def getDensity(temp):
    """
    Calculate the density of SHC320 oil

    Input:
        temp (float): operating temperature [C]

    Output:
        density (float) of the SHC320 oil [kg/m^3]
    """

    temp_k = temp + 273.15  # temp [K]
    r_s = 1032.824951  # density [kg/m^3]
    als = 0.000575  # density temp coe [1/K]

    return r_s * (1 - als * temp_k)  # density [kg/m^3]


def getFilm(alpha_p,
            e_reduc,
            eta_0,
            speed,
            load,
            chi):
    """
    Calculate the film thickness using Hamrock and Dowson equation

    Input:
        alpha_p (float): pressure-viscosity coefficient
        e_reduc (float): reduced e modul
        eta_0 (float): dyn. viscosity at contact entrance
        speed (float): rolling velocity
        load (float): load apply on the ball to disc
        chi (float): ratio of contact ellipse radiuses

    Output:
        film (float): film thickness in ehl contact based on
        Hamrock and Dowson equation
    """

    G = alpha_p * e_reduz   # Werkstoffparam
    U = eta_0 * geschw / (e_reduz * r_kugel)    # Geschw.param
    W = last / (e_reduz * r_kugel ** 2)     # Belastungsparam
    H = 2.69 * (G ** 0.53) * (U ** 0.67) * \
        (1 - 0.61 * np.exp(-0.73 * chi)) / (W ** 0.067)  # Schmierfilmdickesparam

    h_0 = H * r_kugel  # zentrale Schmierfilmdicke

    return h_0


e_stahl = 210 * 1e9  # E-Modul Stahl [N/m^2]
e_glas = 70 * 1e9  # E-Modul Glas [N/m^2]
nu_stahl = 0.3  # Poissonzahl Stahl
nu_glas = 0.21  # Poissonzahl Glas
d_kugel = 19.05 * 1e-3  # Durchmesser Kugel [m]
r_kugel = d_kugel / 2  # Radius Kugel [m]

cos_psi = 0.0
beta_a = 1.0
beta_b = 1.0

# Test parameters
geschwindigkeiten = np.array(getSpeeds(0.01, 40, 20))  # Wälzgeschwindigkeit [m/s]
temperaturen = np.array([40, 60, 80])  # Versuchstemperatur [C]
lasten = np.array([20, 30, 40])  # Last [N]

# Hauptkrümmungsradius [m]
r_kruemmung = r_kugel / 2

# reduzierter E-Modul [N/m^2]
# stahl - glas
e_reduz = 1 / (1/2 * ((1 - nu_stahl ** 2)/e_stahl + (1 - nu_glas ** 2)/e_glas))
# stahl - stahl
# e_reduz = 1 / (1 / 2 * ((1 - nu_stahl ** 2) / e_stahl + (1 - nu_stahl ** 2) / e_stahl))

# Halbachsen der Kontaktellipse [m]
a = beta_a * np.cbrt((3 * lasten * r_kruemmung) / e_reduz)
b = beta_b * np.cbrt((3 * lasten * r_kruemmung) / e_reduz)

# Flächen der Ellipse [m^2]
a_hertz = np.pi * a * b

# maximale Pressung [N/m^2]
p_0 = (3 * lasten) / (2 * np.pi * a * b)

# print out the ehl contact information
for i, last in enumerate(lasten):
    print("EHL contact at %.2f N: a=%f m, b=%f m, p_0=%e N/m^2, A_hertz=%e m^2" %
          (last, a[i], b[i], p_0[i], a_hertz[i]))
    print("------------------------------------------------------------")

# Versuchsöl FVA3
# Dichte bei 40, 60 und 80 C [kg/m^3]
oil_dichte = np.array([865, 850, 837])
# kinematische Viskosität bei 40, 60 und 80 C [m^2/s]
oil_ki_viskositaet = np.array([96, 36, 18.5]) * 1e-6
# dynamische Viskosität bei 40, 60 und 80 C [Ns/m^2]
oil_dyn_viskositaet = oil_dichte * oil_ki_viskositaet
# Viskosiät-Druck-Koeffizient bei 40, 60 und 80 C [m^2/N]
oil_alpha_p = np.array([2.0e-8, 2.0e-8, 2.0e-8])

# Filmdicken nach Dowson und Hamrock
chi = 1  # a/b

# data frame to holds all the values
columns = ["Oil", "Temp", "Load", "Pressung", "Speed", "Film", "Cap"]
data = pd.DataFrame(columns=columns)

# Berechnen der Schmierfilmdicke nach Dowson und Hamrock
for geschw in geschwindigkeiten:
    for i, last in enumerate(lasten):
        for j, temp in enumerate(temperaturen):
            alpha_p = oil_alpha_p[j]    # Druck-Viskos-Koeff
            eta_0 = oil_dyn_viskositaet[j]  # dynamische Visko

            # calculate the film thickness in ehl contact
            h_0 = getFilm(alpha_p, e_reduz, eta_0, geschw, last, chi)

            cap = getCapacitance(a_hertz[i], h_0)   # capacitace in ehl contact

            pressung = p_0[i]   # hertzian stress

            # append data in to dataframe
            temp_data = ["FVA3", temp, last, pressung, geschw, h_0, cap]
            data.loc[len(data)] = temp_data

# export the data in csv file

# group data after temp and load
data_grouped = data.groupby(['Temp', 'Load'])

data_40C_20N = data.loc[(data["Temp"] == 40) & (data["Load"] == 20)]
data_60C_20N = data.loc[(data["Temp"] == 60) & (data["Load"] == 20)]
