from typing import List
import pandas as pd

from flask import current_app


def get_html_from_sheet(excel_file: str, sheet_name: str) -> str:
    df_html = pd.read_excel(excel_file, sheet_name=sheet_name, header=None)
    df_html = df_html.fillna('').astype(str)
    html = '\n'.join(list(df_html.sum(axis=1)))
    return html


def render_html_from_sheet(excel_file: str, sheet_name: str) -> str:
    html = get_html_from_sheet(excel_file, sheet_name)
    return current_app.jinja_env.from_string(html).render()
