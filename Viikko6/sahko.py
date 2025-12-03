# Copyright (c) 2025 Juha Eemeli Väisänen
# License: MIT

from enum import IntEnum
from datetime import datetime, date, time


class EData(IntEnum): 
    """ihmisystävällisempi tiedon haku listoilta """
    ##date = 0
    ##time = 0
    netCon = 0
    netPro= 1
    avgTemp = 2


# Aika;Kulutus (netotettu) kWh;Tuotanto (netotettu) kWh;Vuorokauden keskilämpötila
# 2025-01-01   T00:00:00.000+02:00  == h/m/s/ms/timezone;      1,569;      0,000;     -4,5

def main():
    
    csvFile = '2025.csv'
    data2025 = readCSV(csvFile)
    inputPromptLoop(data2025)


def inputPromptLoop(csv):

    print('\n\n\nValitse raporttityyppi:\n'
    '1) Päiväkohtainen yhteenveto aikaväliltä\n'
    '2) Kuukausikohtainen yhteenveto yhdelle kuukaudelle\n'
    '3) Vuoden 2025 kokonaisyhteenveto\n'
    '4) Lopeta ohjelma\n\n')

    while True:
        prompt = input('Valitse raportti numerolla: ')

        if prompt == '1':
            raportByDate(csv)
        elif prompt == '2':
            monthRaport(csv)
        elif prompt == '3':
            yearRaport(csv)
        elif prompt == '4':
            print('end')
            return



    ##return None

def raportByDate(csv):
    print('\n\n\nValitse aikaväli: ')

    date1 = None
    date2 = None

    while True:
        date1 = input('Alku päivämäärä (xx.xx.xxxx): ')
        try:
            datetime.strptime(date1, "%d.%m.%Y")
            break
        except ValueError:
            print("Väärä inputti")

    while True:
        date2 = input('\nLoppu päivämäärä (xx.xx.xxxx): ')
        try:
            datetime.strptime(date2, "%d.%m.%Y")
            break
        except ValueError:
            print("Väärä inputti")
    
    print(f'\n\nHaetaan yhteenveto aikavälillä: {date1} - {date2}:')
    return ##left here


def monthRaport(csv):
    print('motn raport')
    return None

def yearRaport(csv):
    print('year raport')
    return None


def readCSV(csv):
    dataMap = {}
    avgTemperature = []
    dayIndex = 0

    with open(csv , "r", encoding="utf-8") as f: 
        next(f)

        for line in f: 

            data = line.strip().split(";")
            data_date = datetime.strptime(data[0].strip().split("T")[0], "%Y-%m-%d").date()
            ##data_time = data[0].strip().split("T")[1].strip().split(".")[0] ei tarvine kellonaikaa, kun päivä kerrallaan halutaa dataa?
            ##data_list.append(str(data_time))


            if data_date not in dataMap:
                data_list = []
                data_list.append(float(data[1].replace(",",".")))
                data_list.append(float(data[2].replace(",",".")))

                avgTemperature.append(float(data[3].replace(",",".")))
                dataMap[data_date] = data_list
                dayIndex = 1

            else:
                dayIndex += 1
                dataMap[data_date][EData.netCon] += float(data[1].replace(",","."))
                dataMap[data_date][EData.netPro] += float(data[2].replace(",","."))


                avgTemperature.append(float(data[3].replace(",",".")))
                if dayIndex == 24:
                    dayIndex = 0
                    tempAll = 0
                    for temp in avgTemperature:
                        tempAll += temp
                    tempAll /= 24
                    data_list.append(float(tempAll))

    return dataMap

if __name__ == "__main__":
    main()
