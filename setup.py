from setuptools import setup

setup(
    name="clipea",
    version="0.1.0",
    description=" 📎🟢 Like Clippy but for the CLI. A blazing fast AI helper for your command line ",
    url="https://github.com/dave1010/clipea/",
    author="Dave Hulbert",
    author_email="dave1010@gmail.com",
    license="MIT",
    packages=["clipea"],
    install_requires=["llm"],
    python_requires=">=3.10",
)
