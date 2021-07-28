import setuptools

setuptools.setup(
    name="statetrace_django",
    version="0.0.2",
    packages=setuptools.find_packages(),
    license="LICENSE.txt",
    description="Statetrace for Django",
    install_requires=["Django >= 3.0.0"],
)
