import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()


__version__ = "1.0"

REPO_NAME = "NorthCarolina_CameroonChapter_AngusIssues"
AUTHOR_USER_NAME = "Omdena"
SRC_REPO = "mlProject"
AUTHOR_EMAIL = "omdena@gmail.com"


setuptools.setup(
    name=SRC_REPO,
    version=__version__,
    author=AUTHOR_USER_NAME,
    author_email=AUTHOR_EMAIL,
    description="Using EDA and Forecasting of Best Animal Science Practices",
    long_description=long_description,
    long_description_content="text/markdown",
    url=f"https://dagshub.com/{AUTHOR_USER_NAME}/{REPO_NAME}",
    project_urls={
        "Bug Tracker": f"https://dagshub.com/{AUTHOR_USER_NAME}/{REPO_NAME}/issues",
    },
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src")
)