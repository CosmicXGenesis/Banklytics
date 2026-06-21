import os
import pandas as pd


def read_csv(path):

    return pd.read_csv(path)


def list_csv_files(folder_path):

    return sorted([
        file
        for file in os.listdir(folder_path)
        if file.endswith(".csv")
    ])