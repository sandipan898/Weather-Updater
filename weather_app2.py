import tkinter as tk
import requests
import json
import textwrap as tw

root = tk.Tk()
root.title("Weather Forecast")
root.geometry("620x250+720+70")
root.configure(background = 'light green')

# http://dataservice.accuweather.com/forecasts/v1/daily/1day/191578?apikey=CFfODWB5pWrrIs0uMBjhGeP5uunW09D9&language=en-us&details=false&metric=false


# get the response by request
response = requests.get("http://dataservice.accuweather.com/forecasts/v1/daily/1day/191578?apikey=CFfODWB5pWrrIs0uMBjhGeP5uunW09D9&language=en-us&details=false&metric=false")
info = json.loads(response.content)

# used to save the information get by request
with open("acuuweather_info_local_forecast.txt", "w") as f:
    f.write(str(info))
    f.close() 

"""
# used when more requests can not be possible
with open("acuuweather_info_local_forecast.txt", "r") as f:
    info = f.read()
    f.close()
info = eval(info)
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

def prec_sts_checker():
    if info_DailyForecasts[0]['Day']['HasPrecipitation']:
        return "In Day: " + info_DailyForecasts[0]['Day']['PrecipitationIntensity'] + " " + info_DailyForecasts[0]['Day']['PrecipitationType'] + "\n"

    if info_DailyForecasts[0]['Night']['HasPrecipitation']:
        return "In night : " + info_DailyForecasts[0]['Night']['PrecipitationIntensity'] + " " + info_DailyForecasts[0]['Night']['PrecipitationType'] + "\n"

location_label1 = tk.Label(root, font = ("Helvetica", 14, "bold"), background = "light green", text = "Location : " )
location_label2 = tk.Label(root, font = ("Helvetica", 10, "bold"), background = "light green", text = "@local")
temp_label1 = tk.Label(root, font = ("Helvetica", 14, "bold"), background = "light green", text = "Temnpreature: ")
temp_label2 = tk.Label(root, font = ("Helvetica", 10, "bold"), background = "light green", text = "Minimum : " + str(min_temp) + " F" + "   ||   " + "Maximum : " + str(max_temp) + " F")
current_sts1 = tk.Label(root, font = ("Helvetica", 14, "bold"), background = "light green", text = "Today's Info: ")
current_sts2 = tk.Label(root, font = ("Helvetica", 10, "bold"), background = "light green", text = "Day : " + day_info['IconPhrase'] + "\n\n" + "Night : " + night_info['IconPhrase'])
prec_sts_label1 = tk.Label(root, font = ("Helvetica", 14, "bold"), background = "light green", text = "Precipittion Status : ")
prec_sts_label2 = tk.Label(root, font = ("Helvetica", 10, "bold"), background = "light green", text = prec_sts_checker())
sts_label1 = tk.Label(root, font = ("Helvetica", 14, "bold"), background = "light green", text = "Status :")
sts_label2 = tk.Label(root, font = ("Helvetica", 10, "bold"), background = "light green", text = tw.fill(Text, width = 40))
sts_type_label = tk.Label(root, font = ("Helvetica", 11, "bold"), background = "light green", text = "Type: " + category)
# print(tw.fill(Text))

location_label1.grid(row = 0, column = 0, padx = 10, pady = 5)
location_label2.grid(row = 0, column = 1, padx = 10, pady = 5)
temp_label1.grid(row = 1, column = 0, padx = 10, pady = 0)
temp_label2.grid(row = 1, column = 1, padx = 5, pady = (5, 0))
current_sts1.grid(row = 2, column = 0, padx = 5, pady = 0)
current_sts2.grid(row = 2, column = 1, padx = 5, pady = (10, 0))
prec_sts_label1.grid(row = 3, column = 0, padx = (20, 0), pady = 0)
prec_sts_label2.grid(row = 3, column = 1, padx = 10, pady = (10,0))
sts_label1.grid(row = 4, column = 0, padx = 10, pady = 0)
sts_label2.grid(row = 4, column = 1, padx = 10, pady = (10, 0))
sts_type_label.grid(row = 5, column = 1, padx = 10, pady = (2, 0))

root.mainloop()
