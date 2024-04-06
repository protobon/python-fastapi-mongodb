from app.common.config import Config
from app.start import run
import click


@click.command()
@click.option('--conf', default='config.yml', type=click.Path())
def run_server(conf):
    Config(path=conf)
    run()


if __name__ == "__main__":
    run_server()
