import os
from setuptools import setup
from setuptools.command.install import install

class InstallTasks(install):
    """ set up files """
    def run(self):
        # auto search for certs

        # create user,group for daemon

        # create certs.json
        dataDir = '/etc/acertive/'
        if not os.path.exists(dataDir):
            os.makedirs(dataDir)
            open(dataDir+'certs.json', 'a').close()
        
        # add to init.d

        install.run(self)

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "acertive",
    version = "0.5",
    author = "Nigel Mason",
    author_email = "nigel@nigeldmason.com",
    description = ("An SSL certificate monitor for Linux"),
    license = "GPLv2",
    keywords = "SSL certificate expiry notify",
    url = "https://github.com/ndmason1/acertive",
    packages=["acertive"],
    long_description=read("README.md"),
    install_requires=["pyopenssl", "python-daemon"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities"
    ],
    entry_points={
        'console_scripts': [
            'acertive = acertive.__main__:main'
        ],
    },
    cmdclass={
        'install': InstallTasks
    }
)