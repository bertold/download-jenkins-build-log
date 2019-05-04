import requests
import argparse
import os
import shutil


def parse_command_line_arguments():
    """
    Parses the command-line arguments.
    :return: nothing
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("jobname", help="the name of the job")
    parser.add_argument("-u", "--url", help="the base URL of the Jenkins installation (default: http://localhost:8080)", default="http://localhost:8080")
    parser.add_argument("-b", "--build", help="the build ID (if omitted, the last build log will be downloaded)")
    parser.add_argument("-a", "--all", help="flag to indicate if all logs of the job should be downloaded", action="store_true")
    parser.add_argument("-d", "--directory", help="the target directory (defaults to '<job_name>-<build ID>')")
    parser.add_argument("-l", "--login", help="the login name to the Jenkins server")
    parser.add_argument("-p", "--token", help="the API token to the Jenkins server")
    args = parser.parse_args()

    global job_name
    global jenkins_url
    global build_id
    global download_all
    global target_directory
    global login_name
    global api_token

    job_name = args.jobname
    jenkins_url = args.url
    build_id = args.build
    download_all = args.all
    target_directory = args.directory if args.directory else "{}-{}".format(job_name, build_id if build_id else "last")
    login_name = args.login
    api_token = args.token


def get_last_build():
    """
    :return: the last build ID associate with the job
    """
    response = requests.get("{}/job/{}/api/json".format(jenkins_url, job_name), auth=(login_name, api_token))
    if response.status_code != 200:
        raise Exception("Unexpected error received from server: status code={} reason={}".format(
            response.status_code, response.reason))
    return response.json()['builds'][0]['number']


def create_target_directory():
    try:
        os.mkdir(target_directory)
    except FileExistsError:
        # ignore
        pass


def download_log_simple():
    """
    Download the log of job types that have a single console log
    :return: 0 in case of success, -1 in case of an error
    """
    response = requests.get("{}/job/{}/{}/consoleText".format(jenkins_url, job_name, build_id), stream=True,
                            auth=(login_name, api_token))
    if response.status_code == 200:
        filename = "{}/{}".format(target_directory, build_id)
        with open(filename, 'wb') as f:
            response.raw.decode_content = True
            shutil.copyfileobj(response.raw, f)
            print("Successfully downloaded log to " + filename)
        return 0
    else:
        print("Failed to download log, error code: {}, reason: {} ".format(
            response.status_code, response.reason))
        return -1


def download_log_matrix():
    """
    Download the logs of jobs with multiple console log files
    :return: 0 in case of success, -1 in case of an error
    """
    response = requests.get("{}/job/{}/{}/api/json".format(jenkins_url, job_name, build_id),
                            auth=(login_name, api_token))
    if response.status_code != 200:
        raise Exception("Unexpected error received from server: status code={} reason={}".format(
            response.status_code, response.reason))

    runs = response.json()['runs']
    for run in runs:
        run_url = run['url']
        response = requests.get("{}/consoleText".format(run_url), stream=True,
                                auth=(login_name, api_token))
        if response.status_code == 200:
            # craft a file name that uses the matrix parameters
            filename = "{}/{}_{}".format(
                target_directory, build_id,
                run_url.split('/')[-3].replace('=', '_').replace(',', '_'))
            with open(filename, 'wb') as f:
                response.raw.decode_content = True
                shutil.copyfileobj(response.raw, f)
                print("Successfully downloaded log to " + filename)
        else:
            print("Failed to download log, error code: {}, reason: {} ".format(
                response.status_code, response.reason))
            return -1
    return 0


def download_logs():
    """
    Download the build log file(s) to the destination directory
    :return: 0 in case of success, -1 in case of an error
    """
    create_target_directory()

    global build_id
    if build_id is None:
        build_id = get_last_build()

    response = requests.get("{}/job/{}/{}/api/json".format(jenkins_url, job_name, build_id),
                            auth=(login_name, api_token))
    if response.status_code != 200:
        raise Exception("Unexpected error received from server: status code={} reason={}".format(
            response.status_code, response.reason))

    job_class = response.json()['_class']
    if 'hudson.model.FreeStyleBuild' == job_class:
        return download_log_simple()
    elif 'org.jenkinsci.plugins.workflow.job.WorkflowRun' == job_class:
        return download_log_simple()
    elif 'hudson.matrix.MatrixBuild' == job_class:
        return download_log_matrix()

    return -1


def main():
    parse_command_line_arguments()
    try:
        download_logs()
        return 0
    except Exception as exception:
        print(exception)
        return -1


exit(main())
