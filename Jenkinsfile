
pipeline {
    agent any

    options {
        timestamps()
    }

    stages {

        // 1. Recuperation du code source
        stage('Checkout') {
            steps {
                echo 'Recuperation du code source'
                checkout scm
            }
        }

        // 2. Construction des images Docker
        stage('Build') {
            steps {
                echo 'Construction des images Docker'
                sh 'docker compose build'
            }
        }

        // 3. Execution des tests Backend
        stage('Test') {
            steps {
                echo 'Execution des tests Backend'

                dir('backend') {
                    sh 'python3 -m pip install -r requirements.txt'
                    sh 'python3 -m pytest -v'
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline CI execute avec succes !'
        }

        failure {
            echo 'Echec du pipeline CI !'
        }

        always {
            echo 'Fin du pipeline.'
        }
    }
}
