from setuptools import setup, find_packages

setup(
    name='ssa',
    version='0.0.1',
    description='A platform where scientists can upload algorithms by earning from them, and developers can find the algorithms they need.',
    author='Mattia Neroni, Ph.D, Eng.',
    author_email='mneroni@uoc.edu',
    url='https://github.com/mattianeroni/server-side-algorithms',
    package_dir = {
        'ssa': 'ssa'
    },
    packages=[
        'ssa'
    ],
    python_requires='>=3.8',
    classifiers=[
        "Development Status :: 3 - Alpha"
    ]
)