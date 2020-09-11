const {exec} = require('child_process')
const fs = require('fs');

/**
 * @typedef {Object} Video
 * @property {string} projectFilePath
 * @property {string} rendererName
 * @property {string} templateName
 * @property {string} outputFilePath
 */

/**
 * @typedef {Object} Config
 * @property {string} vegasPath
 * @property {Video[]} videos
 */

/**
 * @param {Array} array 
 * @param {CallableFunction} callback 
 */
async function asyncForEach (array, callback) {
    for (let index = 0; index < array.length; index++) {
        await callback(array[index], index, array);
    }
}

/**
 * @param {Video[]} videos 
 * @param {string} vegasPath
 */
async function renderVideos(videos, vegasPath) {
    await asyncForEach(videos, async (video) => {
        return await renderVideo(video, vegasPath)
    })
}

/**
 * @param {Video} video 
 * @param {string} vegasPath
 */
async function renderVideo(video, vegasPath) {
    return await new Promise((resolve, reject) => {
        fs.writeFile(
            './tmp.csv',
            video.projectFilePath + ';' + video.rendererName + ';' + video.templateName + ';' + video.outputFilePath,
            (err) => {
                if (err) {
                    reject(err)
                }

                const startRender = exec('bash start.sh')
                startRender.addListener('exit', (code) => {
                    resolve(code)
                })
            }
        )
    });
}


fs.readFile('./config.json', 'utf8', (err, configString) => {
    if (err) {
        throw 'Config File Missing : ' + err
    }

    /** @var {Config} */
    const config = JSON.parse(configString)
    
    renderVideos(config.videos, config.vegasPath)
});
