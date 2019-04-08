#! /usr/bin/env python


descr = """Analysis of rfMRI with population-based covariance shrinkage"""

import os
import sys

DISTNAME = "posce"
DESCRIPTION = "POpulation Shrinkage Connectivity Estimator (PoSCE)"
LONG_DESCRIPTION = descr
MAINTAINER = "Mehdi Rahim"
MAINTAINER_EMAIL = "mehdi.rahim@inria.fr"
URL = ""
LICENSE = "new BSD"
DOWNLOAD_URL = ""
VERSION = "0.alpha"

if (
    len(
        set(
            (
                "develop",
                "release",
                "bdist_egg",
                "bdist_rpm",
                "bdist_wininst",
                "install_egg_info",
                "build_sphinx",
                "egg_info",
                "easy_install",
                "upload",
                "--single-version-externally-managed",
            )
        ).intersection(sys.argv)
    )
    > 0
):
    import setuptools


from numpy.distutils.core import setup


def configuration(parent_package="", top_path=None):
    if os.path.exists("MANIFEST"):
        os.remove("MANIFEST")

    from numpy.distutils.misc_util import Configuration

    config = Configuration(None, parent_package, top_path)

    config.add_subpackage("posce")

    return config


if __name__ == "__main__":
    setup(
        configuration=configuration,
        name=DISTNAME,
        maintainer=MAINTAINER,
        include_package_data=True,
        maintainer_email=MAINTAINER_EMAIL,
        description=DESCRIPTION,
        license=LICENSE,
        url=URL,
        version=VERSION,
        download_url=DOWNLOAD_URL,
        long_description=LONG_DESCRIPTION,
        test_suite="nose.collector",  # for python setup.py test
        zip_safe=False,  # the package can run out of an .egg file
        classifiers=[
            "Intended Audience :: Science/Research",
            "Intended Audience :: Developers",
            "License :: OSI Approved",
            "Programming Language :: C",
            "Programming Language :: Python",
            "Topic :: Software Development",
            "Topic :: Scientific/Engineering",
            "Operating System :: Microsoft :: Windows",
            "Operating System :: POSIX",
            "Operating System :: Unix",
            "Operating System :: MacOS",
        ],
        install_requires=["nilearn"],
    )
