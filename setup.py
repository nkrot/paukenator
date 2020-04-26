import setuptools

setup(
    name='Paukenator',
    description="A tool to help you learn a text by heart",
    author="Nikolai Krot",
    author_email="talpus@gmail.com",
    version='0.0.1',
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'paukenator = paukenator.__main__:main'
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ]
)
