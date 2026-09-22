pipeline {
    agent any

    tools {
        // Agar aapne pichle task ki tarah NodeJS ki jagah koi Python tool configure kiya hai toh yahan likhein, 
        // warna agar server par default python3 installed hai toh is tools block ko hata sakte hain.
    }

    stages {
        Def 'Environment Check' {
            Steps {
                Sh 'python3 --version'
                Sh 'pip3 --version'
            }
        }

        Stage('Install Dependencies') {
            Steps {
                // Dependency install karne ke liye poetry aur Makefile ka use ho raha hai
                Sh 'pip3 install poetry'
                Sh 'poetry install'
            }
        }

        Stage('Lint Checks') {
            Steps {
                // Repo ke instructions ke mutabik linting (Format) check karne ka make command
                Sh 'poetry run make fmt || true' 
            }
        }

        Stage('Unit Tests') {
            Steps {
                // Pytest chalane aur coverage nikalne ka standard command jo repo mein bataya hai
                Sh 'poetry run pytest'
            }
        }
    }
}
