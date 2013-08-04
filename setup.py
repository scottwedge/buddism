from setuptools import setup, find_packages

setup(
    name = "buddism",
    version = "1.0",
    url = 'http://scv119.me',
    license = 'Private',
    description = "",
    author = '',
    packages = ["buddism","config"],
    install_requires = ['setuptools',
                        'tornado',
                        'redis',
                        ],
    entry_points="""
    [console_scripts]
    web-server=buddism.app:main
    """,
)
