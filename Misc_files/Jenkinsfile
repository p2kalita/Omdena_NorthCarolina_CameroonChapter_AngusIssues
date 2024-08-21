pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                git url: 'https://dagshub.com/Omdena/NorthCarolina_CameroonChapter_AngusIssues.git',
                    credentialsId: 'a9198d64aa61a78f58c017c42601a90f0c62f79b',
                    branch: 'main'
            }
        }
        stage('Build') {
            steps {
                echo 'Building...'
                // Add your build steps here
            }
        }
        stage('Test') {
            steps {
                echo 'Testing...'
                // Add your test steps here
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying...'
                // Add your deploy steps here
            }
        }
    }
}
