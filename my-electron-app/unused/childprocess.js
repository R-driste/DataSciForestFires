const { ipcMain } = require("electron")
const { spawn } = require("child_process") //get spawn function
const path = require("path") //handle file system paths

function runPyScript(input_features, modelscriptpath){
    return new Promise((resolve, reject) => { //wait for asynch process
        const process = spawn("python", [modelscriptpath]) //create child

        let out = ""
        let error = ""

        process.stdout.on("data", (data) => { //get incoming information
            output += data.toString();
        });

        process.stderr.on("data", (data) => { //catch warnings
            errorOutput += data.toString();
        });

        process.on("close", (code) => { //handling script exit
            if (code !== 0) {
                reject(new Error(`Python exited with code ${code}: ${errorOutput}`));
            } else {
                try {
                const parsed = JSON.parse(output);
                resolve(parsed.prediction);
                } catch (e) {
                reject(new Error(`Failed to parse JSON: ${e.message}`));
                }
            }
        });

        process.stdin.write(JSON.stringify({input_features})); //sending data
        process.stdin.end();

    });
}

//test
runPython([5.1, 3.5, 1.4, 0.2])
  .then(prediction => {
    console.log("Prediction:", prediction);
  })
  .catch(console.error);