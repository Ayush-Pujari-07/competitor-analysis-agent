from setuptools import find_packages, setup
from typing import List

def get_requirements(file_path: str) -> List[str]:
    """
    Retrieves a list of requirements from a file.

    Args:
        file_path (str): The path to the file containing the requirements.

    Returns:
        List[str]: A list of requirements extracted from the file, excluding '-e .'.
    """
    with open(file_path) as file_obj:
        requirements = [req.strip() for req in file_obj.readlines()]
        if '-e .' in requirements:
            requirements.remove('-e .')
    return requirements  

setup(
    name='competitor-analysis-agent',
    version='0.0.1',
    author='ayush-pujari-07',
    author_email='ayush08.pujari@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt'),
)
