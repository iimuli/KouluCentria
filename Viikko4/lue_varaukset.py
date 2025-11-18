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

"""
Ohjelma joka tulostaa tiedostosta luettujen varausten alkiot ja niiden tietotyypit

varausId | nimi | sähköposti | puhelin | varauksenPvm | varauksenKlo | varauksenKesto | hinta | varausVahvistettu | varattuTila | varausLuotu
------------------------------------------------------------------------
201 | Muumi Muumilaakso | muumi@valkoinenlaakso.org | 0509876543 | 2025-11-12 | 09:00 | 2 | 18.50 | True | Metsätila 1 | 2025-08-12 14:33:20
int | str | str | str | datetime.date | datetime.time | int | float | bool | str | datetime
------------------------------------------------------------------------
202 | Niiskuneiti Muumilaakso | niisku@muumiglam.fi | 0451122334 | 2025-12-01 | 11:30 | 1 | 12.00 | False | Kukkahuone | 2025-09-03 09:12:48
int | str | str | str | datetime.date | datetime.time | int | float | bool | str | datetime
------------------------------------------------------------------------
203 | Pikku Myy Myrsky | myy@pikkuraivo.net | 0415566778 | 2025-10-22 | 15:45 | 3 | 27.90 | True | Punainen Huone | 2025-07-29 18:05:11
int | str | str | str | datetime.date | datetime.time | int | float | bool | str | datetime
------------------------------------------------------------------------
204 | Nipsu Rahapulainen | nipsu@rahahuolet.me | 0442233445 | 2025-09-18 | 13:00 | 4 | 39.95 | False | Varastotila N | 2025-08-01 10:59:02
int | str | str | str | datetime.date | datetime.time | int | float | bool | str | datetime
------------------------------------------------------------------------
205 | Hemuli Kasvikerääjä | hemuli@kasvikeraily.club | 0463344556 | 2025-11-05 | 08:15 | 2 | 19.95 | True | Kasvitutkimuslabra | 2025-10-09 16:41:55
int | str | str | str | datetime.date | datetime.time | int | float | bool | str | datetime
------------------------------------------------------------------------
"""
from datetime import datetime


def muunna_varaustiedot(varaus: list) -> list:
    # Tähän tulee siis varaus oletustietotyypeillä (str)
    # Varauksessa on 11 saraketta -> Lista -> Alkiot 0-10
    # Muuta tietotyypit haluamallasi tavalla -> Seuraavassa esimerkki ensimmäisestä alkioista
    muutettuvaraus = []
    # Ensimmäisen alkion = varaus[0] muunnos
    muutettuvaraus.append(int(varaus[0]))
    # Ja tästä jatkuu
    muutettuvaraus.append(varaus[1])
    muutettuvaraus.append(varaus[2])
    muutettuvaraus.append(varaus[3])
    muutettuvaraus.append(datetime.strptime(varaus[4], "%Y-%m-%d").date().strftime("%d.%m.%Y"))
    muutettuvaraus.append(datetime.strptime(varaus[5], "%H:%M").time().strftime("%H.%M"))
    muutettuvaraus.append(int(varaus[6]))
    muutettuvaraus.append(float(varaus[7]))
    muutettuvaraus.append(varaus[8] == "True")
    muutettuvaraus.append(varaus[9])
    muutettuvaraus.append(datetime.strptime(varaus[10], "%Y-%m-%d %H:%M:%S").strftime("%d.%m.%Y %H.%M.%S"))
    return muutettuvaraus

def hae_varaukset(varaustiedosto: str) -> list:
    # HUOM! Tälle funktioille ei tarvitse tehdä mitään!
    # Jos muutat, kommentoi miksi muutit
    varaukset = []
    varaukset.append(["varausId", "nimi", "sähköposti", "puhelin", "varauksenPvm", "varauksenKlo", "varauksenKesto", "hinta", "varausVahvistettu", "varattuTila", "varausLuotu"])
    with open(varaustiedosto, "r", encoding="utf-8") as f:
        for varaus in f:
            varaus = varaus.strip()
            varaustiedot = varaus.split('|')
            varaukset.append(muunna_varaustiedot(varaustiedot))
    return varaukset

def main():
    # HUOM! seuraaville riveille ei tarvitse tehdä mitään!
    # Jos muutat, kommentoi miksi muutit
    # Kutsutaan funkioita hae_varaukset, joka palauttaa kaikki varaukset oikeilla tietotyypeillä
    varaukset = hae_varaukset("varaukset.txt")
    print(" | ".join(varaukset[0]))
    print("------------------------------------------------------------------------")
    for varaus in varaukset[1:]:
        print(" | ".join(str(x) for x in varaus))
        tietotyypit = [type(x).__name__ for x in varaus]
        print(" | ".join(tietotyypit))
        print("------------------------------------------------------------------------")

if __name__ == "__main__":
    main()


#------------------------------------------------------------------------

# def hae_rivi(varaus, rivi):
#     with open(varaus, "r", encoding="utf-8") as f:
#         lines = f.readlines()
#         line = lines[rivi].strip().split("|")
#     return line



# def hae_varausnumero(varaus, rivi):      
#     return hae_rivi(varaus, rivi)[0]

# def hae_varaaja(varaus, rivi):
#     return hae_rivi(varaus, rivi)[1]

# def hae_paiva(varaus, rivi): 
#     return ChangeToFinnishDate(hae_rivi(varaus, rivi)[2])

# def hae_aloitusaika(varaus, rivi): 
#     return ChangeToFinnishTime(hae_rivi(varaus, rivi)[3])

# def hae_tuntimaara(varaus, rivi): 
#     return hae_rivi(varaus, rivi)[4]

# def hae_tuntihinta(varaus, rivi): 
#     return ReplaceDot(hae_rivi(varaus, rivi)[5]) + ' €'

# def laske_kokonaishinta(varaus, rivi): 
#     tuntimaara = int(hae_rivi(varaus, rivi)[4])
#     tuntihinta = float(hae_rivi(varaus, rivi)[5])
#     kokonaishinta = tuntimaara * tuntihinta
#     return ReplaceDot(str(round(kokonaishinta, 2))) + ' €'

# def hae_maksettu(varaus, rivi): 
#     return CheckIfPaid(hae_rivi(varaus, rivi)[6])

# def hae_kohde(varaus, rivi): 
#     return hae_rivi(varaus, rivi)[7]

# def hae_puhelin(varaus, rivi): 
#     return hae_rivi(varaus, rivi)[8]

# def hae_sahkoposti(varaus, rivi): 
#     return hae_rivi(varaus, rivi)[9]









# def main():

#     reservations = "varaukset.txt"

#     prefix_list = [
#         'Varausnumero',
#         'Varaaja',
#         'Päivämäärä',
#         'Aloitusaika',
#         'Tuntimäärä',
#         'Tuntihinta',
#         'Kokonaishinta',
#         'Maksettu',
#         'Kohde',
#         'Puhelin',
#         'Sähköposti',
#     ]
    
#     def_list = [
#         hae_varausnumero,
#         hae_varaaja,
#         hae_paiva,
#         hae_aloitusaika,
#         hae_tuntimaara,
#         hae_tuntihinta,
#         laske_kokonaishinta,
#         hae_maksettu,
#         hae_kohde,
#         hae_puhelin,
#         hae_sahkoposti,
 
#     ]

#     with open(reservations , "r", encoding="utf-8") as f: 
#             lines = f.readlines()

#     print('--------------------------------------------------------------------------------------')
#     print('Reservations:')
#     print('--------------------------------------------------')
#     for x in range(len(lines)):
#         for i in range(len(prefix_list)):
#             print(f'{prefix_list[i]}:  {def_list[i](reservations, x)}')
#         print('--------------------------------------------------------------------------------------')


# if __name__ == "__main__":
#     main()