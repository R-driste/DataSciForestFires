document.getElementById("fire-risk-form").addEventListener("submit", (e) => {
  e.preventDefault();

  const formData = {
    assessed_value: parseFloat(document.querySelector('[name="assessed_value"]').value),
    year_built: parseInt(document.querySelector('[name="year_built"]').value),
    latitude: parseFloat(document.querySelector('[name="latitude"]').value),
    longitude: parseFloat(document.querySelector('[name="longitude"]').value),
    x: parseFloat(document.querySelector('[name="x"]').value),
    y: parseFloat(document.querySelector('[name="y"]').value),
    distance_utility: parseFloat(document.querySelector('[name="distance_utility"]').value)
  };

  window.electronAPI.sendFormData(formData);
});
