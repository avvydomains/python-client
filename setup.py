from setuptools import setup, find_packages


with open('VERSION.txt') as f:
    version = f.readline()


setup(
    name='avvy',
    version=version,
    url='https://github.com/avvydomains/python-client',
    license='MIT',
    description='Avvy Domains (.avax) client implementation',
    long_description='',
    author='Connor Bode',
    author_email='connor@avvy.domains',
    packages=find_packages(),
	include_package_data=True,
    install_requires=[
		'web3',
	],
    zip_safe=False,
    classifiers=[],
)
