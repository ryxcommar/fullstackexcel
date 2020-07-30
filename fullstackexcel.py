import os
import re
from typing import Dict
from typing import List

import pandas as pd
import click

from flask import Flask
from flask import current_app
from flask.cli import FlaskGroup
from flask.cli import run_command

from jinja2 import DictLoader


def get_routes_from_wb(excel_file: str) -> List[Dict[str, str]]:
    routes = pd.read_excel(excel_file, sheet_name='!routes', header=None)
    routes = routes.rename(columns={0: 'route', 1: 'sheet_name'})
    return routes.to_dict(orient='records')


def get_templates_from_wb(excel_file: str) -> List[str]:
    templates = pd.read_excel(excel_file, sheet_name='!templates', header=None)
    return list(templates[0])


def get_html_from_sheet(excel_file: str, sheet_name: str) -> str:
    df_html = pd.read_excel(excel_file, sheet_name=sheet_name, header=None)
    df_html = df_html.fillna('').astype(str)
    html = '\n'.join(list(df_html.sum(axis=1)))
    return html


def render_html_from_sheet(excel_file: str, sheet_name: str) -> str:
    html = get_html_from_sheet(excel_file, sheet_name)
    return current_app.jinja_env.from_string(html).render()


def create_routing_func(excel_file: str, sheet_name: str) -> callable:
    _f = lambda: render_html_from_sheet(excel_file, sheet_name)
    _f.__name__ = re.sub(r'\W+', '', sheet_name.lower())
    return _f


def create_jinja_env(app: Flask, excel_file: str):
    templates = get_templates_from_wb(excel_file)
    app.jinja_env.loader = DictLoader({
        template: get_html_from_sheet(excel_file, template)
        for template in templates
    })


def create_app(excel_file: str = None) -> Flask:
    app = Flask(__name__)
    excel_file = excel_file or os.environ.get('EXCEL_SHEET')

    if excel_file:
        for routing_rule in get_routes_from_wb(excel_file):
            f = create_routing_func(excel_file, routing_rule['sheet_name'])
            app.route(routing_rule['route'])(f)

        create_jinja_env(app, excel_file)

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

        templates = [['example_template']]
        pd.DataFrame(templates).to_excel(sheet_name='!templates', **kwargs)

        example_template = [
            ['<head>', None, None, None],
            [None, '<title>', 'Fullstack with Excel', '</title>'],
            ['</head>', None, None, None],
            ['{% block content %}', None, None, None],
            ['{% endblock %}', None, None, None]
        ]
        pd.DataFrame(example_template).to_excel(sheet_name='example_template', **kwargs)

        hello_world_page = [
            ['{% extends "example_template" %}', None, None],
            ['{% block content %}', None, None],
            ['<b>', 'hello, world!', '</b>'],
            ['{% endblock %}', None, None]
        ]
        pd.DataFrame(hello_world_page).to_excel(sheet_name='hello_world', **kwargs)

        foo_page = [
            ['<head>', None, None],
            [None, '<title>full stack with excel</title>', None],
            ['</head>', None, None],
            ['<i>', 'bar', '</i>']
        ]
        pd.DataFrame(foo_page).to_excel(sheet_name='foo', **kwargs)
