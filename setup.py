# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='Profil3r',
    version="1.0.5",
    packages=find_packages(),
    author="Rog3rSm1th",
    author_email="r0g3r5@protonmail.com",
    install_requires=["pwnedpasswords"],
    description="Profil3r is an OSINT tool that allows you to find the differents social accounts and emails used by a person",
    include_package_data=True,
    url='https://github.com/Rog3rSm1th/Profil3r',
    classifiers=[
        "Programming Language :: Python",
    ],
    license='MIT'
)