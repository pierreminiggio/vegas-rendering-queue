const {exec} = require('child_process')

const startRender = exec('bash start.sh')

startRender.addListener('exit', (code) => {
    console.log(code)
    console.log('exit')
})