import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#df_sweep = pd.read_csv('ladekurve_ebox.csv', names=['Hz', 'Cp', 'D'], skiprows=2)
df_einzeln = pd.read_csv('ladekurve_ebox_einzeln.csv', usecols=[0,1], names=['c', 'd'])

# remove the capacitance less than 0
df_einzeln_clean = df_einzeln.drop(df_einzeln[df_einzeln['c'] < 0].index)

# print out the average value of capacitance
c_mean = df_einzeln_clean['c'].mean()
print('C_mean = %e' % c_mean)

#plt.style.use('ggplot')
# You typically want your plot to be ~1.33x wider than tall. This plot is a rare    
# exception because of the number of lines being plotted on it.    
# Common sizes: (10, 7.5) and (12, 9)    
plt.figure(figsize=(10, 7.5))

# Remove the plot frame lines
ax = plt.subplot()
ax.spines["top"].set_visible(False)
#ax.spines["bottom"].set_visible(False)
ax.spines["right"].set_visible(False)
#ax.spines["left"].set_visible(False)


# Ensure that the axis ticks only show up on the bottom and left of the plot.    
ax.get_xaxis().tick_bottom()    
ax.get_yaxis().tick_left()

# Limit the range of the plot to only where the data is.    
# Avoid unnecessary whitespace.    
plt.ylim(6e-12, 11e-12)    
plt.xlim(0,166)

  
# Make sure your axis ticks are large enough to be easily read.    
#plt.yticks(range(0, 91, 10), [str(x) + "%" for x in range(0, 91, 10)], fontsize=14)
plt.yticks(fontsize=14)
plt.xticks(fontsize=14)  
      
plt.plot(df_einzeln_clean['c'])
plt.plot(y_smoothed)

