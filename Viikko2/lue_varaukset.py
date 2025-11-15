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

def main(printOnlyPaid=False, printOnlySpecificTimes=False):
    # Määritellään tiedoston nimi suoraan koodissa
    varaukset = "varaukset.txt"

    # Avataan tiedosto ja luetaan sisältö
    with open(varaukset, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

        totalHinta = 0.0

        for line in lines:
            varaus = line.split('|')

            varausnumero = int(varaus[0])
            tuntihinta = str(varaus[5])
            maksettu = varaus[6].lower() == 'true'
            varaustunnit = int(varaus[4])
            kokonaishinta = float(tuntihinta) * varaustunnit

            from datetime import datetime, timedelta
            day = datetime.strptime(varaus[2], "%Y-%m-%d").date()
            finnishDay = day.strftime("%d.%m.%Y")

            timeOfDay = datetime.strptime(varaus[3], "%H:%M").time()
            finnishTime = timeOfDay.strftime("%H.%M")

            start_datetime = datetime.combine(day, timeOfDay)
            end_datetime = start_datetime + timedelta(hours=varaustunnit)

            endDateChanged = end_datetime.date() != day
            newEndDate = end_datetime.strftime("%d.%m.%Y") if endDateChanged else None
            newEndTime = end_datetime.strftime("%H.%M")
            
            if printOnlyPaid and not maksettu:
                continue
            if printOnlySpecificTimes and not (8 <= timeOfDay.hour < 12):
                continue

            totalHinta += kokonaishinta


            print('Varausnumero: ',varaus[0])
            print('Varaaja: ',varaus[1])
            print('Päivämäärä: ',finnishDay)
            print('Aloitusaika: ',finnishTime)
            if endDateChanged: print('Lopetuspäivämäärä: ',newEndDate)
            print('Lopetuskellonaika: ',newEndTime)
            print('Tuntimäärä: ',varaustunnit)
            print('Tuntihinta: ',tuntihinta.replace(".", ","),' €')
            print('Kokonaishinta',str(round(kokonaishinta,2)).replace(".",","),' €')
            print(f"Maksettu: {'Kyllä' if maksettu else 'Ei'}")
            print('Kohde: ',varaus[7])
            print('Puhelin: ',varaus[8])
            print('Sähköposti: ',varaus[9])
            print()  # Tyhjä rivi varausten väliin
        print('Yhteensä kokonaishinta: ',str(float(round(totalHinta,2))).replace(".",","),' €')


printOnlyPaid = input("Tulostetaanko vain maksetut varaukset? (Y/n): ")
if printOnlyPaid == "Y" or printOnlyPaid == "y":
    printOnlyPaid = True
elif printOnlyPaid == "N" or printOnlyPaid == "n":
    printOnlyPaid = False
else:
    print("Virheellinen syöte!")
    exit()
printOnlySpecificTimes = input("Tulostetaanko vain 8-12 alkavat varaukset? (Y/n): ")
if printOnlySpecificTimes == "Y" or printOnlySpecificTimes == "y":
    printOnlySpecificTimes = True
elif printOnlySpecificTimes == "N" or printOnlySpecificTimes == "n":
    printOnlySpecificTimes = False
else:
    print("Virheellinen syöte!")
    exit()

main(printOnlyPaid, printOnlySpecificTimes)