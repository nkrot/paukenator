import setuptools

version = {}
with open('src/paukenator/version.py') as fd:
    exec(fd.read(), version)

setuptools.setup(
    name='paukenator',
    description='A tool to help you learn a text by heart',
    author='Nikolai Krot',
    author_email='talpus@gmail.com',
    version=version['__version__'],
    packages=setuptools.find_packages('src'),
    package_dir={'' : 'src'},
    entry_points={
        'console_scripts': [
            'paukenator = paukenator.cli.main:main'
        ]
    },
    classifiers=[
        'Environment :: Console',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Education',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
    ]
)
