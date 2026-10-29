from flask import Flask, request, jsonify, render_template
import os
import pickle
import joblib

app = Flask(__name__)
MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "salary_model.pkl")


def load_model(path):
    errors = []
    try:
        return joblib.load(path)
    except Exception as exc:
        errors.append(f"joblib.load failed: {exc}")

    try:
        with open(path, "rb") as model_file:
            return pickle.load(model_file)
    except Exception as exc:
        errors.append(f"pickle.load failed: {exc}")

    raise RuntimeError(
        "Could not load salary_model.pkl. Check how the model was saved in "
        "train_model.py, then retrain/re-save it if needed. " + " | ".join(errors)
    )


if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(
        f"Model file not found: {MODEL_PATH}. Keep salary_model.pkl beside app.py."
    )

model = load_model(MODEL_PATH)


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json(silent=True) or request.form

    if "experience" not in data:
        return jsonify({"error": "Missing required field: experience"}), 400

    try:
        experience = float(data["experience"])
    except (TypeError, ValueError):
        return jsonify({"error": "experience must be a number"}), 400

    if not 0 <= experience <= 50:
        return jsonify({"error": "experience must be between 0 and 50 years"}), 400

    try:
        prediction = model.predict([[experience]])
        salary = float(prediction[0])
    except Exception as exc:
        return jsonify({
            "error": "Prediction failed. Confirm the model was trained using years of experience as its input feature.",
            "details": str(exc)
        }), 500

    return jsonify({
        "experience": experience,
        "predicted_salary": round(salary, 2),
        "currency": "INR",
        "message": "Salary prediction generated successfully"
    })


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
