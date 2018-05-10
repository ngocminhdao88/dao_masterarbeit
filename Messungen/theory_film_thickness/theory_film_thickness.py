# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt

pgf_with_latex = {                      # setup matplotlib to use latex for output# {{{
    "pgf.texsystem": "pdflatex",        # change this if using xetex or lautex
    "text.usetex": True,                # use LaTeX to write all text
    "font.family": "serif",
    "font.serif": [],                   # blank entries should cause plots 
    "font.sans-serif": [],              # to inherit fonts from the document
    "font.monospace": [],
    "axes.labelsize": 12,               # LaTeX default is 10pt font.
    "font.size": 12,
    "legend.fontsize": 10,               # Make the legend/label fonts 
    "xtick.labelsize": 10,               # a little smaller
    "ytick.labelsize": 10,
    "pgf.preamble": [
        r"\usepackage[utf8x]{inputenc}",    # use utf8 fonts 
        r"\usepackage[T1]{fontenc}",        # plots will be generated
        r"\usepackage[detect-all,locale=DE]{siunitx}",
        ]                                   # using this preamble
    }
# }}}

plt.rcParams.update(pgf_with_latex)

e_stahl = 208000 * 1e6 # E-Modul Stahl [N/m^2]
e_glas = 70000 * 1e6 # E-Modul Glas [N/m^2]
nu_stahl = 0.25 # Poissonzahl Stahl
nu_glas = 0.21 # Poissonzahl Glas
d_kugel = 19.05 * 1e-3 # Durchmesser Kugel [m]
r_kugel = d_kugel / 2 # Radius Kugel [m]

cos_psi = 0.0
beta_a = 1.0
beta_b = 1.0

# Test parameters
walz_geschw = np.array([0.1, 0.14, 0.273, 0.382, 0.749, 1.05, 1.47]) # Wälzgeschwindigkeit [m/s]
temperatur = np.array([40, 60, 80]) # Versuchstemperatur [C]
last = 20.0 # [N]

# Versuchsöl, FVA3 Daten
# FVA3 Dichte bei 40, 60 und 80 C [kg/m^3]
oil_dichte = np.array([865, 850, 837]) 
# FVA3 kinematische Viskosität bei 40, 60 und 80 C [m^2/s]
oil_ki_viskositaet = np.array([96, 38, 19]) * 1e-6 
# FVA3 dynamische Viskosität bei 40, 60 und 80 C [Ns/m^2]
oil_dyn_viskositaet = oil_dichte * oil_ki_viskositaet 
# FVA3 Viskosiät-Druck-Koeffizient bei 40, 60 und 80 C [m^2/N]
oil_alpha_p = np.array([1.95e-8, 1.72e-8, 1.59e-8])


# Hauptkrümmungsradius [m]
r_kruemmung = r_kugel / 2

# reduzierter E-Modul [N/m^2]
e_reduz = 1 / ( 1/2 * ((1 - nu_stahl ** 2)/e_stahl + (1 - nu_glas ** 2)/e_glas))

# Halbachsen der Kontaktellipse [m]
a = beta_a * np.cbrt((3 * last * r_kruemmung) / e_reduz)
b = beta_b * np.cbrt((3 * last * r_kruemmung) / e_reduz)

# maximale Pressung [N/m^2]
p_0 = (3 * last) / (2 * np.pi * a * b)

# Filmdicken nach Dowson und Hamrock
chi = a / b

# Berechnen der Schmierfilmdicke nach Dowson und Hamrock
for i, temp in enumerate(temperatur):
    fig = plt.figure(i, figsize=(12,8.5))
    ax = fig.add_subplot(111)
    ax.set_title(r'Temperatur ' + str(temp) + ' C')
    ax.set_xlabel(r'Geschwindigkeit [m/s]')
    ax.set_ylabel(r'Film [nm]')
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    films = np.array([])

    for geschw in walz_geschw:
        alpha_p = oil_alpha_p[i] # Druck-Viskos-Koeff
        eta_0 = oil_dyn_viskositaet[i] # dynamische Visko

        G = alpha_p * e_reduz # Werkstoffparam
        U = eta_0 * geschw / (e_reduz * r_kruemmung) # Geschw.param
        W = last / (e_reduz * r_kruemmung ** 2) # Belastungsparam
        H = 2.69 * (G ** 0.49) * (U ** 0.68) * \
            (1 - 0.61 * np.exp(-0.73 * chi)) / (W ** 0.067) # Schmierfilmdickesparam

        h_0 = H * r_kruemmung # zentrale Schmierfilmdicke

        films = np.append(films, h_0)
#        print('Geschw %.3f, Temp %.2f, Last %2.f: Schmierfilm %e' % \
#              (geschw, temp, last, h_0))

    films = films * 1e9 # Skaliert auf nm
    ax.plot(walz_geschw, films, 'ro', zorder=1)    
    ax.plot(walz_geschw, films, 'b-', zorder=2)
#    fig.savefig('theory_film_temperatur_' + str(temp) + '.png')

