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
                sh 'echo "OK"'
//                sh 'flake8'
//                sh 'cd django_project && coverage run manage.py test'
            }
        }
    }
}