import setuptools

setuptools.setup(
    name="statetrace_django",
    version="0.0.2",
    packages=["statetrace_django", "statetrace_django.apps", "statetrace_django.migrations"],
    license="LICENSE.txt",
    description="Statetrace for Django",
    install_requires=["Django >= 3.0.0"],
)
