# setup.py

from setuptools import setup, find_packages

setup(
    name='agentserve',
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'fastapi',
        'uvicorn',
        'rq',
        'redis',
        'celery',
        'click',
        'pydantic',
        'pyyaml'
    ],
    entry_points={
        'console_scripts': [
            'agentserve=agentserve.cli:main',
        ],
    },
    author='Peter',
    author_email='peter@getprops.ai',
    description='A framework for hosting and scaling AI agents.',
    url='https://github.com/PropsAI/agentserve',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License'
    ],
)