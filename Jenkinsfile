pipeline {
    agent any

    stages {

        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/proap900/ai-qos-platform.git'
            }
        }

        stage('Build ML Inference Image') {
            steps {
                sh '''
                docker build \
                  -t ml-inference-ci:latest \
                  services/ml-inference
                '''
            }
        }

        stage('Build API Gateway Image') {
            steps {
                sh '''
                docker build \
                  -t api-gateway-ci:latest \
                  services/api-gateway
                '''
            }
        }

        stage('Run Container Smoke Tests') {
            steps {
                sh '''
                docker run -d -p 8001:8001 --name ml-test ml-inference-ci
                sleep 5
                curl -f http://localhost:8001/health
                docker rm -f ml-test
                '''

                sh '''
                docker run -d -p 8000:8000 --name gw-test api-gateway-ci
                sleep 5
                curl -f http://localhost:8000/health
                docker rm -f gw-test
                '''
            }
        }

        stage('Push Images to Docker Hub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh '''
                    echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin

                    docker tag ml-inference-ci:latest $DOCKER_USER/ai-qos-ml-inference:latest
                    docker tag api-gateway-ci:latest $DOCKER_USER/ai-qos-api-gateway:latest

                    docker push $DOCKER_USER/ai-qos-ml-inference:latest
                    docker push $DOCKER_USER/ai-qos-api-gateway:latest
                    '''
                }
            }
        }
    }

    post {
        success {
            echo 'CI pipeline succeeded'
        }
        failure {
            echo 'CI pipeline failed'
        }
    }
}
