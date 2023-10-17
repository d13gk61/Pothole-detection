pipeline {
    agent any

    options{
        buildDiscarder(logRotator(numToKeepStr: '3', daysToKeepStr: '3'))
        timestamps()
    }

    environment{
        registry = 'daockbn/predict-pothole'
        registryCredential = 'dockerhub'      
    }

    stages {
        stage('Test') {           
            steps {
                echo 'Testing model correctness..'
                echo 'always pass'
            }
        }
        stage('Build') {
            steps {
                script {
                    echo 'Building image for deployment..'
                    dockerImage = docker.build registry + ":$BUILD_NUMBER" 
                    echo 'Pushing image to dockerhub..'
                    docker.withRegistry( '', registryCredential ) {
                        dockerImage.push()
                        dockerImage.push('latest')
                    }
                }
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying models..'
                sh 'docker run -d -p 8000:8000 daockbn/predict-pothole:latest'
            }
        }
    }
}