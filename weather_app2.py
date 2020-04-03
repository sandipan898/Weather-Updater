import tkinter as tk
import requests
import json

root = tk.Tk()
root.title("Weather Forecast")
root.geometry("700x300")
root.configure(background = 'light green')

# http://dataservice.accuweather.com/forecasts/v1/daily/1day/191578?apikey=CFfODWB5pWrrIs0uMBjhGeP5uunW09D9&language=en-us&details=false&metric=false

response = requests.get("http://dataservice.accuweather.com/forecasts/v1/daily/1day/191578?apikey=CFfODWB5pWrrIs0uMBjhGeP5uunW09D9&language=en-us&details=false&metric=false")
info = json.loads(response.content)
# print(info)
"""
with open("acuuweather_info_local_forecast.txt", "w") as f:
    f.write(str(info))
    f.close()
"""

info_headLine = info['Headline']
info_DailyForecasts = info['DailyForecasts']
Text = info_headLine['Text']
category = info_headLine['Category']
temperature = info_DailyForecasts[0]['Temperature']
min_temp = temperature['Minimum']['Value']
max_temp = temperature['Maximum']['Value']
day_info = info_DailyForecasts[0]['Day']
night_info = info_DailyForecasts[0]['Night']


def rain_sts_checker():

    if info_DailyForecasts[0]['Day']['HasPrecipitation']:
        return "In Day: " + info_DailyForecasts[0]['Day']['PrecipitationType']

    if info_DailyForecasts[0]['Night']['HasPrecipitation']:
        return "In night : " + info_DailyForecasts[0]['Night']['PrecipitationType']


try:
    temp_label = tk.Label(root, background = "light green", font = ("Helvetica", 10, "bold"), text = "Temnpreature\n" + "Minimum : " + str(min_temp) + " F" + "   ||   " + "Maximum : " + str(max_temp) + " F")
    temp_label.pack(pady = 10)

    d_n_sts_label = tk.Label(root, background = "light green", font = ("Helvetica", 10, "bold"), text = "Day : " + day_info['IconPhrase'] + "\n\n" + "Night : " + night_info['IconPhrase'])
    d_n_sts_label.pack(pady = 10)

    rain_sts_label = tk.Label(root, background = "light green", font = ("Helvetica", 10, "bold"), text = "Rain status" + " \n" + rain_sts_checker())
    rain_sts_label.pack()

    status_label = tk.Label(root, background = "light green", font = ("Helvetica", 10, "bold"), text = "Status : " + Text + "\n\n" + "Type: " + category)
    status_label.pack(pady = 10)
except Exception as e:
    error_lable = tk.Label(root, text = "Error!!!")
    error_lable.pack()

root.mainloop()
