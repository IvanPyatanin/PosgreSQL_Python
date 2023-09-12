import psycopg2

connection = psycopg2.connect(database="clients_db", user="postgres", password="158660", host="localhost")

#удаление БД
def drop_tables():
    with connection.cursor() as cur:
        cur.execute("""drop table client, phone;""")

#функция, создающая БД
def create_db():
    with connection.cursor() as cur:
        cur.execute("""
            create table if not exists client(
            id serial primary key,
            name varchar(50) not null,
            first_name varchar(50) not null,
            email varchar(50) not null);""")
        print("База дынных client создана")

        cur.execute("""
            create table if not exists phone(
            id serial primary key,
            phones text null,
            client_id integer references client(id));""")
        print("База дынных phone создана")


#добавление информации
def create_client(name, first_name, email):
    with connection.cursor() as cur:
        cur.execute("""
            insert into client(name, first_name, email) values (%s, %s, %s);
            """, (name, first_name, email))
        print(f'Клиент {name} создан')

#Добавление номера
def create_phone(phones, client_id):
    with connection.cursor() as cur:
        cur.execute("""
            insert into phone(phones, client_id) values (%s, %s);
            """, (phones, client_id))
    print(f'Номер клиенту {client_id} добавлен')

#Изменение инфыормации
def update_client(client_id, name=None, first_name=None, email=None):
    with connection.cursor() as cur:
        cur.execute("""UPDATE client set name = %s, first_name = %s, email = %s where id = %s""", (name, first_name, email, client_id,))
    print("Данные обновлены")

#удаление телефона
def delete_phone(phones, client_id):
    with connection.cursor() as cur:
        cur.execute("""delete from phone where phones like %s and client_id = %s""", (phones, client_id,))
    print("Номер удален")

#удаление клиента
def delete_client(client_id):
    with connection.cursor() as cur:
        cur.execute("""
        delete from client where id = %s""", (client_id,))
    print(f'Клиент под id {client_id} удален')

#поиск клиента
def find_client(name=None, first_name=None, email=None, phones=None):
    with connection.cursor() as cur:
        cur.execute("""
            select c.name, c.first_name, c.email, p.phones from client c
            join phone p on c.id = p.client_id
            where name like %s or first_name like %s or email like %s or phones like %s""", (name, first_name, email, phones,))
        print(cur.fetchone())

#Вывод информации
# with connection.cursor() as cursor:
#     cursor.execute("""
#         select * from client""")
#     print(cursor.fetchall())

#запуск
# drop_tables()

# create_db()

# create_client("Ivan", "Pyatanin", "ivan.pyatanin@yandex.ru",)
# create_client("Oleg", "Murkin", "Murk@mail.ru",)

# delete_client(3)

# create_phone("+79999999999", 1)
# create_phone("+79998989988", 2)

# update_client(1,"Ivan",)

# find_client('', 'Pyatanin')
# delete_phone("+79999999999", 1)


connection.commit()
connection.close()
print('Ура, ты пока не накосячил!')