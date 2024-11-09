from setuptools import setup, find_packages

setup(
    name='kamu-jp-modern',  # パッケージ名
    version='0.8.6',  # バージョン
    packages=find_packages(),
    description='Modern is a simple package for logging and progress bar and More!',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='DiamondGotCat',
    author_email='chii@kamu.jp',
    url='https://github.com/DiamondGotCat/Modern',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)