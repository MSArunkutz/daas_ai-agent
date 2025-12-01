import csv

def read_csv_to_list_of_dicts(file_path):
    data_list = []
    with open(file_path, mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        data_list = list(reader)        
    return data_list

flood_severity_data = read_csv_to_list_of_dicts("daas/csv_dataset/flood_data_with_coords.csv")