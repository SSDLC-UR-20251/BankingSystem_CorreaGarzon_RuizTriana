pipeline {
    agent any

    stages {
        stage('Clonar código') {
            steps {
                script {
                    checkout scm
                }
            }
        }

        stage('Construir imagen Docker') {
            steps {
                sh 'docker build -t mi_app .'
            }
        }

        stage('Ejecutar contenedor') {
            steps {
                sh 'docker run -d -p 5000:5000 --name mi_app_container mi_app'
                sh 'sleep 5' // Esperar que el servidor levante
            }
        }

        stage('Verificar contenedores') {
            steps {
                sh 'docker ps'
            }
        }

        stage('Instalar dependencias') {
            steps {
                sh '''
                    pip install --upgrade pip
                    pip install selenium
                '''
            }
        }

        stage('Ejecutar pruebas unitarias - validation.py') {
            steps {
                sh '''
                    source ${PYTHON_ENV}/bin/activate
                    python3 validation.py
                '''
            }
        }

        stage('Ejecutar pruebas Selenium - test_banking.py') {
            steps {
                sh '''
                    source ${PYTHON_ENV}/bin/activate
                    python3 test_banking.py
                '''
            }
        }
    }

    post {
        always {
            echo 'Finalizando...'
            sh '''
                docker stop mi_app_container || true
                docker rm mi_app_container || true
            '''
        }
        failure {
            echo 'Hubo un error durante la ejecución del pipeline.'
        }
    }
}
