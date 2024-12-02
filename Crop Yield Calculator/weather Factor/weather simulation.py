import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import expon
import pandas as pd

# historical data
data_clear = pd.read_csv('/Users/ll/Desktop/weather simulation programming/datasets/london_weather_clear.csv')
data_rain = pd.read_csv('/Users/ll/Desktop/weather simulation programming/datasets/london_weather_rain.csv')

solar_radiation_clear = data_clear['global_radiation']
solar_radiation_rain = data_rain['global_radiation']
temperature_clear = data_clear['mean_temp']
temperature_rain = data_rain['mean_temp']
wind_speed_clear = data_clear['wind_speed']
wind_speed_rain = data_rain['wind_speed']
rain_amount = data_rain['precipitation']

# Define mean vector and covariance matrix including wind speed (example values)
mean_vector_clear = [np.mean(temperature_clear),  np.mean(solar_radiation_clear), np.mean(wind_speed_clear)]
mean_vector_rain = [np.mean(temperature_rain),  np.mean(solar_radiation_rain), np.mean(wind_speed_rain)]
M_clear = np.vstack((temperature_clear,solar_radiation_clear,wind_speed_clear))
M_rain = np.vstack((temperature_rain,solar_radiation_rain,wind_speed_rain))

covariance_matrix_clear =np.cov(M_clear)
covariance_matrix_rain =np.cov(M_rain)


# Step 3: Generate temp, solar radiation, and wind speed
annual_temperature_vector = []
annual_wind_speed_vector = []
annual_solar_radiation_vector = []
annual_rain_day = []
annual_loss =[]

for j in range(100):
    solar_radiation_vector = []
    temperature_vector = []
    wind_speed_vector = []
    rain_day_total = 0
    for i in range(365):
        # Simulate rainfall occurrence
        rain_prob_today = 0.55  # Example probability for rainfall occurrence
        rain_day = np.random.binomial(1, rain_prob_today)

        if rain_day == 1:
            sample = np.random.multivariate_normal(mean_vector_rain, covariance_matrix_rain)
            simulated_temp, simulated_solar_radiation, simulated_wind_speed = sample
        else:
            sample = np.random.multivariate_normal(mean_vector_clear, covariance_matrix_clear)
            simulated_temp, simulated_solar_radiation, simulated_wind_speed = sample

        temperature_vector.append(simulated_temp)
        solar_radiation_vector.append(simulated_solar_radiation)
        wind_speed_vector.append(simulated_wind_speed)
        rain_day_total = rain_day_total + rain_day

    wind_speed_vector = np.array(wind_speed_vector)

    # Simulate rain amount
    rain_mean = np.mean(rain_amount)
    rain_std = np.std(rain_amount)
    eta = (rain_mean / rain_std) ** 2
    def gamma_pdf(x, eta):
        return x ** (eta - 1) * np.exp((eta - 1) * (1 - x))

    samples = []
    num_samples = rain_day
    lambda_prop = 1
    M = 2
    while len(samples) < num_samples:
        # sampling
        x = expon.rvs(scale=1 / 1)
        # pdf of objective distribution
        fx = gamma_pdf(x, eta)
        # pdf of proposition density
        gx = lambda_prop * np.exp(-lambda_prop * x)
        # accept/reject
        if np.random.uniform(0, 1) <= fx / (M * gx):
            samples.append(x)

    rain_samples = np.array(samples)
    rainfall_amount =rain_mean*rain_samples

    # severe weather
    threshold_1= 40
    threshold_2 = 34
    n1,n2 = 0,0
    n1 = np.sum(rainfall_amount>threshold_1)
    n2 = np.sum((rainfall_amount<threshold_1)&(rainfall_amount>threshold_2))


    threshold1 = 36
    threshold2 = 34
    m1 = np.sum(wind_speed_vector>threshold1)
    m2 = np.sum((wind_speed_vector<threshold1)&(wind_speed_vector>threshold2))

    loss = 0
    if n1 >0 or m1>0 :
        loss = 0.5
    elif n2>0 or m2>0:
        loss = 0.3
    else:
        loss =loss

    annual_temperature = np.mean(temperature_vector)
    annual_solar_radiation = np.mean(solar_radiation_vector)
    annual_wind_speed = np.mean(wind_speed_vector)

    annual_temperature_vector.append(annual_temperature)
    annual_wind_speed_vector.append(annual_wind_speed)
    annual_solar_radiation_vector.append(annual_solar_radiation)
    annual_rain_day.append(rain_day_total)
    annual_loss.append(loss)

data ={'solar_radiation':annual_solar_radiation_vector,'temperature':annual_temperature_vector,
       'wind speed':annual_wind_speed_vector,'rain_day':annual_rain_day,'loss':annual_loss}
df = pd.DataFrame(data =data)
file_path = '/Users/ll/Desktop/weather simulation/weather dataset/weather_simulation65.csv'
df.to_csv(file_path, index=False)


print('nwd=',annual_rain_day)
print('simulated temp',annual_temperature)
print('simulated solar radiation',annual_solar_radiation)
print('simulated wind speed',annual_wind_speed)
print('simulated extreme weather intensity', annual_loss)









