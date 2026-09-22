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
                // PEP 668 policy bypass krne k liye explicit break flag ka use kiya h
                sh 'pip3 install --user poetry --break-system-packages'
                
                // Project dependencies virtual env runtime context me deploy krna
                sh '''
                    export PATH="$HOME/.local/bin:$PATH"
                    poetry config virtualenvs.in-project true
                    poetry install --no-root
                '''
            }
        }

        stage('Lint Checks') {
            steps {
                sh '''
                    export PATH="$HOME/.local/bin:$PATH"
                    poetry run make fmt || true
                '''
            }
        }

        stage('Unit Tests') {
            steps {
                sh '''
                    export PATH="$HOME/.local/bin:$PATH"
                    poetry run pytest
                '''
            }
        }
    }
}
