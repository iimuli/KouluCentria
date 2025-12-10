# Copyright (c) 2025 Juha Eemeli Väisänen
# License: MIT

from enum import IntEnum, Enum
from datetime import datetime, timedelta

class EData(IntEnum): 
    """ihmisystävällisempi tiedon haku listoilta """
    netCon = 0
    netPro= 1
    avgTemp = 2

class FMonth(Enum):
    """Muunnos suomalaiseen kuukauden nimeen numerolla"""
    Tammikuu = 1
    Helmikuu = 2
    Maaliskuu = 3
    Huhtikuu = 4
    Toukokuu = 5
    Kesäkuu = 6
    Heinäkuu = 7
    Elokuu = 8
    Syyskuu = 9
    Lokakuu = 10
    Marraskuu = 11
    Joulukuu = 12
    @classmethod
    def monthFromNumber(cls, monthNumber):
        return cls(monthNumber).name.capitalize()

csvFile = None

def main():
    """Main, tekee csvFilest(kirjasto) globaalin, jos tiedost on null/None, hakee datan"""
    global csvFile

    if csvFile == None:
        print('getting csv')
        csvFile = readCSV('2025.csv')

    inputPromptLoop(csvFile)


def inputPromptLoop(csv):
    """Selkeet inputit eri vaihtoehdoille while loopis"""

    print('\n\n\nValitse raporttityyppi:\n'
    '1) Päiväkohtainen yhteenveto aikaväliltä\n'
    '2) Kuukausikohtainen yhteenveto yhdelle kuukaudelle\n'
    '3) Vuoden 2025 kokonaisyhteenveto\n'
    '4) Lopeta ohjelma\n\n')

    while True:
        prompt = input('Valitse raportti numerolla: ')

        if prompt == '1':
            raportByDate(csv)
            continue
        elif prompt == '2':
            monthRaport(csv)
            continue
        elif prompt == '3':
            yearRaport(csv)
            continue
        elif prompt == '4':
            print('Hei hei!')
            exit()

def raportByDate(csv):
    """Inputit aikavälille, hakee kaikki datat kyseiseltä aikaväliltä (käyttö, tuotto, keskimääräinen lämpötila)"""

    earliestDate = next(iter(csv))
    latestdate = next(reversed(csv))

    print(f'\n\n\nValitse aikavälillä: {ChangeToFinnishDate(earliestDate)} - {ChangeToFinnishDate(latestdate)}')
    date1 = None
    date2 = None

    while True:
        date1 = input('Alku päivämäärä (xx.xx.xxxx): ')
        try:
            date1 = datetime.strptime(date1, "%d.%m.%Y").date()
            if earliestDate <= date1 <= latestdate:
                break
        except ValueError:
            print("Väärä inputti")

    while True:
        date2 = input('\nLoppu päivämäärä (xx.xx.xxxx): ')
        try:
            date2 = datetime.strptime(date2, "%d.%m.%Y").date()
            if earliestDate <= date2 <= latestdate:
                break
        except ValueError:
            print("Väärä inputti")
    
    days = (date2 - date1).days + 1

    overAllConsumption = 0
    overAllProduction = 0
    tempSum = 0

    print(f'{'-' * 130}\n'
          f'Aikaväli: {ChangeToFinnishDate(date1)} - {ChangeToFinnishDate(date2)}.\n\n'
          'Pvm [päivä/kuukausi/vuosi]           Kokonaiskulutus/vrk [kWh]           Kokonaistuotanto/vrk [kWh]          Keskilämpötila/vrk [°C]\n')

    for i in range(days):

        currentDate = date1 + timedelta(days=i)
        overAllProduction += csv[currentDate][EData.netPro]
        overAllConsumption += csv[currentDate][EData.netCon]
        tempSum += csv[currentDate][EData.avgTemp]
        print(f'{currentDate}{' ' * 30}{csv[currentDate][EData.netCon]:.2f}{' ' * 30}{csv[currentDate][EData.netPro]:.2f}{' ' * 30}{csv[currentDate][EData.avgTemp]:.2f}')

    print(f'\nKokonais kulutus aikavälillä [kWh]          Kokonais tuotto aikavälillä [kWh]        Keskilämpötila aikavälillä [°C]\n\n'
          f'{' ' * 10}{overAllConsumption:.2f}{' ' * 40}{overAllProduction:.2f}{' ' * 40}{(tempSum / days):.2f}\n')
    print(f'\n{'-' * 130}\n\n')


    returnToMain()



def monthRaport(csv):
    """numerolla valittu kuukauden data"""

    print(f'\n\n\nValitse kuukausi: 1 - 12')
    while True:
        selectedMonth = input('Kuukausi (numero): ')
        try:
            if 1 <= int(selectedMonth) <= 12:
                selectedMonth = int(selectedMonth)
                break
        except ValueError:
            print("Väärä inputti")


    overAllConsumption = 0
    overAllProduction = 0
    tempSum = 0
    daysInMonth = 0

    for date in csv.keys():
        if date.month == selectedMonth:
            daysInMonth += 1
            overAllConsumption += csv[date][EData.netCon]
            overAllProduction += csv[date][EData.netPro]
            tempSum += csv[date][EData.avgTemp]

    print(f'\n\n{'-' * 130}\n'
          f'Valittu kuukausi: {FMonth.monthFromNumber(selectedMonth)}, päiviä kirjattu: {daysInMonth}\n\n'
          'Kokonaiskulutus/vrk [kWh]           Kokonaistuotanto/vrk [kWh]          Keskilämpötila/vrk [°C]\n'
          f'{' ' * 10}{overAllConsumption:.2f}{' ' * 30}{overAllProduction:.2f}{' ' * 30}{(tempSum / daysInMonth):.2f}\n'
          f'{'-' * 130}\n\n')


    returnToMain()
    
   

def yearRaport(csv):
    """kaikki vuoden data samaan pakettiin"""

    overAllConsumption = 0
    overAllProduction = 0
    tempSum = 0
    daysInMonth = 0


    for d in csv.keys():
        daysInMonth += 1
        overAllConsumption += csv[d][EData.netCon]
        overAllProduction += csv[d][EData.netPro]
        tempSum += csv[d][EData.avgTemp]

    print(f'\n\n{'-' * 130}\n'
        f'Vuoden 2025 raportti:\n\n'
        'Kokonaiskulutus/vrk [kWh]           Kokonaistuotanto/vrk [kWh]          Keskilämpötila/vrk [°C]\n'
        f'{' ' * 10}{overAllConsumption:.2f}{' ' * 30}{overAllProduction:.2f}{' ' * 30}{(tempSum / daysInMonth):.2f}\n'
        f'{'-' * 130}\n\n')


    returnToMain()


def readCSV(csv):
    """lukee txt, jakaa kaikki omaan date avaimiin kirjastoon (data_date : vuosi, kuukausi, päivä),
      ja tekee niille listan arvoista. Laskee valmiiksi yhteen käytön ja tuoton, sekä keskimääräisen lämpötilan per vrk"""
    dataMap = {}
    avgTemperature = []
    currentDate = None
    appended = False

    with open(csv , "r", encoding="utf-8") as f: 
        next(f)

        for line in f: 

            data = line.strip().split(";")
            data_date = datetime.strptime(data[0].strip().split("T")[0], "%Y-%m-%d").date()
            appended = False

            if data_date not in dataMap: 

                if currentDate != None:
                    tempAll = sum(avgTemperature) / len(avgTemperature)
                    avgTemperature = []
                    dataMap[currentDate].append(float(tempAll))
                    appended = True

                currentDate = data_date
                data_list = []
                data_list.append(float(data[1].replace(",",".")))
                data_list.append(float(data[2].replace(",",".")))

                avgTemperature.append(float(data[3].replace(",",".")))
                dataMap[currentDate] = data_list
                

            else:
                dataMap[currentDate][EData.netCon] += float(data[1].replace(",","."))
                dataMap[currentDate][EData.netPro] += float(data[2].replace(",","."))
                avgTemperature.append(float(data[3].replace(",",".")))

    if appended == False: ##ylijäämä lisäys = jos kyseessä viimeinen haettu päivämäärä
        tempAll = sum(avgTemperature) / len(avgTemperature)
        dataMap[currentDate].append(float(tempAll))

    return dataMap

def ChangeToFinnishDate(date):
     """xxxx.xx.xx -> xx.xx.xxxx"""
     return date.strftime("%d.%m.%Y")

def returnToMain():
    """joka funktion lopussa q inputil valikkoon takaisin, antaa käyttäjälle aikaa perehtyä dataan."""
    print('Paina "q" palataksesi valikkoon.')

    while True:
        returnKey = input()
        try:
            if returnKey == 'q':
                main()
        except ValueError:
            None

if __name__ == "__main__":
    main()
