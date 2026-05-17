import pandas as pd


def load_data(file_path="data/tickets.csv"):
    df = pd.read_csv(file_path)

    # Clean column names
    df.columns = [
        column.strip().lower().replace(" ", "_")
        for column in df.columns
    ]

    return df