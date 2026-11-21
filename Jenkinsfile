
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
                echo 'Execution des tests Backend dans le conteneur Docker'

                sh '''
                    docker compose run --rm backend python -m pytest -v
                '''
            }
        }

        // 4. Analyse de la qualite du code
        stage('SonarQube Analysis') {
            steps {
                script {
                    def scannerHome = tool 'SonarScanner'

                    withSonarQubeEnv('SonarQube') {
                        sh "${scannerHome}/bin/sonar-scanner"
                    }
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
