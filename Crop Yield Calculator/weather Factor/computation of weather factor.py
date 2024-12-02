import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter


#compute e_p0 using historical data
data= pd.read_csv('/Users/ll/Desktop/weather Factor/datasets/london_weather_rain.csv')
solar_radiation = np.array(data['global_radiation'])
temperature = data['mean_temp']
wind_speed = data['wind_speed']
median_vector = np.array([np.median(temperature),  np.median(solar_radiation), np.median(wind_speed)])
n_wet = 200
t = median_vector[0]
r = median_vector[1]
u = median_vector[2]

def evaporation(r,u,t,n):
    return (0.408*0.05*(r-20)+u*(900/(t+273))*2*(1-0.7*(n/(365-n))))/(0.05+0.06665*(1+u))

e0 = evaporation(r,u,t,n_wet) #value of e_p0

# Put the simulation results from csv file here
data_simulated = pd.read_csv('/Users/ll/Desktop/weather Factor/weather simulation Results_annual/weather_simulation_Guard Intercropping_year1.csv')
t = data_simulated['temperature']
r = data_simulated['solar_radiation']
u = data_simulated['wind speed']
n_rain = data_simulated['rain_day']

loss = data_simulated['loss']
coef_crop = 0.7 # guard 0.7,others 1
extreme_factor = (1-coef_crop*loss)

e_simulated = evaporation(r,u,t,n_rain)
e_simulated = e_simulated * (1-0.2) # evaporation inhibition other 0, guard 0.2
k = e_simulated/e0

evaporation_factor = k**(-1/2)
weather_factor = np.multiply(evaporation_factor,extreme_factor)

#take average value as the weather factor in calculator
weather_factor = np.where(np.isnan(weather_factor),np.nanmean(weather_factor),weather_factor)
counter = Counter(weather_factor)
N = 5
most_common = counter.most_common(N)
most_common_numbers = [num for num, freq in most_common]
average = sum(most_common_numbers)/len(most_common_numbers)
print('weather factor is',average)

#visualize the simulated results (sample size = 100)
plt.figure()
plt.hist(weather_factor,color = 'green')
plt.title('Weather Simulation',fontsize =20)
plt.xlabel('Level',fontsize =15)
plt.ylabel('frequency',fontsize =15)
plt.show()