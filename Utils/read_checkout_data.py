import csv
def read_checkout_data(file_path):
    try:
        with open(file_path,newline='') as csvfile:
            reader=csv.DictReader(csvfile)
            data = list(reader)
            #data=list(csv.reader(csvfile))
            return data
    except FileNotFoundError:
        raise Exception(f"File not found:{file_path}")
    except Exception as e:
        raise Exception(f"Error reading file:{e}")