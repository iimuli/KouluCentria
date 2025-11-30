from enum import IntEnum
from enum import StrEnum
from datetime import datetime

class RData(IntEnum):
    id = 0
    name = 1
    email = 2
    phone = 3
    date = 4
    startTime = 5
    duration = 6
    price = 7
    confirmed = 8
    room = 9
    reservationTime = 10
"""
1) Vahvistetut varaukset
- Muumi Muumilaakso, Metsätila 1, 12.11.2025 klo 09.00
- Hemuli Kasvikerääjä, Kasvitutkimuslabra, 5.11.2025 klo 10.30

2) Pitkät varaukset (≥ 3 h)
- Pikku Myy Myrsky, 22.10.2025 klo 15.45, kesto 3 h, Punainen huone
- Nipsu Rahapulainen, 18.9.2025 klo 13.00, kesto 4 h, Varastotila N

3) Varausten vahvistusstatus
Muumi Muumilaakso → Vahvistettu
Niiskuneiti Muumilaakso → EI vahvistettu
Pikku Myy Myrsky → Vahvistettu

4) Yhteenveto vahvistuksista
- Vahvistettuja varauksia: 3 kpl
- Ei-vahvistettuja varauksia: 2 kpl

5) Vahvistettujen varausten kokonaistulot
Vahvistettujen varausten kokonaistulot: 243,50 €

"""

class FontColor(StrEnum): ##jaksoin laittaa vaa yhtee värin
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    RESET = "\033[0m"  


def muunna_varaustiedot(varaus: list) -> list:

    muutettu_varaus = []

    muutettu_varaus.append(int(varaus[0]))
    muutettu_varaus.append(str(varaus[1]))
    muutettu_varaus.append(str(varaus[2]))
    muutettu_varaus.append(str(varaus[3]))
    muutettu_varaus.append(datetime.strptime(varaus[4], "%Y-%m-%d").date())
    muutettu_varaus.append(datetime.strptime(varaus[5], "%H:%M").time()) 
    muutettu_varaus.append(int(varaus[6]))
    muutettu_varaus.append(float(varaus[7]))
    muutettu_varaus.append(bool(varaus[8]== 'True'))
    muutettu_varaus.append(str(varaus[9]))
    muutettu_varaus.append(datetime.strptime(varaus[10], "%Y-%m-%d %H:%M:%S"))
    return muutettu_varaus

def hae_varaukset(varaustiedosto: str) -> list:
    # HUOM! Tälle funktioille ei tarvitse tehdä mitään!
    # Jos muutat, kommentoi miksi muutit
    
    varaukset = []
    ## En tarvitse alempaa listaa = ei tarvetta skipata ensimmäistä iteraatiota joka kerta, vaikka toki niinki voi tehdä
    ##varaukset.append(["varausId", "nimi", "sähköposti", "puhelin", "varauksenPvm", "varauksenKlo", "varauksenKesto", "hinta", "varausVahvistettu", "varattuTila", "varausLuotu"])
    with open(varaustiedosto, "r", encoding="utf-8") as f:
        for varaus in f:
            varaus = varaus.strip()
            varaustiedot = varaus.split('|')
            varaukset.append(muunna_varaustiedot(varaustiedot))
    return varaukset

def ChangeToFinnishTime(time):
    return time.strftime("%H.%M")

def ChangeToFinnishDate(date):
     return date.strftime("%d.%m.%Y")

def main():
    # HUOM! seuraaville riveille ei tarvitse tehdä mitään osassa A!
    # Osa B vaatii muutoksia -> Esim. tulostuksien (print-funktio) muuttamisen.
    # Kutsutaan funkioita hae_varaukset, joka palauttaa kaikki varaukset oikeilla tietotyypeillä
    varaukset = hae_varaukset("varaukset.txt")

    printConfirmedReservations(varaukset)
    printLongReservations(varaukset)
    printReservationStatus(varaukset)
    printSummary(varaukset)
    printTotalIncome(varaukset)

    #Bonus shittii
    
    printHighestIncomeReservation(varaukset)
    printReservationsPerDay(varaukset)
    printFilterByRoom(varaukset)
    printFilterUntilDate(varaukset)
    printAverageDurationForConfirmedReservations(varaukset)

def printConfirmedReservations(varaukset):
    print(f'\n{FontColor.BLUE}1) Vahvistetut varaukset{FontColor.RESET}')
    for reservation in varaukset:
         if reservation[RData.confirmed]:
            print(f'- {reservation[RData.name]}, {reservation[RData.room]}, {ChangeToFinnishDate(reservation[RData.date])} klo {ChangeToFinnishTime(reservation[RData.startTime])}')

def printLongReservations(varaukset):
    print('\n2) Pitkät varaukset (≥ 3 h)')
    for reservation in varaukset:
        if reservation[RData.duration] >= 3:
            print(f'- {reservation[RData.name]}, {ChangeToFinnishDate(reservation[RData.date])} klo {ChangeToFinnishTime(reservation[RData.startTime])}, kesto {reservation[RData.duration]} h, {reservation[RData.room]}')

def printReservationStatus(varaukset):
    print('\n3) Varausten vahvistusstatus')
    for reservation in varaukset:
        status = "Vahvistettu" if reservation[RData.confirmed] else "EI vahvistettu"
        print(f'{reservation[RData.name]} → {status}')

def printSummary(varaukset):
    confirmed_count = sum(1 for r in varaukset if r[RData.confirmed])
    unconfirmed_count = len(varaukset) - confirmed_count

    print('\n4) Yhteenveto vahvistuksista')
    print(f'- Vahvistettuja varauksia: {confirmed_count} kpl')
    print(f'- Ei-vahvistettuja varauksia: {unconfirmed_count} kpl')

def printTotalIncome(varaukset):
    total_income = sum(r[RData.duration] * r[RData.price] for r in varaukset if r[RData.confirmed])
    print('\n5) Vahvistettujen varausten kokonaistulot')
    print(f'Vahvistettujen varausten kokonaistulot: {str(total_income).replace(".",",")} €')

def printHighestIncomeReservation(varaukset):
    highest_income = 0
    highest_reservation = None
    for reservation in varaukset:
            income = reservation[RData.duration] * reservation[RData.price]
            if income > highest_income:
                highest_income = income
                highest_reservation = reservation
                
    if highest_reservation:
        print('\nKallein varaus:')
        print(f'- Nimi: {highest_reservation[RData.name]}')
        print(f'- Varattu tila: {highest_reservation[RData.room]}')
        print(f'- Päivämäärä: {ChangeToFinnishDate(highest_reservation[RData.date])}')
        print(f'- Aloitusaika: {ChangeToFinnishTime(highest_reservation[RData.startTime])}')
        print(f'- Kesto: {highest_reservation[RData.duration]} h')
        print(f'- Kokonaishinta: {str(highest_reservation[RData.price]).replace(".",",")} €')

def printReservationsPerDay(varaukset):
    reservations_per_day = {}
    for reservation in varaukset:
        date = reservation[RData.date]
        if date in reservations_per_day:
            reservations_per_day[date] += 1
        else:
            reservations_per_day[date] = 1
                
    print('\nVarausten määrä per päivä:')
    for date in sorted(reservations_per_day.keys()):
      count = reservations_per_day[date]
      print(f'- {ChangeToFinnishDate(date)}: {count} kpl')

def printFilterByRoom(varaukset):

    allRooms = []
    for v in varaukset:      
        if v[RData.room] not in allRooms:
            allRooms.append(v[RData.room])
    print('\nValitse näytettävät varaukset tilan mukaan. Saatavilla olevat huoneet:')

    roomIndex = 1
    for r in allRooms:
        print(f'{roomIndex} = {r}')
        roomIndex += 1
    print('Kirjoita "s" skipataksesi tämä vaihe.')
    while True:
        try:
            roomInput = input('\nAnna tilan numero: ')
            if roomInput == 's':
                return
            elif 1 <= int(roomInput) <= len(allRooms):
                roomChoice = allRooms[int(roomInput) - 1]
                print(f'\nVarausten suodatus tilan mukaan: {roomChoice}')
                for reservation in varaukset:
                     if reservation[RData.room] == roomChoice:
                         print(f'- {reservation[RData.name]}, {reservation[RData.date]} klo {reservation[RData.startTime]}, kesto {reservation[RData.duration]} h')
                return
            else:
                print("Huone numeroa ei saatavilla! Yritä uudelleen.")
        except ValueError:
            print("Syötä huoneen numero.")

    


def printFilterUntilDate(varaukset):
    print('\nValitse näytettävät varaukset valittuun päivämäärään asti.')
    print('Kirjoita "s" skipataksesi tämä vaihe.')
    while True:
        try:
            dateInput = input('Anna validi päivämäärä muodossa *pp.kk.yyyy*: ')
            if dateInput == 's':
                return
            elif datetime.strptime(dateInput, "%d.%m.%Y"):               
                date = datetime.strptime(dateInput, "%d.%m.%Y").date()
                print(f'\nNäytetään varaukset päivämäärään {ChangeToFinnishDate(date)} asti.')
                for reservation in varaukset:
                        if reservation[RData.date] <= date:
                            print(f'- {reservation[RData.name]}, {ChangeToFinnishDate(reservation[RData.date])} klo {ChangeToFinnishTime(reservation[RData.startTime])}, kesto {reservation[RData.duration]} h')
                return
            else:
                print("???.")
        except ValueError:
            print("Syötä validi päivämäärä.")

    




def printAverageDurationForConfirmedReservations(varaukset):
    total_duration = 0
    confirmed_count = 0
    for reservation in varaukset:
            if reservation[RData.confirmed]:
                total_duration += reservation[RData.duration]
                confirmed_count += 1
                
    average_duration = total_duration / confirmed_count if confirmed_count > 0 else 0
    print(f'\nVahvistettujen varausten keskimääräinen kesto: {average_duration:.2f} h')

if __name__ == "__main__":
    main()

