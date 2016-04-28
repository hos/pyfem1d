from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))


setup(
    name="pyfem1d",

    version="0.0.1",

    description="1d finite elements for testing material formulations",

    author="H. Onur Solmaz",

    packages=find_packages(exclude=["contrib", "docs", "tests"]),

    download_url = "https://github.com/hos/pyfem1d",

    keywords = ["FEM", "materials", "mechanics"],

    extras_require={
        "dev": ["check-manifest"],
        "test": ["coverage"],
    },

    # package_data={
    #     "sample": ["package_data.dat"],
    # },

    # data_files=[("my_data")],

    install_requires={
    },

    entry_points={
        "console_scripts": [
            "pyfem1d=pyfem1d.main:__main__",
        ],
    },
)



