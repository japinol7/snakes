from setuptools import setup

setup(
    name='snakes',
    author='Joan A. Pinol  (japinol)',
    version='1.0.1',
    license='MIT',
    description='Snakes.',
    long_description='Snakes. Similar to classic Snake game but with player versus player version and other surprises.',
    url='https://github.com/japinol7/snakes',
    packages = ['snakes'],
    python_requires='>=3.7',
	install_requires=['pygame'],
    entry_points={
        'console_scripts': [
            'snakes=snakes.__main__:main',
        ],
    },
)
