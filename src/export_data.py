import sqlite3
import json
import csv
import xml.etree.ElementTree as ET
try:
    import yaml
except ImportError:
    yaml = None

from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
DATABASE = PROJECT_ROOT / "db" / "fitness_club.db"
OUT_DIR = PROJECT_ROOT / "out"

def export_data():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    #Запрос: клиенты + их абонементы
    cursor.execute("""
        SELECT 
            К.клиент_id,
            К.ФИО,
            К.номер_телефона,
            А.абонемент_id,
            А.стоимость
        FROM Клиент К
        LEFT JOIN Абонемент А ON К.клиент_id = А.клиент_id
        ORDER BY К.клиент_id
    """)

    rows = cursor.fetchall()
    print(f"Получено {len(rows)} записей.")

    # Собираем данные в структуру: клиент → [абонементы]
    clients = {}
    for row in rows:
        client_id = row[0]
        fio = row[1]
        phone = row[2]
        abon_id = row[3]
        cost = row[4]

        if client_id not in clients:
            clients[client_id] = {
                "клиент_id": client_id,
                "ФИО": fio,
                "номер_телефона": phone,
                "абонементы": []
            }

        if abon_id is not None:
            clients[client_id]["абонементы"].append({
                "id": abon_id,
                "стоимость": cost
            })

    # Преобразуем в список
    data = list(clients.values())

    # Экспорт в JSON
    with open(OUT_DIR / "data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("data.json — сохранён")

    # Экспорт в CSV
    with open(OUT_DIR / "data.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        # Заголовки
        writer.writerow([
            "клиент_id", "ФИО", "номер_телефона",
            "абонемент_id", "абонемент_стоимость"
        ])
        for client in data:
            if client["абонементы"]:
                for abon in client["абонементы"]:
                    writer.writerow([
                        client["клиент_id"],
                        client["ФИО"],
                        client["номер_телефона"],
                        abon["id"],
                        abon["стоимость"]
                    ])
            else:
                # Клиент без абонементов
                writer.writerow([
                    client["клиент_id"],
                    client["ФИО"],
                    client["номер_телефона"],
                    "", ""
                ])
    print("data.csv — сохранён")

    # Экспорт в XML
    root = ET.Element("Клиенты")
    for client in data:
        client_elem = ET.SubElement(root, "Клиент")
        ET.SubElement(client_elem, "клиент_id").text = str(client["клиент_id"])
        ET.SubElement(client_elem, "ФИО").text = client["ФИО"]
        ET.SubElement(client_elem, "номер_телефона").text = client["номер_телефона"]

        if client["абонементы"]:
            abons_elem = ET.SubElement(client_elem, "абонементы")
            for abon in client["абонементы"]:
                abon_elem = ET.SubElement(abons_elem, "Абонемент")
                ET.SubElement(abon_elem, "id").text = str(abon["id"])
                ET.SubElement(abon_elem, "стоимость").text = str(abon["стоимость"])

    tree = ET.ElementTree(root)
    ET.indent(tree, space="  ", level=0)
    tree.write(OUT_DIR / "data.xml", encoding="utf-8", xml_declaration=True)
    print("data.xml — сохранён")

    # Экспорт в YAML
    with open(OUT_DIR / "data.yaml", "w", encoding="utf-8") as f:
        yaml.dump(data, f, allow_unicode=True, default_flow_style=False)
    print("data.yaml — сохранён")
    conn.close()

if __name__ == "__main__":
    export_data()