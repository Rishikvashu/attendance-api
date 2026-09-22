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
                
                sh '''
                    export PATH="$HOME/.local/bin:$PATH"
                    $HOME/.local/bin/poetry config virtualenvs.in-project true
                    
                    # Poetry virtual environment wrapper initialize karna
                    $HOME/.local/bin/poetry run pip install -U pip setuptools wheel --break-system-packages || true
                    
                    # PyYAML compatibility fix: binary wheel force fetch enable karna
                    export PIP_ONLY_BINARY=pyyaml
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
