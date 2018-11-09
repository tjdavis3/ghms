from setuptools import setup

setup (
    name='ghms',
    version='0.1',
    py_modules=['ghms'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        ghms=ghms:cli
    '''
)
