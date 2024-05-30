pipeline {
    agent {
        kubernetes {
            label 'itay'
            idleMinutes 5
            yamlFile 'build-pod.yaml'
            defaultContainer 'ez-docker-helm-build'
        }
    }
    environment {
        GITHUB_CREDS = 'github-pat'
        DOCKER_IMAGE = 'itay1608/recommendation_app'
        MONGO_URI = 'mongodb://root:root@mongo:27017/recommendations_db?authSource=admin'
    }
    stages {
        stage('checkout code') {
            steps {
                checkout scm
            }
        }
        stage('build docker image') {
            steps {
                script {
                    dockerImage = docker.build("${DOCKER_IMAGE}:latest", '--no-cache .')
                }
            }
        }
    }
}
