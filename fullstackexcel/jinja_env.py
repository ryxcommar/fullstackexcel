from typing import List

import pandas as pd

from flask import Flask
from flask import current_app

from jinja2 import DictLoader

from markupsafe import Markup

from .rendering import get_html_from_sheet
from .utils.excel import sheets_in_workbook


def get_templates_from_wb(excel_file: str) -> List[str]:
    if '!templates' not in sheets_in_workbook(excel_file):
        return []
    templates = pd.read_excel(excel_file, sheet_name='!templates', header=None)
    return list(templates[0])


def render_sheet(sheet_name: str):
    df = pd.read_excel(current_app.config['EXCEL_FILE'], sheet_name=sheet_name)
    return Markup(df.to_html(index=None, escape=False))


def create_jinja_env(app: Flask, excel_file: str):
    templates = get_templates_from_wb(excel_file)
    app.jinja_env.loader = DictLoader({
        template: get_html_from_sheet(excel_file, template)
        for template in templates
    })
    app.jinja_env.globals.update(render_sheet=render_sheet)
