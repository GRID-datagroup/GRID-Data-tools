import os
from setuptools import setup, find_namespace_packages


# the data files
def data_files():
    data_file = []
    data_file_dir = "gdt/data"
    for root, dirs, files in os.walk(data_file_dir):
        if files:
            for file in files:
                data_file.append(os.path.join(root.replace("gdt/", ""), file))
    return data_file


def requirement_control():
    requirements = ["gbm-data-tools==1.1.1"]
    return requirements


# Import the version information from the package init file
with open("gdt/__init__.py") as f:
    exec(f.read())

setup(
    name="grid-data-tools",
    version=__version__,
    url="https://grid.com",
    packages=["gdt", "gdt.plot", "gdt.utils"],
    package_data={"gdt.data": data_files()},
    include_package_data=True,
    license="license.txt",
    author="GRID Team",
    author_email="grid@grid.com",
    description="The GRID Data Tools",
    python_requires=">=3.7",
    install_requires=requirement_control(),
)
