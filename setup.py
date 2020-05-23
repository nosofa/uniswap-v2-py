import setuptools
import uniswap

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="uniswap-v2-py",
    version=uniswap.__version__,
    author="Afonso Oliveira",
    author_email="asynctomatic@gmail.com",
    description="A unofficial wrapper for Uniswap V2",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/asynctomatic/uniswap-v2-py",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
