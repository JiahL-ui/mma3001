from setuptools import setup, find_packages

setup(
    name="mma3001-workshop",
    version="0.1.0",
    description="MMA3001 Workshop 1 — Digital Data Management, Documentation, AI and Testing",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.10",
    install_requires=[
        "numpy>=1.24",
    ],
)
