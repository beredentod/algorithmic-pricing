import csv

# Specify the desired order of column names
desired_order = ['id_data', 'date', 'dow', 'weekend',
'p_e5_6oclock_0min', 'p_e5_6oclock_5min', 'p_e5_6oclock_10min', 'p_e5_6oclock_15min', 'p_e5_6oclock_20min', 'p_e5_6oclock_25min', 'p_e5_6oclock_30min', 'p_e5_6oclock_35min', 'p_e5_6oclock_40min', 'p_e5_6oclock_45min', 'p_e5_6oclock_50min', 'p_e5_6oclock_55min',
'p_e5_7oclock_0min', 'p_e5_7oclock_5min', 'p_e5_7oclock_10min', 'p_e5_7oclock_15min', 'p_e5_7oclock_20min', 'p_e5_7oclock_25min', 'p_e5_7oclock_30min', 'p_e5_7oclock_35min', 'p_e5_7oclock_40min', 'p_e5_7oclock_45min', 'p_e5_7oclock_50min', 'p_e5_7oclock_55min',
'p_e5_8oclock_0min', 'p_e5_8oclock_5min', 'p_e5_8oclock_10min', 'p_e5_8oclock_15min', 'p_e5_8oclock_20min', 'p_e5_8oclock_25min', 'p_e5_8oclock_30min', 'p_e5_8oclock_35min', 'p_e5_8oclock_40min', 'p_e5_8oclock_45min', 'p_e5_8oclock_50min', 'p_e5_8oclock_55min',
'p_e5_9oclock_0min', 'p_e5_9oclock_5min', 'p_e5_9oclock_10min', 'p_e5_9oclock_15min', 'p_e5_9oclock_20min', 'p_e5_9oclock_25min', 'p_e5_9oclock_30min', 'p_e5_9oclock_35min', 'p_e5_9oclock_40min', 'p_e5_9oclock_45min', 'p_e5_9oclock_50min', 'p_e5_9oclock_55min',
'p_e5_10oclock_0min', 'p_e5_10oclock_5min', 'p_e5_10oclock_10min', 'p_e5_10oclock_15min', 'p_e5_10oclock_20min', 'p_e5_10oclock_25min', 'p_e5_10oclock_30min', 'p_e5_10oclock_35min', 'p_e5_10oclock_40min', 'p_e5_10oclock_45min', 'p_e5_10oclock_50min', 'p_e5_10oclock_55min',
'p_e5_11oclock_0min', 'p_e5_11oclock_5min', 'p_e5_11oclock_10min', 'p_e5_11oclock_15min', 'p_e5_11oclock_20min', 'p_e5_11oclock_25min', 'p_e5_11oclock_30min', 'p_e5_11oclock_35min', 'p_e5_11oclock_40min', 'p_e5_11oclock_45min', 'p_e5_11oclock_50min', 'p_e5_11oclock_55min',
'p_e5_12oclock_0min', 'p_e5_12oclock_5min', 'p_e5_12oclock_10min', 'p_e5_12oclock_15min', 'p_e5_12oclock_20min', 'p_e5_12oclock_25min', 'p_e5_12oclock_30min', 'p_e5_12oclock_35min', 'p_e5_12oclock_40min', 'p_e5_12oclock_45min', 'p_e5_12oclock_50min', 'p_e5_12oclock_55min',
'p_e5_13oclock_0min', 'p_e5_13oclock_5min', 'p_e5_13oclock_10min', 'p_e5_13oclock_15min', 'p_e5_13oclock_20min', 'p_e5_13oclock_25min', 'p_e5_13oclock_30min', 'p_e5_13oclock_35min', 'p_e5_13oclock_40min', 'p_e5_13oclock_45min', 'p_e5_13oclock_50min', 'p_e5_13oclock_55min',
'p_e5_14oclock_0min', 'p_e5_14oclock_5min', 'p_e5_14oclock_10min', 'p_e5_14oclock_15min', 'p_e5_14oclock_20min', 'p_e5_14oclock_25min', 'p_e5_14oclock_30min', 'p_e5_14oclock_35min', 'p_e5_14oclock_40min', 'p_e5_14oclock_45min', 'p_e5_14oclock_50min', 'p_e5_14oclock_55min',
'p_e5_15oclock_0min', 'p_e5_15oclock_5min', 'p_e5_15oclock_10min', 'p_e5_15oclock_15min', 'p_e5_15oclock_20min', 'p_e5_15oclock_25min', 'p_e5_15oclock_30min', 'p_e5_15oclock_35min', 'p_e5_15oclock_40min', 'p_e5_15oclock_45min', 'p_e5_15oclock_50min', 'p_e5_15oclock_55min',
'p_e5_16oclock_0min', 'p_e5_16oclock_5min', 'p_e5_16oclock_10min', 'p_e5_16oclock_15min', 'p_e5_16oclock_20min', 'p_e5_16oclock_25min', 'p_e5_16oclock_30min', 'p_e5_16oclock_35min', 'p_e5_16oclock_40min', 'p_e5_16oclock_45min', 'p_e5_16oclock_50min', 'p_e5_16oclock_55min',
'p_e5_17oclock_0min', 'p_e5_17oclock_5min', 'p_e5_17oclock_10min', 'p_e5_17oclock_15min', 'p_e5_17oclock_20min', 'p_e5_17oclock_25min', 'p_e5_17oclock_30min', 'p_e5_17oclock_35min', 'p_e5_17oclock_40min', 'p_e5_17oclock_45min', 'p_e5_17oclock_50min', 'p_e5_17oclock_55min',
'p_e5_18oclock_0min', 'p_e5_18oclock_5min', 'p_e5_18oclock_10min', 'p_e5_18oclock_15min', 'p_e5_18oclock_20min', 'p_e5_18oclock_25min', 'p_e5_18oclock_30min', 'p_e5_18oclock_35min', 'p_e5_18oclock_40min', 'p_e5_18oclock_45min', 'p_e5_18oclock_50min', 'p_e5_18oclock_55min',
'p_e5_19oclock_0min', 'p_e5_19oclock_5min', 'p_e5_19oclock_10min', 'p_e5_19oclock_15min', 'p_e5_19oclock_20min', 'p_e5_19oclock_25min', 'p_e5_19oclock_30min', 'p_e5_19oclock_35min', 'p_e5_19oclock_40min', 'p_e5_19oclock_45min', 'p_e5_19oclock_50min', 'p_e5_19oclock_55min',
'p_e5_20oclock_0min', 'p_e5_20oclock_5min', 'p_e5_20oclock_10min', 'p_e5_20oclock_15min', 'p_e5_20oclock_20min', 'p_e5_20oclock_25min', 'p_e5_20oclock_30min', 'p_e5_20oclock_35min', 'p_e5_20oclock_40min', 'p_e5_20oclock_45min', 'p_e5_20oclock_50min', 'p_e5_20oclock_55min',
'p_e5_21oclock_0min', 'p_e5_21oclock_5min', 'p_e5_21oclock_10min', 'p_e5_21oclock_15min', 'p_e5_21oclock_20min', 'p_e5_21oclock_25min', 'p_e5_21oclock_30min', 'p_e5_21oclock_35min', 'p_e5_21oclock_40min', 'p_e5_21oclock_45min', 'p_e5_21oclock_50min', 'p_e5_21oclock_55min',
'p_e5_22oclock_0min', 'p_e5_22oclock_5min', 'p_e5_22oclock_10min', 'p_e5_22oclock_15min', 'p_e5_22oclock_20min', 'p_e5_22oclock_25min', 'p_e5_22oclock_30min', 'p_e5_22oclock_35min', 'p_e5_22oclock_40min', 'p_e5_22oclock_45min', 'p_e5_22oclock_50min', 'p_e5_22oclock_55min']


input_file = '../data/stations_prices_MUC_wide_10-2022.csv'
output_file = '../data/stations_prices_MUC_wide_10-2022_new.csv'


import csv

def get_column_names(csv_file):
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        header = next(reader)  # Read the header row

    return header

csv_file = '../data/stations_prices_MUC_wide_10-2022_new.csv' # Replace with the path to your CSV file
column_names = get_column_names(csv_file)
print("Column names:", column_names)


'''
with open(input_file, "r") as infile, open(output_file, "w", newline="") as outfile:
    reader = csv.DictReader(infile)
    fieldnames = reader.fieldnames

    # Ensure all desired columns are present in the file
    for column in desired_order:
        if column not in fieldnames:
            print(f"Column '{column}' not found in the input CSV.")
            exit(1)

    # Reorder the columns based on the desired order
    writer = csv.DictWriter(outfile, fieldnames=desired_order)
    writer.writeheader()

    for row in reader:
        reordered_row = {column: row[column] for column in desired_order}
        writer.writerow(reordered_row)

print(f"Columns reordered and saved in '{output_file}'.")
'''