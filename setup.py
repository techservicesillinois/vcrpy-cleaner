from setuptools import setup, find_packages

from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
# with open(path.join(here, 'docs/readme.rst'), encoding='utf-8') as f:
#    long_description = f.read()


def version():
    from setuptools_scm.version import get_local_dirty_tag

    def clean_scheme(version):
        # Disable local scheme by default since it is not supported
        # by PyPI (See PEP 440). If code is not committed add +dirty
        # to version to prevent upload to either PyPI or test PyPI.
        return get_local_dirty_tag(version) if version.dirty else ''

    return {'local_scheme': clean_scheme}


setup(
    name='vcrpy-cleaner',
    use_scm_version=version,
    setup_requires=['setuptools_scm'],
    description='Sensitive data cleaners for network cassettes captured'
                ' by the VCR.py testing library.',
    #long_description=long_description,
    #long_description_content_type='text/x-rst',
    url='https://github.com/techservicesillinois/vcrpy-cleaner',
    author='Cybersecurity at the University of Illinois',
    author_email='securitysupport@illinois.edu',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    keywords='vcrpy cleaner sensitive data',
    packages=find_packages('src', exclude=['tests.*', 'tests']),
    package_dir={'': 'src'},
    python_requires='>=3.7',
    install_requires=[
       'vcrpy',
       'jwt',
    ],
    extras_require={
        'test': [
            'pytest',
            'pyjwt',
        ],
    },
    project_urls={
        'Bug Reports':
            'https://github.com/techservicesillinois/vcrpy-cleaner/issues',
        'Source': 'https://github.com/techservicesillinois/vcrpy-cleaner',
    }
)
