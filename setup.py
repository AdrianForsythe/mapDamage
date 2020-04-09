#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import subprocess

from setuptools import setup, Extension
from setuptools.command.install import install as SetuptoolsInstall


class GitVersionInstall(SetuptoolsInstall):
    def run(self):
        if os.path.exists(".git"):
            try:
                version = subprocess.check_output(("git", "describe", "--always", "--tags", "--dirty"))
            except (subprocess.CalledProcessError, OSError) as error:
                raise SystemExit("Could not determine mapDamage version: %s" % (error,))

            with open(os.path.join("mapdamage", "_version.py"), "w") as handle:
                handle.write("#!/usr/bin/env python\n")
                handle.write("__version__ = %r\n" % (version.decode("utf-8").strip(),))

        super().run()


setup(
    cmdclass={'install': GitVersionInstall},
    name='mapdamage',
    version='2.2.0',
    author="Aurélien Ginolhac, Mikkel Schubert, Hákon Jónsson",
    author_email='MSchubert@snm.ku.dk, jonsson.hakon@gmail.com',
    packages=['mapdamage'],
    package_data={'mapdamage': ['Rscripts/*.R', 'Rscripts/stats/*.R', 'tests/*']},
    scripts=['bin/mapDamage'],
    url='https://github.com/ginolhac/mapDamage',
    license='LICENSE.txt',
    description='mapDamage tracks and quantify DNA damage pattern among ancient DNA sequencing reads generated byi Next-Generation Sequencing platforms',
    long_description=open('README.md').read(),
    python_requires=">=3.5",
    install_requires=["pysam"],
    ext_modules=[Extension("mapdamage.seqtk", ["mapdamage/seqtk/seqtk.c"])],
)
