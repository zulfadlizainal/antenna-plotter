#Created by github.com/zulfadlizainal

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

ant_df = pd.read_csv('AntPatternDB.csv', encoding='shift-jis')

# Create Indicators

split_H = ant_df['ANTENNA_ELEMENT'].str.split('V', expand=True)
split_V = split_H.iloc[:, 1].str.split('(', expand=True)
#split_E = split_V.iloc[:,1].str.split(')', expand = True)
HBeam = split_H.iloc[:, 0]
VBeam = 'V' + split_V.iloc[:, 0]
#ETilt = split_E.iloc[:,0]

# Create Info Table

cols = list(ant_df.columns)
ant_df_new = ant_df[[cols[0]] + [cols[2]] + [cols[1]] + [cols[5]] + [cols[4]]]
ant_df_new = pd.concat([ant_df_new, HBeam, VBeam], axis=1)
ant_df_new.columns = ['Antenna Name', 'Vendor',
                      'Gain (dBi)', 'Etilt (°)', 'Pattern', 'HBW', 'VBW']
cols = list(ant_df_new)
ant_df_new = ant_df_new[cols[0:4] + cols[5:7] + [cols[4]]]
ant_df_display = ant_df_new.loc[:, 'Antenna Name':'VBW']

print(' ')
print('### List of Antenna Pattern Database ###')
print(' ')

with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    print(ant_df_display)

print(' ')
print('### End of List ###')
print(' ')

#Select Antenna Pattern for display

select1 = int(input("Sector 1 Antenna Pattern: "))
select2 = int(input("Sector 2 Antenna Pattern: "))
select3 = int(input("Sector 3 Antenna Pattern: "))

azimuth1 = int(input("Sector 1 Azimuth (°): "))
azimuth2 = int(input("Sector 2 Azimuth (°): "))
azimuth3 = int(input("Sector 3 Azimuth (°): "))

#Prepare dataframe for selected antenna - Sec1

draw1 = ant_df_new.loc[select1,'Pattern']
draw1 = draw1.split(' ')
draw1 = pd.DataFrame(draw1)
draw1.drop(draw1.index[[0,1,2,3,724,725,726,727,1448,1449,1450]], inplace = True)
draw1 = draw1.reset_index(drop=True)

#Seperate Horizontal and Vertical DataFrame - Sec1

draw_H1 = draw1.iloc[0:720,:]
draw_H1 = draw_H1.reset_index(drop=True)

draw_H_Deg1 = draw_H1.iloc[::2] #Extract Odd Row Index DataFrame
draw_H_Deg1 = draw_H_Deg1.reset_index(drop=True)
draw_H_Loss1 = draw_H1.iloc[1::2] #Extract Even Row Index Dataframe
draw_H_Loss1 = draw_H_Loss1.reset_index(drop=True)

draw_df1 = pd.concat([draw_H_Deg1, draw_H_Loss1], axis = 1)
draw_df1.columns = ['Angle', 'H_Loss']
draw_df1['Angle'] = draw_df1['Angle'].astype(int)
draw_df1['H_Loss'] = draw_df1['H_Loss'].astype(float)
draw_df1['Radians'] = draw_df1['Angle']*np.pi/180

#Prepare dataframe for selected antenna - Sec2

draw2 = ant_df_new.loc[select2,'Pattern']
draw2 = draw2.split(' ')
draw2 = pd.DataFrame(draw2)
draw2.drop(draw2.index[[0,1,2,3,724,725,726,727,1448,1449,1450]], inplace = True)
draw2 = draw2.reset_index(drop=True)

#Seperate Horizontal and Vertical DataFrame - Sec2

draw_H2 = draw2.iloc[0:720,:]
draw_H2 = draw_H2.reset_index(drop=True)

draw_H_Deg2 = draw_H2.iloc[::2] #Extract Odd Row Index DataFrame
draw_H_Deg2 = draw_H_Deg2.reset_index(drop=True)
draw_H_Loss2 = draw_H2.iloc[1::2] #Extract Even Row Index Dataframe
draw_H_Loss2 = draw_H_Loss2.reset_index(drop=True)

draw_df2 = pd.concat([draw_H_Deg2, draw_H_Loss2], axis = 1)
draw_df2.columns = ['Angle', 'H_Loss']
draw_df2['Angle'] = draw_df2['Angle'].astype(int)
draw_df2['H_Loss'] = draw_df2['H_Loss'].astype(float)
draw_df2['Radians'] = draw_df2['Angle']*np.pi/180

#Prepare dataframe for selected antenna - Sec3

draw3 = ant_df_new.loc[select3,'Pattern']
draw3 = draw3.split(' ')
draw3 = pd.DataFrame(draw3)
draw3.drop(draw3.index[[0,1,2,3,724,725,726,727,1448,1449,1450]], inplace = True)
draw3 = draw3.reset_index(drop=True)

#Seperate Horizontal and Vertical DataFrame - Sec3

draw_H3 = draw3.iloc[0:720,:]
draw_H3 = draw_H3.reset_index(drop=True)

draw_H_Deg3 = draw_H3.iloc[::2] #Extract Odd Row Index DataFrame
draw_H_Deg3 = draw_H_Deg3.reset_index(drop=True)
draw_H_Loss3 = draw_H3.iloc[1::2] #Extract Even Row Index Dataframe
draw_H_Loss3 = draw_H_Loss3.reset_index(drop=True)

draw_df3 = pd.concat([draw_H_Deg3, draw_H_Loss3], axis = 1)
draw_df3.columns = ['Angle', 'H_Loss']
draw_df3['Angle'] = draw_df3['Angle'].astype(int)
draw_df3['H_Loss'] = draw_df3['H_Loss'].astype(float)
draw_df3['Radians'] = draw_df3['Angle']*np.pi/180

#Dataframe to List (All 3 Sectors)

plot_theta1 = draw_df1['Radians'].tolist()
plot_hloss1 = draw_df1['H_Loss'].tolist()

plot_theta2 = draw_df2['Radians'].tolist()
plot_hloss2 = draw_df2['H_Loss'].tolist()

plot_theta3 = draw_df3['Radians'].tolist()
plot_hloss3 = draw_df3['H_Loss'].tolist()


#Shift dataframe based on azimuth and tilt - Functions

def rotate(l, n):
    return l[-n:] + l[:-n]

#List to plot (All 3 Sectors)

plot_hloss1 = rotate(plot_hloss1, azimuth1)

plot_hloss2 = rotate(plot_hloss2, azimuth2)

plot_hloss3 = rotate(plot_hloss3, azimuth3)

#Plotting Antenna Pattern

#Sec 1
plt.figure()
h_ant1 = plt.subplot(1,1,1, projection='polar')
h_ant1.set_theta_direction(-1)           #Clockwise plot
h_ant1.plot(plot_theta1, plot_hloss1, color = 'r', label = 'Sec 1')
plt.title(f"3 Sector Antenna Pattern\n\n")
h_ant1.set_theta_zero_location("N")
h_ant1.set_ylim(50,0)

#Sec 2
h_ant2 = plt.subplot(1,1,1, projection='polar')
h_ant2.set_theta_direction(-1)           #Clockwise plot
h_ant2.plot(plot_theta2, plot_hloss2, color = 'y', label = 'Sec 2')
h_ant2.set_theta_zero_location("N")
h_ant2.set_ylim(50,0)

#Sec 3
h_ant3 = plt.subplot(1,1,1, projection='polar')
h_ant3.set_theta_direction(-1)           #Clockwise plot
h_ant3.plot(plot_theta3, plot_hloss3, color = 'g', label = 'Sec 3')
h_ant3.set_theta_zero_location("N")
h_ant3.set_ylim(50,0)

plt.xlabel(f"\n\nSec 1 Azimuth = {azimuth1}°\nSec 2 Azimuth = {azimuth2}°\nSec 3 Azimuth = {azimuth3}°")

plt.legend(fontsize = 'small' ,loc='upper center', bbox_to_anchor = (0.5, -0.1), ncol = 5, frameon = False)
plt.show()

print(' ')
print('ありがとうございました！！')
print('Download this program: https://github.com/zulfadlizainal')
print('Author: https://www.linkedin.com/in/zulfadlizainal')
print(' ')
