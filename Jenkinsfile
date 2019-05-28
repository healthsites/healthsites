#!/usr/bin/env groovy

pipeline {
    agent {
        dockerfile {
            args '-u root:root'
        }
    }
    environment {
        RABBITMQ_HOST = '127.0.0.1'
    }
    stages {
        stage('Test') {
            steps {
                sh 'cd /home/web/django_project/ && ls -la /home/web/django_project/ && coverage run manage.py test'
                sh 'cd /home/web/django_project/ && flake8'
            }
        }
    }
}