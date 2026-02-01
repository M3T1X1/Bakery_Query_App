import random

import psycopg2
from faker import Faker

fake = Faker("pl_PL")

conn = psycopg2.connect(
    dbname='Bakery_Query_App',
    host="localhost",
    user="postgres",
    password="postgres",
    port="5432"
)

cur = conn.cursor()

def seed():
    print("Czyszczenie bazy danych...")
    tabele = ["Transakcje", "Wypieki", "Produkty", "Dostawcy", "Pracownicy", "Sklepy", "Adresy"]

    for tabela in tabele:
        cur.execute(f"TRUNCATE TABLE {tabela} RESTART IDENTITY CASCADE;")

    print("Baza wyczyszczona. Generowanie nowych danych...")
    adresy_ids = []
    for _ in range(5):
        cur.execute(
            "INSERT INTO Adresy (Wojewodztwo, Miasto, Ulica, Numer_domu_lub_mieszkania) VALUES (%s, %s, %s, %s) RETURNING ID_adresu",
            (fake.administrative_unit(), fake.city(), fake.street_name(), fake.building_number())
        )
        adresy_ids.append(cur.fetchone()[0])

    sklepy_ids = []
    for i in range(5):
        cur.execute(
            "INSERT INTO Sklepy (ID_adresu, Nazwa, Sklep_wlasnosciowy) VALUES (%s, %s, %s) RETURNING ID_sklepu",
            (random.choice(adresy_ids), f"Piekarnia {fake.company()}", fake.boolean())
        )
        sklepy_ids.append(cur.fetchone()[0])

    for _ in range(15):
        cur.execute(
            "INSERT INTO Pracownicy (Imie, Nazwisko, ID_adresu, Stanowisko, Zarobki) VALUES (%s, %s, %s, %s, %s)",
            (fake.first_name(), fake.last_name(), random.choice(adresy_ids),
             random.choice(['Piekarz', 'Sprzedawca', 'Kierownik']), random.uniform(3500, 8000))
        )

    dostawcy_ids = []
    for _ in range(4):
        cur.execute(
            "INSERT INTO Dostawcy (Nazwa, ID_adresu) VALUES (%s, %s) RETURNING ID_dostawcy",
            (fake.company(), random.choice(adresy_ids))
        )
        dostawcy_ids.append(cur.fetchone()[0])

    produkty_ids = []
    surowce_lista = ['Mąka pszenna', 'Drożdże', 'Sól', 'Cukier', 'Ziarna słonecznika', 'Jaja', 'Mleko']

    for surowiec in surowce_lista:
        cur.execute(
            "INSERT INTO Produkty (Nazwa, ID_dostawcy) VALUES (%s, %s) RETURNING ID_produktu",
            (surowiec, random.choice(dostawcy_ids))
        )
        produkty_ids.append(cur.fetchone()[0])

    for _ in range(30 - len(surowce_lista)):
        nazwa_surowca = random.choice(surowce_lista)
        cur.execute(
            "INSERT INTO Produkty (Nazwa, ID_dostawcy) VALUES (%s, %s) RETURNING ID_produktu",
            (nazwa_surowca, random.choice(dostawcy_ids))
        )
        produkty_ids.append(cur.fetchone()[0])


    wypieki_ids = []
    rodzaje_wypieku = ['Chleb żytni', 'Bułka kajzerka', 'Rogal maślany', 'Chleb razowy', 'Bagietka', 'Pączek']

    for _ in range(20):
        nazwa_wypieku = random.choice(rodzaje_wypieku)
        cur.execute(
            """INSERT INTO Wypieki (Nazwa, Cena_produkcji, Czas_wypiekania, ID_produktu, Gramatura)
               VALUES (%s, %s, %s, %s, %s) RETURNING ID_wypieku""",
            (
                f"{nazwa_wypieku}",
                random.uniform(1.0, 5.0),
                f"{random.randint(20, 60)} minutes",
                random.choice(produkty_ids),
                random.choice([50, 100, 500])
            )
        )
        wypieki_ids.append(cur.fetchone()[0])

    for _ in range(100):
        cur.execute(
            "INSERT INTO Transakcje (ID_wypieku, ID_sklepu, Ilosc, Cena) VALUES (%s, %s, %s, %s)",
            (random.choice(wypieki_ids), random.choice(sklepy_ids),
             random.randint(1, 10), random.uniform(2.5, 15.0))
        )

    conn.commit()
    print("Dane zostały pomyślnie wygenerowane!")

seed()
cur.close()
conn.close()