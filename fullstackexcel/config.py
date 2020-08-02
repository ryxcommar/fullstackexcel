from typing import Dict

from flask import Flask

from .utils.excel import load_simple
from .utils.excel import sheets_in_workbook
from .utils.os import parse_config


def get_config_from_excel(excel_file: str, env: str) -> Dict[str, str]:
    sheets = sheets_in_workbook(excel_file)
    if env and f'#config_{env}' in sheets:
        cfg_sheet = f'#config_{env}'
    elif '#config' in sheets:
        cfg_sheet = '#config'
    else:
        return {}
    d = load_simple(excel_file, cfg_sheet, return_type=dict)
    return parse_config(d)


def update_config(app: Flask, excel_file: str):
    user_cfg = get_config_from_excel(excel_file, app.env)
    app.config.update(user_cfg)
