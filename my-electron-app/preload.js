const { contextBridge, ipcRenderer } = require("electron");

contextBridge.exposeInMainWorld("electronAPI", {
  sendFormData: (data) => ipcRenderer.send("form-data", data),
});
