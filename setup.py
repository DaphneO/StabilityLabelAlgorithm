import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="StabilityLabelAlgorithm",
    version="1.0",
    author="Daphne Odekerken",
    author_email="d.odekerken@uu.nl",
    description="Package for estimating justification and stability status of claims",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)