import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.readlines()

setuptools.setup(
    name="osfa",
    version="2.0",
    author="FreehandBlock51",
    author_email="freehandblock51@outlook.com",
    description="One Shell For All",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/FreehandBlock51/OSFA",
    project_urls={
        "Bug Tracker": "https://github.com/FreehandBlock51/OSFA/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src", exclude=("tests","tests.*")),
    python_requires=">=3.6",
    requirements=requirements,
)