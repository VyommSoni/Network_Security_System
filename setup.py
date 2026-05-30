'''The setup.py file is an essential part to package your project.It is used bt setup tools to define the cpnfiguration of  our project
'''

# This is usually the last step we do in deployment or in project ..
from setuptools import find_packages,setup
from typing import List



def get_requirements()->List[str]:
    """
    This function will return list of reuirements

    """
    
    requirements_list=[]  
    try:
        with open("requirements.txt","r",encoding="utf-16") as file:
            files=file.readlines()

            for lines in files:
                requirements=lines.strip()
                if requirements and requirements!='-e .':
                 requirements_list.append(requirements)
    except Exception as e:
        print(f"file not found {e}")

    return requirements_list

setup(
    name="Network_security",
    version="0.0.1",
    author="VyomSoni",
    author_email="svyom21@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements()
)






