from setuptools import setup, find_packages
import os

rootpath = os.path.abspath(os.path.dirname(__file__))

def read(*parts):
    return open(os.path.join(rootpath, *parts), 'r').read()


long_description = '{}'.format(read('README.md'))

setup(
    name='hydro-python-api',
    version='1.1.6',
    include_package_data=True,
    pacotes=find_packages('src'),
    long_description=long_description,
    classifiers=['Development Status :: 1 - Planning',
                 'Environment :: Console',
                 'Intended Audience :: Science/Research',
                 'Intended Audience :: Developers',
                 'Intended Audience :: Education',
                 'License :: OSI Approved :: MIT License',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python',
                 'Topic :: Scientific/Engineering',
                 'Topic :: Education',
                 ],
    url='https://github.com/clebsonpy/AnaHidroPythonApi',
    license='MIT License',
    author='Clebson Farias',
    author_email='clebson2007.farias@gmail.com',
    keywords='ana sar brazil python api',
    description='Developed for hydrological studies',
    install_requires=['defusedxml==0.6.*', 'pandas==1.1.*', 'requests==2.18.*', 'xlrd==1.1.*'],
    packages=['hydro_api'],
)
