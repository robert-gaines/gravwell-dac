pipeline {
    agent {
         label 'res-phy-prd-rpi-1'  
    }

    environment {
        GIT_CREDENTIALS_ID = '88a9dcb0-74dc-44cd-91cd-2ff54e337e1e'  
        GIT_REPOSITORY_URL = 'https://github.com/robert-gaines/gravwell-dac.git'
        GIT_BRANCH = 'main'
    }

    stages {
        stage('Checkout') {
            steps {
                git(
                    credentialsId: "${env.GIT_CREDENTIALS_ID}",
                    url: "${env.GIT_REPOSITORY_URL}",
                    branch: "${env.GIT_BRANCH}"
                )
            }
        }

        stage('Synchronize Configuration Data') {
            steps {
                script {
                    withCredentials([string(credentialsId: 'gravwell-token', variable: 'GRAVWELL_TOKEN')]) {
                        sh """
                           python3 -m venv venv
                           . venv/bin/activate
                           python3 -m pip install -r requirements.txt
                           python3 run.py --token $GRAVWELL_TOKEN --sync-all
                           """   
                    }
                }
            }
        }
    }
}
