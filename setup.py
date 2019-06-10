import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="easy-icm-runner",
    version="1.0.3",
    author="Bachir El Koussa",
    author_email="bgkoussa@gmail.com",
    description="A wrapper for IBM ICMs Scheduler API Calls",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/equinoxfitness/easy-icm-runner/",
    packages=setuptools.find_packages(),
    install_requires=[
          'requests',
      ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)