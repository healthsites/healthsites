#!/usr/bin/env groovy

pipeline {
    agent {
        dockerfile {
            args '-u root:root'
        }
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