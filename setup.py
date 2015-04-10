import os
from setuptools import setup
from setuptools.command.install import install
from ConfigParser import ConfigParser

class InstallTasks(install):
    """ set up files """
    def run(self):        
        
        uid = int(os.getenv('SUDO_UID', '0'))
        gid = int(os.getenv('SUDO_GID', '0'))

        # create directory for daemon PID file
        pid_dir = '/var/run/acertive/'
        if not os.path.isdir(pid_dir):
            os.mkdir(pid_dir)
            os.chown(pid_dir, uid, gid)

        # create config file
        conf_file = 'config.cfg'
        data_dir = '/etc/acertive/'
        if not os.path.isdir(data_dir):
            os.mkdir(data_dir)
            os.chown(data_dir, uid, gid)

        certs_file = 'acertive_tracked.json'
        # if not os.path.isfile(conf_file):
        conf = ConfigParser()
        conf.add_section('MAIN')
        conf.set('MAIN','notifyMethod','log')
        conf.set('MAIN','storedCertsFile', os.path.join(data_dir,certs_file))
        conf.set('MAIN','weeklyThreshold','60')
        conf.set('MAIN','dailyThreshold','14')

        conf.add_section('MAIL')
        conf.set('MAIL','SMTPServerName','localhost')
        conf.set('MAIL','senderAddr','acertive@acertive.d')
        conf.set('MAIL','notifyAddrs','')
        conf.set('MAIL','useTLS', 0)


        with open(os.path.join(data_dir,conf_file), 'wb') as cfile:
            conf.write(cfile)
        os.chown(os.path.join(data_dir,conf_file), uid, gid)
                
        # create tracked certs file        
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)            
        open(os.path.join(data_dir,certs_file), 'a').close()
        os.chown(os.path.join(data_dir,certs_file), uid, gid)

        install.run(self)

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "acertive",
    version = "1.0",
    author = "Nigel Mason",
    author_email = "nigel@nigeldmason.com",
    description = ("An SSL certificate monitor for Linux"),
    license = "GPLv2",
    keywords = "SSL certificate expiry notify",
    url = "https://github.com/ndmason1/acertive",
    packages=["acertive"],
    long_description=read("README.md"),
    install_requires=["pyopenssl"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 2",
        "Topic :: System :: Networking :: Monitoring"
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