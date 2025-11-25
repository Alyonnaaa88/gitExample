from data_access import get_all_clients, get_bookings_by_client, get_client_by_id

print("Все клиенты")
for c in get_all_clients():
    print(c)

print("\nЗаписи клиента 1")
bookings = get_bookings_by_client(1)
for b in bookings:
    print(f"Запись #{b.запись_id} на занятие {b.занятие_id}, статус: {b.статус_занятия}")

print("\nКлиент с ID = 1")
client = get_client_by_id(1)
if client:
    print(f"ФИО: {client.ФИО}")
    print(f"Дата рождения: {client.дата_рождения}")
    print(f"Пол: {client.пол}")
    print(f"Телефон: {client.номер_телефона}")
else:
    print("Клиент с ID=1 не найден")