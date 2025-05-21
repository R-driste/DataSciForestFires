document.getElementById("fire-risk-form").addEventListener("submit", function (event) {
  event.preventDefault();

  const formData = new FormData(event.target);
  const jsonObject = {};

  for (const [key, value] of formData.entries()) {
    jsonObject[key] = value;
  }

  const jsonString = JSON.stringify(jsonObject, null, 2);
  console.log("Submitted JSON:", jsonString);

  // Create a downloadable file
  const blob = new Blob([jsonString], { type: "application/json" });
  const url = URL.createObjectURL(blob);

  const a = document.createElement("a");
  a.href = url;
  a.download = "fire-risk-data.json";
  a.click();

  URL.revokeObjectURL(url);
});
