#!/usr/bin/env groovy

pipeline {
    agent {
        dockerfile true
    }
    stages {
        stage('Test') {
            steps {
                sh 'cd /home/web/django_project/ && coverage run manage.py test'
                sh 'cd /home/web/django_project/ && flake8'
            }
        }
    }
}