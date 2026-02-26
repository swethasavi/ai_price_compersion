import csv

def load_market_data(csv_path):
    data = {}

    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            keys = list(row.keys())

            district = row[keys[0]]
            crop     = row[keys[1]]
            market   = row[keys[2]]
            today    = float(row[keys[3]])
            future   = float(row[keys[4]])

            if district not in data:
                data[district] = {}

            if crop not in data[district]:
                data[district][crop] = {}

            data[district][crop][market] = {
                "today": today,
                "future": future
            }

    return data
