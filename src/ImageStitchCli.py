import click

from Util import *

@click.command()
@click.option('-d', '--difference', default=10)
@click.option('-o', '--output', default="Results.png")
@click.argument('top')
@click.argument('bottom')
def stitchHeroes(difference, top, bottom, output):

    if top == bottom:
        click.echo('Files need to be different.')
        return;


    if not checkExtensions(top) or not checkExtensions(bottom) or not checkExtensions(output):
        click.echo('Files need to be .png, .jpg, or .jpeg.')
        return;

    stitchImages(top, bottom, output, difference)
    click.echo(f'Files saved to {output}')


@click.command()
@click.option('-o', '--output', default="Results.png")
@click.argument('files', nargs=-1, type=click.Path(exists=True))
def stitchBattles(files, output):
    if len(files) < 2:
        click.echo('At least two image files need to be attached.')
        return;

    for file in files:
        if not checkExtensions(file):
            click.echo('Files need to be .png, .jpg, or .jpeg.')
            return;

    hStitch(files, output)
    click.echo(f'Files saved to {output}')

if __name__ == "__main__":
    stitch()
