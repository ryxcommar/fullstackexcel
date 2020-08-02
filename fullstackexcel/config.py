from typing import Dict

from flask import Flask

from .utils.excel import load_simple
from .utils.excel import sheets_in_workbook
from .utils.os import parse_config


def get_config_from_excel(excel_file: str, cfg_name: str) -> Dict[str, str]:
    sheets = sheets_in_workbook(excel_file)
    if cfg_name and cfg_name.startswith('#config') and cfg_name in sheets:
        cfg_sheet = cfg_name
    elif cfg_name and f'#config_{cfg_name}' in sheets:
        cfg_sheet = f'#config_{cfg_name}'
    elif '#config' in sheets:
        cfg_sheet = '#config'
    else:
        return {}
    d = load_simple(excel_file, cfg_sheet, return_type=dict)
    return parse_config(d)


def update_config(app: Flask, excel_file: str, config_name: str = None):
    user_cfg = get_config_from_excel(excel_file, config_name or app.env)
    if 'INHERIT_FROM' in user_cfg:
        update_config(app, excel_file, user_cfg['INHERIT_FROM'])
    app.config.update(user_cfg)
