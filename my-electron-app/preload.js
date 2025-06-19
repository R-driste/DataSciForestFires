const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld("electronAPI", {
  submitVisionForm: (data) => ipcRenderer.send("submit-vision-form", data),
  submitForm: (data) => ipcRenderer.send("submit-form", data),
  onFormResult: (callback) => ipcRenderer.on("form-result", (event, result) => callback(result)),
});