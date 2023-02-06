from bs4 import BeautifulSoup
import requests
from icalendar import vCalAddress, vText, Calendar, Event
import pytz
import tempfile, os
from datetime import datetime
import sys

# TODO: devi sistamare le eccezioni in questa funzione

def get_address(numero_gara):
    
    page = requests.get("https://www.fipav.mo.it/fipav/new/dettagliogara.jsp?gara=" + str(numero_gara))

    # link_gmaps = corpopagina.select('iframe')[0].get("src") # alla fine non ho usato questa strada, ma puoi sempre cambiare

    dati_partita = BeautifulSoup(page.content, 'html.parser').find('div', class_="corpopagina").get_text()
    inizio_indirizzo = dati_partita.find("Palestra")
    fine_indirizzo = dati_partita.find("Risultato")
    return dati_partita[inizio_indirizzo:fine_indirizzo].replace("\n", " ")

def main():
    # url = str(sys.argv[1]) 
    print("Inserici il link del calendario che vuoi esportare (supporta sia il link dell'intero campionato sia quello che visualizza le partite della singola squadra)")
    url = input()

    try:
        page = requests.get(url,timeout=3)
        page.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        raise SystemExit(errh)
    except requests.exceptions.ConnectionError as errc:
        raise SystemExit(errc)
    except requests.exceptions.Timeout as errt:
        raise SystemExit(errt)
    except requests.exceptions.RequestException as err:
        raise SystemExit(err)

    soup = BeautifulSoup(page.content, 'html.parser')

    campionato = soup.select('div h1')[0].get_text()
    campionato = ' '.join(campionato.split())

    corpopagina = soup.find_all('table')[1]
    partite = corpopagina.find_all('tr', class_="dispari") + corpopagina.find_all('tr', class_="pari")
    
    print("Ho trovato " + str(len(partite)) + " partite")

    cal = Calendar()
    cal.add('prodid', '-//My calendar product//mxm.dk//')
    cal.add('version', '2.0')

    for partita in partite:
        numero_gara = partita.select('td a')[0].get("href")[-5:]
        print("Sto analizzando la gara numero: " + str(numero_gara))

        data = partita.find_all('td')[2].get_text()
        orario = partita.find_all('td')[4].get_text()
        squadra1 = partita.find_all('td')[5].get_text()
        squadra2 = partita.find_all('td')[6].get_text()
        indirizzo = get_address(numero_gara)

        event = Event()
        event.add('summary', str(squadra1 + " - " + squadra2))
        event['location'] = indirizzo
        event.add('dtstart', datetime(int(data[-4:]),int(data[3:5]),int(data[0:2]),int(orario[0:2]),int(orario[-2:]),0,tzinfo=pytz.timezone("Europe/Vienna")))
        event.add('dtend', datetime(int(data[-4:]),int(data[3:5]),int(data[0:2]),int(orario[0:2])+2,int(orario[-2:]),0,tzinfo=pytz.timezone("Europe/Vienna")))
        cal.add_component(event)

    f = open(str(nome_campionato) + '.ics', 'wb')
    f.write(cal.to_ical())
    f.close()
    
    # print(cal.to_ical().decode("utf-8")) # stampa su stdout il file 
    print('File "' + str(campionato) + '.ics"' + ' creato')

if __name__ == "__main__":
    main()
