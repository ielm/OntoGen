from setuptools import setup, find_packages

setup(
    name="OntoGen",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "OntoGraph",
        "leialexicon",
        "leiaontology",
        "Flask",
        "Flask-Cors",
        "Flask-SocketIO",
        "requests",
        "nlglib",
    ],
    author="Ivan Leon",
    author_email="leoni@rpi.edu",
    description="LEIA natural language generation service",
    keywords="NLG",
    project_urls={
        "Documentation": "https://app.nuclino.com/LEIA/OntoGen/",
        "Source Code": "https://bitbucket.org/ielm/OntoGen/src/master/",
    },
)
