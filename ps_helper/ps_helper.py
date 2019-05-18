import click
import os

"""
Arrange necessary commands.

1. build from source
2. test with one input
3. test with whole input
4. make configure file for easy reusement
    - source
    - executable name
    - test case path
    - info option (show detail, not detail)
"""


@click.group()
def cli():
    pass


@cli.command()
@click.argument('source', type=click.Path(exists=True))
@click.option('--build-command', default="g++", help="command to build from input")
@click.option('--build-parameter', default='-o', help="Additional parameter for build")
@click.option('--output', default="a.out", help="path to make output")
@click.option('--verbose', '-v', is_flag=True, help='Enables verbose mode')
def build(source, build_command, build_parameter, output, verbose):
    if verbose:
        click.echo(
            click.style(
                "This Command will execute\n"
                f"{build_command} {source} {build_parameter} {output}",
                fg='green',
                bold=True
            )
        )
    os.system(f"{build_command} {source} {build_parameter} {output}")


@cli.command()
def hello():
    click.echo(click.style('Hello World!', fg='green'))
    click.echo(click.style('Some more text', bg='blue', fg='white'))
    click.echo(click.style('ATTENTION', blink=True, bold=True))
    click.echo("Hello world!")


if __name__ == '__main__':
    cli()
