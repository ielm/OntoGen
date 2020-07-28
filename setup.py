from setuptools import setup, find_packages

setup(
    name="OntoGen",
    version="0.0.4",
    packages=find_packages(),

    install_requires=[
        "OntoGraph",
        "OntoAgent",
        "OntoGraph-OntoLang",
        "leialexicon",
        "leiaschemata",
        "leiaontology",
        "Flask",
        "Flask-Cors",
        "Flask-SocketIO",
        "requests",
        "nlglib"
    ],

    author="Ivan Leon",
    author_email="leoni@rpi.edu",
    description="LEIA natural language generation module",
    keywords="NLG",
    project_urls={
        "Documentation": "https://bitbucket.org/leia-rpi/OntoGen/wiki/Home",
        "Source Code": "https://bitbucket.org/leia-rpi/OntoGen/",
    }
) 
