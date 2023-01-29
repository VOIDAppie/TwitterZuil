import tkinter
import psycopg2
from time import strftime

# Functies
def klok():
    tijd = strftime('%H:%M:%S')
    tijd_label.config(text=tijd)
    tijd_label.after(1000, klok)


def vergeet_alles():
    bericht_is_opgeslagen.place_forget()
    selecteer_beoordeling.place_forget()
    geen_berichten_over.place_forget()
    vraag_eerst_om_bericht.place_forget()
    verzend_eerst_bericht.place_forget()


def bericht_opvragen():
    if len(bericht_veld.get('1.0', 'end-1c')) > 0:
        vergeet_alles()
        verzend_eerst_bericht.place(relx=0.5, rely=0.8, anchor=tkinter.CENTER)
    else:
        cursor.execute('SELECT * FROM klant WHERE status IS NULL LIMIT 1')
        rows = cursor.fetchall()
        if not rows:
            vergeet_alles()
            geen_berichten_over.place(relx=0.5, rely=0.8, anchor=tkinter.CENTER)
            return None

        # naam veld
        naam = rows[0][1]
        naam_veld.configure(state=tkinter.NORMAL)
        naam_veld.delete(0, tkinter.END)
        naam_veld.insert(0, naam)
        naam_veld.configure(state=tkinter.DISABLED)
        naam_veld.place(relx=0.275, rely=0.25, anchor=tkinter.W)

        # station veld
        station = rows[0][3]
        station_veld.configure(state=tkinter.NORMAL)
        station_veld.delete(0, tkinter.END)
        station_veld.insert(0, station)
        station_veld.configure(state=tkinter.DISABLED)
        station_veld.place(relx=0.275, rely=0.33, anchor=tkinter.W)

        # bericht veld
        bericht = rows[0][2]
        bericht_veld.configure(state=tkinter.NORMAL)
        bericht_veld.delete(1.0, tkinter.END)
        bericht_veld.insert(1.0, bericht)
        bericht_veld.configure(state=tkinter.DISABLED)
        bericht_veld.place(relx=0.2, rely=0.42)


def bericht_opslaan():
    if bericht_veld.get('1.0', 'end-1c') == '':
        vergeet_alles()
        vraag_eerst_om_bericht.place(relx=0.5, rely=0.8, anchor=tkinter.CENTER)
        return None

    cursor.execute('SELECT * FROM klant WHERE status IS NULL LIMIT 1')
    rows = cursor.fetchall()
    klant_id = rows[0][0]
    value = rad_btn_status.get()

    if value == 1:
        cursor.execute('UPDATE klant SET STATUS = \'Goedgekeurd\' WHERE klant_id = %s', (klant_id,))
        con.commit()

        vergeet_alles()
        bericht_is_opgeslagen.place(relx=0.5, rely=0.8, anchor=tkinter.CENTER)
    elif value == 2:
        cursor.execute('UPDATE klant SET STATUS = \'Afgekeurd\' WHERE klant_id = %s', (klant_id,))
        con.commit()

        vergeet_alles()
        bericht_is_opgeslagen.place(relx=0.5, rely=0.8, anchor=tkinter.CENTER)
    else:
        vergeet_alles()
        selecteer_beoordeling.place(relx=0.5, rely=0.8, anchor=tkinter.CENTER)

    if value == 1 or value == 2:
        # naam veld
        naam_veld.configure(state=tkinter.NORMAL)
        naam_veld.delete(0, tkinter.END)
        naam_veld.configure(state=tkinter.DISABLED)
        naam_veld.place(relx=0.275, rely=0.25, anchor=tkinter.W)

        # station veld
        station_veld.configure(state=tkinter.NORMAL)
        station_veld.delete(0, tkinter.END)
        station_veld.configure(state=tkinter.DISABLED)
        station_veld.place(relx=0.275, rely=0.33, anchor=tkinter.W)

        # bericht veld
        bericht_veld.configure(state=tkinter.NORMAL)
        bericht_veld.delete(1.0, tkinter.END)
        bericht_veld.configure(state=tkinter.DISABLED)
        bericht_veld.place(relx=0.2, rely=0.42)


# Kleuren
ns_geel = '#ffc72c'
ns_blauw = '#002d72'

# Tkinter scherm
root = tkinter.Tk()
root['background'] = ns_geel
root.resizable(False, False)
root.geometry('960x540')
root.title('Moderatie')


# Titel
titel = tkinter.Label(root)
titel.configure(text='Moderatie', font=('Calibri', 72))
titel['background'] = ns_geel
titel['foreground'] = ns_blauw
titel.pack(side=tkinter.TOP)

# Bericht gedeelte
naam_label = tkinter.Label(root)
naam_label.configure(text='Naam: ', font=('Calibri', 14, 'bold'))
naam_label['background'] = ns_geel
naam_label['foreground'] = ns_blauw
naam_label.place(relx=0.2, rely=0.25, anchor=tkinter.W)

naam_veld = tkinter.Entry(root)
naam_veld.configure(font=('Calibri', 12), state=tkinter.DISABLED)
naam_veld.place(relx=0.275, rely=0.25, anchor=tkinter.W)

station_label = tkinter.Label(root)
station_label.configure(text='Station: ', font=('Calibri', 14, 'bold'))
station_label['background'] = ns_geel
station_label['foreground'] = ns_blauw
station_label.place(relx=0.2, rely=0.33, anchor=tkinter.W)

station_veld = tkinter.Entry(root)
station_veld.configure(font=('Calibri', 12), state=tkinter.DISABLED)
station_veld.place(relx=0.275, rely=0.33, anchor=tkinter.W)

bericht_label = tkinter.Label(root)
bericht_label.configure(text='Bericht: ', font=('Calibri', 14, 'bold'))
bericht_label['background'] = ns_geel
bericht_label['foreground'] = ns_blauw
bericht_label.place(relx=0.2, rely=0.395, anchor=tkinter.W)

bericht_veld = tkinter.Text(root)
bericht_veld.configure(font=('Calibri', 12), width=70, height=2, state=tkinter.DISABLED)
bericht_veld.place(relx=0.2, rely=0.42)

# Radiobuttons
rad_btn_status = tkinter.IntVar()

rad_goedgekeurd = tkinter.Radiobutton(root)
rad_goedgekeurd.configure(text='Goedgekeurd', variable=rad_btn_status, value=1, font=('Calibri', 14, 'bold'))
rad_goedgekeurd['background'] = ns_geel
rad_goedgekeurd['foreground'] = ns_blauw

rad_afgekeurd = tkinter.Radiobutton(root)
rad_afgekeurd.configure(text='Afgekeurd', variable=rad_btn_status, value=2, font=('Calibri', 14, 'bold'))
rad_afgekeurd['background'] = ns_geel
rad_afgekeurd['foreground'] = ns_blauw

rad_goedgekeurd.place(relx=0.2, rely=0.525)
rad_afgekeurd.place(relx=0.2, rely=0.575)

# Optiebuttons
opvraag_btn = tkinter.Button(root)
opvraag_btn.configure(text='bericht opvragen', font=('Calibri', 12, 'bold'), command=bericht_opvragen)
opvraag_btn['background'] = ns_blauw
opvraag_btn['foreground'] = 'white'
opvraag_btn_status = 0

opslaan_btn = tkinter.Button(root)
opslaan_btn.configure(text='opslaan', font=('Calibri', 12, 'bold'), command=bericht_opslaan)
opslaan_btn['background'] = ns_blauw
opslaan_btn['foreground'] = 'white'

opvraag_btn.place(relx=0.5, rely=0.525)
opslaan_btn.place(relx=0.5, rely=0.6)

# Messages
bericht_is_opgeslagen = tkinter.Label(root)
bericht_is_opgeslagen.configure(text='Het bericht is opgeslagen...', font=('Calibri', 14, 'bold'))
bericht_is_opgeslagen['background'] = ns_geel
bericht_is_opgeslagen['foreground'] = ns_blauw

verzend_eerst_bericht = tkinter.Label(root)
verzend_eerst_bericht.configure(text='SLA EERST HET GEGEVEN BERICHT OP!', font=('Calibri', 14))
verzend_eerst_bericht['background'] = ns_geel
verzend_eerst_bericht['foreground'] = 'red'

selecteer_beoordeling = tkinter.Label(root)
selecteer_beoordeling.configure(text='SELECTEER EERST EEN BEOORDELING!', font=('Calibri', 14))
selecteer_beoordeling['background'] = ns_geel
selecteer_beoordeling['foreground'] = 'red'

vraag_eerst_om_bericht = tkinter.Label(root)
vraag_eerst_om_bericht.configure(text='VRAAG EERST EEN BERICHT OP!', font=('Calibri', 14))
vraag_eerst_om_bericht['background'] = ns_geel
vraag_eerst_om_bericht['foreground'] = 'red'

geen_berichten_over = tkinter.Label(root)
geen_berichten_over.configure(text='ER ZIJN GEEN BERICHTEN MEER OVER!', font=('Calibri', 14))
geen_berichten_over['background'] = ns_geel
geen_berichten_over['foreground'] = 'green'

# Klok
tijd_label = tkinter.Label(root, font=('Calibri', 14, 'bold'), background=ns_geel, foreground=ns_blauw)
tijd_label.place(relx=0.5, rely=0.95, anchor=tkinter.CENTER)
klok()

# Database koppeling
con = psycopg2.connect(host='localhost', port=15432, database='zuil', user='zuil', password='zuil')
cursor = con.cursor()

tkinter.mainloop()