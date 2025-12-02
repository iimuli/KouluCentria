# Copyright (c) 2025 Juha Eemeli Väisänen
# License: MIT

from enum import IntEnum
from datetime import datetime

class EData(IntEnum): 
    """ihmisystävällisempi tiedon haku listoilta """
    day = 0
    date = 1
    consumption1 = 2
    consumption2 = 3
    comsumption3 = 4
    production1 = 5
    production2 = 6
    production3= 7


def main(): 
    """ main :) """
    data_list = DictionaryPerDay("viikko42.csv")
    calculateKWHperDay(data_list)
 

def calculateKWHperDay(data_list):
    """Perus looppi, printtaa kaikki listan datat"""

    print('Viikon 42 sähkönkulutus ja -tuotanto (kWh, vaiheittain)\n\nPäivä         Pvm         Kulutus [kWh]                 Tuotanto [kWh]\n             (pv.kk.vvvv)  v1      v2      v3            v1     v2     v3\n---------------------------------------------------------------------------')

    for d in data_list.values():

        """suoraan printatta jonossa variablet? tehä listaan variablet ja tulostaa koko lista? Lisätä yhteen stringiin kaikki valuet? teenpä pitkän stringin."""
        day = d[EData.day]
        date = d[EData.date]
        k1 = toKWH(d[EData.consumption1])
        k2 = toKWH(d[EData.consumption2])
        k3 = toKWH(d[EData.comsumption3])
        t1 = toKWH(d[EData.production1])
        t2 = toKWH(d[EData.production2])
        t3 = toKWH(d[EData.production3])

        """Modulaarinen asettelu tehtävän annon pohjan mukaisesti, ei tarvihe jatkuvasti manuaalisesti rivivälejä asetella jos pituus muutoksia ilmenee"""
        prnt = day + ' ' * (14 - len(day))
        prnt += date + ' ' * (13 - len(date))
        prnt += k1 + ' ' * (8 - len(k1))
        prnt += k2 + ' ' * (8 - len(k2))
        prnt += k3 + ' ' * (14 - len(k3))
        prnt += t1 + ' ' * (7 - len(t1))
        prnt += t2 + ' ' * (7 - len(t2))
        prnt += t3

        print(prnt)
    
def ChangeToFinnishDate(date):
    """Päivämäärä muunnos suomalaizee"""
    paiva = datetime.strptime(date, "%Y-%m-%d").date()
    return paiva.strftime("%d.%m.%Y")

    
def GetDayFromList(value): 
     """Muuntaa listalta aika hässäkän päivä numeroksi"""
     date = value[0].strip().split(":")
     dayData = date[0].strip().split("T")
     return dayData[0].strip().split("-")[2]

def ChangeToFinnishTime(time):
    """Aika muutos suomalaisee"""
    aika = datetime.strptime(time, "%H:%M").time()
    return aika.strftime("%H.%M")


def DictionaryPerDay(textFile): 
    """tekee jokaiselle päivälle oman dicionaryn/mapin, käytetään stringejä dynamicin sijaan koska laiska :)"""
    data_list = {}
    weekday_list = ['Maanantai', 'Tiistai', 'Keskiviikko', 'Torstai', 'Perjantai', 'Lauantai', 'Sunnuntai']
    weekDayIndex = 0

    with open(textFile , "r", encoding="utf-8") as f: 
        next(f)
        for line in f: 
            data = line.strip().split(";")

            datestT = data[0].split("T")[0]
            dates = datestT.split("-")  
            """avain päivän nimen mukaan, jos haluttais isompi selattava lista, laittaisin päivämäärän mukaan xx.xx.xxxx"""
            day = dates[2]

            if day not in data_list:
                """tekee uuden listan jokaiselle päivälle, jos ei ole jo olemassa. Käyttäisin normaalisti tässäkin xx.xx.xxxx muotoa jollai tapaa"""
                data_list[day] = []

                data_list[day].append(weekday_list[weekDayIndex])
                weekDayIndex += 1
                if weekDayIndex > len(weekday_list):
                    weekDayIndex = 0

                data_list[day].append(ChangeToFinnishDate(datestT))
                """data_list[day].append(data[0].split("T")[1]) ajan saisin listaan, mutta tällä hetkellä ei tarpeellinen"""
                data_list[day].append(data[1]) 
                data_list[day].append(data[2]) 
                data_list[day].append(data[3]) 
                data_list[day].append(data[4])  
                data_list[day].append(data[5])  
                data_list[day].append(data[6]) 
           
            else:
                """Jos päivä jo olemassa. summaa kaikki saman päivän wh lukemat asianmukaisesti. Tällä hetkellä ei tarvitse eriksee varastoida tunti kohtaisia määriä."""
                for i in range(2, len(data_list[day])):
                    data_list[day][i] = CombineNumbers(data_list[day][i], data[i-1]) 
            
    return data_list


def CombineNumbers(data1, data2):
    """yhdistää kahden Str:n int valuet"""
    num1 = int(data1)
    num2 = int(data2)
    return str(num1 + num2)

def toKWH(value):
    """wh => kwh muunnos 2. decimaalilla, palauttaa stringin"""
    kwh = round((int(value) / 1000),2)
    return ('%.2f' % kwh).replace(".",",")


if __name__ == "__main__":
    main()


