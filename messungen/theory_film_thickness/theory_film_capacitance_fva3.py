"""
Calculate the theory capacitace based on the film thicknes
"""

import numpy as np
import matplotlib.pyplot as plt

def getCapacitance(a_hertz, e0, er, h0):
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

def onPick(event, fig, ax):
    """
    Print out the picked value
    """
    this_line = event.artist # get the picked line
    text = ax.texts[0] # get the text object in axis
    x_data = this_line.get_xdata() # get x datas from line
    y_data = this_line.get_ydata() # get y datas form line
    ind = event.ind # get index of the picked elements
    points = tuple(zip(x_data[ind], y_data[ind])) # zip picked points in tuple
    points = points[0] # get the first picked point
    tx = "film: %e\nc: %e" % points # build text
    text.set_text(tx)
    text.set_position(points) # location to draw text
    print("onpick points:", points)

    fig.canvas.draw_idle() # draw text

# calculate the Hertzschen contact
e_stahl = 210 * 1e9 # E-Modul Stahl [N/m^2]
e_glas = 70 * 1e9 # E-Modul Glas [N/m^2]
nu_stahl = 0.3 # Poissonzahl Stahl
nu_glas = 0.21 # Poissonzahl Glas
d_kugel = 19.05 * 1e-3 # Durchmesser Kugel [m]
r_kugel = d_kugel / 2 # Radius Kugel [m]
cos_psi = 0.0
beta_a = 1.0
beta_b = 1.0

# Test parameters
last = 20.0 # [N]

# Hauptkrümmungsradius [m]
r_kruemmung = r_kugel / 2

# reduzierter E-Modul [N/m^2]
e_reduz = 1 / ( 1/2 * ((1 - nu_stahl ** 2)/e_stahl + (1 - nu_glas ** 2)/e_glas))

# Halbachsen der Kontaktellipse [m]
a = beta_a * np.cbrt((3 * last * r_kruemmung) / e_reduz)
b = beta_b * np.cbrt((3 * last * r_kruemmung) / e_reduz)

# maximale Pressung [N/m^2]
p_0 = (3 * last) / (2 * np.pi * a * b)

# hertz contact area
a_hertz = np.pi * a * b # [m^2}

# films thicknes
films = np.arange(1, 601)
films = films * 1e-9 # [nm]

kc = 3.5 # factor to convert c_contact to c_hertz
epsilon_0 = 8.85e-15 # electric field constant [As/Vm]
epsilon_r = 2.06 # relative dielectric constant

# calculate the capacitace in ehl contact
caps = getCapacitance(a_hertz, epsilon_0, epsilon_r, films)
# calculate the measurement capacitace
caps = caps * kc

# setup the plot
fig, ax = plt.subplots()
ax.set_title("Theory capacitace over film thickness")
line, = ax.plot(films, caps, linewidth=0.5, picker=1) # 1 point tolerance
text = ax.text(0, 0, "")
ax.set_xlabel("Film [nm]")
ax.set_ylabel("Cap [F]")

fig.canvas.mpl_connect('pick_event', lambda event, fig=fig, ax=ax:
                       onPick(event, fig, ax))

plt.show()
