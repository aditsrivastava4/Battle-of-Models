"""
Battle of Models - AI Debate Simulation
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="battle-of-models",
    version="2.0.0",
    author="Adit Srivastava",
    author_email="aditsrivastava4@gmail.com",
    description="AI Debate Simulation with Multiple Language Models",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aditsrivastava4/Battle-of-Models",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.10",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "battle-of-models-api=api:app",
            "battle-of-models-gradio=app:app",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
