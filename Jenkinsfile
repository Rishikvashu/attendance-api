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
        POETRY_VIRTUALENVS_CREATE = 'true'
        POETRY_VIRTUALENVS_IN_PROJECT = 'true'
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
        
        stage('Diagnose Poetry Environment') {
            steps {
                sh '''
                    set +e
        
                    echo "===== PYTHON ====="
                    which python3
                    python3 --version
        
                    echo "===== POETRY ====="
                    which poetry
                    poetry --version
        
                    echo "===== VIRTUALENV CONFIG ====="
                    poetry config virtualenvs.create
                    poetry config virtualenvs.in-project
        
                    echo "===== POETRY ENV INFO ====="
                    poetry env info
        
                    echo "===== PYTHON EXECUTABLE ====="
                    poetry run python -c "import sys; print(sys.executable)"
        
                    echo "===== POETRY ENVIRONMENT VARIABLES ====="
                    env | grep -E '^(POETRY_VIRTUALENVS_CREATE|VIRTUAL_ENV|PYTHONPATH)=' || true
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    set -eu

                    poetry config virtualenvs.create true
                    poetry config virtualenvs.in-project true

                    poetry install --no-root --no-interaction --no-ansi
                '''
            }
        }

        stage('Code Quality - Pylint') {
            steps {
                sh '''
                    set -eu

                    poetry run pylint \
                        router/ \
                        client/ \
                        models/ \
                        utils/ \
                        app.py \
                        --ignore-patterns='(^|/)tests/'
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
