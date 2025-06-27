from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as file:
    long_des = file.read()

setup(
    name="fakedpy",
    version="1.3",
    packages=find_packages(),
    package_data={"fakedpy": ["*.py"]},
    install_requires=[
        'pandas',
        'faker'
    ],
    description="A Python library for generating fake data with various output formats.",
    long_description=long_des,
    long_description_content_type="text/markdown",
    author="Arya Wiratama",
    author_email= "aryawiratama2401@gmail.com",
    python_requires='>=3.10'
)