pipeline {
    agent {
         label 'res-vrt-prd-cdr'  
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
                    branch: "${env.GIT_BRANCH}",
                )
            }
        }

        stage('Install Requirements') {
            steps {
                    script {
                        sh(script:"""
                                  python3 -m venv venv
                                  . venv/bin/activate
                                  python3 -m pip install -r requirements.txt
                                  """)
                    }
              }
        }

        stage('Lint Definition Files') {
            steps {
                    script {
                        def LINTER_RESULT = sh(script:"""
                                            python3 -m venv venv
                                            . venv/bin/activate
                                            python3 run.py --lint-all-files
                                            """, returnStatus: true)
                        env.LINTER_RESULT = LINTER_RESULT
                        if(env.LINTER_RESULT == '0') {
                            echo "Defintion file linting passed"
                        }
                        if(env.LINTER_RESULT == '1') {
                            error("Defintion file linting failed")
                        }
                    }
              }
        }
        
        stage('Validate Queries') {
            steps {
                    script {
                        
                            withCredentials([string(credentialsId: 'gravwell-token', variable: 'GRAVWELL_TOKEN')]){
                                def VALIDATION_RESULT = sh(script:"""
                                                                   python3 -m venv venv
                                                                   . venv/bin/activate
                                                                   python3 run.py --token $GRAVWELL_TOKEN --validate-queries
                                                                   """, returnStatus: true)
                                env.VALIDATION_RESULT = VALIDATION_RESULT
                                if(env.VALIDATION_RESULT == '0') {
                                    echo "Query validation passed"
                                }
                                if(env.VALIDATION_RESULT == '1') {
                                    error("Query validation failed")
                                }
                          }
                    }
            }
        }
        
        stage('Synchronize Configuration Data') {
            steps {
                script {
                    withCredentials([string(credentialsId: 'gravwell-token', variable: 'GRAVWELL_TOKEN')]) {
                        sh """
                           python3 -m venv venv
                           . venv/bin/activate
                           python3 run.py --token $GRAVWELL_TOKEN --sync-all
                           """   
                    }
                }
            }
        }
    }
}