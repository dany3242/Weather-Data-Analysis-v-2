import csv
import matplotlib.pyplot as plt

filename = "timestrafikk_sykkelmotorveien_juni_2026_innlagte_feil.csv"

while True:
    valgt_dato = input("Skriv inn en dato (YYYY-MM-DD, f.eks. 2026-06-03): ").strip()
    if len(valgt_dato) == 10 and valgt_dato[4] == '-' and valgt_dato[7] == '-':
        break
    else:
        print("Ugyldig datoformat. Vennligst bruk YYYY-MM-DD.")


data_stavanger = {}
data_sandnes = {}


try:
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter=';')
        
        for row in reader:
            if row['Dato'] == valgt_dato:
                felt = row['Felt']
                tid = row['Fra tidspunkt']
                
              
                try:
                    mengde = int(row['Trafikkmengde'])
                except ValueError:
                  
                    mengde = 0
                
    
                if felt == 'Totalt i retning Stavanger':
                    data_stavanger[tid] = mengde
                elif felt == 'Totalt i retning Sandnes':
                    data_sandnes[tid] = mengde
except FileNotFoundError:
    print(f"Feil: Fant ikke filen {filename}.")
    exit()


alle_timer = sorted(list(set(list(data_stavanger.keys()) + list(data_sandnes.keys()))))

if not alle_timer:
    print(f"Ingen data funnet for datoen {valgt_dato}. Sjekk om datoen er riktig.")
    exit()


y_stavanger = [data_stavanger.get(tid, 0) for tid in alle_timer]
y_sandnes = [data_sandnes.get(tid, 0) for tid in alle_timer]


plt.figure(figsize=(12, 6))
plt.plot(alle_timer, y_stavanger, label='Mot Stavanger', color='blue', marker='o')
plt.plot(alle_timer, y_sandnes, label='Mot Sandnes', color='red', marker='s')

plt.title(f"Sykkeltrafikk på {valgt_dato}")
plt.xlabel("Time")
plt.ylabel("Antall passeringer")
plt.xticks(rotation=45)
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()

plt.show()
