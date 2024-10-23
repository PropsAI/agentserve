# setup.py

from setuptools import setup, find_packages

setup(
    name='agentserve',
    version='0.1.6',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'fastapi',
        'uvicorn',
        'rq',
        'redis',
        'click'
    ],
    entry_points={
        'console_scripts': [
            'agentserve=agentserve.cli:main',
        ],
    },
    package_data={
        'agentserve': ['templates/*']
    },
    author='Peter',
    author_email='peter@getprops.ai',
    description='An SDK for hosting and managing AI agents.',
    url='https://github.com/PropsAI/agentserve',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License'
    ],
)