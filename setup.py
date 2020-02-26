from os import path

from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))
about = {}
with open(path.join(here, 'py_abac', 'version.py'), mode='r', encoding='utf-8') as f:
    exec(f.read(), about)

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

extra_requires_mongo = [
    'pymongo~=3.5'
]
extra_requires_sql = [
    'SQLAlchemy~=1.3'
]
extra_requires_doc = [
    'sphinx==2.4.1'
]
extra_requires_utils = [
    'pytest~=4.0',
    'pytest-cov~=2.6',
    'pylint~=1.0',
    'bandit~=1.6',
    'mongomock~=3.0',
]
extra_requires_dev = extra_requires_utils + \
                     extra_requires_mongo + \
                     extra_requires_sql + \
                     extra_requires_doc

if __name__ == '__main__':
    setup(
        name='py_abac',
        description='Attribute-based access control (ABAC)',
        keywords='ACL ABAC access-control policy security authorization permission',
        version=about['__version__'],
        author='Ketan Goyal',
        author_email='ketangoyal1988@gmail.com',
        license="Apache 2.0 license",
        url='https://github.com/ketgo/py-abac',
        long_description=long_description,
        long_description_content_type='text/markdown',
        py_modules=['py_abac'],
        python_requires='>=3.4',
        install_requires=[
            'marshmallow~=3.2',
            'marshmallow-oneofschema~=2.0',
            'objectpath~=0.6'
        ],
        extras_require={
            'dev': extra_requires_dev,
            'doc': extra_requires_doc,
            'mongo': extra_requires_mongo,
            'sql': extra_requires_sql,
        },
        packages=find_packages(exclude=('tests', 'benchmarks')),
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
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: Implementation :: PyPy',
        ],
    )
