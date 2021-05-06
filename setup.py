import pathlib

from setuptools import setup

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='cowin',
    version='0.0.5',
    description='Python wrapper for CoWin API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url=' https://github.com/backtrackbaba/cowin',
    author='Saiprasad Balasubramanian',
    author_email='sai.cosmo@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',

        'Environment :: Console',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
    ],
    keywords='cowin, covid, vaccine',
    packages=['cowin_api'],
    include_package_data=True,
    python_requires='>=3.6, <4',
    install_requires=[
        'fake-useragent==0.1.11',
        'pytest==6.2.3',
        'requests==2.25.1'
    ],
    project_urls={  # Optional
        'Bug Reports': 'https://github.com/backtrackbaba/cowin/issues',
        'Source': 'https://github.com/backtrackbaba/cowin',
    },
)
