import json
import os
from datetime import datetime, timedelta
import locale

locale.setlocale(locale.LC_TIME, 'it_IT')


def extractDataFromJSON(nameFile: str) -> dict:

    path: str = os.path.join('resource', nameFile)
    try:
        with open(path) as f:
            data: dict = json.load(f)
        return data
    except FileNotFoundError:
        raise FileNotFoundError(f"Errore: Il file {nameFile} non è stato trovato.")



def extractMatchInCasa(data: dict) -> list:
    
    partiteInCasa: list = [partita for partita in data  if partita['homeTeam'] == 'Napoli']
    partiteInCasa.sort(key=lambda partita: datetime.strptime(partita['date'], '%d %b'))
    
    return partiteInCasa

def returnNextMatchTaskSchedulte(partiteInCasa: list) -> str:

    dataAttuale =  datetime.now()
    prossimaPartita = None

    for partita in partiteInCasa:
        dataPartita = datetime.strptime(partita['date'], '%d %b')
        if dataAttuale.month == 12 and dataPartita.month < 12: 
            dataPartita = dataPartita.replace(year=dataAttuale.year + 1)
        else: 
            dataPartita = dataPartita.replace(year=dataAttuale.year)
        dataNotifica = dataPartita - timedelta(days=3)
        
        if dataNotifica.date() == dataAttuale.date():
            prossimaPartita = partita
            break
    if prossimaPartita: 
        return (f"La prossima partita è: {prossimaPartita['date']} {prossimaPartita['time']}: {prossimaPartita['homeTeam']} vs {prossimaPartita['awayTeam']}") 

def findNextMatch(partiteInCasa: list) -> str:
    """
    Trova la prossima partita in casa.
    
    :param partiteInCasa: Lista delle partite in casa.
    :return: Dettagli della prossima partita.
    """
    dataAttuale = datetime.now()
    prossimaPartita = None
    minDiff = timedelta.max

    for partita in partiteInCasa:
        dataPartita = datetime.strptime(partita['date'], '%d %b')
        if dataAttuale.month == 12 and dataPartita.month < 12:
            dataPartita = dataPartita.replace(year=dataAttuale.year + 1)
        else:
            dataPartita = dataPartita.replace(year=dataAttuale.year)
        differenza = dataPartita - dataAttuale

        if timedelta(0) < differenza < minDiff:
            minDiff = differenza
            prossimaPartita = partita

    if prossimaPartita:
        return f"La prossima partita è: {prossimaPartita['date']} {prossimaPartita['time']}: {prossimaPartita['homeTeam']} vs {prossimaPartita['awayTeam']}"
    else:
        return "Nessuna partita in casa trovata."

def returnNextMatchTaskSchedulte() -> str:
    data = extractDataFromJSON('matches.json')
    partiteInCasa = extractMatchInCasa(data)
    return returnNextMatchTaskSchedulte(partiteInCasa)

def returnNextMatch() -> str:
    data = extractDataFromJSON('matches.json')
    partiteInCasa = extractMatchInCasa(data)
    return findNextMatch(partiteInCasa)