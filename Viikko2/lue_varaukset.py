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

def main():
    # Määritellään tiedoston nimi suoraan koodissa
    varaukset = "varaukset.txt"

    # Avataan tiedosto ja luetaan sisältö
    with open(varaukset, "r", encoding="utf-8") as f:
        varaus = f.read().strip()

    varaus = varaus.split('|')

    varausnumero = int(varaus[0])
    tuntihinta = str(varaus[5])
    maksettu = bool(varaus[6])
    varaustunnit = int(varaus[4])

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




    print('Varausnumero: ',varaus[0])
    print('Varaaja: ',varaus[1])
    print('Päivämäärä: ',finnishDay)
    print('Aloitusaika: ',finnishTime)
    if endDateChanged: print('Lopetuspäivämäärä: ',newEndDate)
    print('Lopetuskellonaika: ',newEndTime)
    print('Tuntimäärä: ',varaustunnit)
    print('Tuntihinta: ',tuntihinta.replace(".", ","),' €')
    print('Kokonaishinta',str(float(tuntihinta)*varaustunnit).replace(".",","),' €')
    print(f"Maksettu: {'Kyllä' if maksettu else 'Ei'}")
    print('Kohde: ',varaus[7])
    print('Puhelin: ',varaus[8])
    print('Sähköposti: ',varaus[9])


if __name__ == "__main__":
    main()