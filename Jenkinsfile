pipeline {
    agent any

    options {
        timestamps()
        skipDefaultCheckout(true)
        disableConcurrentBuilds()
    }

    parameters {
        booleanParam(
            name: 'RUN_UNIT_TESTS',
            defaultValue: false,
            description: 'Enable this option to run unit tests'
        )
    }

    environment {
        PATH = "/var/lib/jenkins/.local/bin:/usr/local/bin:${env.PATH}"
        PYTHONUNBUFFERED = '1'
    }

    stages {

        // ==========================================
        // Stage 1: Checkout Source Code
        // ==========================================
        stage('Checkout') {
            steps {
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: '*/main']],
                    userRemoteConfigs: [[
                        url: 'https://github.com/Rishikvashu/attendance-api.git',
                        credentialsId: 'github-pat'
                    ]]
                ])

                sh '''
                    echo "=================================="
                    echo "Repository Checkout Successful"
                    echo "=================================="

                    git log -1 --oneline
                '''
            }
        }

        // ==========================================
        // Stage 2: Verify CI Tools
        // ==========================================
        stage('Verify CI Tools') {
            steps {
                sh '''
                    set -e

                    echo "Checking Python..."
                    python3 --version

                    echo "Checking Poetry..."
                    poetry --version

                    echo "Checking Gitleaks..."
                    gitleaks version

                    echo "Checking Git..."
                    git --version

                    echo "All required CI tools are available."
                '''
            }
        }

        // ==========================================
        // Stage 3: Diagnose Poetry Environment
        // ==========================================
        stage('Diagnose Poetry Environment') {
            steps {
                sh '''
                    echo "Checking Poetry configuration..."
                    poetry env info || true

                    echo "Checking Python version..."
                    poetry run python --version

                    echo "Checking installed dependencies..."
                    poetry show --installed || poetry show
                '''
            }
        }

        // ==========================================
        // Stage 4: Install Dependencies
        // ==========================================
        stage('Install Dependencies') {
            steps {
                sh '''
                    set -e

                    echo "Installing project dependencies..."

                    poetry install --no-interaction

                    echo "Dependency installation completed."
                '''
            }
        }

        // ==========================================
        // Stage 5: Code Quality - Pylint
        // ==========================================
        stage('Code Quality - Pylint') {
            steps {
                sh '''
                    set -e

                    echo "Running Pylint..."

                    poetry run pylint \
                        --fail-under=8.0 \
                        $(git ls-files '*.py')
                '''
            }
        }

        // ==========================================
        // Stage 6: Unit Tests (Optional)
        // ==========================================
        stage('Unit Tests') {
            when {
                expression {
                    return params.RUN_UNIT_TESTS
                }
            }

            steps {
                sh '''
                    set -e

                    mkdir -p reports

                    echo "Running Unit Tests..."

                    poetry run python -m pytest \
                        --junitxml=reports/pytest.xml \
                        --cov=. \
                        --cov-report=xml:reports/coverage.xml
                '''
            }

            post {
                always {
                    junit(
                        testResults: 'reports/pytest.xml',
                        allowEmptyResults: true
                    )

                    archiveArtifacts(
                        artifacts: 'reports/coverage.xml',
                        allowEmptyArchive: true
                    )
                }
            }
        }

        // ==========================================
        // Stage 7: Credential Scan - Gitleaks
        // ==========================================
        stage('Credential Scan - Gitleaks') {
            steps {
                sh '''
                    set -e

                    echo "=================================="
                    echo "Starting Credential Scanning"
                    echo "=================================="

                    gitleaks detect \
                        --source . \
                        --redact \
                        --verbose \
                        --exit-code 1

                    echo "=================================="
                    echo "Gitleaks Scan Passed"
                    echo "No credentials detected."
                    echo "=================================="
                '''
            }
        }
    }

    // ==========================================
    // Post-Build Actions
    // ==========================================
    post {
        success {
            echo 'Pipeline completed successfully.'
        }

        failure {
            echo 'Pipeline failed. Check the Console Output for details.'
        }

        always {
            echo 'Build execution completed.'

            cleanWs()
        }
    }
}