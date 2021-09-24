from setuptools import setup

# pip install --editable .

setup(
    name='imgstitch-cli',
    py_modules=['ImageStitchCli', 'Util'],
    install_requires=[
        'Click',
        'opencv-python',
        'scikit-build',
        'importlib; python_version == "3.9"',
        'packaging'
    ],
    entry_points='''
        [console_scripts]
        stitchHeroes=ImageStitchCli:stitchHeroes
        stitchBattles=ImageStitchCli:stitchBattles
    ''',
)