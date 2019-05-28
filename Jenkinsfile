#!/usr/bin/env groovy

pipeline {
    agent {
        dockerfile true
    }
    stages {
        stage('Test') {
            steps {
                sh 'coverage run manage.py test'
                sh 'flake8'
            }
        }
    }
}