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
        GITHUB_TOKEN=credentials("github-creds")
        GITHUB_API_URL ='https://api.github.com'
        GITHUB_REPO ="itaymosco/final_project"
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
        stage('push docker image'){
            when{
                branch 'master'
            }
            steps{
                script {
                    docker.withRegistry('https://registry.hub.docker.com', 'docker-creds') {
                        dockerImage.push("latest")
                    }  
                }
            }
        }
        stage('Create merge request'){
            when {
                not {
                    branch 'master'
                }
            }
            steps {
                withCredentials([string(credentialsId: 'github-creds', variable: 'GITHUB_TOKEN')]) {
                    script {
                        def branchName = env.BRANCH_NAME
                        def pullRequestTitle = "Merge ${branchName} into master"
                        def pullRequestBody = "Automatically generated merge request for branch ${branchName}"
 
                        sh """
                            curl -X POST -H "Authorization: token ${GITHUB_TOKEN}" \
                            -d '{ "title": "${pullRequestTitle}", "body": "${pullRequestBody}", "head": "${branchName}", "base": "master" }' \
                            ${GITHUB_API_URL}/repos/${GITHUB_REPO}/pulls
                        """
                    }
                }
            }
        }
    }
}