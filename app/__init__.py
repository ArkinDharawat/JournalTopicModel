import click
from flask import Flask
app = Flask(__name__)
@app.cli.command('set-db')
@click.argument("db_type")
def set_db(db_type):
    print(db_type)
    from app import views