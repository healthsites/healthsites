#!/usr/bin/env groovy

pipeline {
    agent {
        dockerfile {
            dir 'deployment/docker'
        }
    }
    stages {
        stage('Test') {
            steps {
                sh 'curl --version'
            }
        }
    }
}