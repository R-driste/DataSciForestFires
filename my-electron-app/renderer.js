const { ipcRenderer } = require('electron');

document.getElementById('submitButton').addEventListener('click', () => {
    const selectedFeature = document.getElementById('selectedFeature').value;

    const inputs = {
        homesBurnt: parseInt(document.getElementById('homesBurnt').value),
        injuries: parseInt(document.getElementById('injuries').value),
        businessesDestroyed: parseInt(document.getElementById('businessesDestroyed').value),
        vehiclesDamaged: parseInt(document.getElementById('vehiclesDamaged').value),
        areaBurned: parseInt(document.getElementById('areaBurned').value),
    };

    ipcRenderer.send('predict-damage', { selectedFeature, inputs });
});

ipcRenderer.on('prediction-result', (event, result) => {
    if (result.error) {
        document.getElementById('result').innerText = `Error: ${result.error}`;
    } else {
        document.getElementById('result').innerText = `Predicted Value for Selected Feature: ${result.prediction}`;
    }
});

const selectedFeatureDropdown = document.getElementById('selectedFeature');
const inputFields = document.querySelectorAll('input[type="number"]');

selectedFeatureDropdown.addEventListener('change', () => {
    inputFields.forEach(input => input.disabled = false);
    const selectedFeature = selectedFeatureDropdown.value;
    const targetInput = document.getElementById(selectedFeature);
    if (targetInput) {
        targetInput.disabled = true;
    }
});

selectedFeatureDropdown.dispatchEvent(new Event('change'));