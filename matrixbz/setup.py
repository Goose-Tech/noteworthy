from setuptools import setup, find_packages

setup(name='matrixbz',
      url="https://decentralabs.io",
      author_email="hi@decentralabs.io",
      version='0.0.1',
      packages=find_packages(),
      zip_safe=False,
      install_requires=[
        'matrix-nio==0.10.0',
        'requests==2.23.0',
        'Pillow==7.1.2'
      ]
     )
