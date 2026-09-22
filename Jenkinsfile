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
                // Poetry pipeline ke liye binary paths globally load karna ya local tool setup
                sh 'pip3 install --user poetry || pip3 install poetry'
                sh 'export PATH="$HOME/.local/bin:$PATH" && poetry install'
            }
        }

        stage('Lint Checks') {
            steps {
                // Makefile me clean fmt command available h use execute kr rahe h
                sh 'export PATH="$HOME/.local/bin:$PATH" && poetry run make fmt || true' 
            }
        }

        stage('Unit Tests') {
            steps {
                // Pytest se application modules components test kr rahe h
                sh 'export PATH="$HOME/.local/bin:$PATH" && poetry run pytest'
            }
        }
    }
}
