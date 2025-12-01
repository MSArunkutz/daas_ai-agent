import csv

def read_csv_to_list_of_dicts(file_path):
    data_list = []
    with open(file_path, mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        data_list = list(reader)        
    return data_list

flood_safety_tips_data = read_csv_to_list_of_dicts("daas/csv_dataset/curated_flood_safety_tips.csv")

def get_tips_by_categories(categories: list[str]) -> list:
    normalized = [c.strip().lower() for c in categories]
    return [
        entry["Tip"]
        for entry in flood_safety_tips_data
        if entry["Category"].strip().lower() in normalized
    ]