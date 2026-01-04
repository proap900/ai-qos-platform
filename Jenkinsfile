pipeline {
    agent any

    environment {
        REGISTRY = 'docker.io'
        IMAGE_ML = 'ai-qos-ml-inference'
        IMAGE_API = 'ai-qos-api-gateway'
        TAG = 'latest'
    }

    stages {

        stage('Checkout Source Code') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/proap900/ai-qos-platform.git'
            }
        }

        stage('Build ML Inference Image') {
            steps {
                sh '''
                docker build \
                  -t ${IMAGE_ML}:${TAG} \
                  services/ml-inference
                '''
            }
        }

        stage('Build API Gateway Image') {
            steps {
                sh '''
                docker build \
                  -t ${IMAGE_API}:${TAG} \
                  services/api-gateway
                '''
            }
        }

        stage('Container Smoke Tests') {
            steps {
                sh '''
                docker run -d -p 8001:8001 --name ml-test ${IMAGE_ML}:${TAG}
                sleep 5
                curl -f http://localhost:8001/health
                docker rm -f ml-test
                '''

                sh '''
                docker run -d -p 8000:8000 --name api-test ${IMAGE_API}:${TAG}
                sleep 5
                curl -f http://localhost:8000/health
                docker rm -f api-test
                '''
            }
        }

        stage('Push Images to Docker Hub') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-creds',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )
                ]) {
                    sh '''
                    echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin

                    docker tag ${IMAGE_ML}:${TAG} $DOCKER_USER/${IMAGE_ML}:${TAG}
                    docker tag ${IMAGE_API}:${TAG} $DOCKER_USER/${IMAGE_API}:${TAG}

                    docker push $DOCKER_USER/${IMAGE_ML}:${TAG}
                    docker push $DOCKER_USER/${IMAGE_API}:${TAG}
                    '''
                }
            }
        }

        stage('Deploy to Kubernetes (Minikube)') {
            steps {
                sh '''
                kubectl apply -f deploy/k8s/ml-inference-deployment.yaml
                kubectl apply -f deploy/k8s/ml-inference-service.yaml

                kubectl apply -f deploy/k8s/api-gateway-deployment.yaml
                kubectl apply -f deploy/k8s/api-gateway-service.yaml

                kubectl rollout restart deployment/ml-inference
                kubectl rollout restart deployment/api-gateway
                '''
            }
        }
    }

    post {
        success {
            echo 'CI/CD pipeline completed successfully'
            echo 'Use `minikube service api-gateway` and `minikube service ml-inference` to access services'
        }
        failure {
            echo 'Pipeline failed – check logs'
        }
    }
}
