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
    let i = 0;
    await asyncForEach(videos, async (video) => {
        i++;
        console.info('Video ' + i + '/' + videos.length)
        return await renderVideo(video, vegasPath)
    })
}

/**
 * @param {Video} video 
 * @param {string} vegasPath
 */
async function renderVideo(video, vegasPath) {
    console.info('Rendering ' + video.outputFilePath + '...')
    return await new Promise((resolve, reject) => {
        fs.writeFile(
            './tmp.csv',
            video.projectFilePath + ';' + video.rendererName + ';' + video.templateName + ';' + video.outputFilePath,
            (err) => {
                if (err) {
                    reject(err)
                }

                const command = '"' + vegasPath + '" -SCRIPT:"' + __dirname + '\\RenderProject\\RenderProject\\Class1.cs"'
                const startRender = exec(command)
                startRender.addListener('exit', (code) => {
                    console.info(video.outputFilePath + ' rendered !')
                    console.info('')
                    resolve(code)
                })
            }
        )
    });
}

fs.readFile('./config.json', 'utf8', async (err, configString) => {
    if (err) {
        throw 'Config File Missing : ' + err
    }

    /** @var {Config} */
    const config = JSON.parse(configString)
    
    await renderVideos(config.videos, config.vegasPath)
    process.exit(0)
});
