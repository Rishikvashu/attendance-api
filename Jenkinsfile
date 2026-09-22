pipeline {
    agent any

    stages {
        stage('Environment Check') {
            steps {
                sh 'python3 --version'
                sh 'pip3 --version'
            }
        }

        stage('Install Dependencies') {
            steps {
                // Poetry bypass karke native venv isolation implement kiya hai
                sh '''
                    python3 -m venv venv
                    ./venv/bin/pip install --upgrade pip setuptools wheel
                    
                    # Poetry configuration backup binary wheels use karna
                    pip3 install --user poetry --break-system-packages || true
                    export PATH="$HOME/.local/bin:$PATH"
                    
                    # PyYAML dynamic setup configuration injection
                    ./venv/bin/pip install "pyyaml==6.0.1" --only-binary=:all: || ./venv/bin/pip install pyyaml==6.0.2
                    
                    # Poetry dependencies export karke clean venv me install karna
                    $HOME/.local/bin/poetry export -f requirements.txt --output requirements.txt --without-hashes || true
                    
                    # Requirements install execution block
                    if [ -f requirements.txt ]; then
                        ./venv/bin/pip install -r requirements.txt
                    else
                        $HOME/.local/bin/poetry install --no-root
                    fi
                '''
            }
        }

        stage('Lint Checks') {
            steps {
                sh '''
                    if [ -d "venv" ]; then
                        ./venv/bin/pip install pylint flake8 || true
                        ./venv/bin/flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics || true
                    fi
                '''
            }
        }

        stage('Unit Tests') {
            steps {
                sh '''
                    if [ -d "venv" ]; then
                        ./venv/bin/pip install pytest pytest-cov || true
                        ./venv/bin/pytest
                    fi
                '''
            }
        }
    }
}
