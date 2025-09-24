from setuptools import setup, find_packages

setup(
    name='NetTK',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'scapy==2.6.1',
        'numpy',
        'matplotlib==3.9.4',
    ],
    entry_points={
        'console_scripts': [
            'netTK=nettk.netTK:main',
            'netTKAnalysis=nettk.netTKAnalysis:main',
        ],
    },
)
