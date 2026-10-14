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
        PATH = "/var/lib/jenkins/.local/bin:/usr/local/bin:${env.PATH}"
    }

    stages {

        // ==========================================
        // 1. CHECKOUT
        // ==========================================
        stage('Checkout') {
            steps {
                checkout scm

                sh '''
                    set -eu

                    echo "===== CHECKED OUT COMMIT ====="
                    git rev-parse --short HEAD

                    echo "===== CURRENT BRANCH ====="
                    git branch --show-current
                '''
            }
        }

        // ==========================================
        // 2. VERIFY CI TOOLS
        // ==========================================
        stage('Verify CI Tools') {
            steps {
                sh '''
                    set -eu

                    echo "===== VERIFYING PYTHON ====="
                    command -v python3
                    python3 --version

                    echo "===== VERIFYING POETRY ====="
                    command -v poetry
                    poetry --version

                    echo "===== VERIFYING GITLEAKS ====="
                    command -v gitleaks
                    gitleaks version

                    echo "===== VERIFYING GIT ====="
                    command -v git
                    git --version
                '''
            }
        }

        // ==========================================
        // 3. DIAGNOSE POETRY ENVIRONMENT
        // ==========================================
        stage('Diagnose Poetry Environment') {
            steps {
                sh '''
                    set -eu

                    echo "===== BASE PYTHON ====="
                    python3 --version
                    which python3

                    echo "===== POETRY CONFIGURATION ====="
                    poetry config virtualenvs.create
                    poetry config virtualenvs.in-project

                    echo "===== CREATING / CHECKING VIRTUALENV ====="
                    poetry run python -c \
                        "import sys; print(sys.executable)"

                    echo "===== POETRY ENVIRONMENT INFO ====="
                    poetry env info

                    echo "===== PYTHON ENVIRONMENT VARIABLES ====="
                    env | grep -E \
                        '^(POETRY_VIRTUALENVS_CREATE|VIRTUAL_ENV|PYTHONPATH)=' \
                        || true
                '''
            }
        }

        // ==========================================
        // 4. INSTALL DEPENDENCIES
        // ==========================================
        stage('Install Dependencies') {
            steps {
                sh '''
                    set -eu

                    echo "===== CONFIGURING POETRY ====="

                    poetry config virtualenvs.create true
                    poetry config virtualenvs.in-project true

                    echo "===== INSTALLING PROJECT DEPENDENCIES ====="

                    poetry install \
                        --no-root \
                        --no-interaction \
                        --no-ansi

                    echo "===== VERIFYING PYTEST ====="

                    poetry run python -m pytest --version

                    echo "===== VERIFYING PYLINT ====="

                    poetry run pylint --version
                '''
            }
        }

        // ==========================================
        // 5. CODE QUALITY - PYLINT
        // APPLICATION CODE ONLY; EXCLUDE TESTS
        // ==========================================
        stage('Code Quality - Pylint') {
            steps {
                sh '''
                    set -eu

                    echo "===== COLLECTING APPLICATION FILES ====="

                    : > pylint-files.txt

                    for directory in router client models utils; do
                        if [ -d "$directory" ]; then
                            find "$directory" \
                                -type f \
                                -name "*.py" \
                                ! -path "*/tests/*" \
                                -print
                        fi
                    done > pylint-files.txt

                    if [ -f app.py ]; then
                        echo "app.py" >> pylint-files.txt
                    fi

                    echo "===== FILES SELECTED FOR PYLINT ====="
                    cat pylint-files.txt

                    if [ ! -s pylint-files.txt ]; then
                        echo "ERROR: No application Python files found."
                        exit 1
                    fi

                    echo "===== CHECKING TEST EXCLUSION ====="

                    if grep -E '(^|/)tests/' pylint-files.txt; then
                        echo "ERROR: Test files found in Pylint input."
                        exit 1
                    else
                        echo "PASS: Test files excluded."
                    fi

                    echo "===== RUNNING PYLINT ====="

                    xargs -r poetry run pylint < pylint-files.txt
                '''
            }
        }

        // ==========================================
        // 6. UNIT TESTS
        // ==========================================
        stage('Unit Tests') {
            steps {
                sh '''
                    set -eu

                    echo "===== PREPARING REPORT DIRECTORY ====="

                    mkdir -p reports

                    echo "===== RUNNING PYTEST ====="

                    poetry run python -m pytest \
                        --junitxml=reports/pytest.xml \
                        --cov=. \
                        --cov-report=xml:reports/coverage.xml

                    echo "===== UNIT TESTS COMPLETED ====="
                '''
            }
        }

        // ==========================================
        // 7. CREDENTIAL SCAN - GITLEAKS
        // ==========================================
        stage('Credential Scan - Gitleaks') {
            steps {
                sh '''
                    set -eu

                    echo "===== GITLEAKS VERSION ====="
                    gitleaks version

                    echo "===== SCANNING GIT REPOSITORY ====="

                    gitleaks git . \
                        --redact \
                        --no-banner

                    echo "===== GITLEAKS SCAN COMPLETED ====="
                '''
            }
        }
    }

    // ==========================================
    // POST-BUILD ACTIONS
    // ==========================================
    post {

        always {
            echo '===== PROCESSING TEST REPORTS ====='

            junit(
                testResults: 'reports/pytest.xml',
                allowEmptyResults: true
            )

            echo '===== ARCHIVING REPORTS ====='

            archiveArtifacts(
                artifacts: 'reports/**',
                allowEmptyArchive: true
            )
        }

        success {
            echo 'Attendance API CI pipeline passed.'
        }

        failure {
            echo 'Attendance API CI pipeline failed. Check the failed stage logs.'
        }

        cleanup {
            deleteDir()
        }
    }
}
