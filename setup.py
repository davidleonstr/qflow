from setuptools import setup, find_packages

setup(
    name="QFlow",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "setuptools",
        "QtPy",
        "rpack @ git+https://github.com/davidleonstr/rpack.git@080667c3f9494afdb0c26c79fbb773422a1dc111"
    ],
    description="Python microframework designed to simplify the management of PyQt/PySide applications.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author="David León",
    author_email="davidalfonsoleoncarmona@gmail.com",
    url="https://github.com/davidleonstr/qflow",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11.3",
    include_package_data=True,
)

# I use Python 3.13.1.