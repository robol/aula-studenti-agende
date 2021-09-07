# Agende / Aula Studenti

Questo script permette di creare gli slot per prenotare il proprio posto nelle aule
del dipartimento di Matematica, Pisa, creando gli slot su agende.unipi.it. 

Legge i cookie da Google Chrome, per riciclare la sessione attiva su agende.unipi.it, 
e fa delle chiamate AJAX per inserire gli slot richiesti. 

Per installare le dipendenze richieste:
```
python3 -mvenv env 
. env/bin/activate
pip3 install -r requirements.txt
```

Per creare dei nuovi slot:
```
. env/bin/activate
python3 ./genera2.py xxx-yyy-zzz 2021-09-10 2021-09-20 
```
Il numero di posti, orari, ecc., vanno modificati direttamente nel codice per ora. Gli 
orari sono UTC. 
