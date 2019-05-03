import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="download-jenkins-build-log-bertold",
    version="0.0.1a3",
    author="Bertold Kolics",
    author_email="bertold@qualityraven.com",
    description="Command-line utility for downloading Jenkins job console logs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bertold/download-jenkins-build-log",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Topic :: Software Development :: Build Tools"
    ],
    keywords="Jenkins logs tools",
    project_urls={ "Source": "https://github.com/bertold/download-jenkins-build-log"},
    python_requires=">=3",
    install_requires=['requests'],
    entry_points = {
        'console_scripts': ['download-jenkins-build-log=DownloadJenkinsBuildLog.downloader:main'],
    }
)