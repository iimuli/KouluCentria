from enum import Enum

class ReservationEnum(Enum):
    name = 0
    date = 1
    startTime = 2
    duration = 3
    room = 4
    confirmed = 5
    price = 6
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
def main():

    
    reservations = "varaukset.txt"
    reservations_list = [] 

    with open(reservations , "r", encoding="utf-8") as f: 
        for line in f: 

            reservation = line.strip().split("|")
            newReservation = [] 

            newReservation.append(reservation[0]) #Varaajan nimi
            newReservation.append(reservation[1]) #Päivämäärä
            newReservation.append(reservation[2]) #Aloitusaika
            newReservation.append(str(reservation[3]))  #Tuntimäärä
            newReservation.append(reservation[4])  #Kohde
            newReservation.append(reservation[5] == 'True')  #Vahvistettu
            newReservation.append(str(reservation[6])) #Tuntihinta
            reservations_list.append(newReservation) 

    printConfirmedReservations(reservations_list)
    printLongReservations(reservations_list)
    printReservationStatus(reservations_list)
    printSummary(reservations_list)
    printTotalIncome(reservations_list)
    printHighestIncomeReservation(reservations_list)
    printReservationsPerDay(reservations_list)
    printFilterByRoom(reservations_list, input('\nAnna tilan nimi: '))
    printFilterUntilDate(reservations_list, input('\nAnna päivämäärä (pp.kk.vvvv): '))
    printAverageDurationForConfirmedReservations(reservations_list)

    
def printConfirmedReservations(reservations_list):
    print('1) Vahvistetut varaukset')
    for reservation in reservations_list:
            print(f'- {reservation[ReservationEnum.name.value]}, {reservation[ReservationEnum.room.value]}, {reservation[ReservationEnum.date.value]} klo {reservation[ReservationEnum.startTime.value]}')
    
def printLongReservations(reservations_list):
    print('\n2) Pitkät varaukset (≥ 3 h)')
    for reservation in reservations_list:
        if int(reservation[ReservationEnum.duration.value]) >= 3:
            print(f'- {reservation[ReservationEnum.name.value]}, {reservation[ReservationEnum.date.value]} klo {reservation[ReservationEnum.startTime.value]}, kesto {reservation[ReservationEnum.duration.value]} h, {reservation[ReservationEnum.room.value]}')

def printReservationStatus(reservations_list):
    print('\n3) Varausten vahvistusstatus')
    for reservation in reservations_list:
        status = "Vahvistettu" if reservation[ReservationEnum.confirmed.value] else "EI vahvistettu"
        print(f'{reservation[ReservationEnum.name.value]} → {status}')

def printSummary(reservations_list):
    confirmed_count = sum(1 for r in reservations_list if r[ReservationEnum.confirmed.value])
    unconfirmed_count = len(reservations_list) - confirmed_count

    print('\n4) Yhteenveto vahvistuksista')
    print(f'- Vahvistettuja varauksia: {confirmed_count} kpl')
    print(f'- Ei-vahvistettuja varauksia: {unconfirmed_count} kpl')

def printTotalIncome(reservations_list):
    total_income = sum(int(r[ReservationEnum.duration.value]) * int(r[ReservationEnum.price.value]) for r in reservations_list if r[ReservationEnum.confirmed.value])
    print('\n5) Vahvistettujen varausten kokonaistulot')
    print(f'Vahvistettujen varausten kokonaistulot: {total_income} €')

def printHighestIncomeReservation(reservations_list):
    highest_income = 0
    highest_reservation = None
    for reservation in reservations_list:
            income = int(reservation[ReservationEnum.duration.value]) * int(reservation[ReservationEnum.price.value])
            if income > highest_income:
                highest_income = income
                highest_reservation = reservation
                
    if highest_reservation:
        print('\nKallein varaus:')
        print(f'- Nimi: {highest_reservation[ReservationEnum.name.value]}')
        print(f'- Varattu tila: {highest_reservation[ReservationEnum.room.value]}')
        print(f'- Päivämäärä: {highest_reservation[ReservationEnum.date.value]}')
        print(f'- Aloitusaika: {highest_reservation[ReservationEnum.startTime.value]}')
        print(f'- Kesto: {highest_reservation[ReservationEnum.duration.value]} h')
        print(f'- Kokonaishinta: {highest_reservation[ReservationEnum.price.value]}')

def printReservationsPerDay(reservations_list):
    reservations_per_day = {}
    for reservation in reservations_list:
            date = reservation[ReservationEnum.date.value]
            if date in reservations_per_day:
                reservations_per_day[date] += 1
            else:
                reservations_per_day[date] = 1
                
    print('\nVarausten määrä per päivä:')
    for date, count in reservations_per_day.items():
        print(f'- {date}: {count} kpl')

def printFilterByRoom(reservations_list, room_name):
    print(f'\nVarausten suodatus tilan mukaan: {room_name}')
    for reservation in reservations_list:
            if reservation[ReservationEnum.room.value] == room_name:
                print(f'- {reservation[ReservationEnum.name.value]}, {reservation[ReservationEnum.date.value]} klo {reservation[ReservationEnum.startTime.value]}, kesto {reservation[ReservationEnum.duration.value]} h')

def printFilterUntilDate(reservations_list, end_date):
    print(f'\nVaraukset annetun päivämäärän jälkeen:')
    for reservation in reservations_list:
            if reservation[ReservationEnum.date.value] <= end_date:
                print(f'- {reservation[ReservationEnum.name.value]}, {reservation[ReservationEnum.date.value]} klo {reservation[ReservationEnum.startTime.value]}, kesto {reservation[ReservationEnum.duration.value]} h')

def printAverageDurationForConfirmedReservations(reservations_list):
    total_duration = 0
    confirmed_count = 0
    for reservation in reservations_list:
            if reservation[ReservationEnum.confirmed.value]:
                total_duration += int(reservation[ReservationEnum.duration.value])
                confirmed_count += 1
                
    average_duration = total_duration / confirmed_count if confirmed_count > 0 else 0
    print(f'\nVahvistettujen varausten keskimääräinen kesto: {average_duration:.2f} h')

if __name__ == "__main__":
    main()

