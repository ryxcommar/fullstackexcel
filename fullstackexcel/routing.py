import os
import re
from typing import List
from typing import Dict
from typing import Union

import pandas as pd

from flask import Flask
from flask import Blueprint

from .rendering import render_html_from_sheet


def create_blueprint(blueprint_excel_file: str):
    bp_name = os.path.splitext(os.path.split(blueprint_excel_file)[1])[0]
    bp = Blueprint(bp_name, __name__)
    register_routes_to_pbo(bp, blueprint_excel_file)
    return bp


def register_blueprints(app: Flask, excel_file: str):
    for fn in get_blueprints_list_from_wb(excel_file):
        bp = create_blueprint(fn)
        app.register_blueprint(bp)


def get_routes_from_wb(excel_file: str) -> List[Dict[str, str]]:
    routes = pd.read_excel(excel_file, sheet_name='!routes', header=None)
    routes = routes.rename(columns={0: 'route', 1: 'sheet_name'})
    return routes.to_dict(orient='records')


def get_blueprints_list_from_wb(excel_file: str) -> List[str]:
    bp_list = pd.read_excel(excel_file, sheet_name='!blueprints', header=None)
    return list(bp_list[0])


def create_routing_func(excel_file: str, sheet_name: str) -> callable:
    _f = lambda: render_html_from_sheet(excel_file, sheet_name)
    _f.__name__ = re.sub(r'\W+', '', sheet_name.lower())
    return _f


def register_routes_to_pbo(pbo: Union[Flask, Blueprint], excel_file: str):
    for routing_rule in get_routes_from_wb(excel_file):
        f = create_routing_func(excel_file, routing_rule['sheet_name'])
        pbo.route(routing_rule['route'])(f)

