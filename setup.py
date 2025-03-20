from setuptools import find_packages, setup

setup(
    name="fakedpy",
    version="1.0",
    packages=find_packages(),
    package_data={"fakedpy": ["*.py"]},
    install_requires=[
        'pandas',
        'faker'
    ],
    description="A simple fake data generator that exports results to CSV",
    author="aryawiratama2401@gmail.com",
    python_requires='>=3.10'
)