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
                // Poetry securely user space me install ho rahi hai
                sh 'pip3 install --user poetry --break-system-packages'
                
                // Poetry ke binary path ko environment me explicit update karna
                sh '''
                    export PATH="$HOME/.local/bin:$PATH"
                    $HOME/.local/bin/poetry config virtualenvs.in-project true
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
