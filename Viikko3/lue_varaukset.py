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
Kohde: Kokoustila 
Puhelin: 0401234567
Sähköposti: anna.virtanen@example.com

"""

#OLIPA VAIKEE TEHÄ FUNKTIOIL TÄMMÖNEN PÖKÄLE OMASTA MIELESTÄ VIIKKO2 OPTIMOINNIN JÄLKEEN
#YRITÄN YLEENSÄ MINIMOIDA SAMOJEN KOODIEN TOISTAMISTA

def hae_rivi(varaus, rivi):
    with open(varaus, "r", encoding="utf-8") as f:
        lines = f.readlines()
        line = lines[rivi].strip().split("|")
    return line



def hae_varausnumero(varaus, rivi):      
    return hae_rivi(varaus, rivi)[0]

def hae_varaaja(varaus, rivi):
    return hae_rivi(varaus, rivi)[1]

def hae_paiva(varaus, rivi): 
    return ChangeToFinnishDate(hae_rivi(varaus, rivi)[2])

def hae_aloitusaika(varaus, rivi): 
    return ChangeToFinnishTime(hae_rivi(varaus, rivi)[3])

def hae_tuntimaara(varaus, rivi): 
    return hae_rivi(varaus, rivi)[4]

def hae_tuntihinta(varaus, rivi): 
    return ReplaceDot(hae_rivi(varaus, rivi)[5]) + ' €'

def laske_kokonaishinta(varaus, rivi): 
    tuntimaara = int(hae_rivi(varaus, rivi)[4])
    tuntihinta = float(hae_rivi(varaus, rivi)[5])
    kokonaishinta = tuntimaara * tuntihinta
    return ReplaceDot(str(round(kokonaishinta, 2))) + ' €'

def hae_maksettu(varaus, rivi): 
    return CheckIfPaid(hae_rivi(varaus, rivi)[6])

def hae_kohde(varaus, rivi): 
    return hae_rivi(varaus, rivi)[7]

def hae_puhelin(varaus, rivi): 
    return hae_rivi(varaus, rivi)[8]

def hae_sahkoposti(varaus, rivi): 
    return hae_rivi(varaus, rivi)[9]






def ReplaceDot(text): #Vaihtaa pisteen pilkuksi
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


def main():

    reservations = "varaukset.txt"

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
    
    def_list = [
        hae_varausnumero,
        hae_varaaja,
        hae_paiva,
        hae_aloitusaika,
        hae_tuntimaara,
        hae_tuntihinta,
        laske_kokonaishinta,
        hae_maksettu,
        hae_kohde,
        hae_puhelin,
        hae_sahkoposti,
 
    ]

    with open(reservations , "r", encoding="utf-8") as f: 
            lines = f.readlines()

    print('--------------------------------------------------------------------------------------')
    print('Reservations:')
    print('--------------------------------------------------')
    for x in range(len(lines)):
        for i in range(len(prefix_list)):
            print(f'{prefix_list[i]}:  {def_list[i](reservations, x)}')
        print('--------------------------------------------------------------------------------------')


if __name__ == "__main__":
    main()