pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
        skipDefaultCheckout(true)
        timeout(time: 20, unit: 'MINUTES')
    }

    environment {
        PYTHONUNBUFFERED = '1'
        PIP_DISABLE_PIP_VERSION_CHECK = '1'
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm

                sh 'git rev-parse --short HEAD'
            }
        }

        stage('Verify CI Tools') {
            steps {
                sh '''
                    set -eu

                    command -v python3
                    command -v poetry
                    command -v gitleaks

                    python3 --version
                    poetry --version
                    gitleaks version
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    set -eu

                    poetry install --no-root --no-interaction --no-ansi

                    poetry run python -m pip install pylint
                '''
            }
        }

        stage('Code Quality - Pylint') {
            steps {
                sh '''
                    set -eu

                    poetry run pylint router/ client/ models/ utils/ app.py
                '''
            }
        }

        stage('Unit Tests') {
            steps {
                sh '''
                    set -eu

                    mkdir -p reports

                    poetry run python -m pytest \
                        --junitxml=reports/pytest.xml \
                        --cov=. \
                        --cov-report=xml:reports/coverage.xml
                '''
            }
        }

        stage('Credential Scan - Gitleaks') {
            steps {
                sh '''
                    set -eu

                    gitleaks git . --redact --no-banner
                '''
            }
        }
    }

    post {
        always {
            junit testResults: 'reports/pytest.xml',
                  allowEmptyResults: true

            archiveArtifacts artifacts: 'reports/**',
                             allowEmptyArchive: true
        }

        success {
            echo 'Attendance API CI pipeline passed.'
        }

        failure {
            echo 'Attendance API CI pipeline failed. Check the stage logs.'
        }

        cleanup {
            deleteDir()
        }
    }
}
