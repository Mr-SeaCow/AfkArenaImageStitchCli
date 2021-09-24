import click
from Util import *

@click.command()
@click.option('-d', '--difference', default=10)
@click.option('-o', '--output', default="Results.png")
@click.argument('top')
@click.argument('bottom')
def stitch(difference, top, bottom, output):

    if top == bottom:
        click.echo('Files need to be different.')
        return;


    if not checkExtensions(top) or not checkExtensions(bottom) or not checkExtensions(output):
        click.echo('Files need to be .png, .jpg, or .jpeg.')
        return;

    stitchImages(top, bottom, output, difference)
    click.echo(f'Files saved to {output}')

if __name__ == "__main__":
    stitch()