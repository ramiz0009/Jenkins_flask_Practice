pipeline {
    agent any
    
    environment {
        VENV_DIR = 'venv'
        APP_PORT = '8000'
        PID_FILE = 'app.pid'
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo '=== Checking out code from GitHub ==='
                checkout scm
            }
        }
        
        stage('Build') {
            steps {
                echo '=== Installing Dependencies ==='
                sh '''
                    # Remove old virtual environment
                    rm -rf ${VENV_DIR}
                    
                    # Create virtual environment
                    python3 -m venv ${VENV_DIR}
                    
                    # Activate and install dependencies
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }
        
        stage('Test') {
            steps {
                echo '=== Running Unit Tests ==='
                sh '''
                    . ${VENV_DIR}/bin/activate
                    
                    # Run pytest with verbose output
                    pytest tests/ -v --tb=short || exit 1
                '''
            }
        }
        
        stage('Deploy to Staging') {
            steps {
                echo '=== Deploying to Staging Environment ==='
                
                // Setup environment variables
                withCredentials([
                    string(credentialsId: 'MONGO_URI', variable: 'MONGO_URI'),
                    string(credentialsId: 'SECRET_KEY', variable: 'SECRET_KEY')
                ]) {
                    sh '''
                        echo "=== Debugging Credential Injection ==="
                        # Create .env file
                        echo "MONGO_URI=${MONGO_URI}" > .env
                        echo "SECRET_KEY=${SECRET_KEY}" >> .env
                        
                        # Stop previous instance if running
                        if [ -f ${PID_FILE} ]; then
                            PID=$(cat ${PID_FILE})
                            if ps -p $PID > /dev/null 2>&1; then
                                echo "Stopping previous instance (PID: $PID)"
                                kill $PID
                                sleep 3
                            fi
                            rm -f ${PID_FILE}
                        fi
                        
                        # Kill any process on port 8000
                        if lsof -Pi :${APP_PORT} -sTCP:LISTEN -t >/dev/null 2>&1; then
                            echo "Killing process on port ${APP_PORT}"
                            kill -9 $(lsof -t -i:${APP_PORT}) || true
                            sleep 2
                        fi
                        
                        # Start application
                        . ${VENV_DIR}/bin/activate
                        nohup python3 app.py > app.log 2>&1 &
                        echo $! > ${PID_FILE}
                        
                        # Wait for application to start
                        sleep 5
                        
                        # Verify deployment
                        if ps -p $(cat ${PID_FILE}) > /dev/null 2>&1; then
                            echo "Application deployed successfully!"
                            echo "PID: $(cat ${PID_FILE})"
                        else
                            echo "Deployment failed!"
                            cat app.log
                            exit 1
                        fi
                    '''
                }
            }
        }
        
        stage('Health Check') {
            steps {
                echo '=== Performing Health Check ==='
                sh '''
                    # Wait for app to be ready
                    sleep 3
                    
                    # Check if application responds
                    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:${APP_PORT}/ || echo "000")
                    
                    if [ "$HTTP_CODE" = "200" ]; then
                        echo "Health check PASSED! Application is running."
                        echo "Application URL: http://localhost:${APP_PORT}"
                    else
                        echo "Health check FAILED! HTTP Status: $HTTP_CODE"
                        cat app.log
                        exit 1
                    fi
                '''
            }
        }
    }
    
    post {
        success {
            echo '=== Pipeline Completed Successfully! ==='
            emailext (
                subject: "SUCCESS: Jenkins Pipeline - ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """
                    <h2>Build Successful!</h2>
                    <p><strong>Job:</strong> ${env.JOB_NAME}</p>
                    <p><strong>Build Number:</strong> ${env.BUILD_NUMBER}</p>
                    <p><strong>Status:</strong> SUCCESS</p>
                    <p><strong>Application URL:</strong> http://your-server:${APP_PORT}</p>
                    <p>Check console output at: ${env.BUILD_URL}</p>
                """,
                to: 'sheikhramiz666@gmail.com',
                mimeType: 'text/html'
            )
        }
        
        failure {
            echo '=== Pipeline Failed! ==='
            sh '''
                # Cleanup on failure
                if [ -f ${PID_FILE} ]; then
                    kill $(cat ${PID_FILE}) 2>/dev/null || true
                    rm -f ${PID_FILE}
                fi
            '''
            emailext (
                subject: "FAILURE: Jenkins Pipeline - ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """
                    <h2>Build Failed!</h2>
                    <p><strong>Job:</strong> ${env.JOB_NAME}</p>
                    <p><strong>Build Number:</strong> ${env.BUILD_NUMBER}</p>
                    <p><strong>Status:</strong> FAILURE</p>
                    <p>Check console output at: ${env.BUILD_URL}</p>
                    <p>Please review the logs and fix the issues.</p>
                """,
                to: 'sheikhramiz666@gmail.com',
                mimeType: 'text/html'
            )
        }
        
        always {
            echo '=== Archiving Artifacts ==='
            archiveArtifacts artifacts: 'app.log', allowEmptyArchive: true
            cleanWs(deleteDirs: true, patterns: [[pattern: 'venv/**', type: 'INCLUDE']])
        }
    }
}
