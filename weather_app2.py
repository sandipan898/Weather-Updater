import tkinter as tk
# from PIL import *
# from tkinter import PhotoImage
import requests
import json
import textwrap as tw
import sqlite3
from tkinter import messagebox as mg

root2 = None
location_code_enrty = None
zipcodes = None
zipcode_label = None
info_frame = None
root_frame = None

global root 

# http://dataservice.accuweather.com/forecasts/v1/daily/1day/ ?apikey=CFfODWB5pWrrIs0uMBjhGeP5uunW09D9&language=en-us&details=false&metric=false


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



def view_selectd_data(zip_id):
    # To view selected data by zipcode

    global info_frame
    try:
        info_frame.destroy()
    except:
        pass
    
    try: 
        conn = sqlite3.connect("WeatherData.db")
        c = conn.cursor()
        c.execute("SELECT *, oid FROM locationBasedData WHERE oid = " + zip_id)
        records = c.fetchone()
        conn.commit()
        conn.close()
        print(records)

        zipinfo = ''
        for record in records:
            # zipinfo += "zipcode = " + str(record[0]) + "id = " + str(record[8]) + "\n"
            zipinfo += tw.fill(str(record), width = 50) + "\n"

        info_frame = tk.Frame(root2,background = "light green")
        info_frame.grid(row = 1, column = 1, columnspan = 2)

        print_info = tk.Label(info_frame, text = zipinfo, font = ("Helvetica", 10, "bold"), background = "light green")
        print_info.grid(row = 0, column = 0)

    except Exception as OperationalError:
        mg.showerror("Operation Error", "None or Wrong ID Selected")
        root2.destroy()
        show_data()
    
def delete_data(val):
    # To delete a saved record from the database
    try:
        conn = sqlite3.connect('WeatherData.db')
        c = conn.cursor()
        c.execute("DELETE FROM locationBasedData WHERE oid = " + val)
        conn.commit()
        conn.close()
        mg.showinfo("Successful", "Data Successfully Deleted")
    except Exception as e:
        mg.showerror("Operation Error", "No ID Selected")
        
    root2.destroy()
    show_data()        


def show_data():
    # show saved location data from database
    global root2

    # info_frame.destroy()

    root2 = tk.Tk()
    root2.title('Previous Record')
    root2.configure(background = 'light green')
    root2.geometry("635x250+700+90")
    # root.iconbitmap("weather_icon2.ico")
   
    conn = sqlite3.connect("WeatherData.db")
    c = conn.cursor()
    c.execute("SELECT *, oid FROM locationBasedData")
    records = c.fetchall()
    conn.commit()
    conn.close()
    global zipcode_label

    zipcodes = ''
    for record in records:
        zipcodes += "id = " + str(record[8]) + " zipcode = " + str(record[0]) + "\n"
    
    title_label = tk.Label(root2, text = "Saved Data", font = ("Helvetica", 12, "bold"), background = "light green")
    title_label.grid(row = 0, column = 0, padx = 10, pady = 10)
    # global zipcodes
    
    zipcode_label = tk.Label(root2, text = zipcodes, font = ("Helvetica", 10, "bold"), background = "light green")
    zipcode_label.grid(row = 1, column = 0, padx = 10, pady = 10)
    
    # print(zip_entry.get())

    btn_frame = tk.Frame(root2, background = "light green")
    btn_frame.grid(row = 0, column = 1)

    zip_entry = tk.Entry(btn_frame)
    zip_entry.grid(row = 0, column = 0, padx = 10)
    
    select_btn = tk.Button(btn_frame, text = "Show Data by ID", font = ("Helvetica", 10, "bold"), background = "light green", command = lambda: view_selectd_data(zip_entry.get()))
    select_btn.grid(row = 0, column = 1, padx = 7, pady = 5, ipadx = 10)

    delete_btn = tk.Button(btn_frame, text = "Delete Data by ID",  font = ("Helvetica", 10, "bold"), background = "light green", command = lambda: delete_data(zip_entry.get()))
    delete_btn.grid(row = 0, column = 2, padx = 7, pady = 5, ipadx = 10)
    
    
def get_location_update(code):
    # to get the response by request and show the data

    # root.destroy()
    print(code)
    global root_frame
    try:
        root_frame.destroy()
    except:
        pass
    
    response = requests.get("http://dataservice.accuweather.com/forecasts/v1/daily/1day/" + code + "?apikey=CFfODWB5pWrrIs0uMBjhGeP5uunW09D9&language=en-us&details=false&metric=false")
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
        # check for the precipitation information

        if info_DailyForecasts[0]['Day']['HasPrecipitation']:
            return "In Day: " + info_DailyForecasts[0]['Day']['PrecipitationIntensity'] + " " + info_DailyForecasts[0]['Day']['PrecipitationType'] + "\n"

        if info_DailyForecasts[0]['Night']['HasPrecipitation']:
            return "In night : " + info_DailyForecasts[0]['Night']['PrecipitationIntensity'] + " " + info_DailyForecasts[0]['Night']['PrecipitationType'] + "\n"
        
        return "No precipitation"
        

    root_frame = tk.Frame(root, background = 'light green')
    root_frame.grid(row = 0, column = 0)

    temp_label1 = tk.Label(root_frame, font = ("Helvetica", 14, "bold"), background = "light green", text = "Temnpreature: ")
    temp_label2 = tk.Label(root_frame, font = ("Helvetica", 10, "bold"), background = "light green", text = "Minimum : " + str(min_temp) + " F" + "   ||   " + "Maximum : " + str(max_temp) + " F")
    current_sts1 = tk.Label(root_frame, font = ("Helvetica", 14, "bold"), background = "light green", text = "Today's Info: ")
    current_sts2 = tk.Label(root_frame, font = ("Helvetica", 10, "bold"), background = "light green", text = "Day : " + day_info['IconPhrase'] + "\n\n" + "Night : " + night_info['IconPhrase'])
    prec_sts_label1 = tk.Label(root_frame, font = ("Helvetica", 14, "bold"), background = "light green", text = "Precipittion Status : ")
    prec_sts_label2 = tk.Label(root_frame, font = ("Helvetica", 10, "bold"), background = "light green", text = prec_sts_checker())
    sts_label1 = tk.Label(root_frame, font = ("Helvetica", 14, "bold"), background = "light green", text = "Status :")
    sts_label2 = tk.Label(root_frame, font = ("Helvetica", 10, "bold"), background = "light green", text = tw.fill(Text, width = 40))
    sts_type_label = tk.Label(root_frame, font = ("Helvetica", 11, "bold"), background = "light green", text = "Type: " + category)

    update_btn = tk.Button(root_frame, text = "Save Data",font = ("Helvetica", 9, "bold"),  command = lambda: add_to_database(location_code_enrty.get(), min_temp , max_temp, day_info['IconPhrase'], night_info['IconPhrase'], prec_sts_checker(), Text, category))
    compare_btn = tk.Button(root_frame, text = "Compare", font = ("Helvetica", 9, "bold"), command = compare_stat)
    show_btn = tk.Button(root_frame, font = ("Helvetica", 9, "bold"), text = "Show" + "\nsaved records", command = show_data)

    temp_label1.grid(row = 1, column = 0, padx = 10, pady = 0)
    temp_label2.grid(row = 1, column = 1, padx = 5, pady = (5, 0))
    current_sts1.grid(row = 2, column = 0, padx = 5, pady = 0)
    current_sts2.grid(row = 2, column = 1, padx = 5, pady = (10, 0))
    prec_sts_label1.grid(row = 3, column = 0, padx = (20, 0), pady = (5,0))
    prec_sts_label2.grid(row = 3, column = 1, padx = 10, pady = (12,2))
    sts_label1.grid(row = 4, column = 0, padx = 10, pady = (5,0))
    sts_label2.grid(row = 4, column = 1, padx = 10, pady = (10, 0))
    sts_type_label.grid(row = 5, column = 1, padx = 10, pady = (5, 0))
    update_btn.grid(row = 3, column  = 2, ipadx = 10, pady = 10)
    show_btn.grid(row = 4, column = 2)
    compare_btn.grid(row = 2, column = 2)


    location_code_enrty = tk.Entry(root_frame)
    location_code_enrty.focus()
    location_code_enrty.insert(0, code)
    location_code_enrty.grid(row = 0, column = 1, padx = 10, pady = 5)
    
    get_location_btn = tk.Button(root_frame, font = ("Helvetica", 11, "bold"), text = "GO!", command = lambda: get_location_update(location_code_enrty.get()))
    get_location_btn.grid(row = 0, column = 2)
    location_label1 = tk.Label(root_frame, font = ("Helvetica", 14, "bold"), background = "light green", text = "Enter Location : " )
    location_label1.grid(row = 0, column = 0, padx = 10, pady = 5)


if __name__ == '__main__':
        
    root = tk.Tk()
    root.title("Weather Forecast")
    root.geometry("650x270+700+80")
    root.configure(background = 'light green')
    # root.iconbitmap(True, PhotoImage(file="weather_icon3.ico"))
    # root.iconbitmap("weather_icon2.ico")


    root_frame = tk.Frame(root, background = 'light green')
    root_frame.grid(row = 0, column = 0)

    location_code_enrty = tk.Entry(root_frame)
    location_code_enrty.focus()
    location_code_enrty.grid(row = 0, column = 1, padx = 10, pady = 5)
    # print(location_code_enrty.get())
    get_location_btn = tk.Button(root_frame, font = ("Helvetica", 11, "bold"), text = "GO!", command = lambda: get_location_update(location_code_enrty.get()))
    get_location_btn.grid(row = 0, column = 2)


    location_label1 = tk.Label(root_frame, font = ("Helvetica", 14, "bold"), background = "light green", text = "Enter Location : " )
    location_label1.grid(row = 0, column = 0, padx = 10, pady = 5)

    root.mainloop()
