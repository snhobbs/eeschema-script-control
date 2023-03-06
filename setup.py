#!/usr/bin/env python3
from setuptools import setup, find_packages
from glob import glob


requirements = []
with open("requirements.txt", "r") as f:
    for line in requirements:
        requirements.append(line)


with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()


setup(name='eeschema_script_control',
    version='0.1.0',
    description='',
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author='Simon Hobbs',
    author_email='',
    license='MIT',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Linux",
    ],
    python_requires='>=3.6',
    install_requires=requirements,
    #test_suite='nose.collector',
    #tests_require=['nose'],
    #scripts=list(glob("bin/*.py")),
    entry_points={
            #'console_scripts': [
            #]
    },
    #include_package_data=True,
    #zip_safe=True)
    )
