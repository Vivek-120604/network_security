'''
setup.py file is an essential component of a Python project that uses setuptools for packaging and distribution.It 
describes your project -its name ,version, author info, and a short description.
'''




from setuptools import setup, find_packages


def get_requirements():
    """
    this function will return list of requirements 
    """
    requirements_lst = []
    try:
        with open("requirements.txt") as f:
            lines = f.readlines()
            for line in lines:
                requirement = line.strip()
                if requirement and requirement!= '-e .' :
                    requirements_lst.append(requirement)
                
    except FileNotFoundError:
        print("requirements.txt file not found. Proceeding without external dependencies.")
    return requirements_lst

print(get_requirements())
 
 
setup(
    name='network_security_project',
    version = '0.1.0',
    author = 'Vivek Kumar Singh',
    author_email = 'iamvivekkumar12@gmail.com',
    description = 'A project on network security',
    packages = find_packages(),
    install_requires = get_requirements(),
    
 )