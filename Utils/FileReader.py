import csv
def load_csv_data(file_path):
    rows=[]
    try:
        with open(file_path, 'r') as datafile:
            reader = csv.reader(datafile)
            next(reader)
            for row in reader:
                rows.append(tuple(row))
        return rows
    except FileNotFoundError:
        raise Exception(f"File not found:{file_path}")
    except Exception as e:
        raise Exception(f"Error reading file:{e}")