import os
import re
import csv
import traceback

# file names might follow formats like 
# 2022-2023_q3_deviation.csv
# Deviations - Quarter 3 2018.csv
# Deviations - Quater 2 202021.csv
# Expansions Quarter 1 2024-2025.csv
# we want
# weather it's an expansion or a deviation
# which year it is from
# which quarter it is from
# file names that mention two years seem to reliably 
# have data from the first year

def extract_year(s):
    count = 0
    result = ''

    for char in s:
        if char.isdigit():
            result += char
            count += 1
            if count == 4:
                return result
        else:
            result = ''
            count = 0

    return None

def extract_quarter(s):
    s = s.lower()
    if "quater " in s:
        return s.split("quater ")[1][0]
    if "quarter " in s:
        return s.split("quarter ")[1][0]
    if "q" in s:
        return s.split("q")[1][0]
    return None

def clean_filename(fn):
    fn = fn.lower()

    dev_exp_type = None
    if "deviation" in fn:
        dev_exp_type = "deviation"
    else:
        dev_exp_type = "expansion"

    year = extract_year(fn)

    quarter = extract_quarter(fn)

    cfn =f"{dev_exp_type}_{year}_q{quarter}.csv"
    return cfn 

def is_header(header_row):
    header_keywords = ['department', 'date', 'supplier', 'contract', 'value', 'period', 'quarter']
    num_blank_columns = header_row.count("")
    likely_header_keywords = 0
    for col_name in header_row:
        for header_kw in header_keywords:
            if header_kw in col_name.lower():
                likely_header_keywords += 1
    if likely_header_keywords > 4:
        return True



def identify_department_column(header):
    for i,v in enumerate(header):
        if "department" in v.lower():
            return i
    return None
    return None

def identify_supplier_column(header):
    for i,v in enumerate(header):
        if "supplier" in v.lower():
            return i

    return None

def identify_value_column(header):
    candidates = {}
    for i, v in enumerate(header):
        if "value" in v.lower():
            candidates[v] = i

    if len(candidates) > 1:
        clean_candidates = {}
        for c in candidates:
            if "previous" in c.lower() or "original" in c.lower() or "pevious" in c.lower() or "prev" in c.lower():
                continue
            clean_candidates[c] = candidates[c]
        candidates = clean_candidates


    if len(candidates) > 1:
        pass
        # print("WE STILL HAVE TOO MANY CANDIDATES FOR VALUE")
        # print(candidates)

    for c in candidates:
        return candidates[c] # return column index of any candidate that is left


def clean_value(value):
    if value.count("R") > 1:
        print(value)
        print(value.count("\n"))
    value = ''.join([x for x in value if x.isdigit()])
    return value

### 
# clean file should have these columns 
# * year
# * quarter
# * expansion_deviation 
# * department
# * supplier
# * amount
# * original file name
# * original line number


csv_dir = "csvs"
csv_files = os.listdir(csv_dir)
errors = 0
row_errors = 0
row_success = 0

outfile = open('output.csv', mode='w', newline='', encoding='utf-8')
writer = csv.writer(outfile)
header = "year quarter dev_exp department supplier value original_value file_name".split()
writer.writerow(header)  # Write the header


for csv_file in csv_files:
    clean_fn = clean_filename(csv_file)
    fp = os.path.join(csv_dir, csv_file)

    print("--------- STARTING -------------")
    print(csv_file)
    print(clean_fn)
    print("===============================")
    file_rows = 0
    with open(fp, mode='r', newline='') as file:
        reader = csv.reader(file)
        header = next(reader)
        while not is_header(header):
            header = next(reader)

        supplier = identify_supplier_column(header)
        department = identify_department_column(header)
        value_i = identify_value_column(header)


        
        try:
            # deviation_2018_q4.csv
            dev_exp, year, quarter = clean_fn[:-4].split("_")
            print(year, quarter, dev_exp)
            for i, v in enumerate(reader):
                file_rows += 1
                try:
                    value = v[value_i]
                    c_value = clean_value(value)
                    row = year, quarter, dev_exp, v[department], v[supplier], c_value, value, csv_file
                    print(row)
                    if all(row):
                        writer.writerow(row)
                    row_success += 1
                except Exception as e:
                    row_errors += 1
            # print("year, quarter, dev_exp, header[department], header[supplier], header[value], 
            print(file_rows)
        except Exception as e:
            print(e)
            errors+=1
print("file errors", errors)
print("row errors", row_errors)
print("row success", row_success)
outfile.close()







    





