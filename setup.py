from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as file:
    long_des = file.read()

setup(
    name="fakedpy",
    version="1.1",
    packages=find_packages(),
    package_data={"fakedpy": ["*.py"]},
    install_requires=[
        'pandas',
        'faker'
    ],
    description="A simple fake data generator that exports results to CSV",
    long_description=long_des,
    long_description_content_type="text/markdown",
    author="aryawiratama2401@gmail.com",
    python_requires='>=3.10'
)