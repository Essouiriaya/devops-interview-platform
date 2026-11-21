pipeline {
    agent any

    options {
        timestamps()
    }

    stages {

        stage('Checkout') {
            steps {
                echo 'Recuperation du code source'
                checkout scm
            }
        }

        stage('Build') {
            steps {
                echo 'Construction des images Docker'
                bat 'docker compose build'
            }
        }

        stage('Test') {
            steps {
                echo 'Execution des tests Backend'

                dir('backend') {
                    bat 'python -m pip install -r requirements.txt'
                    bat 'python -m pytest -v'
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
