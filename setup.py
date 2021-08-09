from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / 'README.md').read_text(encoding='utf-8')

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

setup(
    name='DolaBot-Slate',
    version='1.0.1',
    author='Slate',
    description='Python Splatoon-orientated Discord Bot that can interact with SplatTag',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/kjhf/DolaBot',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],

    keywords='slapp, slate, splatoon, dola',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    python_requires='>=3.9, <4',
    project_urls={  # Optional
        'Bug Reports': 'https://github.com/kjhf/Dola/issues',
        'Source': 'https://github.com/kjhf/Dola/',
        'Discord': 'https://discord.gg/wZZv2Cr',
    },
)
