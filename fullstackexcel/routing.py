import os
import re
from typing import List
from typing import Dict
from typing import Union

import pandas as pd

from flask import Flask
from flask import Blueprint

from .rendering import render_html_from_sheet
from .utils.excel import sheets_in_workbook
from .utils.excel import load_simple


def create_blueprint(blueprint_excel_file: str):
    bp_name = os.path.splitext(os.path.split(blueprint_excel_file)[1])[0]
    bp = Blueprint(bp_name, __name__)
    register_routes_to_pbo(bp, blueprint_excel_file)
    return bp


def register_blueprints(app: Flask, excel_file: str):
    for fn in get_blueprints_list_from_wb(excel_file):
        bp = create_blueprint(fn)
        app.register_blueprint(bp)


def get_routes_from_wb(excel_file: str) -> Dict[str, str]:
    if '#routes' not in sheets_in_workbook(excel_file):
        return {}
    return load_simple(excel_file, '#routes', return_type=dict)


def get_blueprints_list_from_wb(excel_file: str) -> List[str]:
    if '#blueprints' not in sheets_in_workbook(excel_file):
        return []
    return load_simple(excel_file, '#blueprints', return_type=list)


def create_routing_func(excel_file: str, sheet_name: str) -> callable:
    _f = lambda: render_html_from_sheet(excel_file, sheet_name)
    _f.__name__ = re.sub(r'\W+', '', sheet_name.lower())
    return _f


def register_routes_to_pbo(pbo: Union[Flask, Blueprint], excel_file: str):
    for endpoint, rule in get_routes_from_wb(excel_file).items():
        f = create_routing_func(excel_file, endpoint)
        pbo.route(rule)(f)
