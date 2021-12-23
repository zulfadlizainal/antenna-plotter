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

select = int(input("Antenna Pattern Number: "))
azimuth = int(input("Antenna Azimuth (°): "))
mtilt = int(input("Antenna Mechanical Tilt (°): "))

#Prepare dataframe for selected antenna

draw = ant_df_new.loc[select,'Pattern']
draw = draw.split(' ')
draw = pd.DataFrame(draw)
draw.drop(draw.index[[0,1,2,3,724,725,726,727,1448,1449,1450]], inplace = True)
draw = draw.reset_index(drop=True)

#Seperate Horizontal and Vertical DataFrame

draw_H = draw.iloc[0:720,:]
draw_H = draw_H.reset_index(drop=True)
draw_V = draw.iloc[720:1440,:]
draw_V = draw_V.reset_index(drop=True)

draw_H_Deg = draw_H.iloc[::2] #Extract Odd Row Index DataFrame
draw_H_Deg = draw_H_Deg.reset_index(drop=True)
draw_H_Loss = draw_H.iloc[1::2] #Extract Even Row Index Dataframe
draw_H_Loss = draw_H_Loss.reset_index(drop=True)

draw_V_Deg = draw_V.iloc[::2] #Extract Odd Row Index DataFrame
draw_V_Deg = draw_V_Deg.reset_index(drop=True)
draw_V_Loss = draw_V.iloc[1::2] #Extract Even Row Index Dataframe
draw_V_Loss = draw_V_Loss.reset_index(drop=True)

draw_df = pd.concat([draw_H_Deg, draw_H_Loss, draw_V_Loss], axis = 1)
draw_df.columns = ['Angle', 'H_Loss', 'V_Loss']
draw_df['Angle'] = draw_df['Angle'].astype(int)
draw_df['H_Loss'] = draw_df['H_Loss'].astype(float)
draw_df['V_Loss'] = draw_df['V_Loss'].astype(float)
draw_df['Radians'] = draw_df['Angle']*np.pi/180

#Extract ETilt Value

etilt = ant_df_new.loc[select, 'Etilt (°)']

#Dataframe to List

plot_theta = draw_df['Radians'].tolist()
plot_hloss = draw_df['H_Loss'].tolist()
plot_vloss = draw_df['V_Loss'].tolist()

#Shift dataframe based on azimuth and tilt

def rotate(l, n):
    return l[-n:] + l[:-n]

#List to plot

plot_hloss = rotate(plot_hloss, azimuth)
plot_vloss = rotate(plot_vloss, mtilt)

#Plotting Antenna Pattern

#Horizontal Antenna Pattern
plt.figure()
h_ant = plt.subplot(2,2,1, projection='polar')
h_ant.set_theta_direction(-1)           #Clockwise plot
h_ant.plot(plot_theta, plot_hloss)
plt.title("Horizontal Antenna Pattern\n   ")
h_ant.set_theta_zero_location("N")
h_ant.set_ylim(50,0)
plt.xlabel(f"Azimuth = {azimuth}°")

#Vertical Antenna Pattern
v_ant = plt.subplot(2,2,2, projection='polar')
v_ant.set_theta_direction(-1)           #Clockwise plot
v_ant.plot(plot_theta, plot_vloss)
plt.title("Vertical Antenna Pattern\n   ")
v_ant.set_theta_zero_location("E")
v_ant.set_ylim(50,0)
plt.xlabel(f"MTilt + ETilt = {mtilt+etilt}°")

plt.savefig('AntPat.png', dpi=300, bbox_inches='tight')
plt.show()

print(' ')
print('ありがとうございました！！')
print('Download this program: https://github.com/zulfadlizainal')
print('Author: https://www.linkedin.com/in/zulfadlizainal')
print(' ')
