import argparse
import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime


def main():
    cik, documentType, date = argparser()

    print("Loading results...")

    url = searchCIK(cik, documentType, date)

    _13F = get13F(url)

    _13Ftxt = getTxt(_13F)

    txtdata = getData(_13Ftxt)

    holdings, totalShares = getHoldingsDictionary(txtdata)

    excelFileName = str(cik) + "-" + date + ".tsv"

    populateTSV(holdings, totalShares, excelFileName)

    print("Results loaded.")


def argparser():
    parser = argparse.ArgumentParser(description='Type in a ticker or CIK.')
    parser.add_argument('CIK', help='Type CIK')
    parser.add_argument("-t", "--documentType", default=13, help="Provide the document type.")
    parser.add_argument('-d', '--date', type=int, default=None, help='Enter a date to find the last document before that date. Date Format: YYYYMMDD')

    args = parser.parse_args()
    cik = args.CIK
    if args.documentType:
        documentType = args.documentType
    else:
        documentType = 13
    if args.date:
        date = args.date
    else:
        now = datetime.now()
        date = now.strftime("%Y%m%d")
    return cik, documentType, date


def searchCIK(parameter, documentType, date):
    if date == None:
        date = ""
    url = f"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={parameter}&type={documentType}&dateb={date}&count=40&scd=filings"
    return url


def get13F(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    table_a = soup.find(id="seriesDiv").find_all('tr')[1].find_all('a')[0]
    link = table_a.get('href')
    searchurl = "https://www.sec.gov" + link
    return searchurl


def getTxt(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    table_a = soup.select('#formDiv')[1].find_all('tr')[-1].find_all('a')[0]
    link = table_a.get('href')
    txturl = "https://www.sec.gov" + link
    return txturl


def getData(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    table = soup.find_all('informationtable')[0].find_all('infotable')
    return table


def getHoldingsDictionary(table):
    holdingsDictionary = dict()
    totalShares = 0
    for i in range(len(table)):
        name = table[i].find('nameofissuer').string
        shares = int(table[i].find('sole').string)
        value = int(table[i].find('value').string)
        totalShares += shares
        if name in holdingsDictionary:
            holdingsDictionary[name][0] += shares
            holdingsDictionary[name][1] += value
        else:
            holdingsDictionary[name] = [shares, value]

    return holdingsDictionary, totalShares


def populateTSV(holdingsDictionary, totalShares, filename):
    with open(f"output/{filename}", 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter="\t")
        writer.writerow(['Name of Issuer', 'Shares', 'Value of Shares', 'Percentage'])
        for key, value in holdingsDictionary.items():
            writer.writerow([key, value[0], value[1], value[0] / totalShares])


main()
