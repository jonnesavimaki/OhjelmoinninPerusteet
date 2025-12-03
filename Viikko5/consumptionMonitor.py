# Copyright (c) 2025 Jonne Savimäki
# License: MIT
from datetime import datetime, date, time

def readFile(file: str) -> list:
    """Read CSV file and return data as a list of lists"""
    with open(file, "r", encoding="utf-8") as f:
        data = []
        for line in f:
            data.append(line.strip("\n").split(";"))
        del data[0]
        return data
    
def formatTime(data) -> list:
    """Converts date from ISO format to Finnish format"""
    dayOfWeek = ["Maanantai", "Tiistai", "Keskiviikko", "Torstai", "Perjantai", "Lauantai", "Sunnuntai"]
    for line in data:
        parsedDate = datetime.fromisoformat(line[0])
        weekDay = dayOfWeek[parsedDate.weekday()]
        parsedDate = parsedDate.strftime("%d.%m.%Y")
        line.insert(0, weekDay)
        line[1] = parsedDate
    return data

def convertWhToKWh(data) -> list:
    """Converts Wh to kWh"""
    for line in data:
        line[2] = float(line[2]) / 1000
        line[3] = float(line[3]) / 1000
        line[4] = float(line[4]) / 1000
        line[5] = float(line[5]) / 1000
        line[6] = float(line[6]) / 1000
        line[7] = float(line[7]) / 1000
    return data

def groupDays(data) -> list:
    """Converts raw data and groups data by days"""
    maanantai = []
    tiistai = []
    keskiviikko = []
    torstai = []
    perjantai = []
    lauantai = []
    sunnuntai = []
    week = [None, None, None, None, None, None, None]
    for line in data:
        if line[0] == "Maanantai":
            maanantai.append(line[2:8])
            week[0] = line[0:2]
        if line[0] == "Tiistai":
            tiistai.append(line[2:8])
            week[1] = line[0:2]
        if line[0] == "Keskiviikko":
            keskiviikko.append(line[2:8])
            week[2] = line[0:2]
        if line[0] == "Torstai":
            torstai.append(line[2:8])
            week[3] = line[0:2]
        if line[0] == "Perjantai":
            perjantai.append(line[2:8])
            week[4] = line[0:2]
        if line[0] == "Lauantai":
            lauantai.append(line[2:8])
            week[5] = line[0:2]
        if line[0] == "Sunnuntai":
            sunnuntai.append(line[2:8])
            week[6] = line[0:2]
    maanantai = [sum(col) for col in zip(*maanantai)]
    tiistai = [sum(col) for col in zip(*tiistai)]
    keskiviikko = [sum(col) for col in zip(*keskiviikko)]
    torstai = [sum(col) for col in zip(*torstai)]
    perjantai = [sum(col) for col in zip(*perjantai)]
    lauantai = [sum(col) for col in zip(*lauantai)]
    sunnuntai = [sum(col) for col in zip(*sunnuntai)]
    weekData = [maanantai, tiistai, keskiviikko, torstai, perjantai, lauantai, sunnuntai]

    for i, day in enumerate(weekData):
        for j, item in enumerate(day):
            val = round(float(item), 2)
            weekData[i][j] = str(val).replace(".", ",")
    return weekData, week

def main():
    """Prints the complete output"""
    file = "viikko42.csv"
    data = readFile(file)
    print("Viikon 42 sähkönkulutus ja -tuotanto (kWh, vaiheittain)")
    print("\nPäivä\t\tPvm\t\tKulutus [kWh]\t\t\tTuotanto [kWh]\n\t\t(pv.kk.vvvv)\tv1\tv2\tv3\t\tv1\tv2\tv3")
    print("------------------------------------------------------------------------------------")
    formatTime(data)
    convertWhToKWh(data)
    weekData = groupDays(data)
    print(f"{weekData[1][0][0]}\t{weekData[1][0][1]}\t{weekData[0][0][0]}\t{weekData[0][0][1]}\t{weekData[0][0][2]}\t\t{weekData[0][0][3]}\t{weekData[0][0][4]}\t{weekData[0][0][5]}")
    print(f"{weekData[1][1][0]}\t\t{weekData[1][1][1]}\t{weekData[0][1][0]}\t{weekData[0][1][1]}\t{weekData[0][1][2]}\t\t{weekData[0][1][3]}\t{weekData[0][1][4]}\t{weekData[0][1][5]}")
    print(f"{weekData[1][2][0]}\t{weekData[1][2][1]}\t{weekData[0][2][0]}\t{weekData[0][2][1]}\t{weekData[0][2][2]}\t\t{weekData[0][2][3]}\t{weekData[0][2][4]}\t{weekData[0][2][5]}")
    print(f"{weekData[1][3][0]}\t\t{weekData[1][3][1]}\t{weekData[0][3][0]}\t{weekData[0][3][1]}\t{weekData[0][3][2]}\t\t{weekData[0][3][3]}\t{weekData[0][3][4]}\t{weekData[0][3][5]}")
    print(f"{weekData[1][4][0]}\t{weekData[1][4][1]}\t{weekData[0][4][0]}\t{weekData[0][4][1]}\t{weekData[0][4][2]}\t\t{weekData[0][4][3]}\t{weekData[0][4][4]}\t{weekData[0][4][5]}")
    print(f"{weekData[1][5][0]}\t{weekData[1][5][1]}\t{weekData[0][5][0]}\t{weekData[0][5][1]}\t{weekData[0][5][2]}\t\t{weekData[0][5][3]}\t{weekData[0][5][4]}\t{weekData[0][5][5]}")
    print(f"{weekData[1][6][0]}\t{weekData[1][6][1]}\t{weekData[0][6][0]}\t{weekData[0][6][1]}\t{weekData[0][6][2]}\t\t{weekData[0][6][3]}\t{weekData[0][6][4]}\t{weekData[0][6][5]}")
if __name__ == "__main__":
    main()