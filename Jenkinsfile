
pipeline {
    agent any

    environment {
        DOCKERHUB_USER = 'techcloud12'
        IMAGE_NAME = 'salary-prediction'
        APP_SERVER = 'ubuntu@3.108.6.188'
        SSH_KEY = '/var/lib/jenkins/.ssh/salary_app_deploy'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t ${DOCKERHUB_USER}/${IMAGE_NAME}:latest .'
            }
        }

        stage('Login to Docker Hub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_TOKEN'
                )]) {
                    sh '''
                        echo "$DOCKER_TOKEN" | docker login \
                          -u "$DOCKER_USER" --password-stdin
                    '''
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                sh 'docker push ${DOCKERHUB_USER}/${IMAGE_NAME}:latest'
            }
        }

        stage('Deploy to Application EC2') {
            steps {
                sh '''
                    ssh -i "$SSH_KEY" \
                      -o IdentitiesOnly=yes \
                      -o StrictHostKeyChecking=yes \
                      "$APP_SERVER" \
                      "sudo docker pull ${DOCKERHUB_USER}/${IMAGE_NAME}:latest && \
                       (sudo docker rm -f salary-prediction || true) && \
                       sudo docker run -d --restart unless-stopped \
                         --name salary-prediction \
                         -p 80:5000 \
                         ${DOCKERHUB_USER}/${IMAGE_NAME}:latest"
                '''
            }
        }
    }

    post {
        success {
            echo 'Salary Prediction application deployed successfully!'
        }
        failure {
            echo 'Pipeline failed. Check the Jenkins console output.'
        }
    }
}
