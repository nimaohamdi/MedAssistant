from setuptools import setup, find_packages

setup(
    name="MedAssistant",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
     
        "requests",
        "pandas"
    ],
    entry_points={
        "console_scripts": [
            "medassistant=medassistant.med:main" 
        ]
    },
    author="Nima Hamdi ",
    author_email="nima.jozhamdi@gmail.com.com",
    description="A Python package for managing and accessing medical data.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/nimaohamdi/MedAssistant",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
