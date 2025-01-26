from setuptools import setup

APP = ['CipherX.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'packages': ['customtkinter', 'hashlib', 'tkinter'],
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
