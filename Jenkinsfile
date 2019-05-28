#!/usr/bin/env groovy

pipeline {
    agent {
        dockerfile true
    }
    stages {
        stage('Test') {
            steps {
                sh 'pwd && ls -la && sleep 300'
//                sh 'django_project/coverage run manage.py test'
//                sh 'flake8'
            }
        }
    }
}