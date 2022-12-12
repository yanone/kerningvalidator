from setuptools import setup, find_packages
import platform
import os

this_directory = os.path.dirname(__file__)

WIN = platform.system() == "Windows"
MAC = platform.system() == "Darwin"
LINUX = platform.system() == "Linux"

install_requires = [
    line.strip()
    for line in open(os.path.join(this_directory, "requirements.txt")).readlines()
    if bool(line.strip()) and not line.strip().startswith("#")
]
long_description = open(os.path.join(this_directory, "README.md")).read()
print(install_requires)

setup(
    name="kerningvalidator",  # How you named your package folder (MyLib)
    version="0.1.1.post3",  # .post2
    license="apache-2.0",
    # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    author="Yanone",  # Type in your name
    author_email="post@yanone.de",  # Type in your E-Mail
    url="https://github.com/yanone/kerningvalidator",
    # Provide either the link to your github or to your website
    keywords=["fonts"],  # Keywords that define your package best
    install_requires=install_requires,
    entry_points={
        "console_scripts": [
            "kerningvalidator = kerningvalidator.cli:main",
        ]
    },
    package_dir={"": "Lib"},
    packages=find_packages("Lib"),
    include_package_data=True,
    long_description=long_description,
    long_description_content_type="text/markdown",
)
