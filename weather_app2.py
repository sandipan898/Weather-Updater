import tkinter as tk
# from PIL import *
# from tkinter import PhotoImage
import requests
import json
import textwrap as tw
import sqlite3

root2 = None
location_code_enrty = None

root = tk.Tk()
root.title("Weather Forecast")
root.geometry("620x250+710+80")
root.configure(background = 'light green')
# root.iconbitmap(True, PhotoImage(file="weather_icon3.ico"))
# root.iconbitmap("favicon.ico")

"""
root = tk.Tk()
img = PhotoImage(file='your-icon')
root.tk.call('wm', 'iconphoto', root._w, img)
"""
# http://dataservice.accuweather.com/forecasts/v1/daily/1day/191578?apikey=CFfODWB5pWrrIs0uMBjhGeP5uunW09D9&language=en-us&details=false&metric=false


def add_to_database(zipcode, min_temp, max_temp, day_info, night_info, precipitation_sts, status, category):
    # adding weather record to database
    try: 
        conn = sqlite3.connect('WeatherData.db')
        c = conn.cursor()
        c.execute("""CREATE TABLE locationBasedData (
                        zipcode integer,
                        max_temp text,
                        min_temp text,
                        day_info text,
                        night_info text,
                        precipitation_sts text,
                        status text,
                        category text
                        )""")
        conn.commit()
        conn.close()
    except Exception as e:
        pass

    conn = sqlite3.connect('WeatherData.db')
    c = conn.cursor()
    c.execute("INSERT INTO locationBasedData VALUES (:zipcode, :max_temp, :min_temp, :day_info, :night_info, :precipitation_sts, :status, :category)", 
                {
                    'zipcode': zipcode,
                    'max_temp': max_temp,
                    'min_temp': min_temp,
                    'day_info': day_info,
                    'night_info': night_info,
                    'precipitation_sts': precipitation_sts,
                    'status': status,
                    'category': category
                })
    conn.commit()
    conn.close()


def compare_stat():
    # to compare weather ststistics of different location

    pass

def select_op(option):
        print(option)
        # print(op.get())
        # To select the mode of showing data
        conn = sqlite3.connect('WeatherData.db')
        c = conn.cursor()
        c.execute("SELECT *, oid FROM locationBasedData")

        if option == 'one':
            records = c.fetchone()
        else:
            records = c.fetchall()
        print(records)

        print_record = ''
        for record in records:
            print_record += str(record) + "\n"
            # print_record = print_record + "Zip Code: " + str(record[0]) + "Max_temp: " + str(record[1]) + " Min_temp: " + str(record[2]) + "\n"

        print_info = tk.Label(root2, text =  print_record, font = ("Helvetica", 10, "bold"), background = "light green")
        print_info.grid(row = 3, column = 0, columnspan = 2)

        conn.commit()
        conn.close()


def show_data():
    # show saved location data from database
    global root2
    root2 = tk.Tk()
    root2.title('Previous Record')
    root2.configure(background = 'light green')
    
    option_label = tk.Label(root2, text = "Select option", font = ("Helvetica", 10, "bold"), background = "light green")
    option_label.grid(row = 0, column = 0)

    options = [
                ("Show currently saved data", "one"),
                ("Show all data","all")
              ]
    
    op = tk.StringVar()
    # op.set('Show currently saved data')
    op.set("NULL")
    # for option, values in options:
    tk.Radiobutton(root2, text = "Show currently saved data", variable = op, value = "one", font = ("Helvetica", 10, "bold"), background = "light green").grid(row = 1, column = 0)
    tk.Radiobutton(root2, text = "Show all data", variable = op, value = "all", font = ("Helvetica", 10, "bold"), background = "light green").grid(row = 1, column = 2)
        
    print(op.get())
    select_btn = tk.Button(root2, text = "Select", font = ("Helvetica", 10, "bold"), background = "light green", command = lambda: select_op(op.get()))
    select_btn.grid(row = 2, column = 0)


def get_location_update():
    # to get the response by request and show the data

    # global info
    """
    response = requests.get("http://dataservice.accuweather.com/forecasts/v1/daily/1day/" + location_code_enrty.get() + "?apikey=CFfODWB5pWrrIs0uMBjhGeP5uunW09D9&language=en-us&details=false&metric=false")
    
    # global info
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
        
        return "No precipitation"

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
    update_btn = tk.Button(root, text = "Save Data",font = ("Helvetica", 9, "bold"),  command = lambda: add_to_database(location_code_enrty.get(), min_temp , max_temp, day_info['IconPhrase'], night_info['IconPhrase'], prec_sts_checker(), Text, category))
    compare_btn = tk.Button(root, text = "Compare", font = ("Helvetica", 9, "bold"), command = compare_stat)
    show_btn = tk.Button(root, font = ("Helvetica", 9, "bold"), text = "Show" + "\nsaved records", command = show_data)

    temp_label1.grid(row = 1, column = 0, padx = 10, pady = 0)
    temp_label2.grid(row = 1, column = 1, padx = 5, pady = (5, 0))
    current_sts1.grid(row = 2, column = 0, padx = 5, pady = 0)
    current_sts2.grid(row = 2, column = 1, padx = 5, pady = (10, 0))
    prec_sts_label1.grid(row = 3, column = 0, padx = (20, 0), pady = (7,0))
    prec_sts_label2.grid(row = 3, column = 1, padx = 10, pady = (10,2))
    sts_label1.grid(row = 4, column = 0, padx = 10, pady = (5,0))
    sts_label2.grid(row = 4, column = 1, padx = 10, pady = (10, 0))
    sts_type_label.grid(row = 5, column = 1, padx = 10, pady = (5, 0))
    update_btn.grid(row = 3, column  = 2, ipadx = 10, pady = 10)
    show_btn.grid(row = 4, column = 2)
    compare_btn.grid(row = 2, column = 2)


location_code_enrty = tk.Entry(root)
location_code_enrty.focus()
get_location_btn = tk.Button(root, font = ("Helvetica", 11, "bold"), text = "GO!", command = get_location_update)
location_label1 = tk.Label(root, font = ("Helvetica", 14, "bold"), background = "light green", text = "Enter Location : " )
location_label1.grid(row = 0, column = 0, padx = 10, pady = 5)
location_code_enrty.grid(row = 0, column = 1, padx = 10, pady = 5)
get_location_btn.grid(row = 0, column = 2)

root.mainloop()
