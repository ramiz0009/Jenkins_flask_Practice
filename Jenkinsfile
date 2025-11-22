pipeline {
    agent any

    stages {

        stage('Build') {
            steps {
                echo "Installing dependencies..."
                sh """
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                """
            }
        }

        stage('Test') {
            steps {
                echo "Running pytest..."
                sh """
                    . venv/bin/activate
                    pytest --maxfail=1 --disable-warnings -q
                """
            }
        }

        stage('Deploy') {
            when {
                expression { currentBuild.result == null || currentBuild.result == 'SUCCESS' }
            }
            steps {
                echo "Deploying Flask application to staging..."
                
                // Example: Copy files to a server or start the app
                sh """
                    . venv/bin/activate
                    nohup python app.py &
                """
            }
        }
    }

    post {
        always {
            echo "Pipeline completed."
        }
        success {
            echo "Build succeeded!"
        }
        failure {
            echo "Build failed!"
        }
    }
}
