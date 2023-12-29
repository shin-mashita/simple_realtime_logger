import serial
import matplotlib.pyplot as plt 
import numpy as np
import datetime
import csv
import os

ser = serial.Serial(
    port='COM5',
    baudrate=115200,
)

logger_data = []

curr_gen_disp = []
curr_buck_disp = []
volt_gen_disp = []
volt_buck_disp = []
power_buck_disp = []
rpm_disp = []

time_vec = []

if not os.path.exists("./data.csv"):
    f = open("./data.csv", 'a',newline='')
    writer = csv.writer(f)
    fields = ["Time", "Generator output current", "Generator output voltage", "Buck output current", "Buck output voltage", "Buck output power","Generator RPM"]
    writer.writerow(fields)
else: 
    f = open("./data.csv", 'a',newline='')
    writer = csv.writer(f)

fig, axes = plt.subplots(nrows=2, ncols=3)

plt.sca(axes[0,0])
axes[0,0].set_ylim(-500, 3000)
plt.xticks(fontsize=8, rotation = 45)

plt.sca(axes[0,1])
axes[0,1].set_ylim(-5, 35)
plt.xticks(fontsize=8, rotation = 45)

plt.sca(axes[0,2])
axes[0,2].set_ylim(-500, 3000)
plt.xticks(fontsize=8, rotation = 45)

plt.sca(axes[1,0])
axes[1,0].set_ylim(-5, 25)
plt.xticks(fontsize=8, rotation = 45)

plt.sca(axes[1,1])
axes[1,1].set_ylim(0, 75000)
plt.xticks(fontsize=8, rotation = 45)

plt.sca(axes[1,2])
axes[1,2].set_ylim(0, 600)
plt.xticks(fontsize=8, rotation = 45)

while(True):
    start = ser.read(1)
    if(start == b'X'):
        s = ser.readline()
        s = s.decode()
        s = s.lstrip('X')
        s = s[0:s.find("O")]

        try:
            logger_data = [float(num) for num in s.split(",") if num != ''] # [curr_gen, volt_gen, curr_buck, volt_buck, power_buck, rpm_gen]
        except ValueError:
            continue

        if(len(logger_data) == 6):
            time = datetime.datetime.now()
            writer.writerow([time] + logger_data)
            curr_gen_disp.append(logger_data[0])
            volt_gen_disp.append(logger_data[1])
            curr_buck_disp.append(logger_data[2])
            volt_buck_disp.append(logger_data[3])
            power_buck_disp.append(logger_data[4])
            rpm_disp.append(logger_data[5])
            time_vec.append(time)

            if(len(curr_gen_disp) > 50):
                curr_gen_disp.pop(0)
                volt_gen_disp.pop(0)
                curr_buck_disp.pop(0)
                volt_buck_disp.pop(0)
                power_buck_disp.pop(0)
                rpm_disp.pop(0)
                time_vec.pop(0)
            
            plt.subplot(2,3,1)
            plt.plot(time_vec, curr_gen_disp, color = "red")
            plt.subplot(2,3,2)
            plt.plot(time_vec, volt_gen_disp, color = "blue")
            plt.subplot(2,3,3)
            plt.plot(time_vec, curr_buck_disp, color = "green")
            plt.subplot(2,3,4)
            plt.plot(time_vec, volt_buck_disp, color = "violet")
            plt.subplot(2,3,5)
            plt.plot(time_vec, power_buck_disp, color = "orange")
            plt.subplot(2,3,6)
            plt.plot(time_vec, rpm_disp, color = "black")
            plt.pause(0.05)
        
            # print(logger_data[4])

