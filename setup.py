from setuptools import setup, find_packages

setup(
    name='NetTK',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'scapy',
        'numpy',
        'matplotlib',
    ],
)
