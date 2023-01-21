import os
import re

import pandas as pd


def join_csv_files(folder_name):
    base_folder_path = "C:\\Users\\Avell 1513\\Desktop\\TCC I"
    folder_path = os.path.join(base_folder_path, folder_name)

    # Create a new folder with the same name as the original folder, where the concatenated file will be stored
    new_folder_path = os.path.join(base_folder_path, f"concatenated_{folder_name}")
    if not os.path.exists(new_folder_path):
        os.makedirs(new_folder_path)

    dfs = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            filepath = os.path.join(folder_path, filename)
            df = pd.read_csv(filepath)
            df.insert(0, "Title", filename, True)
            dfs.append(df)

    # Concatenate all data into one DataFrame

    df_final = pd.concat(dfs, ignore_index=True)

    # write out to the concatenated csv file
    concatenated_filepath = os.path.join(
        new_folder_path, f"{folder_name}_concatenated.csv"
    )
    df_final.to_csv(concatenated_filepath, index=False)


join_csv_files("hmsAjustados")
join_csv_files("NPSHsAjustados")
join_csv_files("PotenciasAjustados")


import csv


def transform_string(s: str) -> str:
    s = s.replace("ksb_meganorm", "KSB MegaNorm")
    s = s.replace(".csv", "")
    s = s.replace("_", " ")
    if s.split()[-1].rstrip() in ["Potencia", "NPSH"]:
        s = " ".join(s.split()[:-1])
    return s


def transform_file(input_file: str, output_file: str, transform_func: callable):
    data = []
    with open(input_file, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            row["Title"] = transform_func(row["Title"])
            data.append(row)

    with open(output_file, mode="w") as csvfile:
        fieldnames = ["Title", "Q", "Hm"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)


input_file_hm = r"C:\Users\Avell 1513\Desktop\TCC I\concatenated_hmsAjustados\hmsAjustados_concatenated.csv"
output_file_hm = (
    r"C:\Users\Avell 1513\Desktop\TCC I\concatenated_hmsAjustados\transformed.csv"
)
transform_file(input_file_hm, output_file_hm, transform_string)

input_file_NPSH = r"C:\Users\Avell 1513\Desktop\TCC I\concatenated_NPSHsAjustados\NPSHsAjustados_concatenated.csv"
output_file_NPSH = (
    r"C:\Users\Avell 1513\Desktop\TCC I\concatenated_NPSHsAjustados\transformed.csv"
)
transform_file(input_file_NPSH, output_file_NPSH, transform_string)

input_file_Potencia = r"C:\Users\Avell 1513\Desktop\TCC I\concatenated_PotenciasAjustados\PotenciasAjustados_concatenated.csv"
output_file_Potencia = (
    r"C:\Users\Avell 1513\Desktop\TCC I\concatenated_PotenciasAjustados\transformed.csv"
)
transform_file(input_file_Potencia, output_file_Potencia, transform_string)
