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
                sh 'flake8'
                sh 'coverage run manage.py test'
            }
        }
    }
}