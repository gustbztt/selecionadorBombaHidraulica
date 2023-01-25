import csv
import os
from typing import List

import pandas as pd


def transform_string(s: str) -> str:
    s = s.replace("ksb_meganorm", "KSB MegaNorm")
    s = s.replace(".csv", "")
    s = s.replace("_", " ")
    if s.split()[-1].rstrip() in ["Potencia", "NPSH"]:
        s = " ".join(s.split()[:-1])
    return s


def transform_file(
    input_file: str, output_file: str, transform_func: callable, fieldnames: List[str]
):
    data = []
    with open(input_file, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            row["nome_bomba"] = transform_func(row["nome_bomba"])
            data.append(row)

    with open(output_file, mode="w") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)


def process_folder(folder_name: str, fieldnames: List[str]):
    base_folder_path = "C:\\Users\\Avell 1513\\Desktop\\TCC I"
    folder_path = os.path.join(base_folder_path, folder_name)

    new_folder_path = os.path.join(
        base_folder_path, f"concatenated_{folder_name}")
    if not os.path.exists(new_folder_path):
        os.makedirs(new_folder_path)

    dfs = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            filepath = os.path.join(folder_path, filename)
            df = pd.read_csv(filepath)
            df.insert(0, "nome_bomba", filename, True)
            dfs.append(df)

    df_final = pd.concat(dfs, ignore_index=True)

    concatenated_filepath = os.path.join(
        new_folder_path, f"{folder_name}_concatenated.csv"
    )
    df_final.to_csv(concatenated_filepath, index=False)

    output_file = os.path.join(new_folder_path, "transformed.csv")
    transform_file(concatenated_filepath, output_file,
                   transform_string, fieldnames)


process_folder("hmsAjustados", ["nome_bomba", "Q", "Hm"])
process_folder("NPSHsAjustados", ["nome_bomba", "Q", "NPSH"])
process_folder("PotenciasAjustados", ["nome_bomba", "Q", "Potencia"])
