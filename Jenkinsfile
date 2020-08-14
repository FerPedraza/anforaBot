def getContainerInfo() {
  def containersPrefix = 'bot_'
  def workspacePrefix = 'chatbots-'
	def name = 'botanfora'

  return [
    name: "${containersPrefix}${name}",
    image: "${containersPrefix}${name}",
    workspace: "/${workspacePrefix}${name}"
  ]
}

def getEnvironments() {
  def port = 5000

  return [
    local: [
      runPort: port
    ],
    qa: [
      runPort: port
    ],
    prod: [
      runPort: port
    ]
  ]
}

pipeline {
  environment {
    networkName = 'chatbots_dbnet'
  }
  agent any
  stages {
    stage('Start container') {
      steps { startContainer() }
    }
    stage('Load backend') {
      steps { loadBackend() }
    }
    stage('Deploy server') {
      steps { deployServer() }
    }
  }
}

/**
 * @param name Docker command name (e.g 'cp', 'build')
 * @param args Commang Arguments
 */
def dockerCommand(String name, String args) {
  sh "docker ${name} ${args}"
}

/**
 * @param container Container name
 * @param args Commang Arguments
 */
def dockerExec(String container, String args) {
  dockerCommand('exec', "${container} ${args}")
}

def createEnvFile(obj) {
  writeFile file: '.env', text: "${buildEnvVariables(obj)}"
}

def getConfig() {
  def envConfigs = getEnvironments()
  return envConfigs[env.BUILD_ENV]
}

def buildEnvVariables(obj) {
  def resultStr = ''
  obj.each { key, value ->
    resultStr += "${key}=${value}\n"
  }
  return resultStr
}

def buildEnv(options) {
  return [
    PORT: 3000,
    PRODUCTION: options.PRODUCTION ? 'true' : 'false',
    DB_HOST: options.DB_HOST,
    DB_PORT: options.DB_PORT,
    DB_DATABASE: options.DB_DATABASE,
    DB_USERNAME: options.DB_USERNAME,
    DB_PASSWORD: options.DB_PASSWORD,
    DB_SCHEMA: options.DB_SCHEMA,
    SECRET: options.SECRET
  ]
}

def upContainer(info, String args = '') {
  // Check if container exists
  def container = sh(returnStdout: true, script: "docker ps -aq -f name=${info.name}")
  if (container) {
    // Check if container is running
    isRunning = sh(returnStdout: true, script: "docker ps -q -f name=${info.name}")
    if (!isRunning?.trim()) {
      dockerCommand('container', "start ${info.name}")
    }
  } else {
    dockerCommand('build', "-t ${info.image} .")
    dockerCommand('run', "-it -d --name ${info.name}${args} ${info.image}")
  }
}

// ================================================================================================
// Build steps
// ================================================================================================

def startContainer() {
  def containerInfo = getContainerInfo()
  def config = getConfig()
  upContainer(containerInfo, " -p ${config.runPort}:5000")
}

def loadBackend() {
  def container = getContainerInfo()
  def config = getConfig()
  def options = config.env

  /* def envVariables = buildEnv(options)
  createEnvFile(envVariables) */
  dockerExec(container.name, "sh -c 'rm -rf ${container.workspace}/*'")
  try {
    dockerExec(container.name, "sh -c 'rm -rf ${container.workspace}/.*'")
  } catch (e) { }
  dockerCommand('cp', ". ${container.name}:${container.workspace}/")
  // dockerExec(container.name, "cat ./.env")
  dockerExec(container.name, "pip install -r requirements.txt")
}

def deployServer() {
  def container = getContainerInfo()
  /* def config = getConfig() */
  try {
    dockerExec(container.name, "pkill gunicorn")
  } catch (e) { }
  dockerExec("-i ${container.name}", "bash -c \"cd . && gunicorn --config gunicorn.conf.py bot_service:app\"")
}