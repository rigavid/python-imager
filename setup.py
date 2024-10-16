from setuptools import setup, find_packages

VERSION = '0.0.0' 
DESCRIPTION = 'Python image program'
LONG_DESCRIPTION = 'A package to create images, manage files and more.'

setup(
        name="pyimg", 
        version=VERSION,
        author="T-Sana",
        author_email="tsana.code@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=["numpy", "opencv-python", "screeninfo"],
        keywords=['python', 'image'],
        classifiers= [
            "Programming Language :: Python :: 3",
            "Operating System :: Linux :: Fedora",
            "Operating System :: Microsoft :: Windows",
        ]
)