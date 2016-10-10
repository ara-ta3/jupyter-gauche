from setuptools import setup, find_packages


setup(name='jupyter_gauche',
      version='0.0.4',
      description='Gauche Kernel for Jupyter Notebook',
      install_requires = [
            'ipykernel',
            'pexpect',
            ],
      author='ara_ta3',
      author_email='tarata43@yahoo.co.jp',
      url='http://arata.hatenadiary.com',
      packages=find_packages(),
      entry_points="""
      [console_scripts]
      """,)
