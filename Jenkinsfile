pipeline {
    agent {         // any
      node {        // Option
        label "Python3"
      }
    }

    options{
      timestamps()
      disableConcurrentBuilds()             // Parallelism is prohibited, only one build is allowed at a time.
      timeout(time: 30, unit: 'MINUTES')    // java.util.concurrent.TimeUnit
    }

    /**
     * Environment variables
     */
    environment {
        GIT_URL       = 'git@github.com:jeffwji/Monitor.git'
        CREDENTIAL    = 'Github'
        BRANCH        = 'develop'
        PYPI_CREDENTIAL = "PypiRepo"
    }

    /**
     * The compilation process consists multiple stages.
     */
    stages {
        /**
         * Each stage can be divided into steps
         */
        stage('Clear up workspace') {
            steps {
                // print environment variables
                sh 'printenv'

                // clear cache cache
                echo "Delete workspace ${workspace}"

                dir("${workspace}") {
                    deleteDir()
                }
                dir("${workspace}@tmp") {
                    deleteDir()
                }
            }
        }

        /**
         * Dload source code
         */
        stage('Get code from Github') {
            steps {
                script{     // Java script
                  println('Get code from Github') 
                }
                git branch: "${env.BRANCH}", credentialsId: "${env.CREDENTIAL}", url: "${env.GIT_URL}"   // Apply environment variables from the `env` namespace
            }
        }

        /**
         * Install dependency for coverage and unittest(nosetests) and language checking
         */
        stage('Install testing dependency') {
            steps {
                echo 'Initial virtual environment'
                dir("${workspace}") {
                    sh "python3 -m venv .venv"
                }

                echo 'Install testing dependency'
                /**
                 * withPythonEnv needs `Jenkins Pyenv plugin` to support
                 */
                withPythonEnv("${workspace}/.venv/bin/"){
                    dir("${workspace}") {
                        sh 'pip install wheel nose coverage nosexcover pylint twine'
                        sh 'pip install -r requirements.txt'
                        sh 'pip list'
                    }
                }
            }
        }

        /**ocker
         * Run coverage or regular unit test
         */
        stage('Testing') {
            steps {
                echo 'Run test cases'
                withPythonEnv("${workspace}/.venv/bin/"){
                    dir("${workspace}") {
                        // sh 'python setup.py test'
                        sh 'nosetests -sv --with-xunit --xunit-file=nosetests.xml --with-xcoverage --xcoverage-file=coverage.xml'
                    }
                }
            }
        }

        /**
         * Call SonarQube scanner
         * It will load in coverage and other reports generated from previous step.
         */
        //stage('Sonar scan') {
        //    steps {
        //        withPythonEnv("${workspace}/.venv/bin/"){
        //            dir("${workspace}") {
        //                script {sonarHome=tool 'SonarQube Scanner'}    // name is defined in `Global Tool Configuration`
        //                withSonarQubeEnv('MySonarQube') {                      // name is defined in `Configure System`
        //                    sh 'echo workspace=${sonarHome}'
        //                    sh 'sonar-scanner \
        //                        -Dsonar.host.url=http://192.168.56.110:9000 \
        //                        -Dsonar.projectKey=Monitor \
        //                        -Dsonar.projectVersion=1.0 \
        //                        -Dsonar.language=py \
        //                        -Dsonar.tests=./tests \
        //                        -Dsonar.exclusions=setup.py,**/__init__.py \
        //                        -Dsonar.sourceEncoding=UTF-8 \
        //                        -Dsonar.python.xunit.reportPath=nosetests.xml \
        //                        -Dsonar.python.coverage.reportPaths=coverage.xml \
        //                        -Dsonar.python.pylint=/usr/local/bin/pylint \
        //                        -Dsonar.python.pylint_config=.pylintrc \
        //                        -Dsonar.python.pylint.reportPath=pylint-report.txt'
        //                }
        //            }
        //        }
        //
        //        timeout(time: 10, unit: 'MINUTES') {
        //            waitForQualityGate abortPipeline: true
        //        }
        //    }
        //}

        /**
         * Package
         *
         * Python version standard：https://www.python.org/dev/peps/pep-0440/
         */
        stage('Build') {
            steps {
                echo 'Build Monitor'
                withPythonEnv("${workspace}/.venv/bin/"){
                    dir("${workspace}") {
                        sh 'python setup.py egg_info -b.dev$(date "+%s") bdist_wheel'
                    }
                }
            }
        }

        /**
         * Pushing to Nexus
         *
         * Run the following commands on client:
         *   pip config set global.index https://io.hibiup.com/nexus/repository/pypi-central/simple
         *   pip config set global.index-url https://io.hibiup.com/nexus/repository/pypi-central/simple
         *   pip config set global.trusted-host io.hibiup.com
         *   pip config set global.extra-index-url https://io.hibiup.com/nexus/repository/pypi/simple
         */
        stage('Pushing to Repository') {
            steps {
                echo 'Upload Monitor'
                withPythonEnv("${workspace}/.venv/bin/"){
                    dir("${workspace}") {
                        withCredentials([usernamePassword(credentialsId: "${env.PYPI_CREDENTIAL}", passwordVariable: 'pass', usernameVariable: 'user')]){
                            sh '''cat << EOF > .pypirc
[distutils]
    index-servers=
        internal_pypi

[internal_pypi]
    repository: https://io.hibiup.com/nexus/repository/pypi/
    username: ${user}
    password: ${pass}
EOF'''

                            sh 'twine upload --config-file=.pypirc -r internal_pypi dist/*'
                        }
                    }
                }
            }
        }
    }

    /**
     * Post build process
     */
    post{
        // Always run
        always{
            echo "Always"
        }

        // Conditional run
        success {
            echo currentBuild.description = "Success"    // currentBuild.description will bring the information back to the control panel
            /**
            emailext (
                subject: "SUCCESSFUL: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]'",
                body: """<p>SUCCESSFUL: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]':</p>
                    <p>Check console output at &QUOT;<a href='${env.BUILD_URL}'>${env.JOB_NAME} [${env.BUILD_NUMBER}]</a>&QUOT;</p>""",
                recipientProviders: [[$class: 'DevelopersRecipientProvider'], [$class: 'RequesterRecipientProvider']]
            )
            */
        }

        failure{
            echo  currentBuild.description = "Failure"
            /**
            emailext (
                subject: "FAILED: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]'",
                body: """<p>FAILED: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]':</p>
                    <p>Check console output at &QUOT;<a href='${env.BUILD_URL}'>${env.JOB_NAME} [${env.BUILD_NUMBER}]</a>&QUOT;</p>""",
                recipientProviders: [[$class: 'DevelopersRecipientProvider'], [$class: 'RequesterRecipientProvider']]                                            
            )
            */
        }

        aborted{
            echo currentBuild.description = "Aborted"
            /**
            emailext (
                subject: "Aborted: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]'",
                body: """<p>ABORTED: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]':</p>
                    <p>Check console output at &QUOT;<a href='${env.BUILD_URL}'>${env.JOB_NAME} [${env.BUILD_NUMBER}]</a>&QUOT;</p>""",
                recipientProviders: [[$class: 'DevelopersRecipientProvider'], [$class: 'RequesterRecipientProvider']]                                            
            )
            */
        }
    }
}
