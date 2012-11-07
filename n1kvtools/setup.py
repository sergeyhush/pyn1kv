from distutils.core import setup
setup(
	name = 'n1kvtools',
	version = '0.1dev',
	packages = ['pyn1kvexpect'],
	license = 'LICENSE.txt',
	long_description = open('README.txt').read(),
	install_requires = [
		"pexpect >= 2.4",
	],
)
