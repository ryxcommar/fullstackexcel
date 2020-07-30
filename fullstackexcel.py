import os
import re
from typing import Dict
from typing import List

import pandas as pd
import click

from flask import Flask
from flask.cli import FlaskGroup
from flask.cli import run_command


def get_routes_from_wb(excel_file: str) -> List[Dict[str, str]]:
    routes = pd.read_excel(excel_file, sheet_name='!routes', header=None)
    routes = routes.rename(columns={0: 'route', 1: 'sheet_name'})
    return routes.to_dict(orient='records')


def create_html_from_sheet(excel_file: str, sheet_name: str) -> str:
    df_html = pd.read_excel(excel_file, sheet_name=sheet_name, header=None)
    df_html = df_html.fillna('').astype(str)
    return '\n'.join(list(df_html.sum(axis=1)))


def create_routing_func(excel_file: str, sheet_name: str) -> callable:
    _f = lambda: create_html_from_sheet(excel_file, sheet_name)
    _f.__name__ = re.sub(r'\W+', '', sheet_name.lower())
    return _f


def create_app(excel_file: str = None) -> Flask:
    app = Flask(__name__)
    excel_file = excel_file or os.environ.get('EXCEL_SHEET')

    if excel_file:
        for routing_rule in get_routes_from_wb(excel_file):
            f = create_routing_func(excel_file, routing_rule['sheet_name'])
            app.route(routing_rule['route'])(f)

    return app


@click.group(cls=FlaskGroup, create_app=create_app)
def cli():
    pass


@cli.command('run-excel')
@click.argument('excel_sheet')
@click.pass_context
def run_excel(ctx, excel_sheet):
    click.echo(f'Deploying {excel_sheet}')
    os.environ['FLASK_APP'] = f"{__name__}:create_app('{excel_sheet}')"
    os.environ['EXCEL_SHEET'] = excel_sheet
    ctx.invoke(run_command, reload=True)


@cli.command('create-demo')
def create_demo():
    fn = 'demo_website.xlsx'
    with pd.ExcelWriter(fn, engine='xlsxwriter') as writer:
        kwargs = {
            'excel_writer': writer,
            'header': False,
            'index': False
        }

        routes = [['/', 'hello_world'], ['/foo', 'foo']]
        pd.DataFrame(routes).to_excel(sheet_name='!routes', **kwargs)

        hello_world_page = [
            ['<head>', '<title>full stack with excel</title>', None],
            ['</head>', None, None],
            ['<i>', 'hello, world!', '</i>']
        ]
        pd.DataFrame(hello_world_page).to_excel(sheet_name='hello_world', **kwargs)

        foo_page = [
            ['<head>', '<title>full stack with excel</title>', None],
            ['</head>', None, None],
            ['<b>', 'bar', '</b>']
        ]
        pd.DataFrame(foo_page).to_excel(sheet_name='foo', **kwargs)
