import setuptools

version = {}
with open('src/paukenator/version.py') as fd:
    exec(fd.read(), version)

with open("README.rst", "r", encoding='utf-8') as fd:
    long_description = fd.read()

setuptools.setup(
    name='paukenator',
    description='A tool to help you practice with a text.',
    long_description=long_description,
    long_description_content_type="text/x-rst",
    author='Nikolai Krot',
    author_email='talpus@gmail.com',
    version=version['__version__'],
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},
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
        'License :: OSI Approved :: MIT License',
    ]
)
