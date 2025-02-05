pipeline {
    agent {
        docker {
            image 'python:3.10-slim'  // Use a Python 3.10 Docker image
        }
    }
    environment {
        EC2_HOST = credentials('EC2_HOST')  // Store EC2_HOST in Jenkins credentials
        EC2_USER = credentials('EC2_USER')  // Store EC2_USER in Jenkins credentials
        SSH_KEY = credentials('SSH_KEY')    // Store SSH_KEY in Jenkins credentials
    }
    stages {
        stage('Checkout Repository') {
            steps {
                checkout scm  // Check out the repository
            }
        }
        stage('Set Up Python') {
            steps {
                sh 'python -m venv myenv'  // Create a Python virtual environment
                sh 'source myenv/bin/activate'  // Activate the virtual environment
            }
        }
        stage('Install Dependencies') {
            steps {
                sh '''
                    source myenv/bin/activate
                    pip install -r requirements.txt
                '''
            }
        }
        stage('Check Dataset Changes and Retrain') {
            steps {
                sh '''
                    source myenv/bin/activate
                    python train.py  // Retrain the model if dataset changes
                '''
            }
        }
        stage('Deploy Model to EC2') {
            steps {
                sh '''
                    # Save the SSH key and fix any potential issues with carriage returns
                    echo "$SSH_KEY" | tr -d '\r' > Flaskapp.pem
                    chmod 600 Flaskapp.pem

                    # Create the .ssh directory if it doesn't exist
                    mkdir -p ~/.ssh

                    # Automatically add the EC2 host to the known_hosts file without user interaction
                    ssh-keyscan -H $EC2_HOST >> ~/.ssh/known_hosts

                    # Debugging - Check environment variables
                    echo "EC2_USER: $EC2_USER"
                    echo "EC2_HOST: $EC2_HOST"

                    # Verify the SSH key
                    cat Flaskapp.pem

                    # Ensure folder exists on EC2
                    ssh -i Flaskapp.pem $EC2_USER@$EC2_HOST '[ -d "/home/$EC2_USER/models" ] || sudo mkdir -p /home/$EC2_USER/models'

                    # Copy model file to EC2
                    scp -i Flaskapp.pem models/model_*.pkl $EC2_USER@$EC2_HOST:/home/$EC2_USER/models/
                '''
            }
        }
    }
    post {
        success {
            echo 'Pipeline succeeded!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}