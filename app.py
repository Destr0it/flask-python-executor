from flask import Flask, request, jsonify
import io
import contextlib
import traceback

app = Flask(__name__)

@app.route("/run", methods=["POST"])
def run_code():
    data = request.get_json()

    # Отримуємо код від гравця
    code = data.get("code", "")

    # Підготуємо "пісочницю" — окремий простір для виконання
    safe_locals = {}

    # Перехоплюємо весь текстовий вивід
    output_buffer = io.StringIO()

    try:
        with contextlib.redirect_stdout(output_buffer):
            exec(code, {"__builtins__": {}}, safe_locals)

        result = output_buffer.getvalue()
        if result.strip() == "":
            result = "✅ Код виконано без помилок"

        return jsonify({"output": result})

    except Exception:
        error_text = traceback.format_exc()
        return jsonify({"error": error_text}), 400


@app.route("/", methods=["GET"])
def index():
    return "Flask Python Executor — працює! 🚀"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
