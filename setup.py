import setuptools

from pkg_resources import parse_requirements


with open('requirements.txt', 'r') as f:
    requirements = [
        str(r)
        for r in parse_requirements(f)
    ]

requirements.append('setuptools')

setuptools.setup(
    name='opticam-dbx',
    use_autover=True,
    description='Tool for downloading Opticam surveillance camera videos from Dropbox',
    url='https://github.com/jannero/opticam-dbx',
    author='Janne Rönkkö',
    author_email='jroo@iki.fi',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Topic :: Utilities',
    ],
    keywords='opticam dropbox surveillace camera cctv',
    packages=[
        'opticam_dbx',
    ],
    python_requires='>=3.6',
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'opticam-dbx = opticam_dbx.cli:main',
        ],
    },
    setup_requires=[
        'setuptools_autover',
    ],
)
