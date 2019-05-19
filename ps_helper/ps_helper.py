import click
import os

from subprocess import Popen, PIPE, STDOUT, check_output
import time
import math

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
@click.option('--executable', default="a.out", help="path to make output")
@click.option('--verbose', '-v', is_flag=True, help='Enables verbose mode')
def build(source, build_command, build_parameter, executable, verbose):
    if verbose:
        click.echo(
            click.style(
                "This Command will execute\n"
                f"{build_command} {source} {build_parameter} {executable}",
                fg='green',
                bold=True
            )
        )
    val = os.system(f"{build_command} {source} {build_parameter} {executable}")
    if val != 0:
        raise OSError("Build failed!")


@cli.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.option('--output-file', '-o', type=click.Path(exists=True))
@click.option('--executable', default="./a.out")
@click.option('--verbose', '-v', is_flag=True, help='Enables verbose mode')
@click.option('--time-limit', '-t', default=1, help="Timeout seconds")
def test(input_file, output_file, executable, verbose, time_limit):
    if not output_file:
        output_file = input_file.replace('in', 'out')

    start_time = time.time()
    output = check_output(f"{executable} < {input_file}", shell=True, timeout=time_limit)
    time_cost = time.time() - start_time
    output = output.decode('ascii')

    diff_output = Popen(f"echo {output} | diff -w {output_file} - ", stderr=STDOUT, stdout=PIPE, shell=True)
    diff_stdout, diff_stderr = diff_output.communicate()
    click.echo(f"Test case {input_file} : ", nl=False)

    if verbose:
        if diff_output.returncode == 0:
            click.echo(click.style(f"Success", fg='green'))
        else:
            click.echo(click.style(f"Fail", fg='red'))
            click.echo(diff_stdout)

            click.echo(
                f"execution time : {math.floor(time_cost*100)}ms"
            )
    return time_cost


@cli.command()
def hello():
    click.echo(click.style('Hello World!', fg='green'))
    click.echo(click.style('Some more text', bg='blue', fg='white'))
    click.echo(click.style('ATTENTION', blink=True, bold=True))
    click.echo("Hello world!")
