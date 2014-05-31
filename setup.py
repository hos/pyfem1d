from distutils.core import setup

setup(name = "feminist",
    version = "100",
    description = "1d finite elements for testing material formulations",
    author = "nrs",
    author_email = "onur@kreix.com",
    url = "https://github.com/nrs",
    packages = ['feminist', 'feminist.constitutive', 'feminist.load'],
    package_data = {'feminist' : ["feminist/*.py"],
                    'feminist.constitutive' : ["feminist/constitutive/*.py"],
                    'feminist.load' : ["feminist/load/*.py"]},
    scripts = ["bin/feminist"],
    #long_description = """Really long text here."""
)
