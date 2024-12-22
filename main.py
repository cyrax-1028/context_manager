import psycopg2
from colorama import Fore, init

init(autoreset=True)

def connect_db():
    return psycopg2.connect(
        database="najot_talim",
        user="postgres",
        password="1",
        host="localhost",
        port="5432"
    )

class Person:
    def __init__(self, id, name, age):
        self.id = id
        self.name = name
        self.age = age

    @staticmethod
    def get_all_person():
        with connect_db() as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT * FROM person')
                for row in cur:
                    yield Person(row[0], row[1], row[2])

    @staticmethod
    def get_one_person(id):
        with connect_db() as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT * FROM person WHERE id = %s', (id,))
                row = cur.fetchone()
                if row:
                    return Person(row[0], row[1], row[2])
                return None

    @staticmethod
    def add_person(name, age):
        with connect_db() as conn:
            with conn.cursor() as cur:
                cur.execute(''' 
                    INSERT INTO person (name, age) VALUES (%s, %s)
                ''', (name, age))
                conn.commit()
        print(Fore.GREEN + f"Person {name} added successfully.")

def create_person_table():
    with connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute(''' 
                CREATE TABLE IF NOT EXISTS person (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    age INTEGER NOT NULL
                )
            ''')
            conn.commit()
    print(Fore.GREEN + "Table created successfully or already created.")

create_person_table()

while True:
    print("\nTanlovingizni tanlang:")
    print(Fore.CYAN + "1. Get all persons")
    print(Fore.CYAN + "2. Get person by ID")
    print(Fore.CYAN + "3. Add person")
    print(Fore.CYAN + "4. Exit")

    choice = input("Enter your choice: ")

    if choice == '1':
        print(Fore.MAGENTA + "All persons:")
        for person in Person.get_all_person():
            print(Fore.BLUE + f"ID: {person.id}, Name: {person.name}, Age: {person.age}")
    elif choice == '2':
        person_id = int(input("Enter person ID: "))
        person = Person.get_one_person(person_id)
        if person:
            print(Fore.GREEN + f"ID: {person.id}, Name: {person.name}, Age: {person.age}")
        else:
            print(Fore.RED + "Person not found.")
    elif choice == '3':
        name = input("Enter person's name: ")
        age = int(input("Enter person's age: "))
        Person.add_person(name, age)
    elif choice == '4':
        print(Fore.RED + "Exiting...")
        break
    else:
        print(Fore.RED + "Invalid choice. Please try again.")
