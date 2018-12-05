@Library('jenkins-helpers@v0.1.13') _

def label = "kaknas-${UUID.randomUUID().toString()}"

podTemplate(
    label: label,
    annotations: [
        podAnnotation(key: "jenkins/build-url", value: env.BUILD_URL ?: ""),
        podAnnotation(key: "jenkins/github-pr-url", value: env.CHANGE_URL ?: ""),
    ],
    containers: [
        containerTemplate(
            name: 'docker',
            command: '/bin/cat -',
            image: 'docker:17.06.2-ce',
            resourceRequestCpu: '200m',
            resourceRequestMemory: '300Mi',
            resourceLimitCpu: '200m',
            resourceLimitMemory: '300Mi',
            ttyEnabled: true
        ),
        containerTemplate(
            name: 'python3',
            image: 'python:3.6.4',
            command: '/bin/cat -',
            resourceRequestCpu: '1000m',
            resourceRequestMemory: '500Mi',
            resourceLimitCpu: '1000m',
            resourceLimitMemory: '500Mi',
            envVars: [envVar(key: 'PYTHONPATH', value: '/usr/local/bin'),
                      envVar(key: 'JENKINS_URL', value: env.JENKINS_URL),
                      envVar(key: 'BRANCH_NAME', value: env.BRANCH_NAME),
                      envVar(key: 'BUILD_NUMBER', value: env.BUILD_NUMBER),
                      envVar(key: 'BUILD_URL', value: env.BUILD_URL),
                      envVar(key: 'CHANGE_ID', value: env.CHANGE_ID),
            ],
            ttyEnabled: true
        ),
        containerTemplate(name: 'node',
                         image: 'node:carbon',
                         resourceRequestCpu: '2000m',
                         resourceRequestMemory: '2500Mi',
                         resourceLimitCpu: '2000m',
                         resourceLimitMemory: '2500Mi',
                         ttyEnabled: true),
    ],
    volumes: [
        secretVolume(
            secretName: 'jenkins-docker-builder',
            mountPath: '/jenkins-docker-builder',
            readOnly: true),
        secretVolume(
            secretName: 'pip-credentials',
            mountPath: '/pip-credentials',
            readOnly: true
        ),
        hostPathVolume(hostPath: '/var/run/docker.sock', mountPath: '/var/run/docker.sock')]) {
    properties([buildDiscarder(logRotator(daysToKeepStr: '30', numToKeepStr: '20'))])
    node(label) {
        def gitCommit
        container('jnlp') {
            stage('Checkout') {
                checkout(scm)
                gitCommit = sh(returnStdout: true, script: 'git rev-parse --short HEAD').trim()
            }
        }
        container('python3') {
            stage('Install dependencies') {
                sh('mkdir -p $HOME/.config/pip/')
                sh('cp /pip-credentials/pip.conf $HOME/.config/pip/pip.conf')
                sh('pip download -r requirements.txt -d dist/')
                sh("pip install --find-links='./dist/' -r requirements.txt")
            }
            stage('Run linter') {
                sh('(pylint --disable=fixme --output-format=parseable --reports=n cognite_search_loader 2>&1 | tee pylint.txt) || true')
                ViolationsToGitHub([
                        createCommentWithAllSingleFileComments: false,
                        createSingleFileComments: true,
                        commentOnlyChangedContent: true,
                        repositoryName: "${scm.getUserRemoteConfigs()[0].getUrl().tokenize('/')[3].split("\\.")[0]}",
                        pullRequestId: "${env.CHANGE_ID}",
                        violationConfigs: [[
                                parser: 'PYLINT',
                                pattern: '.*/pylint\\.txt$',
                                reporter: 'pylint'
                        ]]
                    ])
            }
        }
        container('node') {
            stage('Build') {
              dir('kaknas-vue') {
                sh('npm install')
                sh('npm run build')
                sh('cp -r dist/* ../kaknas/')
                sh('mv ../kaknas/index.html ../kaknas/static/')
              }

            }
        }
        container('docker') {
            stage('Build Docker container') {
                sh("docker build -t eu.gcr.io/cognitedata/kaknas:${gitCommit} .")
            }
            if(env.BRANCH_NAME != "master") {
                echo "Not in master branch. Will not push image. Skip."
                return
            }
            stage('Push Docker container') {
                sh('#!/bin/sh -e\n' + 'docker login -u _json_key -p "$(cat /jenkins-docker-builder/credentials.json)" https://eu.gcr.io')
                sh("docker push eu.gcr.io/cognitedata/kaknas:${gitCommit}")
            }
        }
    }
}
