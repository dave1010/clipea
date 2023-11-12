"""Setup file for clipea
"""
from setuptools import setup, find_packages

setup(
    name="clipea",
    version="0.1.0",
    description=" 📎🟢 Like Clippy but for the CLI. A blazing fast AI helper for your command line ",
    url="https://github.com/dave1010/clipea/",
    author="Dave Hulbert",
    author_email="dave1010@gmail.com",
    license="MIT",
    packages=find_packages(),
    install_requires=["llm"],
    python_requires=">=3.10",
    package_data={"clipea": ["*.txt", "clipea.zsh"]},
    entry_points={"console_scripts": ["clipea = clipea.__main__:clipea_main"]},
)
