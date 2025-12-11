# Copyright (c) 2025 Jonne Savimäki
# License: MIT
from datetime import datetime, date, timedelta


def importFileAsList(filePath: str) -> list:
    """Imports file as list, removes first line and splits at semicolon"""
    data = []
    with open(filePath, 'r', encoding='utf-8') as file:
        for line in file:
            data.append(line.strip().split(';'))
        del data[0]  # Remove header
    return data

def convertListToDict(dataList: list) -> list:
    """Converts list to list of dicts, where each dict represents a row with proper data types"""
    dictList = []
    for item in dataList:
        dataDict = {
            "date" : datetime.fromisoformat(item[0]).date(),
            "consumption" : float(item[1].replace(',', '.')),
            "production" : float(item[2].replace(',', '.')),
            "dailyTemp" : float(item[3].replace(',', '.'))
        }
        dictList.append(dataDict)
    return dictList

def groupByDate(dictList: list) -> dict:
    """Groups data by date, summing consumption and production, keeping dailyTemp"""
    groupedData = {}
    for each in dictList:
        day = each['date']
        if day not in groupedData:
            groupedData[day] = {
                "consumption": 0.0,
                "production": 0.0,
                "dailyTemp": []
            }
        groupedData[day]['consumption'] += each['consumption']
        groupedData[day]['production'] += each['production']
        groupedData[day]['dailyTemp'] = each['dailyTemp']
    return groupedData




def mainInput(groupedData: dict):
    """Handles main user input for report type selection"""
    mainChoice = input("Valitse raporttityyppi:\n1) Päiväkohtainen raportti aikaväliltä\n2) Kuukausikohtainen yhteenveto yhdelle kuukaudelle\n3) Vuoden 2025 kokonaisyhteenveto\n4) Lopeta ohjelma\n")
    if mainChoice == '1':
        return reportFromTimeRange(groupedData)
    if mainChoice == '2':
        return reportFromMonth(groupedData)
    if mainChoice == '3':
        return reportYearlySummary(groupedData)
    if mainChoice == '4':
        exit()

def secondaryInput(reportData: dict, groupedData: dict):
    """Handles secondary user input after report generation"""
    secondaryChoice =input("Mitä haluat tehdä seuraavaksi?\n1) Kirjoita raportti tiedostoon raportti.txt\n2) Luo uusi raportti\n3) Lopeta\n")
    if secondaryChoice == '1':
        writeReportToFile(reportData, groupedData)
    if secondaryChoice == '2':
        reportData = mainInput(groupedData)
        secondaryInput(reportData, groupedData)
    if secondaryChoice == '3':
        exit()

def reportFromTimeRange(groupedData: dict) -> dict:
    """Generates report from user-defined time range"""
    startDate = input("Anna alkupäivä (pp.kk.vvvv): ")
    endDate = input("Anna loppupäivä (pp.kk.vvvv): ")
    startDateObj = datetime.strptime(startDate, "%d.%m.%Y").date()
    endDateObj = datetime.strptime(endDate, "%d.%m.%Y").date()

    print(f"Raportti ajalta {startDate} - {endDate}:")
    dateRangeData = []
    while startDateObj <= endDateObj:
        dateRangeData.append({
            "consumption": groupedData.get(startDateObj, {}).get("consumption", 0.0),
            "production": groupedData.get(startDateObj, {}).get("production", 0.0),
            "dailyTemp": groupedData.get(startDateObj, {}).get("dailyTemp", None)
        })

        startDateObj += timedelta(days=1)
    totalConsumption = sum(day["consumption"] for day in dateRangeData)
    totalProduction = sum(day["production"] for day in dateRangeData)
    totalConsumption = round(totalConsumption, 2)
    totalProduction = round(totalProduction, 2)
    totalConsumption = str(totalConsumption).replace('.', ',')
    totalProduction = str(totalProduction).replace('.', ',')
    
    # Filter out None values before calculating average
    temps = [day["dailyTemp"] for day in dateRangeData if day["dailyTemp"] is not None]
    avgTemp = sum(temps) / len(temps) if temps else 0.0
    
    print(f"Kulutus yhteensä: {totalConsumption} kWh")
    print(f"Tuotanto yhteensä: {totalProduction} kWh")
    print(f"Keskilämpötila: {avgTemp:.1f} °C")

    return {"type": "timeRange", "dateRange": (startDate, endDate), "dataToWrite": (totalConsumption, totalProduction, avgTemp)}
    


def reportFromMonth(groupedData: dict) -> dict:
    """Generates report for a specific month"""
 
    month = input("Anna kuukauden numero (1-12): ")
    monthInt = int(month)
    monthNames = ["Tammikuu", "Helmikuu", "Maaliskuu", "Huhtikuu", "Toukokuu", "Kesäkuu", "Heinäkuu", "Elokuu", "Syyskuu", "Lokakuu", "Marraskuu", "Joulukuu"]
    if monthInt == 12:
        endDateObj = date(2025, 12, 31)
    else:
        endDateObj = date(2025, monthInt + 1, 1) - timedelta(days=1)
    startDateObj = date(2025, monthInt, 1)
    startDate = startDateObj.strftime("%d.%m.%Y")
    endDate = endDateObj.strftime("%d.%m.%Y")

    print(f"Raportti ajalta {startDate} - {endDate}:")
    dateRangeData = []
    while startDateObj <= endDateObj:
        dateRangeData.append({
            "consumption": groupedData.get(startDateObj, {}).get("consumption", 0.0),
            "production": groupedData.get(startDateObj, {}).get("production", 0.0),
            "dailyTemp": groupedData.get(startDateObj, {}).get("dailyTemp", None)
        })

        startDateObj += timedelta(days=1)
    totalConsumption = sum(day["consumption"] for day in dateRangeData)
    totalProduction = sum(day["production"] for day in dateRangeData)
    totalConsumption = round(totalConsumption, 2)
    totalProduction = round(totalProduction, 2)
    totalConsumption = str(totalConsumption).replace('.', ',')
    totalProduction = str(totalProduction).replace('.', ',')
    
    # Filter out None values before calculating average
    temps = [day["dailyTemp"] for day in dateRangeData if day["dailyTemp"] is not None]
    avgTemp = sum(temps) / len(temps) if temps else 0.0
    
    print(f"Kulutus yhteensä: {totalConsumption} kWh")
    print(f"Tuotanto yhteensä: {totalProduction} kWh")
    print(f"Keskilämpötila: {avgTemp:.1f} °C")

    return {"type": "month", "dataToWrite": (monthNames[monthInt - 1], totalConsumption, totalProduction, avgTemp)}

def reportYearlySummary(groupedData: dict) -> dict: 
    startDateObj = date(2025, 1, 1)
    endDateObj = date(2025, 12, 31)
    dateRangeData = []
    while startDateObj <= endDateObj:
        dateRangeData.append({
            "consumption": groupedData.get(startDateObj, {}).get("consumption", 0.0),
            "production": groupedData.get(startDateObj, {}).get("production", 0.0),
            "dailyTemp": groupedData.get(startDateObj, {}).get("dailyTemp", None)
        })

        startDateObj += timedelta(days=1)
    totalConsumption = sum(day["consumption"] for day in dateRangeData)
    totalProduction = sum(day["production"] for day in dateRangeData)
    totalConsumption = round(totalConsumption, 2)
    totalProduction = round(totalProduction, 2)
    totalConsumption = str(totalConsumption).replace('.', ',')
    totalProduction = str(totalProduction).replace('.', ',')
    
    # Filter out None values before calculating average
    temps = [day["dailyTemp"] for day in dateRangeData if day["dailyTemp"] is not None]
    avgTemp = sum(temps) / len(temps) if temps else 0.0
    
    print(f"Kulutus yhteensä: {totalConsumption} kWh")
    print(f"Tuotanto yhteensä: {totalProduction} kWh")
    print(f"Keskilämpötila: {avgTemp:.1f} °C")


    return {"type": "year", "dataToWrite": (totalConsumption, totalProduction, avgTemp)}

def writeReportToFile(reportData: dict, groupedData: dict):
    """Writes the generated report to a text file"""
    with open('raportti.txt', 'w', encoding='utf-8') as file:
        if reportData["type"] == "month":
            month, totalConsumption, totalProduction, avgTemp = reportData["dataToWrite"]
            file.write(f"Kuukausikohtainen raportti:\n")
            file.write(f"Kuukausi: {month}\n")
        elif reportData["type"] == "timeRange":
            totalConsumption, totalProduction, avgTemp = reportData["dataToWrite"]
            startDate, endDate = reportData["dateRange"]
            file.write(f"Päiväkohtainen raportti:\n")
            file.write(f"Ajanjaksolta {startDate} - {endDate}\n")
        else:
            totalConsumption, totalProduction, avgTemp = reportData["dataToWrite"]
        file.write(f"Vuosiraportti:\n")
        file.write(f"Kulutus yhteensä: {totalConsumption} kWh\n")
        file.write(f"Tuotanto yhteensä: {totalProduction} kWh\n")
        file.write(f"Keskilämpötila: {avgTemp:.1f} °C\n")
    print("Raportti kirjoitettu tiedostoon raportti.txt")
    reportData = mainInput(groupedData)
    secondaryInput(reportData, groupedData)

def main():
    filePath = '2025.csv'
    dataList = importFileAsList(filePath)
    dictList = convertListToDict(dataList)
    groupedData = groupByDate(dictList)
    reportData = mainInput(groupedData)
    secondaryInput(reportData, groupedData)

if __name__ == "__main__":
    main()