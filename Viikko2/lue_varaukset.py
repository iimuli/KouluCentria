from datetime import datetime
"""
Ohjelma joka lukee tiedostossa olevat varaustiedot
ja tulostaa ne konsoliin. Alla esimerkkitulostus:

Varausnumero: 123
Varaaja: Anna Virtanen
Päivämäärä: 31.10.2025
Aloitusaika: 10.00
Tuntimäärä: 2
Tuntihinta: 19.95 €
Kokonaishinta: 39.9 €
Maksettu: Kyllä
Kohde: Kokoustila A
Puhelin: 0401234567
Sähköposti: anna.virtanen@example.com

"""
def ReplaceDot(text): #Vaihtaa YHDEN pisteen pilkuksi
    newText = text.replace('.',',')
    return newText

def ChangeToFinnishDate(date): #Päivämäärä muunnos
    paiva = datetime.strptime(date, "%Y-%m-%d").date()
    return paiva.strftime("%d.%m.%Y")

def ChangeToFinnishTime(time): #Aika muutos
    aika = datetime.strptime(time, "%H:%M").time()
    return aika.strftime("%H.%M")

def CheckIfPaid(paid): #Onko maksettu? palauta teksti
    text = paid.strip()

    if(text == "True"):  return 'Kyllä'
    elif(text == "False"):  return 'Ei'
    else:  return 'Virhe'

def CheckIfReservationWithin(reservationTime, startTime, endTime): #Selvittää, onko varaus aika aloitus-loppu ajan välillä
    reservation = datetime.strptime(reservationTime.replace('.', ':'), "%H:%M").time()
    start = datetime.strptime(startTime, "%H:%M").time()
    end = datetime.strptime(endTime, "%H:%M").time()

    return start <= reservation <= end #Palauttaa joko True/False

def main():
    reservations = "varaukset.txt"
    startTime = '08:00'
    endTime = '12:00'

    printUnpaid = False #True, jos halutaan printata myös maksaneet
    printAllTimes = False #True, jos halutaan printata kaikki ajat

    prefix_list = [
        'Varausnumero',
        'Varaaja',
        'Päivämäärä',
        'Aloitusaika',
        'Tuntimäärä',
        'Tuntihinta',
        'Kokonaishinta',
        'Maksettu',
        'Kohde',
        'Puhelin',
        'Sähköposti',
        ]

    value_list = [] #Lista kaikista varauksista (Tyhjä tällä hetkellä)
    totalPrice = 0 #Tämän hetkinen kokonaishinta
    paidAmount = 0 #Jos maksettu, lisää tähän

    with open(reservations , "r", encoding="utf-8") as f: #Lue txt tiedosto
        for line in f: #Lue jokainen rivi erikseen

            reservation = line.strip().split("|")  #Tee lista ja eristä tiedot | välillä
            newReservation = [] #Luo uusi varaus

            newReservation.append(reservation[0]) #0Varausnumero  ------- append -> lisää listaan
            newReservation.append(reservation[1]) #1Varaaja
            newReservation.append(ChangeToFinnishDate(reservation[2])) #2Päivämäärä
            newReservation.append(ChangeToFinnishTime(str(reservation[3]))) #3Aloitusaika
            newReservation.append(str(reservation[4]))  #4Tuntimäärä
            newReservation.append(ReplaceDot(str(reservation[5])) + ' €') #5Tuntihinta

            price = float(reservation[5]) * int(reservation[4]) #Laske tunnit * hinta
            totalPrice += price #Lisää kokonais hintaan

            newReservation.append(ReplaceDot(str(price)) + ' €') #6Kokonaishinta
            newReservation.append(CheckIfPaid(reservation[6])) #7 Onko maksettu
            if(reservation[6] == 'True'): paidAmount += price #Jos maksettu, lisää maksettuihin

            newReservation.append(reservation[7]) #8Kohde
            newReservation.append(reservation[8]) #9Puhelin
            newReservation.append(reservation[9]) #10Sähköposti
  
            value_list.append(newReservation) #Lisää uusi varaus listaan






    totalReservations = len(value_list) #Varausten määrä
    print('--------------------------------------------------------------------------------------')
    print('Reservations:')
    for i in range(totalReservations): #Jokaista varausta kohtaan ->  
        if (printUnpaid == False and value_list[i][7] == 'Ei'): #Verrataan boolean ja onko maksettu
            continue   
        if (printAllTimes == False and CheckIfReservationWithin(value_list[i][3], startTime, endTime) == False): #Verrataan boolean ja onko aikamääreessä
            continue        
        print('--------------------------------------------------')
        for p in range(len(prefix_list)): #Tulostaa jokaisen varaus tiedon (oletus 11 tieto per varaus, muutoin error)
            print(prefix_list[p] + ': ' + str(value_list[i][p])) 
    print('--------------------------------------------------------------------------------------')
    print(f'Total price: {ReplaceDot(str(round(totalPrice, 2)))} €, Paid amount: {ReplaceDot(str(round(paidAmount, 2)))} €') #Pyöristää kokonaishinnan kahteen decimaaliin

if __name__ == "__main__":
    main()