# FipavMoToIcalendar
Generatore di file .ics per i calendari FIPAV regionali disponibili al sito: https://www.fipav.mo.it/fipav/index.jsp

## Setup
E' indispensabile aver installato [python](https://www.python.org/downloads/). 

E' consigliato l'uso di [pip](https://pip.pypa.io/en/stable/installation/) per l'installazione dei moduli aggiuntivi.

Installazione moduli aggiuntivi:

MacOS/Linux:
```shell
python -m pip install -r requirements.txt
```

Windows:
```batch
py -m pip install -r requirements.txt
```

## Utilizzo
Salvare lo script `main.py` in un cartella.

Aprire la riga di comando e scrivere:
```
python main.py
```

Successivamente inserire il link del campionato che si vuole esportare. E' possibile sia inserire il link di un intero campionato (es. quello 1 Divisione) ma anche inserire il link che di un campionato visualizza solo le partite di una singola squadra.
A seconda della tipologia di link verrá creato un file che contiene tutte le partite del campionato di tutte le squadre oppure tutte le partite di un campionato di una singola squadra.

Il programma creerá un file `.ics` nella stessa cartella che poi potrá essere importato su google calendar.


## License
The project is under MIT license and it's in no way affiliated with FIPAV