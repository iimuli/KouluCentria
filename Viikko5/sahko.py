from enum import Enum
from datetime import datetime

class ElectricityDataEnum(Enum):
    time = 0
    consumption1 = 1
    consumption2 = 2
    comsumption3 = 3
    production1 = 4
    production2 = 5
    production3= 6


def main():

    weekday_list = ['maanantai', 'tiistai', 'keskiviikko', 'torstai', 'perjantai', 'lauantai', 'sunnuntai']
    data_list = DictionaryPerDay("viikko42.csv")

    calculateKWHperDay(data_list, weekday_list)
 

def calculateKWHperDay(data_list, weekdays):
    #print(list)
    print('Viikon 42 sähkönkulutus ja -tuotanto (kWh, vaiheittain)\n\nPäivä         Pvm         Kulutus [kWh]                 Tuotanto [kWh]\n             (pv.kk.vvvv)  v1      v2      v3            v1     v2     v3\n---------------------------------------------------------------------------')
    kwhPerDay = {}
    index = 0

    for d in data_list.values():
        print(GetDayFromList(d))
        index += 1
        #print(f'{weekdays[index]}{' ' * (14 - len(weekdays[w]))}{date}{' ' * 3}{ChangeWHtoKWHSTR(int(list[0][1]))}{' ' * (8 - len(ChangeWHtoKWHSTR(int(list[0][2]))))}{ChangeWHtoKWHSTR(int(list[0][2]))}{' ' * (8 - len(ChangeWHtoKWHSTR(int(list[0][2]))))}{ChangeWHtoKWHSTR(int(list[0][3]))}{' ' * (14 - len(ChangeWHtoKWHSTR(int(list[0][3]))))}{ChangeWHtoKWHSTR(int(list[0][4]))}{' ' * (7 - len(ChangeWHtoKWHSTR(int(list[0][4]))))}{ChangeWHtoKWHSTR(int(list[0][5]))}{' ' * (7 - len(ChangeWHtoKWHSTR(int(list[0][5]))))}{ChangeWHtoKWHSTR(int(list[0][5]))}')

    
def GetDayFromList(value):
     date = value[0].strip().split(":")
     dayData = date[0].strip().split("T")
     return dayData[0].strip().split("-")[2]

def ChangeToFinnishTime(time): #Aika muutos
    aika = datetime.strptime(time, "%H:%M").time()
    return aika.strftime("%H.%M")

def ChangeToFinnishDate(date): #Päivämäärä muunnosd
    paiva = datetime.strptime(date, "%Y-%m-%d").date()
    return paiva.strftime("%d.%m.%Y")

def ChangeWHtoKWHSTR(wh):
    kwh = wh / 1000
    return str(kwh).replace('.',',')

def DictionaryPerDay(textFile):
    data_list = {}
    with open(textFile , "r", encoding="utf-8") as f: 
        next(f)
        for line in f: 
            data = line.strip().split(";")

            datestT = data[0].split("T")[0]
            dates = datestT.split("-")  
            day = dates[2]

            if day not in data_list:
                data_list[day] = []
                data_list[day].append(data[0]) 
                data_list[day].append(data[1]) 
                data_list[day].append(data[2]) 
                data_list[day].append(data[3]) 
                data_list[day].append(data[4])  
                data_list[day].append(data[5])  
                data_list[day].append(data[6]) 
            else:
                for i in range(2, 7):
                    data_list[day][i] = CombineNumbers(data_list[day][i], data[i])
    return data_list


def CombineNumbers(data1, data2):
    num1 = int(data1)
    num2 = int(data2)
    return str(num1 + num2)

if __name__ == "__main__":
    main()


