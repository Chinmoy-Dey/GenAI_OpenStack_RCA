from setuptools import setup, find_packages

setup(
    name="logbert_app",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "torch",
        "transformers",
        "pandas",
        "scikit-learn"
    ],
)
