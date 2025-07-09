from setuptools import setup, find_packages

setup(
    name="QFlow",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "setuptools"
    ],
    description="Python microframework designed to simplify the management of PyQt/PySide applications.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author="David León",
    author_email="davidalfonsoleoncarmona@gmail.com",
    url="https://github.com/davidleonstr/QFlow",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11.3",
)

# I use Python 3.13.1.