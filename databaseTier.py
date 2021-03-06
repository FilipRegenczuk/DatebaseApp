""" DatabaseTier module consists of connection to database and mechanisms of data """

import mysql.connector

class Database:

    def __init__(self):
        self.connection = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = '6015',
        database = 'del'
        )
        self.cursor = self.connection.cursor()
        

    def __del__(self):
        self.connection.close()


    def view(self):
        view = """
            SELECT id_danych, imie, nazwisko, imie_i_nazwisko_rodowe_ojca, imie_i_nazwisko_rodowe_matki, data_urodzenia, miejsce_urodzenia, kraj_pochodzenia, plec, pesel, stan_cywilny, obywatelstwo_lub_stan_bezpanstwowca, adres_zameldowania_na_pobyt_staly, kraj_miejsca_zamieszkania, kraj_poprzedniego_miejsca_zamieszkania, data_zgonu 
            FROM dane_osobowe
        """
        self.cursor.execute(view)
        rows = self.cursor.fetchall()
        return rows


    def search(self, pesel, name, surname):
        search = """
            SELECT id_danych, imie, nazwisko, imie_i_nazwisko_rodowe_ojca, imie_i_nazwisko_rodowe_matki, data_urodzenia, miejsce_urodzenia, kraj_pochodzenia, plec, pesel, stan_cywilny, obywatelstwo_lub_stan_bezpanstwowca, adres_zameldowania_na_pobyt_staly, kraj_miejsca_zamieszkania, kraj_poprzedniego_miejsca_zamieszkania, data_zgonu 
            FROM dane_osobowe 
            WHERE pesel=%s OR (imie=%s AND nazwisko=%s)
        """
        self.cursor.execute(search, (pesel, name, surname))
        rows = self.cursor.fetchall()
        return rows
        

    def insert(self, name, surname, father, mother, birthDate, birthCity, birthCountry, sex, pesel, state, nationality, address, country, countryPriev, deathDate):
        insert = """
            INSERT INTO dane_osobowe (imie, nazwisko, imie_i_nazwisko_rodowe_ojca, imie_i_nazwisko_rodowe_matki, data_urodzenia, miejsce_urodzenia, kraj_pochodzenia, plec, pesel, stan_cywilny, obywatelstwo_lub_stan_bezpanstwowca, adres_zameldowania_na_pobyt_staly, kraj_miejsca_zamieszkania, kraj_poprzedniego_miejsca_zamieszkania, data_zgonu) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        if countryPriev == "None" and deathDate == "None":
            self.cursor.execute(insert, (name, surname, father, mother, birthDate, birthCity, birthCountry, sex, pesel, state, nationality, address, country, None, None))
        elif countryPriev == "None":
            self.cursor.execute(insert, (name, surname, father, mother, birthDate, birthCity, birthCountry, sex, pesel, state, nationality, address, country, None, deathDate))
        elif deathDate == "None":
            self.cursor.execute(insert, (name, surname, father, mother, birthDate, birthCity, birthCountry, sex, pesel, state, nationality, address, country, countryPriev, None))
        else:
            self.cursor.execute(insert, (name, surname, father, mother, birthDate, birthCity, birthCountry, sex, pesel, state, nationality, address, country, countryPriev, deathDate))

        self.connection.commit()


    def update(self, id, name, surname, father, mother, birthDate, birthCity, birthCountry, sex, pesel, state, nationality, address, country, countryPriev, deathDate):
        update = """
            UPDATE dane_osobowe
            SET imie=%s, nazwisko=%s, imie_i_nazwisko_rodowe_ojca=%s, imie_i_nazwisko_rodowe_matki=%s, data_urodzenia=%s, miejsce_urodzenia=%s, kraj_pochodzenia=%s, plec=%s, pesel=%s, stan_cywilny=%s, obywatelstwo_lub_stan_bezpanstwowca=%s, adres_zameldowania_na_pobyt_staly=%s, kraj_miejsca_zamieszkania=%s, kraj_poprzedniego_miejsca_zamieszkania=%s, data_zgonu=%s, czy_edytowane='Y' 
            WHERE id_danych=%s
        """
        flagDown = """
            UPDATE dane_osobowe
            SET czy_edytowane = 'N'
            WHERE id_danych=%s
        """
        if countryPriev == "None" and deathDate == "None":
            self.cursor.execute(update, (name, surname, father, mother, birthDate, birthCity, birthCountry, sex, pesel, state, nationality, address, country, None, None, id))
        elif countryPriev == "None":
            self.cursor.execute(update, (name, surname, father, mother, birthDate, birthCity, birthCountry, sex, pesel, state, nationality, address, country, None, deathDate, id))
        elif deathDate == "None":
            self.cursor.execute(update, (name, surname, father, mother, birthDate, birthCity, birthCountry, sex, pesel, state, nationality, address, country, countryPriev, None, id))
        else:
            self.cursor.execute(update, (name, surname, father, mother, birthDate, birthCity, birthCountry, sex, pesel, state, nationality, address, country, countryPriev, deathDate, id))

        self.cursor.execute(flagDown, (id,))
        self.connection.commit()


    def insert_proporsal(self, id, service, newData):
        insert = """
            INSERT INTO wnioski (id_danych, typ_wniosku, nowe_dane)
            VALUES (%s, %s, %s)
        """
        self.cursor.execute(insert, (id, service, newData))
        self.connection.commit()


    def combobox_countries_input(self):
        data = []
        self.cursor.execute("SELECT * FROM widok_kraje")

        for row in self.cursor.fetchall():
            data.append(row[0])
        
        return data

    
    def combobox_states_input(self):
        data= []
        self.cursor.execute("SELECT * FROM widok_stany_cywilne")

        for row in self.cursor.fetchall():
            data.append(row[0])

        return data

    
    def combobox_services_input(self):
        data = []
        self.cursor.execute("SELECT typ_wniosku FROM uslugi")

        for row in self.cursor.fetchall():
            data.append(row[0])

        return data

    
    def view_history(self, id):
        view_history = """
            SELECT *
            FROM przeszle_dane_osobowe
            WHERE id_danych=%s
        """
        self.cursor.execute(view_history, (id,))
        rows = self.cursor.fetchall()
        return rows
