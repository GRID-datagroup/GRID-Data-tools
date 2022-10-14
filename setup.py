from setuptools import setup


def requirement_control():
    requirements = ["gbm-data-tools==1.1.1"]
    return requirements


# Import the version information from the package init file
with open("grid/__init__.py") as f:
    exec(f.read())

setup(
    name="grid-data-tools",
    version=__version__,
    url="https://grid.com",
    packages=["grid", "grid.binning", "grid.data", "grid.plot", "grid.utils"],
    license="license.txt",
    author="GRID Team",
    author_email="grid@grid.com",
    description="The GRID Data Tools",
    python_requires=">=3.7",
    install_requires=requirement_control(),
)
