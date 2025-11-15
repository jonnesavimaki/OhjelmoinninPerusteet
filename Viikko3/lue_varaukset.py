"""
Ohjelma joka lukee tiedostossa olevat varaustiedot
ja tulostaa ne konsoliin käyttäen funkitoita.
Alla esimerkkitulostus:

Varausnumero: 123
Varaaja: Anna Virtanen
Päivämäärä: 31.10.2025
Aloitusaika: 10.00
Tuntimäärä: 2
Tuntihinta: 19,95 €
Kokonaishinta: 39,90 €
Maksettu: Kyllä
Kohde: Kokoustila A
Puhelin: 0401234567
Sähköposti: anna.virtanen@example.com

"""
from datetime import datetime, timedelta

def hae_varausnumero(varaus):
    reservationNumber = varaus[0]
    return int(reservationNumber)

def hae_varaaja(varaus):
    name = varaus[1]
    return name

def hae_paiva(varaus):
    reservationStartDate = datetime.strptime(varaus[2], "%Y-%m-%d").date()
    reservationStartDate = reservationStartDate.strftime("%d.%m.%Y")
    return reservationStartDate

def hae_aloitusaika(varaus):
    reservationStartTime = datetime.strptime(varaus[3], "%H:%M").time()
    reservationStartTime = reservationStartTime.strftime("%H.%M")
    return reservationStartTime

def hae_lopetusaika(varaus):
    reservedHours = int(varaus[4])
    startDate = datetime.strptime(varaus[2], "%Y-%m-%d").date()
    startTime = datetime.strptime(varaus[3], "%H:%M").time()
    startDateTime = datetime.combine(startDate, startTime)
    endDateTime = startDateTime + timedelta(hours=reservedHours)
    endDateChange = endDateTime.date() != startDate

    newEndDate = endDateTime.strftime("%d.%m.%Y") if endDateChange else None
    newEndTime = endDateTime.strftime("%H.%M")
    return newEndDate, newEndTime


def hae_tuntimaara(varaus):
    reservationHours = varaus[4]
    return int(reservationHours)

def hae_tuntihinta(varaus):
    reservationHourRate = varaus[5]
    return reservationHourRate

def laske_kokonaishinta(varaus):
    totalCost = int(varaus[4]) * float(varaus[5])
    totalCost = round(totalCost, 2)
    return totalCost

def hae_maksettu(varaus):
    isPaid = varaus[6].lower() == 'true'
    return isPaid

def hae_kohde(varaus):
    reservationLocation = varaus[7]
    return reservationLocation

def hae_puhelin(varaus):
    phoneNumber = varaus[8]
    return phoneNumber

def hae_sahkoposti(varaus):
    emailAddress = varaus[9]
    return emailAddress

def tulosta_varaus(varaus):


    print(f"Varausnumero: {hae_varausnumero(varaus)}")
    print(f"Varaaja: {hae_varaaja(varaus)}")
    print(f"Päivämäärä: {hae_paiva(varaus)}")
    print(f"Aloitusaika: {hae_aloitusaika(varaus)}")
    endDate, endTime = hae_lopetusaika(varaus)
    if endDate != None:
        print(f"Lopetuspäivä: {endDate}")
    print(f"Lopetusaika: {endTime}")
    print(f"Tuntimäärä: {hae_tuntimaara(varaus)}")
    print(f"Tuntihinta: {hae_tuntihinta(varaus).replace('.', ',')} €")
    print(f"Kokonaishinta: {laske_kokonaishinta(varaus):.2f}".replace('.', ',') + " €")
    maksettu = "Kyllä" if hae_maksettu(varaus) else "Ei"
    print(f"Maksettu: {maksettu}")
    print(f"Kohde: {hae_kohde(varaus)}")
    print(f"Puhelin: {hae_puhelin(varaus)}")
    print(f"Sähköposti: {hae_sahkoposti(varaus)}")
    print()  # Tyhjä rivi varauksien väliin

def main(printSpecificPerson=False,specificPerson=''):
    # Maaritellaan tiedoston nimi suoraan koodissa
    varaukset = "varaukset.txt"

    found = False

    # Avataan tiedosto, luetaan ja splitataan sisalto
    with open(varaukset, "r", encoding="utf-8") as f:
        lines = f.read().strip().splitlines()
        
        for line in lines:
            varaus = line.split('|')
            if printSpecificPerson and hae_varaaja(varaus).strip().lower() != specificPerson.strip().lower():
                continue
            tulosta_varaus(varaus)
            found = True
    if printSpecificPerson and not found:
        print(f"Ei löytynyt varauksia henkilölle: {specificPerson.strip().title()}")

    # Toteuta loput funktio hae_varaaja(varaus) mukaisesti
    # Luotavat funktiota tekevat tietotyyppien muunnoksen
    # ja tulostavat esimerkkitulosteen mukaisesti

    
printSpecificPerson = input("Valitaanko vain yksittäinen henkilö? (Y) (Jätä tyhjäksi, jos tulostetaan kaikki.): ")
if printSpecificPerson.lower() == 'y':
        specificPerson = input("Valitse henkilö: ").strip().lower()
        main(True, specificPerson)
elif printSpecificPerson.lower() == '':
    main(False)
else:
    print("Virheellinen syöte!")
    exit()
    


    