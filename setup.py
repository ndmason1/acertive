import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "acertive",
    version = "0.5",
    author = "Nigel Mason",
    author_email = "nigel@nigeldmason.com",
    description = ("An SSL certificate monitor for Linux"),
    license = "GPLv2",
    keywords = "example documentation tutorial",
    url = "https://github.com/ndmason1/acertive",
    packages=["acertive"],
    long_description=read("README.md"),
    install_requires=["pyopenssl"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities"
    ],
    entry_points={
        'console_scripts': [
            'acertive = acertive.__main__:main'
        ],
    }
)