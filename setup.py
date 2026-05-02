from setuptools import setup, find_packages

setup(
    name="slidr",
    version="0.1.0",
    author="Ali Bahar",
    description="AI Presentation Maker - Create presentations from topics or documents",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/blastbraker/Slidr",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "slidr=slidr.gui:main",
        ],
    },
)