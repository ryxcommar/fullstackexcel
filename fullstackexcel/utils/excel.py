import pandas as pd


def sheets_in_workbook(excel_file: str):
    return pd.ExcelFile(excel_file).sheet_names
