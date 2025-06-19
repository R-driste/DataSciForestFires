const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const { PythonShell } = require('python-shell');
const fs = require('fs');
const { dialog } = require('electron');

let mainWindow;
let result = 7;

let categories = ['Damaged (1-50%)', 'Destroyed (>50%)', 'No Damage'];
let significance = ["Your home typically had a lower risk of damage ranging from 1-50%. Make sure to stay prepared for future fires.",
    "Historically, homes like this have been prone to get significantly damaged >50%. It is not 100% determined your house will be destroyed, but it is statistically more likely.",
    "Your home is statistically likely to not get damaged at all, but this is not a guarantee so still prepare for the worst."];

app.on("ready", () => {
    mainWindow = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            preload: path.join(__dirname, "preload.js"),
            contextIsolation: true,
            nodeIntegration: false
        }
    });
    mainWindow.loadFile("index.html");
});

ipcMain.on("submit-form", (event, formData) => {
    console.log("Classification Running!");

    const options = {
        mode: "json",
        pythonOptions: ["-u"],
        scriptPath: path.join(__dirname),
    };

    const pyshell = new PythonShell("class.py", options);
    pyshell.send(formData);

    pyshell.on("message", (message) => {
        const prediction = message.prediction;
        const explanation = message.explanation || "No explanation provided";

        dialog.showMessageBox(mainWindow, {
            type: 'info',
            title: 'Prediction Result',
            message: `Prediction: ${categories[prediction]}\nExplanation: ${significance[prediction]}`,
        });

        event.sender.send("form-result", { prediction });
        result = prediction;
    });

    pyshell.end((err) => {
        if (err) {
            console.error("Python error:", err);
            event.sender.send("form-result", { error: "Prediction failed" });
        }
    });
});

ipcMain.on("submit-vision-form", (event, formData) => {
    console.log("Vision Running!");

    //choose correct script based on image type selected
    let scriptName = "vision.py";
    if (formData.imageType && formData.imageType.toLowerCase().includes("satellite")) {
        scriptName = "vision2.py";
    }

    const options = {
        mode: "json",
        pythonOptions: ["-u"],
        scriptPath: path.join(__dirname),
    };

    const pyshell = new PythonShell(scriptName, options);

    pyshell.send(formData);

    pyshell.on("message", (message) => {
        const prediction = message.prediction;
        const explanation = message.explanation;

        dialog.showMessageBox(mainWindow, {
            type: 'info',
            title: 'Vision Model Result',
            message: `Prediction: ${prediction}\nExplanation: ${explanation}`,
        });
        event.sender.send("form-result", { prediction });
    });

    pyshell.end((err) => {
        if (err) {
            console.error("Python error:", err);
            event.sender.send("form-result", { error: "Vision prediction failed" });
        }
    });
});
