# Web server to check uncheck files we don't want to use, and export it as json
import os
import json
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename



#read json file
with open("results.json", "r") as f:
    results = json.load(f)

# Create Flask app
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html", results=results)

@app.route("/export", methods=["POST"])
def export():
    # Get each checkbox value
    for lemma in results:
        results[lemma]["checked"] = request.form.get(f"checkbox_{lemma}", False)



    # Create new dictionary with only checked results
    new_results = {}
    for lemma in results:
        if results[lemma]["checked"]:
            new_results[lemma] = results[lemma]
    # Save new dictionary to JSON file
    with open("new_results.json", "w") as f:
        json.dump(new_results, f)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
    