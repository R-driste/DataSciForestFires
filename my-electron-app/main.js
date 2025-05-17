const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const { PythonShell } = require('python-shell');

let mainWindow;

app.on('ready', () => {
    mainWindow = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false,
        },
    });

    mainWindow.loadFile('index.html');
});

ipcMain.on('predict-damage', (event, inputData) => {
    const { selectedFeature, inputs } = inputData;

    const options = {
        mode: 'json',
        pythonOptions: ['-u'],
        scriptPath: __dirname,
        args: [JSON.stringify(inputs), selectedFeature],
    };

    PythonShell.run('predict.py', options, (err, results) => {
        if (err) {
            console.error(err);
            event.sender.send('prediction-result', { error: 'Prediction failed' });
        } else {
            const prediction = results[0]; // Get the prediction result
            event.sender.send('prediction-result', { prediction });
        }
    });
});