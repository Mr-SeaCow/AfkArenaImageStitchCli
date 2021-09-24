from setuptools import setup

# pip install --editable .

setup(
    name='imgstitch-cli',
    py_modules=['ImageStitchCli', 'Util'],
    install_requires=[
        'Click',
        'opencv-python',

    ],
    entry_points='''
        [console_scripts]
        stitch=ImageStitchCli:stitch
    ''',
)