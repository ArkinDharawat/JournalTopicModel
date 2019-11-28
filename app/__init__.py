from flask import Flask
# from argparse import ArgumentParser

# parser = ArgumentParser()
# parser.add_argument('-db_type', default="sql")
# args = parser.parse_args()

app = Flask(__name__)
import app.views

if __name__ == '__main__':
  app.run(host='0.0.0.0')