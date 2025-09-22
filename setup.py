from setuptools import setup, find_packages
setup(
    name="cybersleuth",
    version="0.1.0",
    description="Windows-friendly CLI cybersecurity toolset",
    author="Your Name",
    author_email="you@example.com",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "certifi",
        "idna",
        "rich",
        "scapy",
        "requests",
    ],
    entry_points={
        "console_scripts": [
            "cybersleuth=cybersleuth:main",  # points to cybersleuth/__init__.py main()
        ],
    },
)

