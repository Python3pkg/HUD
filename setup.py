#!/usr/bin/env python3
from setuptools import setup, find_packages

setup(
    name="HUD",
    version="0.1",
    packages=find_packages(),
    install_requires= [
    
        "homeassistant==0.31.1",
        "icon-font-to-png==0.3.6",
        "Jinja2==2.8",
        "MarkupSafe==0.23",
        "Pillow==3.4.2",
        "pytz==2016.7",
        "PyYAML==3.12",
        "requests==2.11.1",
        "six==1.10.0",
        "sseclient==0.0.12",
        "tinycss==0.4",
        "typing==3.5.2.2",
        "voluptuous==0.9.2",
        "pgu==0.18",
        "pygame==1.9.2b8"
        
    ],
    dependency_links = 
    
    [
        
        "https://github.com/parogers/pgu/archive/67558479fe9050ba567a39fc9faa32ce74eba786.tar.gz#egg=pgu-0.18",
        "https://bitbucket.org/pygame/pygame/get/010a750596cf.tar.gz#egg=pygame-1.9.2b8"
    ]
)
