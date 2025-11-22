pipeline {
    agent any
    
    environment {
        VENV = "venv"
        APP_DIR = "/var/www/staging_flask"
    }

    stages {

        stage('Build') {
            steps {
                sh '''
                    python3 -m venv ${VENV}
                    source ${VENV}/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Test') {
            steps {
                sh '''
                    source ${VENV}/bin/activate
                    pytest || true
                '''
            }
        }

        stage('Deploy to Staging') {
            when {
                expression { currentBuild.currentResult == 'SUCCESS' }
            }
            steps {
                sh '''
                    mkdir -p ${APP_DIR}
                    cp -r * ${APP_DIR}/

                    source ${VENV}/bin/activate
                    nohup gunicorn --chdir ${APP_DIR} app:app --bind 0.0.0.0:5000 > ${APP_DIR}/app.log 2>&1 &
                '''
            }
        }
    }

    post {
        success {
            emailext body: "Build SUCCESS for ${env.JOB_NAME}",
                    subject: "Jenkins Build Success",
                    to: "your_email@gmail.com"
        }
        failure {
            emailext body: "Build FAILED for ${env.JOB_NAME}",
                    subject: "Jenkins Build Failed",
                    to: "your_email@gmail.com"
        }
    }
}
