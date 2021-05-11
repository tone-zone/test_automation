pipeline {
  agent any
  stages {
    stage('Git') {
      steps {
        git(url: 'https://github.com/tone-zone/test_automation.git', branch: 'main')
      }
    }

    stage('test') {
      steps {
        powershell 'pytest test_automationstore.py'
      }
    }

  }
}