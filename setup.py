import os
from setuptools import setup
import pathlib

here = pathlib.Path(__file__).parent
os.chdir(here)

icons = {
    "64": ["pynes/ui/icons/64x64/apps/"+x for x in os.listdir("pynes/ui/icons/64x64/apps")],
    "128": ["pynes/ui/icons/128x128/apps/"+x for x in os.listdir("pynes/ui/icons/128x128/apps")],
    "256": ["pynes/ui/icons/256x256/apps/"+x for x in os.listdir("pynes/ui/icons/256x256/apps")],
    "512": ["pynes/ui/icons/512x512/apps/"+x for x in os.listdir("pynes/ui/icons/512x512/apps")],
    "scalable": ["pynes/ui/icons/scalable/apps/"+x for x in os.listdir("pynes/ui/icons/scalable/apps")],
}

os.system('chmod +777 org.astralco.pyne.desktop')
os.system('chmod +777 scripts/pynes')

setup(
    name="pynes",
    version="3.1.0",
    author="AstralDev",
    author_email="ekureedem480@gmail.com",
    description='A simple python mine game',
    long_description=str(open('README.md').read()),
    long_description_content_type="text/markdown",
    license="LGPL v3",
    keywords="mines bomb",
    python_requires=">=3",
    install_requires=["timeutilities"],
    scripts=["scripts/pynes"],
    packages=['pynes'],
    package_data={
        'pynes':['ui/style.css', 'ui/style.css', 'ui/colors.css', 'ui/menu.xml',
                     'ui/bomb.svg', 'ui/flagged.svg', 'ui/flagged-unsure.svg']
    },
    data_files=[
        ("share/applications", ["org.astralco.pyne.desktop"]),
        ("share/icons/hicolor/512x512/apps", icons["512"]),
        ("share/icons/hicolor/128x128/apps", icons["128"]),
        ("share/icons/hicolor/256x256/apps", icons["256"]),
        ("share/icons/hicolor/64x64/apps", icons["64"]),
        ("share/icons/hicolor/scalable/apps", icons["scalable"]),
    ]
)
