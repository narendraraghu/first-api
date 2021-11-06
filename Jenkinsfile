pipeline {
    agent any

    stage("Git Clone"){

            git credentialsId: 'GIT_CREDENTIALS', url: 'https://github.com/narendraraghu/hello-api.git'
        }

         stage('Build') {

           sh 'python3 app.py'

        }

        stage("Docker build"){
            sh 'docker version'
            sh 'docker build -t hello-api .'
            sh 'docker image list'
            sh 'docker tag d94698199328 narendrakareli/hello-api'
        }

        withCredentials([string(credentialsId: 'DOCKER_HUB_PASSWORD', variable: 'PASSWORD')]) {
            sh 'docker login --username=narendrakareli -p $PASSWORD'
        }

        stage("Push Image to Docker Hub"){
            sh 'docker push narendrakareli/hello-api'
        }

        stage("SSH Into k8s Server") {
            def remote = [:]
            remote.name = 'K8S master'
            remote.host = '100.0.0.2'
            remote.user = 'vagrant'
            remote.password = 'vagrant'
            remote.allowAnyHosts = true

            stage('Put k8s-spring-boot-deployment.yml onto k8smaster') {
                sshPut remote: remote, from: 'pod.yaml', into: '.'
            }

            stage('Deploy  Python Code') {
              sshCommand remote: remote, command: "kubectl apply -f pod.yaml"
            }
        }

}