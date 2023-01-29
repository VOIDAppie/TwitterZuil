import tkinter
from time import strftime
from datetime import datetime
import psycopg2


# real time klok
def klok():
    tijd = strftime('%H:%M:%S')
    tijd_label.config(text=tijd)
    tijd_label.after(1000, klok)

# Button Function
def clear_textfields():
    bericht_verzonden.place_forget()
    te_lang_label.place_forget()
    vul_station_bericht_in.place_forget()
    station_te_lang_exception.place_forget()
    naam_te_lang_exception.place_forget()
    combi_te_lang_exception.place_forget()


def save_data():
    station = station_veld.get()
    naam = naam_veld.get()
    bericht = bericht_veld.get('1.0', 'end-1c')
    status = None
    now = datetime.now()
    datum = now.strftime('%Y-%m-%d')

    if len(station) > 255:
        clear_textfields()
        station_te_lang_exception.place(relx=0.475, rely=0.41, anchor=tkinter.W)
        return None

    if len(naam) > 255:
        clear_textfields()
        naam_te_lang_exception.place(relx=0.51, rely=0.41, anchor=tkinter.W)
        return None

    if station == '' or bericht == '':
        clear_textfields()
        vul_station_bericht_in.place(relx=0.475, rely=0.41, anchor=tkinter.W)
        return None

    if len(bericht) > 140:
        clear_textfields()
        te_lang_label.place(relx=0.41, rely=0.41, anchor=tkinter.W)
        return None

    if (len(bericht) + len(station) + len(naam) + 2) > 140:
        clear_textfields()
        combi_te_lang_exception.place(relx=0.34, rely=0.41, anchor=tkinter.W)
        return None

    if naam == '':
        naam = '(anoniem)'

    cursor.execute('INSERT INTO klant(naam, bericht, station, datum, status) VALUES(%s, %s, %s, %s, %s)',
                   (naam, bericht, station, datum, status))
    con.commit()

    station_veld.delete(0, tkinter.END)
    naam_veld.delete(0, tkinter.END)
    bericht_veld.delete('1.0', tkinter.END)
    clear_textfields()
    bericht_verzonden.place(relx=0.4, rely=0.8, anchor=tkinter.W)


# NS kleurencodes
ns_geel = '#ffc72c'
ns_blauw = '#002d72'

# Tkinter root scherm
root = tkinter.Tk()
root.resizable(False, False)
root['background'] = ns_geel
root.geometry('960x540')
root.title('NS Berichtenzuil')
# root.iconbitmap('ns_logo.ico')

# Header
title = tkinter.Label(root)
title.configure(text='NS Berichtenzuil', font=('Calibri', 72))
title['background'] = ns_geel
title['foreground'] = ns_blauw

title.pack(side=tkinter.TOP)

# Stations Frame
station_frame = tkinter.Frame(root)
station_frame['background'] = ns_geel

# Station Label
station_label = tkinter.Label(station_frame)
station_label.configure(text='*Station: ', font=('Calibri', 14, 'bold'))
station_label['background'] = ns_geel
station_label['foreground'] = ns_blauw

# Station textfield
station_veld = tkinter.Entry(station_frame)
station_veld.configure(width=30)

station_label.pack(side=tkinter.LEFT)
station_veld.pack(side=tkinter.LEFT, padx=87)
station_frame.place(relx=0.2, rely=0.275, anchor=tkinter.W)

# Naam Frame
naam_frame = tkinter.Frame(root)
naam_frame['background'] = ns_geel

# Naam Label
naam_label = tkinter.Label(naam_frame)
naam_label.configure(text='Naam (optioneel): ', font=('Calibri', 14, 'bold'))
naam_label['background'] = ns_geel
naam_label['foreground'] = ns_blauw

# Naam textfield
naam_veld = tkinter.Entry(naam_frame)
naam_veld.configure(width=30)

naam_label.pack(side=tkinter.LEFT)
naam_veld.pack(side=tkinter.LEFT, padx=5)
naam_frame.place(relx=0.2, rely=0.32, anchor=tkinter.W)

# Bericht Frame
bericht_frame = tkinter.Frame(root)
bericht_frame['background'] = ns_geel

# Bericht Label
bericht_label = tkinter.Label(bericht_frame)
bericht_label.configure(text='*Bericht: ', font=('Calibri', 14, 'bold'))
bericht_label['background'] = ns_geel
bericht_label['foreground'] = ns_blauw

# All messages
te_lang_label = tkinter.Label(root)
te_lang_label.configure(text='UW BERICHT IS TE LANG! (max. 140 karakters)', font=('Calibri', 14))
te_lang_label['background'] = ns_geel
te_lang_label['foreground'] = 'red'

vul_station_bericht_in = tkinter.Label(root)
vul_station_bericht_in.configure(text='STATION OF BERICHT MIST! (verplicht)', font=('Calibri', 14))
vul_station_bericht_in['background'] = ns_geel
vul_station_bericht_in['foreground'] = 'red'

bericht_verzonden = tkinter.Label(root)
bericht_verzonden.configure(text='Uw bericht is verzonden...', font=('Calibri', 14, 'bold'))
bericht_verzonden['background'] = ns_geel
bericht_verzonden['foreground'] = ns_blauw

station_te_lang_exception = tkinter.Label(root)
station_te_lang_exception.configure(text='HET INGEVULDE STATION IS TE LANG!', font=('Calibri', 14))
station_te_lang_exception['background'] = ns_geel
station_te_lang_exception['foreground'] = 'red'

naam_te_lang_exception = tkinter.Label(root)
naam_te_lang_exception.configure(text='DE INGEVULDE NAAM IS TE LANG!', font=('Calibri', 14))
naam_te_lang_exception['background'] = ns_geel
naam_te_lang_exception['foreground'] = 'red'

combi_te_lang_exception = tkinter.Label(root)
combi_te_lang_exception.configure(text='UW BERICHT NAAM STATION COMBINATIE IS TE LANG!', font=('Calibri', 14))
combi_te_lang_exception['background'] = ns_geel
combi_te_lang_exception['foreground'] = 'red'

# Bericht veld
bericht_veld = tkinter.Text(root)
bericht_veld.configure(width=70, height=5, font=('Calibri', 12))

bericht_label.pack(side=tkinter.LEFT)
bericht_veld.place(relx=0.2, rely=0.530, anchor=tkinter.W)
bericht_frame.place(relx=0.2, rely=0.41, anchor=tkinter.W)

# Verzendknop
verzend_knop = tkinter.Button(root, command=save_data)
verzend_knop.configure(text='verzend', font=('Calibri', 14, 'bold'))
verzend_knop['background'] = ns_blauw
verzend_knop['foreground'] = 'white'

verzend_knop.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)

# Klok
tijd_label = tkinter.Label(root, font=('Calibri', 14, 'bold'), background=ns_geel, foreground=ns_blauw)
tijd_label.place(relx=0.5, rely=0.95, anchor=tkinter.CENTER)
klok()

# Database koppeling

con = psycopg2.connect(host='localhost', port=15432, database='zuil', user='zuil', password='zuil')
cursor = con.cursor()

root.mainloop()
