# download-jenkins-build-log utility

![Build status](https://travis-ci.org/bertold/download-jenkins-build-log.svg?branch=master)

Use
```bash
download-jenkins-build-log.py -h
```
to see all the available options.

For example, to download the console log of a freestyle project `my-freestyle-job`
with the build number `123` into the target directory of `logs` from the Jenkins
instance at `https://myjenkins.example.com:8080`, use the following command line:
```bash
download-jenkins-build-log.py --url https://myjenkins.example.com:8080 --build 123 --directory logs my-freestyle-job
```

The tool will return `0` in case of successful execution, and `-1` in case of an error. 