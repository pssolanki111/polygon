from setuptools import setup

with open('README.md') as file:
    long_description = file.read()

setup(
    name='polygon',
    version='0.9.8',
    packages=['polygon', 'polygon.forex', 'polygon.crypto', 'polygon.stocks', 'polygon.streaming',
              'polygon.reference_apis', 'polygon.options'],
    url='https://github.com/pssolanki111/polygon',
    license='MIT',
    author='P S Solanki',
    author_email='google_was_my_idea@gmail.com',
    description='A Complete Python Wrapper for Polygon.io APIs. Public Alpha Release',
    long_description=long_description,
    long_description_content_type="text/markdown",
    project_urls={
        "Issue Tracker": "https://github.com/pssolanki111/polygon/issues",
        "Discussions": "https://github.com/pssolanki111/polygon/discussions",
        "Support": "https://www.patreon.com/pssolanki"
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        'Topic :: Office/Business :: Financial :: Investment',
    ],
    python_requires='>=3.6',
    install_requires=[
        'requests',
        'websockets',
        'websocket-client',
        'httpx'],
    keywords='finance trading equities bonds options research data',
)
