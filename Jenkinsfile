
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


        // 5. Detection des secrets
        stage('Gitleaks Scan') {
            steps {
                echo 'Detection des secrets dans Git history'

                sh '''
                    gitleaks git . --redact --exit-code 1
                '''
            }
        }

        // 6. Analyse des vulnerabilites Docker
        stage('Trivy Scan') {
            steps {
                echo 'Analyse des vulnerabilites de l image Docker Backend'

                sh '''
                    docker run --rm \
                        -v /var/run/docker.sock:/var/run/docker.sock \
                        -v trivy-cache:/root/.cache/ \
                        aquasec/trivy:latest image \
                        --scanners vuln \
                        --severity HIGH,CRITICAL \
                        --exit-code 0 \
                        devops-interview-platform-backend:latest
                '''
            }
        }


        // 7. Publication des images Docker sur GHCR
        stage('Push to GHCR') {
            steps {
                echo 'Publication des images Docker sur GitHub Container Registry'

                withCredentials([string(
                    credentialsId: 'jenkins-ghcr-token',
                    variable: 'GHCR_TOKEN'
                )]) {
                    sh '''
                        set +x
                        set -e

                        trap 'docker logout ghcr.io >/dev/null 2>&1 || true' EXIT

                        echo "$GHCR_TOKEN" | docker login ghcr.io \
                            --username Essouiriaya \
                            --password-stdin

                        docker tag devops-interview-platform-backend:latest \
                            ghcr.io/essouiriaya/devops-interview-platform-backend:latest

                        docker tag devops-interview-platform-frontend:latest \
                            ghcr.io/essouiriaya/devops-interview-platform-frontend:latest

                        docker push ghcr.io/essouiriaya/devops-interview-platform-backend:latest

                        docker push ghcr.io/essouiriaya/devops-interview-platform-frontend:latest
                    '''
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
