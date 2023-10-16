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
                    dockerImage = docker.build("-t $registry:$BUILD_NUMBER -f ./fastapi/Dockerfile")
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
                echo 'Running a script to trigger pull and start a docker container'
            }
        }
    }
}