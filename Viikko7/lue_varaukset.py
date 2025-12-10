# Copyright (c) 2025 Ville Heikkiniemi
#
# This code is licensed under the MIT License.
# You are free to use, modify, and distribute this code,
# provided that the original copyright notice is retained.
#
# See LICENSE file in the project root for full license information.

# Käytän sanakirjoja, koska ne helpottavat koodin luettavuutta, kun sisältö on heti nimessä

from datetime import datetime

def muunna_varaustiedot(varaus) -> dict:
    muutettu_varaus = {}
    muutettu_varaus["varausId"] = int(varaus[0])
    muutettu_varaus["nimi"] = varaus[1]
    muutettu_varaus["sähköposti"] = varaus[2]
    muutettu_varaus["puhelin"] = varaus[3]
    muutettu_varaus["varauksenPvm"] = datetime.strptime(varaus[4], "%Y-%m-%d").date()
    muutettu_varaus["varauksenKlo"] = datetime.strptime(varaus[5], "%H:%M").time()
    muutettu_varaus["varauksenKesto"] = int(varaus[6])
    muutettu_varaus["hinta"] = float(varaus[7])
    muutettu_varaus["varausVahvistettu"] = varaus[8].lower() == "true"
    muutettu_varaus["varattuTila"] = varaus[9]
    muutettu_varaus["varausLuotu"] = datetime.strptime(varaus[10], "%Y-%m-%d %H:%M:%S")
    return muutettu_varaus

def hae_varaukset(varaustiedosto: str) -> dict:
    varaukset = {}
    with open(varaustiedosto, "r", encoding="utf-8") as f:
        for varaus in f:
            varaus = varaus.strip()
            varaustiedot = varaus.split('|')
            varaukset[varaustiedot[0]] = muunna_varaustiedot(varaustiedot)
    return varaukset


def vahvistetut_varaukset(varaukset: dict):
    for varaus in varaukset.values():
        if varaus["varausVahvistettu"]:
            print(f"- {varaus['nimi']}, {varaus['varattuTila']}, {varaus['varauksenPvm'].strftime('%d.%m.%Y')} klo {varaus['varauksenKlo'].strftime('%H.%M')}")
    print()

def pitkat_varaukset(varaukset: dict):
    for varaus in varaukset.values():
        if(varaus["varauksenKesto"] >= 3):
            print(f"- {varaus['nimi']}, {varaus['varauksenPvm'].strftime('%d.%m.%Y')} klo {varaus['varauksenKlo'].strftime('%H.%M')}, kesto {varaus['varauksenKesto']} h, {varaus['varattuTila']}")

    print()

def varausten_vahvistusstatus(varaukset: dict):
    for varaus in varaukset.values():
        if(varaus["varausVahvistettu"]):
            print(f"{varaus['nimi']} → Vahvistettu")
        else:
            print(f"{varaus['nimi']} → EI vahvistettu")

    print()

def varausten_lkm(varaukset: dict):
    vahvistetutVaraukset = 0
    eiVahvistetutVaraukset = 0
    for varaus in varaukset.values():
        if(varaus["varausVahvistettu"]):
            vahvistetutVaraukset += 1
        else:
            eiVahvistetutVaraukset += 1

    print(f"- Vahvistettuja varauksia: {vahvistetutVaraukset} kpl")
    print(f"- Ei-vahvistettuja varauksia: {eiVahvistetutVaraukset} kpl")
    print()

def varausten_kokonaistulot(varaukset: dict):
    varaustenTulot = 0
    for varaus in varaukset.values():
        if(varaus["varausVahvistettu"]):
            varaustenTulot += varaus["varauksenKesto"]*varaus["hinta"]
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