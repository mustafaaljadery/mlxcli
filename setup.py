from setuptools import setup, find_packages

setup(
    name='mlxcli',
    version='0.1.7',
    packages=find_packages(),
    install_requires=[
        'cmd2',
        "mlx", 
        "mlx_lm"
    ],
    entry_points={
        'console_scripts': [
            'mlxcli=mlxcli.main:main',
        ],
    },
)