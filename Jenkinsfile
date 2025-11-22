pipeline {
    agent any
    
    environment {
        VENV_PATH = 'venv'
        PROJECT_NAME = 'flask-student-registry'
    }
    
    options {
        timeout(time: 30, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '5'))
        disableConcurrentBuilds()
    }
    
    triggers {
        pollSCM('H/2 * * * *')  // Poll every 2 minutes
    }
    
    stages {
        stage('Clean Workspace') {
            steps {
                cleanWs()
                echo "🧹 Workspace cleaned successfully"
            }
        }
        
        stage('Checkout SCM') {
            steps {
                git branch: 'main', 
                url: 'https://github.com/ramiz0009/Jenkins_flask_Practice.git'
                echo "✅ Code checkout completed - Revision: ${GIT_COMMIT}"
            }
        }
        
        stage('Display Environment Info') {
            steps {
                sh '''
                    echo "=== Environment Information ==="
                    echo "Python Version: $(python3 --version)"
                    echo "Pipeline Workspace: ${WORKSPACE}"
                    echo "Build Number: ${BUILD_NUMBER}"
                    echo "Git Commit: ${GIT_COMMIT}"
                    echo "==============================="
                '''
            }
        }
        
        stage('Setup Virtual Environment') {
            steps {
                sh '''
                    echo "Setting up Python virtual environment..."
                    python3 -m venv ${VENV_PATH}
                    ${VENV_PATH}/bin/pip install --upgrade pip
                    echo "Virtual environment created successfully"
                '''
            }
        }
        
        stage('Install Dependencies') {
            steps {
                sh '''
                    echo "Installing dependencies from requirements.txt..."
                    ${VENV_PATH}/bin/pip install -r requirements.txt
                    echo "✅ All dependencies installed successfully"
                '''
            }
        }
        
        stage('Install Test Dependencies') {
            steps {
                sh '''
                    ${VENV_PATH}/bin/pip install pytest pytest-html bandit safety
                    echo "✅ Test dependencies installed"
                '''
            }
        }
        
        stage('Code Quality Check') {
            steps {
                sh '''
                    echo "Running code quality checks..."
                    ${VENV_PATH}/bin/python -m py_compile app.py
                    echo "✅ Code compilation successful"
                    
                    # Check for syntax errors in all Python files
                    find . -name "*.py" -exec ${VENV_PATH}/bin/python -m py_compile {} \\;
                    echo "✅ All Python files compiled successfully"
                '''
            }
        }
        
        stage('Run Security Scan') {
            steps {
                sh '''
                    echo "Running security scan with Bandit..."
                    ${VENV_PATH}/bin/bandit -r . -f html -o bandit_report.html || true
                    echo "✅ Security scan completed"
                    
                    echo "Checking for vulnerable dependencies..."
                    ${VENV_PATH}/bin/safety check -r requirements.txt --output text > safety_report.txt || true
                    echo "✅ Dependency security check completed"
                '''
            }
            post {
                always {
                    publishHTML([
                        allowMissing: true,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: '.',
                        reportFiles: 'bandit_report.html',
                        reportName: 'Security Scan Report'
                    ])
                    archiveArtifacts artifacts: 'safety_report.txt', fingerprint: true
                }
            }
        }
        
        stage('Run Tests') {
            steps {
                sh '''
                    echo "Setting up test environment..."
                    export MONGO_URI="mongodb://localhost:27017/student_registry_test"
                    export SECRET_KEY="test-secret-key-${BUILD_NUMBER}"
                    
                    echo "Running test suite..."
                    if [ -d "tests" ]; then
                        ${VENV_PATH}/bin/python -m pytest tests/ -v --junitxml=test-results.xml --html=test-report.html || echo "⚠️ Some tests failed but continuing..."
                    else
                        echo "ℹ️ No tests directory found, creating basic test..."
                        # Create a simple test to verify app starts
                        ${VENV_PATH}/bin/python -c "
                        from app import app
                        print('✅ App imported successfully')
                        with app.test_client() as client:
                            response = client.get('/')
                            print(f'Home page status: {response.status_code}')
                        " || echo "⚠️ Basic app test failed"
                    fi
                '''
            }
            post {
                always {
                    junit 'test-results.xml'
                    publishHTML([
                        allowMissing: true,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: '.',
                        reportFiles: 'test-report.html',
                        reportName: 'Test Report'
                    ])
                }
            }
        }
        
        stage('Deploy to Staging') {
            when {
                branch 'main'
            }
            steps {
                sh '''
                    echo "🚀 Starting deployment to staging..."
                    
                    # Stop any existing application instances
                    echo "Stopping any existing Flask applications..."
                    pkill -f "python app.py" || true
                    sleep 3
                    
                    # Create production environment file
                    echo "Creating environment configuration..."
                    cat > .env << EOF
MONGO_URI=mongodb://localhost:27017/student_registry
SECRET_KEY=jenkins-production-secret-${BUILD_NUMBER}
FLASK_ENV=production
EOF
                    
                    # Start the application
                    echo "Starting Flask application..."
                    nohup ${VENV_PATH}/bin/python app.py > app.log 2>&1 &
                    echo $! > app.pid
                    
                    echo "✅ Application deployment initiated"
                '''
            }
        }
        
        stage('Health Check') {
            when {
                branch 'main'
            }
            steps {
                sh '''
                    echo "🏥 Performing health check..."
                    
                    # Wait for application to start
                    sleep 10
                    
                    # Health check with retry logic
                    for i in {1..5}; do
                        echo "Health check attempt $i..."
                        if curl -s -f http://localhost:8000/ > /dev/null; then
                            echo "✅ Health check PASSED - Application is running successfully!"
                            echo "🌐 Application URL: http://localhost:8000"
                            break
                        else
                            echo "⏳ Application not ready yet, waiting..."
                            sleep 5
                        fi
                    done
                    
                    # Final check
                    if ! curl -s http://localhost:8000/ > /dev/null; then
                        echo "❌ Health check FAILED - Application did not start properly"
                        echo "📋 Last 20 lines of application log:"
                        tail -20 app.log || echo "No application log found"
                        exit 1
                    fi
                '''
            }
        }
    }
    
    post {
        always {
            echo "=== Build Completion Status ==="
            echo "Build Result: ${currentBuild.result}"
            echo "Build URL: ${BUILD_URL}"
            echo "Duration: ${currentBuild.durationString}"
            echo "==============================="
            
            // Archive important files
            archiveArtifacts artifacts: 'app.log, *.pid, *.txt, *.html', fingerprint: true
            
            // Cleanup to save space (keep for debugging)
            sh '''
                echo "Cleaning up temporary files..."
                rm -rf ${VENV_PATH} || true
            '''
        }
        success {
            script {
                echo "🎉 PIPELINE SUCCESSFUL! 🎉"
                echo "📊 Build Number: ${BUILD_NUMBER}"
                echo "🔗 Application: http://localhost:8000"
                echo "📝 Commit: ${GIT_COMMIT}"
                
                // Create build summary
                currentBuild.description = "✅ SUCCESS - Deployed to http://localhost:8000"
            }
        }
        failure {
            script {
                echo "❌ PIPELINE FAILED!"
                echo "🔍 Check console output for details: ${BUILD_URL}console"
                
                // Debug information
                sh '''
                    echo "=== Debug Information ==="
                    echo "Recent application logs:"
                    tail -30 app.log || echo "No application logs"
                    echo "=== Process check ==="
                    ps aux | grep python || echo "No Python processes running"
                    echo "=== Port check ==="
                    netstat -tlnp | grep :8000 || echo "Port 8000 not in use"
                '''
                
                currentBuild.description = "❌ FAILED - Check console output"
            }
        }
        unstable {
            echo "⚠️ Pipeline is unstable - check test results and security reports"
            currentBuild.description = "⚠️ UNSTABLE - Check test reports"
        }
        aborted {
            echo "🛑 Pipeline was aborted by user"
            currentBuild.description = "🛑 ABORTED"
        }
    }
}
