from setuptools import setup, find_namespace_packages


setup(
    name="gold-vault",
    version="0.1.0",
    packages=find_namespace_packages(where="src"),
    package_dir={"": "src"},
    entry_points={
        'console_scripts': [
            'gvault = gvault.cli:cli_main',
        ],
    },
)
