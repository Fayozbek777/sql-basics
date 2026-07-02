import sqlite3
import random
import string
from datetime import datetime, timedelta

# Инициализация и настройка базы данных
connection = sqlite3.connect("base.db")
cursor = connection.cursor()
cursor.execute("PRAGMA foreign_keys = ON;")

# --- 1. СОЗДАНИЕ ТАБЛИЦ ---
print("⏳ Создание структуры таблиц...")
# Сначала дропаем старые таблицы, если они забаговались
cursor.executescript("""
DROP TABLE IF EXISTS transactions;
DROP TABLE IF EXISTS cards;
DROP TABLE IF EXISTS accounts;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    email TEXT UNIQUE,
    phone TEXT,
    passport TEXT,
    secret_hash TEXT
);

CREATE TABLE accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    account_number TEXT UNIQUE,
    balance REAL,
    currency TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE cards (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id INTEGER,
    card_number TEXT UNIQUE,
    cvv TEXT,
    expiration TEXT,
    status TEXT,
    FOREIGN KEY (account_id) REFERENCES accounts(id) ON DELETE CASCADE
);

CREATE TABLE transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    from_account TEXT,
    to_account TEXT,
    amount REAL,
    timestamp TEXT,
    FOREIGN KEY (from_account) REFERENCES accounts(account_number)
);
""")
connection.commit()

# --- 2. НАБОРЫ ДАННЫХ ДЛЯ РЕАЛИСТИЧНОГО ФЕЙКА ---
first_names = [
    "Александр",
    "Дмитрий",
    "Сергей",
    "Андрей",
    "Алексей",
    "Максим",
    "Евгений",
    "Иван",
    "Михаил",
    "Артем",
    "Елена",
    "Ольга",
    "Наталья",
    "Анна",
    "Татьяна",
    "Мария",
    "Ирина",
    "Светлана",
    "Юлия",
    "Анастасия",
]
last_names = [
    "Иванов",
    "Петров",
    "Смирнов",
    "Сергеев",
    "Волков",
    "Кузнецов",
    "Попов",
    "Васильев",
    "Соколов",
    "Новиков",
    "Федоров",
    "Морозов",
    "Воробьев",
    "Киселев",
    "Зайцев",
    "Павлов",
    "Козлов",
    "Степанов",
    "Николаев",
    "Орлов",
]
currencies = ["RUB", "USD", "EUR", "UZS", "KZT"]


def generate_phone():
    return f"+7(9{random.randint(10,99)}){random.randint(100,999)}-{random.randint(10,99)}-{random.randint(10,99)}"


def generate_passport():
    return f"{random.randint(40, 99)} {random.randint(10, 99)} {random.randint(100000, 999999)}"


def generate_hash():
    return "".join(random.choices(string.hexdigits.lower(), k=32))


# --- 3. ГЕНЕРАЦИЯ ДАННЫХ ---
TOTAL_USERS = 50_000
BATCH_SIZE = 10_000

print(f"🚀 Начинается генерация {TOTAL_USERS} клиентов и связанных данных...")

users_batch = []
accounts_batch = []
cards_batch = []
transactions_batch = []

account_id_counter = 1
account_numbers_pool = []

for u_id in range(1, TOTAL_USERS + 1):
    f_name = random.choice(first_names)
    l_name = random.choice(last_names)
    if f_name[-1] in ["а", "я"] and l_name[-1] == "в":
        l_name += "а"

    full_name = f"{l_name} {f_name}"
    email = f"{l_name.lower()}{u_id}@fakebank.com"
    phone = generate_phone()
    passport = generate_passport()
    secret_hash = generate_hash()

    # Ровно 6 значений, которые теперь соответствуют структуре таблицы users
    users_batch.append((u_id, full_name, email, phone, passport, secret_hash))

    for _ in range(random.randint(1, 2)):
        acc_num = "".join(random.choices(string.digits, k=16))
        account_numbers_pool.append(acc_num)
        balance = round(random.uniform(100.0, 750000.0), 2)
        currency = random.choice(currencies)

        accounts_batch.append((account_id_counter, u_id, acc_num, balance, currency))

        if random.random() < 0.85:
            card_num = f"{random.choice(['4', '5'])}{''.join(random.choices(string.digits, k=15))}"
            cvv = f"{random.randint(100, 999)}"
            exp = f"{random.randint(1, 12):02d}/{random.randint(27, 32)}"
            status = "active" if random.random() < 0.9 else "blocked"

            cards_batch.append((account_id_counter, card_num, cvv, exp, status))

        account_id_counter += 1

print("↳ Запись пользователей в базу...")
cursor.executemany("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?);", users_batch)

print("↳ Запись расчетных счетов...")
cursor.executemany("INSERT INTO accounts VALUES (?, ?, ?, ?, ?);", accounts_batch)

print("↳ Эмиссия пластиковых карт...")
cursor.executemany(
    "INSERT INTO cards (account_id, card_number, cvv, expiration, status) VALUES (?, ?, ?, ?, ?);",
    cards_batch,
)
connection.commit()

print("↳ Симуляция межбанковских транзакций...")
start_date = datetime.now() - timedelta(days=90)

for idx, from_acc in enumerate(account_numbers_pool):
    for _ in range(random.randint(2, 5)):
        to_acc = random.choice(account_numbers_pool)
        if to_acc == from_acc:
            to_acc = "".join(random.choices(string.digits, k=16))

        amount = round(random.uniform(10.0, 5000.0), 2)
        rand_timestamp = start_date + timedelta(seconds=random.randint(0, 7776000))

        transactions_batch.append(
            (from_acc, to_acc, amount, rand_timestamp.strftime("%Y-%m-%d %H:%M:%S"))
        )

for i in range(0, len(transactions_batch), BATCH_SIZE):
    cursor.executemany(
        "INSERT INTO transactions (from_account, to_account, amount, timestamp) VALUES (?, ?, ?, ?);",
        transactions_batch[i : i + BATCH_SIZE],
    )

connection.commit()

# --- 4. ПРОВЕРКА РЕЗУЛЬТАТОВ ---
print("\n📊 СТАТИСТИКА СОЗДАННОЙ БАЗЫ ДАННЫХ:")
print("-" * 40)
for table in ["users", "accounts", "cards", "transactions"]:
    count = cursor.execute(f"SELECT COUNT(*) FROM {table};").fetchone()[0]
    print(f" Таблица {table: <13} | Строк: {count:,}")
print("-" * 40)
print("🎉 База данных base.db успешно сформирована!")

connection.close()
