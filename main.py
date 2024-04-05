from app.api import run
from app.common.config import Config
import click
import yaml


@click.command()
@click.option('--conf', default='config.yml', type=click.Path())
def run_server(conf):
    config = dict()
    yaml.load(conf, config)
    Config(config)
    run()


if __name__ == "__main__":
    run_server()
