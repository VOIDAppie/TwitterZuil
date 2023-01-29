from tkinter import *
from time import strftime
import psycopg2
import requests
import json
from datetime import datetime

con = psycopg2.connect(host='localhost', port=15432, database='zuil', user='zuil', password='zuil')
cursor = con.cursor()

# NS kleurencodes
ns_geel = '#ffc72c'
ns_blauw = '#002d72'
# Initialize Window
root = Tk()
root['background'] = ns_geel
root.geometry("960x540")  # size of the window by default
root.resizable(0, 0)  # to make the window size fixed
# title of our window
root.title("Stationshal")

# ----------------------Functions to fetch and display weather info
city_value = StringVar()


def time_format_for_location(utc_with_tz):
    local_time = datetime.utcfromtimestamp(utc_with_tz)
    return local_time.time()


city_value = StringVar()

aantal_berichten = 0
aantal_seconden = 0

def klok():
    try:
        global aantal_seconden
        global aantal_berichten

        if aantal_seconden == 2:
            cursor.execute('SELECT * FROM klant')
            rows = cursor.fetchall()
            bericht = rows[aantal_berichten]

            print(rows[aantal_berichten])

            berichtString = f'Naam: {bericht[0]}\n\nStation: {bericht[2]}\n\nDatum: {bericht[3]}\n\nBericht: {bericht[1]}'
            bericht_toner_veld.delete(1.0, END)
            bericht_toner_veld.insert(1.0, berichtString)


            # #Facilities
            # cursor.execute('SELECT * FROM station_service')
            # station_rows = cursor.fetchall()
            # for row in station_rows:
            #     if bericht[2] == row[0]:
            #         faciliteitBericht = f'{row[0]}: '
            #
            #         if (row[2] == True):
            #             faciliteitBericht += f'OV-Fiets, '
            #
            #         if row[3] == True:
            #             faciliteitBericht += f'Elevator, '
            #
            #         if row[4] == True:
            #             faciliteitBericht += f'Toilet, '
            #
            #         if row[5] == True:
            #             faciliteitBericht += f'Park_and_ride, '
            #
            #         faciliteitBericht = faciliteitBericht[0: -1] + '.'
            #
            #         faciliteiten_veld.delete(1.0, END)
            #         faciliteiten_veld.insert(faciliteitBericht)

            aantal_seconden = 0
            aantal_berichten += 1

        aantal_seconden += 1



        tijd = strftime('%H:%M:%S')
        tijd_label.config(text=tijd)
        tijd_label.after(1000, klok)
    except IndexError:
        print("kaasworst")
        aantal_seconden = 0
        aantal_berichten = 0
        klok()

def showWeather():

    api_key = "52545412be492f65bfffbd2633d79242"  # sample API

    # Get city name from user from the input field (later in the code)
    city_name = city_value.get()

    # API url
    weather_url = 'http://api.openweathermap.org/data/2.5/weather?q=' + city_name + '&appid=' + api_key

    # Get the response from fetched url
    response = requests.get(weather_url)

    # changing response from json to python readable
    weather_info = response.json()

    tfield.delete("1.0", "end")  # to clear the text field for every new output

    # as per API documentation, if the cod is 200, it means that weather data was successfully fetched

    if weather_info['cod'] == 200:
        kelvin = 273  # value of kelvin

        # -----------Storing the fetched values of weather of a city

        temp = int(weather_info['main']['temp'] - kelvin)  # converting default kelvin value to Celcius
        feels_like_temp = int(weather_info['main']['feels_like'] - kelvin)
        pressure = weather_info['main']['pressure']
        humidity = weather_info['main']['humidity']
        wind_speed = weather_info['wind']['speed'] * 3.6
        sunrise = weather_info['sys']['sunrise']
        sunset = weather_info['sys']['sunset']
        timezone = weather_info['timezone']
        cloudy = weather_info['clouds']['all']
        description = weather_info['weather'][0]['description']

        sunrise_time = time_format_for_location(sunrise + timezone)
        sunset_time = time_format_for_location(sunset + timezone)

        # assigning Values to our weather varaible, to display as output

        weather = f"De weer van : {city_name}\nTemperatuur (Celsius): {temp}°\nGevoelstemperatuur (Celsius): {feels_like_temp}°\nDruk: {pressure} hPa\nLuchtvochtigheid: {humidity}%\nZonsopgang om {sunrise_time} en zonsondergang om {sunset_time}\nbewolking: {cloudy}%\nInfo: {description}"
    else:
        weather = f"\n\tDe weer van '{city_name}' niet gevonden!\n\tVoer alstublieft een geldige stad in !!"

    tfield.insert(INSERT, weather)  # to insert or send value in our Text Field to display output


# ------------------------------Frontend part of code - Interface


city_head = Label(root, text='Voer de stad in ', font='Arial 12 bold').pack(pady=10)  # to generate label heading

inp_city = Entry(root, textvariable=city_value, width=24, font='Arial 14 bold').pack()

Button(root, command=showWeather, text="Check het weer", font="Arial 10", bg='lightblue', fg='black',
       activebackground="teal", padx=5, pady=5).pack(pady=20)

# to show output
#Bericht label
weer_tonen_label = Label(root, text="Weer:", font='arial 12 bold').place(relx=0.25, rely=0.25, anchor=CENTER)

#Bericht label
berichten_toner_label = Label(root, text="Bericht:", font='arial 12 bold').place(relx=0.75, rely=0.25, anchor=CENTER)

#Weer info veld
tfield = Text(root)
tfield.configure(font=('Calibri', 12), width=46, height=10)
tfield.place(relx=0.25, rely=0.5, anchor=CENTER)

#Bericht info veld
bericht_toner_veld = Text(root)
bericht_toner_veld.configure(font=('Calibri', 12), width=46, height=10)
bericht_toner_veld.place(relx=0.75, rely=0.5, anchor=CENTER)

#Faciliteiten
#Faciliteiten label
faciliteiten_label = Label(root)
faciliteiten_label.configure(text="Faciliteiten:", font=('Calibri', 14))
faciliteiten_label.place(relx=0.5, rely=0.7, anchor=CENTER)

#Faciliteiten veld
faciliteiten_veld = Text(root)
faciliteiten_veld.configure(font=('Calibri', 12), width=106, height=3)
faciliteiten_veld.place(relx=0.5, rely=0.8, anchor=CENTER)

# Klok
tijd_label = Label(root, font=('Calibri', 14, 'bold'), background=ns_geel, foreground=ns_blauw)
tijd_label.place(relx=0.5, rely=0.95, anchor=CENTER)
klok()


root.mainloop()