#!/usr/bin/env groovy

pipeline {
    agent {
        dockerfile {
            args '-u root:root'
        }
    }
    environment {
        DATABASE_URL = 'postgres://postgres:@localhost:5432/test_db'
        SECRET_KEY = 'secret'
        DJANGO_SETTINGS_MODULE = 'core.settings.test_travis'
        RABBITMQ_HOST = 'localhost'
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