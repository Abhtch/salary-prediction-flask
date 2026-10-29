const form = document.getElementById("predictionForm");
const resultBox = document.getElementById("result");
const statusBox = document.getElementById("status");
const salaryBox = document.getElementById("salary");
const jsonOutput = document.getElementById("jsonOutput");
const submitButton = document.getElementById("submitButton");

form.addEventListener("submit", async function (event) {
    event.preventDefault();

    resultBox.hidden = false;
    statusBox.className = "";
    statusBox.textContent = "Predicting...";
    salaryBox.textContent = "";
    jsonOutput.textContent = "";
    submitButton.disabled = true;

    const experience = Number(document.getElementById("experience").value);

    try {
        const response = await fetch("/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ experience: experience })
        });

        const data = await response.json();
        jsonOutput.textContent = JSON.stringify(data, null, 2);

        if (!response.ok) {
            statusBox.className = "error";
            statusBox.textContent = data.error || "Prediction failed.";
        } else {
            statusBox.textContent = "Prediction successful";
            salaryBox.textContent = "Predicted Salary: " +
                Number(data.predicted_salary).toLocaleString(undefined, {
                    style: "currency",
                    currency: "INR",
                    maximumFractionDigits: 2
                });
        }
    } catch (error) {
        statusBox.className = "error";
        statusBox.textContent = "Could not connect to the API. Check that Flask is running.";
    } finally {
        submitButton.disabled = false;
    }
});
