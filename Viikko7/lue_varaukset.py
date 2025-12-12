# Copyright (c) 2025 Ville Heikkiniemi, modified by Juha Eemeli Väisänen
#
# This code is licensed under the MIT License.
# You are free to use, modify, and distribute this code,
# provided that the original copyright notice is retained.
#
# See LICENSE file in the project root for full license information.
#
#
#
# Käytössä kirjastomalli
# Selkeetähä se on, oon aina pyrkiny käyttää ensisijaisesti kirjastoja, koska dataa saa enemmän ja helpommin säilytettyä. 
# Joskus huuruissa tehnyt esim dictionary{dictionary}, hehe
# Peli projekteis taas käytän olio muotosia koodeja enemmän (C#)


from datetime import datetime


def hae_varaukset(varaustiedosto: str) -> list:
    varaukset = []

    with open(varaustiedosto, "r", encoding="utf-8") as f:
        for varaus in f:
            varaukset.append(muunnaMuumiKirjastoksi(varaus.strip().split('|')))
    return varaukset

def muunnaMuumiKirjastoksi(varaus_lista: list[str]) -> dict:
    
    muumiKirjasto = {}
    muumiKirjasto['id'] = varaus_lista[0]
    muumiKirjasto['nimi'] = varaus_lista[1]
    muumiKirjasto['sahkoposti'] = varaus_lista[2]
    muumiKirjasto['puhelin'] = varaus_lista[3]
    muumiKirjasto['paiva'] = datetime.strptime(varaus_lista[4], "%Y-%m-%d").date()
    muumiKirjasto['kellonaika'] = datetime.strptime(varaus_lista[5], "%H:%M").time()
    muumiKirjasto['kesto'] = int(varaus_lista[6])
    muumiKirjasto['hinta'] = float(varaus_lista[7])
    muumiKirjasto['vahvistettu'] = bool(varaus_lista[8] == "True")
    muumiKirjasto['kohde'] = varaus_lista[9]
    muumiKirjasto['luotu'] = datetime.strptime(varaus_lista[10], "%Y-%m-%d %H:%M:%S")

    return muumiKirjasto


def vahvistetut_varaukset(varaukset: list):
    for varaus in varaukset:
        if(varaus['vahvistettu']):
            print(f'- {varaus["nimi"]}, {varaus["kohde"]}, {varaus["nimi"]}, {varaus["paiva"].strftime("%d.%m.%Y")} klo {varaus["kellonaika"].strftime("%H.%M")}')

    print()

def pitkat_varaukset(varaukset: list):
    for varaus in varaukset:
        if(varaus['kesto'] >= 3):
            print(f"- {varaus['nimi']}, {varaus['paiva'].strftime('%d.%m.%Y')} klo {varaus['kellonaika'].strftime('%H.%M')}, kesto {varaus['kesto']} h, {varaus['kohde']}")

    print()

def varausten_vahvistusstatus(varaukset: list):
    for varaus in varaukset:
        if(varaus['vahvistettu']):
            print(f"{varaus['nimi']} → Vahvistettu")
        else:
            print(f"{varaus['nimi']} → EI vahvistettu")

    print()

def varausten_lkm(varaukset: list):
    vahvistetutVaraukset = 0
    eiVahvistetutVaraukset = 0
    for varaus in varaukset:
        if(varaus['vahvistettu']):
            vahvistetutVaraukset += 1
        else:
            eiVahvistetutVaraukset += 1

    print(f"- Vahvistettuja varauksia: {vahvistetutVaraukset} kpl")
    print(f"- Ei-vahvistettuja varauksia: {eiVahvistetutVaraukset} kpl")
    print()

def varausten_kokonaistulot(varaukset: list):
    varaustenTulot = 0
    for varaus in varaukset:
        if(varaus['vahvistettu']):
            varaustenTulot += varaus['hinta']*varaus['kesto']
    print("Vahvistettujen varausten kokonaistulot:", f"{varaustenTulot:.2f}".replace('.', ','), "€")
    print()



def main():
    varaukset = hae_varaukset("varaukset.txt")
    print("1) Vahvistetut varaukset")
    vahvistetut_varaukset(varaukset)
    print("2) Pitkät varaukset (≥ 3 h)")
    pitkat_varaukset(varaukset)
    print("3) Varausten vahvistusstatus")
    varausten_vahvistusstatus(varaukset)
    print("4) Yhteenveto vahvistuksista")
    varausten_lkm(varaukset)
    print("5) Vahvistettujen varausten kokonaistulot")
    varausten_kokonaistulot(varaukset)

if __name__ == "__main__":
    main()