from setuptools import setup, find_packages

setup(
        name='giovannietiziana',
        version='0.1',
        description='Matrimonio',
        long_description=__doc__,
        packages=['translations'],
        include_package_data=True,
        zip_safe=False,
        install_requires=[
        ],
        entry_points={
            'console_scripts': [
                'giovannietiziana = translations.cli:start_cli'
        ]
    }

)