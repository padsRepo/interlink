# This file is used to run interlink from the CLI..
# Copyright Joe Corso armyglass@hotmail.com

'''
This module is used to access Interlink from the CLI.
'''

import click
from interlink.formulator import DB, Generator
import interlink as i
import os
from flask import render_template

class Model:
  '''Test Model'''
  def __init__(self):
    pass


  def report(table):
    gen = Generator('accounting', 'DB_USER', 'DB_PASS')
    colName, colRow, error, title = gen.generateReport(table)
    char = "-" * os.get_terminal_size()[0]
    margin = ' '.center(int(os.get_terminal_size()[0] / 2))
    border = click.style("*" * os.get_terminal_size()[0], fg='cyan')
    title = click.style(f'{margin}{title} Report\n', fg='cyan')
    header = click.echo(border + title + border)
    col = ''
    row = ''
    c = [colRow[i] for i in range(len(colRow))]
    show = click.style(f'{c}', fg='red')
    for i in colName:
      col += click.style(f'{i[0]:<13}', fg='magenta')
      row += click.style(f'{colRow[0][0]:<13}', fg='magenta')
      #print(colName[i][0], '\n', colRow[0][i], '\n', colRow[1][i])
    #rowt = click.style(f'{[r for r in colRow]}', fg='magenta')
    body = click.echo(f'{col}\n{row}\n{show}\n')

@click.group()
@click.version_option(i.__version__)
def cli():
  ''' CLI Mode '''
  print("CLI MODE")

@cli.command('report')
@click.option('-t', '--table', required=True, help='The table to generate a report for', default='rawMaterials')
def report(table):
  '''Generate a report for table'''
  Model.report(table)

all_colors = (
    "black",
    "red",
    "green",
    "yellow",
    "blue",
    "magenta",
    "cyan",
    "white",
    "bright_black",
    "bright_red",
    "bright_green",
    "bright_yellow",
    "bright_blue",
    "bright_magenta",
    "bright_cyan",
    "bright_white",
)


@cli.command('colors')
def colors():
    """This script prints some colors. It will also automatically remove
    all ANSI styles if data is piped into a file.

    Give it a try!
    """
    for color in all_colors:
        click.echo(click.style(f"I am colored {color}", fg=color))
    for color in all_colors:
        click.echo(click.style(f"I am colored {color} and bold", fg=color, bold=True))
    for color in all_colors:
        click.echo(click.style(f"I am reverse colored {color}", fg=color, reverse=True))
    for color in all_colors:
        click.echo(click.style(f"I am background colored {color}", bg=color))

    click.echo(click.style("I am blinking", blink=True))
    click.echo(click.style("I am underlined", underline=True))

if __name__ == '__main__':
    cli() 
    colors()


