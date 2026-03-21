from setuptools import setup, find_packages

setup(
    name="empredictor",
    version="0.2",
    packages=find_packages("src"),
    package_dir={"": "src"},
    python_requires=">=3.10",
    install_requires=[
        "Flask>=3.0",
        "Flask-Cors>=4.0",
        "pydantic>=2.6",
        "pandas>=2.2",
        "numpy>=1.26",
    ],
)
