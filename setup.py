from distutils.core import setup

setup(name = "pyfem1d",
    version = "100",
    description = "1d finite elements for testing material formulations",
    author = "nrs",
    author_email = "onur@kreix.com",
    url = "https://github.com/nrs",
    packages = ['pyfem1d', 'pyfem1d.constitutive', 'pyfem1d.load'],
    package_data = {'pyfem1d' : ["pyfem1d/*.py"],
                    'pyfem1d.constitutive' : ["pyfem1d/constitutive/*.py"],
                    'pyfem1d.load' : ["pyfem1d/load/*.py"]},
    scripts = ["bin/pyfem1d"],
    #long_description = """Really long text here."""
)
