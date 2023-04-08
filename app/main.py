from flask import Flask, render_template, request, jsonify
from .schemas import llm, chain
from .spaced_rep import SpacedRep

app = Flask(__name__)

@app.route("/", methods=["GET",'POST'])
def index():
    if request.method == "POST":
        user_id = request.form.get("user_input")
        prompt = request.form.get("prompt")
        response = llm.generate(chain, prompt, user_id)
        return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)


