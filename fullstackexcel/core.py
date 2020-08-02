import os

import pandas as pd
import click

from flask import Flask
from flask.cli import FlaskGroup
from flask.cli import run_command

from .config import update_config
from .routing import register_blueprints
from .routing import register_routes_to_pbo
from .jinja_env import create_jinja_env

from .utils.excel import build_workbook_from_dict


def create_app(excel_file: str = None) -> Flask:
    app = Flask(__name__)
    excel_file = excel_file or os.environ.get('EXCEL_FILE')
    app.config['EXCEL_FILE'] = excel_file

    if excel_file:
        update_config(app, excel_file)
        register_blueprints(app, excel_file)
        register_routes_to_pbo(app, excel_file)
        create_jinja_env(app, excel_file)

    return app


@click.group(cls=FlaskGroup, create_app=create_app)
def cli():
    pass


@cli.command('run-excel', context_settings={'ignore_unknown_options': True})
@click.argument('excel_file', nargs=-1, type=click.Path())
@click.option('--env', '-e',
              default=lambda: os.getenv('FSE_ENV', 'production'),
              help='Your config environment. Different config environments are '
                   'managed using #config_{env} sheets. `development` and '
                   '`production` are always valid configs by default.')
@click.pass_context
def run_excel(ctx, excel_file, env):
    """Deploy your Excel file as a website."""
    if len(excel_file) == 0:
        if 'EXCEL_FILE' in os.environ:
            _excel_file = os.environ['EXCEL_FILE']
        else:
            raise TypeError('Please either define an excel file to load as an '
                            'argument (recommended), or define an `EXCEL_FILE` '
                            'environment variable.')
    elif len(excel_file) == 1:
        _excel_file = excel_file[0]
    else:
        raise TypeError("You cannot submit more than 1 Excel file. If you'd "
                        'like to support multiple Excel files, create a '
                        '`#blueprints` sheet.')
    click.echo(f'Deploying {_excel_file}')
    os.environ['FLASK_APP'] = f"{__name__}:create_app('{_excel_file}')"
    os.environ['EXCEL_FILE'] = _excel_file
    os.environ['FLASK_ENV'] = env
    ctx.invoke(run_command, reload=True)


@cli.command('create-demo')
def create_demo():

    base = {
        '#routes': [
            ['hello_world', '/'],
            ['foo', '/foo']
        ],
        '#templates': [
            ['example_template']
        ],
        '#blueprints': [
            ['example_blueprint.xlsx']
        ],
        '#config': [
            ['SECRET_KEY', '%SECRET_KEY%'],
            ['PREFERRED_URL_SCHEME', 'http']
        ],
        '#config_development': [
            ['INHERIT_FROM', '#config'],
            ['TESTING', True],
            ['DEBUG', True]
        ],
        'example_template': [
            ['<head>', None, None, None],
            [None, '<title>', 'Fullstack with Excel', '</title>'],
            ['</head>', None, None, None],
            ['{% block content %}', None, None, None],
            ['{% endblock %}', None, None, None]
        ],
        'hello_world': [
            ['{% extends "example_template" %}', None, None],
            ['{% block content %}', None, None],
            ['<b>', 'hello, world!', '</b>'],
            ['<br />', '<br />', None],
            ['<a href="{{ url_for(\'foo\') }}">', 'See some data?', '</a>'],
            ['{% endblock %}', None, None]
        ],
        '&actual_table': [
            ['Name', 'Number of pets'],
            ['Bob', 4],
            ['Mary', 2],
            ['Joe', 0]
        ],
        'foo': [
            ['{% extends "example_template" %}', None],
            ['{% block content %}', None],
            [None, "<h3>My Friends' Pets</h3>"],
            [None, '<br \>'],
            [None, '{{ render_sheet("&actual_table") }}'],
            [None, '<br \>'],
            [None, 'Want to see a blueprint now?'],
            [None, '<a href="{{ url_for(\'example_blueprint.bar\') }}">Click here!</a>'],
            ['{% endblock %}', None]
        ]
    }

    bp = {
        '#routes': [
            ['bar', '/bar']
        ],
        'bar': [
            ['{% extends "example_template" %}', None],
            ['{% block content %}', None],
            [None, 'This page was created using a blueprint.'],
            ['{% endblock %}', None, None],
        ]
    }

    build_workbook_from_dict(data=base, file_name='demo_website.xlsx')
    build_workbook_from_dict(data=bp, file_name='example_blueprint.xlsx')
