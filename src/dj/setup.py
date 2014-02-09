#!/usr/bin/env python
from distutils.core import setup

setup(name="django",
	description="NotesGroup Site",
	author="PimenTech",
	author_email="info@_nospam_pimentech.net",
	url="http://www.pimentech.fr",
	packages=[
		'dj',
		'dj.notesgroup',
	],
	package_dir = {'': '..'},
)
