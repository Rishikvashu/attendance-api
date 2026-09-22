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
                sh 'pip3 install --user poetry --break-system-packages'
                
                // Setuptools issue fix karne ke liye virtualenv initialize karke manual setup updates kiye hain
                sh '''
                    export PATH="$HOME/.local/bin:$PATH"
                    $HOME/.local/bin/poetry config virtualenvs.in-project true
                    
                    # Lock compilation crash fix pipeline hooks
                    $HOME/.local/bin/poetry run pip install -U setuptools wheel --break-system-packages || true
                    
                    # Install dependencies recursively
                    $HOME/.local/bin/poetry install --no-root
                '''
            }
        }

        stage('Lint Checks') {
            steps {
                sh '''
                    export PATH="$HOME/.local/bin:$PATH"
                    $HOME/.local/bin/poetry run make fmt || true
                '''
            }
        }

        stage('Unit Tests') {
            steps {
                sh '''
                    export PATH="$HOME/.local/bin:$PATH"
                    $HOME/.local/bin/poetry run pytest
                '''
            }
        }
    }
}
