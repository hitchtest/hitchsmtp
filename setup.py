# -*- coding: utf-8 -*
from setuptools import setup, find_packages
import codecs
import sys
import os


def read(*parts):
    # intentionally *not* adding an encoding option to open
    # see here: https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
    return codecs.open(os.path.join(os.path.abspath(os.path.dirname(__file__)), *parts), 'r').read()

long_description = read('README.rst')

setup(name="hitchsmtp",
      version="0.1",
      description="Mock SMTP server that logs incoming messages to stdout as JSON for easy parsing and testing by the hitch framework.",
      long_description=long_description,
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
          'Topic :: Software Development :: Quality Assurance',
          'Topic :: Software Development :: Testing',
          'Topic :: Software Development :: Libraries',
          'Operating System :: Unix',
          'Environment :: Console',
          'Topic :: Communications :: Email',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
#          'Programming Language :: Python :: 3',
#          'Programming Language :: Python :: 3.1',
#          'Programming Language :: Python :: 3.2',
#          'Programming Language :: Python :: 3.3',
      ],
      keywords='hitch testing framework bdd tdd declarative tests testing smtp email mock server',
      author='Colm O\'Connor',
      author_email='colm.oconnor.github@gmail.com',
      url='https://hitch.readthedocs.org/',
      license='AGPL',
      packages=find_packages(exclude=["tests*",]),
      package_data={},
      entry_points=dict(console_scripts=['hitchsmtp=hitchsmtp:smtp.main', ]),
      install_requires=['hitchserve',],
      zip_safe=False,
)
