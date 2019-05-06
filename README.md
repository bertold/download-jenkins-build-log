# download-jenkins-build-log utility

![Build status](https://travis-ci.org/bertold/download-jenkins-build-log.svg?branch=master)
[![PyPI version](https://badge.fury.io/py/download-jenkins-build-log.svg)](https://badge.fury.io/py/download-jenkins-build-log)

This is a simple tool that enables downloading console output files
from Jenkins jobs. Freestyle, pipeline and matrix jobs are supported.

## Pre-requisites

Python 3.3 or later

## Installation

```
pip3 install download-jenkins-build-log
```



## Basic Usage

Use
```bash
download-jenkins-build-log -h
```
to see all the available options.

For example, to download the console log of a freestyle project `my-freestyle-job`
with the build number `123` into the target directory of `logs` from the Jenkins
instance at `https://myjenkins.example.com:8080`, use the following command line:
```bash
download-jenkins-build-log --url https://myjenkins.example.com:8080 --build 123 --directory logs my-freestyle-job
```

## Authentication

You may use the ```--login``` to set the user name and the ```--token``` to set
the password or API token to access Jenkins. Jenkins documentation recommends
creating an [API token](https://wiki.jenkins.io/display/JENKINS/Authenticating+scripted+clients)
to use with tools.

Alternatively, you can also provide credentials with the following environment
variables.

| Environment variable name                  | Description           |
|--------------------------------------------|-----------------------|
| ```DOWNLOAD_JENKINS_BUILD_LOG_LOGIN```     | login name            |
| ```DOWNLOAD_JENKINS_BUILD_LOG_API_TOKEN``` | password or API token |

## Return Codes

The tool will return `0` in case of successful execution, and `-1` in case of an error. 
