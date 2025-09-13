from setuptools import setup, find_packages

setup(
    name="easycli",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],
    author="Parham Fakhari",
    author_email="parhamfakhari.nab2020@gmail.com",
    description="A simple CLI builder for Python",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/parhamfakhar1/easycli",
    license="MIT",
)