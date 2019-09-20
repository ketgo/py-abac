from os import path

from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))
about = {}
with open(path.join(here, 'pyabac', 'version.py'), mode='r', encoding='utf-8') as f:
    exec(f.read(), about)

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

if __name__ == '__main__':
    setup(
        name='pyabac',
        description='Attribute-based access control (ABAC) python SDK',
        keywords='ACL ABAC access-control policy security authorization permission',
        version=about['__version__'],
        author='Ketan Goyal',
        author_email='ketangoyal1988@gmail.com',
        license="Apache 2.0 license",
        url='https://github.com/ketgo/pyabac.git',
        long_description=long_description,
        long_description_content_type='text/markdown',
        py_modules=['pyabac'],
        python_requires='>=3.4',
        install_requires=[
            'pymongo~=3.5',
            'marshmallow',
            'marshmallow-oneofschema',
            'jsonpath-ng'
        ],
        extras_require={
            'dev': [
                'pytest~=4.0',
                'pytest-cov~=2.6',
                'pylint~=1.0'
            ]
        },
        packages=find_packages(exclude='tests'),
        classifiers=[
            'Intended Audience :: Developers',
            'License :: OSI Approved :: Apache Software License',
            'Operating System :: OS Independent',
            'Topic :: System :: Systems Administration',
            'Topic :: System :: Networking',
            'Topic :: System :: Networking :: Firewalls',
            'Topic :: Security',
            'Topic :: Software Development',
            'Topic :: Utilities',
            'Natural Language :: English',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: Implementation :: PyPy',
            'Programming Language :: Python :: Implementation :: CPython',
        ],
    )
