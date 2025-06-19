//upon form submission for pre damage pred
document.getElementById("fire-risk-form").addEventListener("submit", async function (e) {
  e.preventDefault();

  const formData = new FormData(e.target);
  const json = {};

  for (let [key, value] of formData.entries()) {
    json[key] = value;
  }

  const response = await fetch("/predict", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(json)
  });

  const result = await response.json();
  alert("Risk Prediction: " + result.prediction);
});
