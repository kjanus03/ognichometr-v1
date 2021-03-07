import requests

lat = 51.61759
lon = 15.31486
API_key = '0ca416bae89b399cf44e8310dbfb4359'
units = 'metric'
api_call = f'http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_key}&units={units}'

r = requests.get(api_call)
r.raise_for_status()
dane = r.json()['list']
dni = [d for d in dane]

daty = []
temperatury = []
wiatry = []
chmury = []

for d in dane:
    if d['dt_txt'][11:] == "18:00:00":
        data = d['dt_txt'][:10]
        daty.append(data)

        temperatura = (d['main']['temp'], d['main']['feels_like'])
        wiatr = d['wind']['speed']
        zachmurzenie = d['clouds']['all']

        temperatury.append(temperatura)
        wiatry.append(wiatr)
        chmury.append(zachmurzenie)

        print(data, temperatura, wiatr, chmury)



import datetime
import csv

dzien = daty[0]

import re

hourRegex = re.compile("\d:\d\d:\d\d")





def policz_punkty(data_konkr):

    dzien = data_konkr
    wybor_dnia = daty.index(dzien)
    temperatura = temperatury[wybor_dnia][0]
    odczuwalna = temperatury[wybor_dnia][1]
    wiatr = wiatry[wybor_dnia]
    zachmurzenie = chmury[wybor_dnia]

    url = f'https://api.sunrise-sunset.org/json?lat=51.6212&lng=-15.4224&date={dzien}'
    r = requests.get(url)
    contents = r.json()
    zachod = contents['results']['sunset']

    def policz_za_pogode():
        punkty_za_temperature = 0
        if 0 < temperatura < 25:

            punkty_za_temperature += temperatura * 8
        elif 25 <= temperatura <= 30:
            punkty_za_temperature += 200
        elif temperatura > 30:
            punkty_za_temperature += (55 - temperatura) * 8

        if 0 < odczuwalna < 25:
            punkty_za_temperature += temperatura * 8
        elif 25 <= odczuwalna <= 31:
            punkty_za_temperature += 200
        elif odczuwalna > 31:
            punkty_za_temperature += (56 - temperatura) * 8

        if 1 < wiatr < 11:
            punkty_za_wiatr = 55
        elif 0 <= wiatr <= 1:
            punkty_za_wiatr = 45
        else:
            punkty_za_wiatr = 55 - wiatr / 2

        if zachmurzenie < 20:
            punkty_za_chmury = 95
        elif zachmurzenie < 75:
            punkty_za_chmury = 95 + (zachmurzenie * (-1)) + 20
        else:
            punkty_za_chmury = 0

        pogoda = punkty_za_temperature + punkty_za_wiatr + punkty_za_chmury
        return pogoda

    def policz_za_wolne():
        wolne = 0
        year, month, day = (int(x) for x in dzien.split('-'))
        ans = datetime.date(year, month, day)
        d1 = (ans.strftime("%A"))

        if d1 == 'Friday' or d1 == 'Saturday':
            wolne = 300

        if month == 7 or month == 8:
            wolne = 300

        if month == 6 and day > 24:
            wolne = 300

        return wolne

    def policz_za_zachod():
        zachod = 0
        year, month, day = (int(x) for x in dzien.split('-'))
        ans = datetime.date(year, month, day)
        if month in [11, 12, 1, 2]:
            zachod = 0
        if month == 6 or (month == 7 and day < 10):
            zachod = 100
        if month == 7 and day > 10:
            zachod = 100 - day / 10
        if month == 5:
            zachod = 100 - 15 / day
        if month == 8:
            zachod = 80
        if month == 4:
            zachod = 60
        if month == 9:
            zachod = 50
        if month == 10:
            zachod = 33
        if month == 3:
            zachod = 25
        return zachod

    def policz_za_gwiazdy():
        gwiazdy = 0
        wydarzenie = '---'
        with open('database2.csv') as csv_file:
            reader = csv.reader(csv_file)
            dates, wydarzenia = [], []
            for linia in reader:
                dates.append(linia[0])
                wydarzenia.append(linia[1])
        year, month, day = (str(x) for x in dzien.split('-'))
        data = '.'.join([day, month, year])

        if data in dates:
            ind = dates.index(data)
            wydarzenie = wydarzenia[ind]
            gwiazdy = 50

        return [gwiazdy, wydarzenie]

    pogoda_dnia = policz_za_pogode()
    wolne_dnia = policz_za_wolne()
    zachod_dnia = policz_za_zachod()
    gwiazdy_dnia = policz_za_gwiazdy()

    punkty = pogoda_dnia + wolne_dnia + zachod_dnia + gwiazdy_dnia[0]
    tekst = f'\nPogoda - {round(policz_za_pogode(), 2)}pkt.,  ' \
            f'\n  Temperatura: {temperatura}C' \
            f'\n  Temp. Odczuwalna: {odczuwalna}C' \
            f'\n  Wiatr: {wiatr}m/s' \
            f'\n  Zachmurzenie: {zachmurzenie}%' \
            f'\n  Zachód Słońca: {zachod} czasu letniego.\n' \

    if wolne_dnia != 0:
        tekst += f'\nDzień wolny! - 300pkt'

    tekst += f'\nZdarzenia astronomiczne - {gwiazdy_dnia[0]}pkt: ' \
            f'\n  {gwiazdy_dnia[1]}\n' \
            f'\nProgram do wyniku dolicza też punkty za długość dnia!' \
            f' \nDziękujemy za skorzystanie z usług.'
    return [round(punkty, 2), tekst]



    print(f'Punkty za wolne: {policz_za_wolne()}')
    print(f'Punkty za zachod slonca: {policz_za_zachod()}')
    print(f'Punkty za zjawiska astronomiczne: {policz_za_gwiazdy()}')


print(f'\nDzisiejsze szanse na ognicho: {policz_punkty(dzien)[1]}/1000 pkt.')
