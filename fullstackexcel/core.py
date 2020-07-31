import os

import pandas as pd
import click

from flask import Flask
from flask.cli import FlaskGroup
from flask.cli import run_command

from .routing import register_blueprints
from .routing import register_routes_to_pbo
from .jinja_env import create_jinja_env


def create_app(excel_file: str = None) -> Flask:
    app = Flask(__name__)
    excel_file = excel_file or os.environ.get('EXCEL_FILE')
    app.config['EXCEL_FILE'] = excel_file

    if excel_file:
        register_blueprints(app, excel_file)
        register_routes_to_pbo(app, excel_file)
        create_jinja_env(app, excel_file)

    return app


@click.group(cls=FlaskGroup, create_app=create_app)
def cli():
    pass


@cli.command('run-excel')
@click.argument('excel_file')
@click.pass_context
def run_excel(ctx, excel_file):
    click.echo(f'Deploying {excel_file}')
    os.environ['FLASK_APP'] = f"{__name__}:create_app('{excel_file}')"
    os.environ['EXCEL_FILE'] = excel_file
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

        templates = [['example_blueprint.xlsx']]
        pd.DataFrame(templates).to_excel(sheet_name='!blueprints', **kwargs)

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
            ['<br />', '<br />', None],
            ['<a href="/foo">', 'See some data?', '</a>'],
            ['{% endblock %}', None, None]
        ]
        pd.DataFrame(hello_world_page).to_excel(sheet_name='hello_world', **kwargs)

        actual_table = [
            ['Name', 'Number of pets'],
            ['Bob', 4],
            ['Mary', 2],
            ['Joe', 0]
        ]
        pd.DataFrame(actual_table).to_excel(sheet_name='&actual_table', **kwargs)

        foo_page = [
            ['{% extends "example_template" %}', None],
            ['{% block content %}', None],
            [None, "<h3>My friends' Pets</h3>"],
            [None, '<br \>'],
            [None, '{{ render_sheet("&actual_table") }}'],
            ['{% endblock %}', None]
        ]
        pd.DataFrame(foo_page).to_excel(sheet_name='foo', **kwargs)

    fn_bp = 'example_blueprint.xlsx'
    with pd.ExcelWriter(fn_bp, engine='xlsxwriter') as writer:
        kwargs = {
            'excel_writer': writer,
            'header': False,
            'index': False
        }
        routes = [['/bar', 'bar']]
        pd.DataFrame(routes).to_excel(sheet_name='!routes', **kwargs)

        example_bp_page = [
            ['{% extends "example_template" %}', None],
            ['{% block content %}', None],
            [None, 'This page was created using a blueprint'],
            ['{% endblock %}', None, None],
        ]
        pd.DataFrame(example_bp_page).to_excel(sheet_name='bar', **kwargs)
