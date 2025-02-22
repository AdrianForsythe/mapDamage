#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import subprocess
import sys

# Version check prior to non-stdlib imports
if sys.version_info < (3, 5):
    sys.stderr.write(
        "ERROR: mapDamage requires Python v3.5 or above, but "
        "Python v%i.%i was used\n" % sys.version_info[:2]
    )
    sys.exit(1)


from setuptools import setup, Extension
from setuptools.command.build_py import build_py as SetuptoolsBuildPy


class GitVersionBuild(SetuptoolsBuildPy):
    def run(self):
        if os.path.exists(".git"):
            try:
                version = subprocess.check_output(
                    ("git", "describe", "--always", "--tags", "--dirty")
                )
            except (subprocess.CalledProcessError, OSError) as error:
                raise SystemExit("Could not determine mapDamage version: %s" % (error,))

            with open(os.path.join("mapdamage", "_version.py"), "w") as handle:
                handle.write("#!/usr/bin/env python\n")
                handle.write("__version__ = %r\n" % (version.decode("utf-8").strip(),))

        super().run()


setup(
    cmdclass={"build_py": GitVersionBuild},
    name="mapdamage",
    version="2.2.1",
    author="Aurélien Ginolhac, Mikkel Schubert, Hákon Jónsson",
    packages=["mapdamage"],
    package_data={"mapdamage": ["r/*.r", "r/stats/*.r", "tests/*"]},
    entry_points={"console_scripts": ["mapDamage=mapdamage.main:entry_point"]},
    url="https://github.com/ginolhac/mapDamage",
    license="LICENSE.txt",
    description="mapDamage tracks and quantifies DNA damage patterns in ancient DNA sequencing reads generated by Next-Generation Sequencing platforms",
    long_description=open("README.md").read(),
    long_description_content_type='text/markdown',
    python_requires=">=3.5",
    install_requires=["coloredlogs", "pysam"],
    ext_modules=[
        Extension(
            "mapdamage.seqtk", sources=["mapdamage/seqtk/seqtk.c"], libraries=["z"],
        )
    ],
)
