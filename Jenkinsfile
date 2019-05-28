#!/usr/bin/env groovy

pipeline {
    agent {
        dockerfile true
    }
    stages {
        stage('Test') {
            steps {
                sh 'echo "OK"'
                sh 'cd /home/web/ && coverage run manage.py test'
                sh 'flake8'
            }
        }
    }
}