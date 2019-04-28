import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name='dbtsdk',
    version='0.2',
    author="Rob Dunham",
    author_email="devnilpo@gmail.com",
    description="DBT API SDK for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Nilpo/dbt-sdk-python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ]
)