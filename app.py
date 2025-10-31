from flask import Flask, request, jsonify
import io
import contextlib
import traceback

app = Flask(__name__)

# Дозволені функції для "пісочниці"
ALLOWED_BUILTINS = {
    "print": print,
    "range": range,
    "len": len,
    "int": int,
    "float": float,
    "str": str,
    "bool": bool,
}

@app.route("/run", methods=["POST"])
def run_code():
    data = request.get_json()
    code = data.get("code", "")
    inputs = data.get("inputs", [])  # Нове поле для input()
    
    input_iter = iter(inputs)
    
    # Псевдо input
    def fake_input(prompt=""):
        try:
            return next(input_iter)
        except StopIteration:
            raise Exception("Більше немає вхідних даних для input()")
    
    # Додаємо fake_input до дозволених функцій
    safe_builtins = ALLOWED_BUILTINS.copy()
    safe_builtins["input"] = fake_input

    safe_locals = {}
    output_buffer = io.StringIO()

    try:
        # Перехоплюємо вивід print
        with contextlib.redirect_stdout(output_buffer):
            exec(code, {"__builtins__": safe_builtins}, safe_locals)

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

@app.route("/status", methods=["GET"])
def status():
    return "Server is running ✅"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
