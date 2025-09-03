from flask import Flask, render_template, request, jsonify

import algo_las 

import pandas as pd
import io

app = Flask(__name__)


## Gilles LAS
@app.route("/correctionlas")
def grilleLAS():
    return render_template("grillelas.html")

@app.route("/las-count-qcm", methods=["POST"])
def lascountqcm():
    file = request.files.get("reponses")
    if not file:
        return jsonify({"error": "Pas de fichier donnée"}), 500
    try:
        # extraire les donnés du doc envoyé par iostream
        filedata = file.stream.read()
        filestream = io.StringIO(filedata.decode("UTF8"), newline=None)
        data = pd.read_csv(filestream)
        
        # compter nombres QCM
        n_qcm = (data.shape[1] - algo_las.n_info_cols)/6

        filestream.close()
        file.close()

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({'rows': n_qcm})

@app.route("/las-calc-note", methods=["POST"])
def lascalcnotes():
    try: 
        file = request.files.get("reponses")
        shs = True if request.form.get("shs") == "true" else False
        answers = request.form.get("answerlist").split(",")
    except Exception as e:
        return jsonify({"error": f"Non possible de lire POST : {e}"}), 500

    try:
        # extraire les donnés du doc envoyé par iostream
        filedata = file.stream.read()
        filestream = io.StringIO(filedata.decode("UTF8"), newline=None)
        data = pd.read_csv(filestream)
    except Exception as e :
        return jsonify({"error": f"Non possible de passer en filestream : {e}"}), 500
    
    try:
        output = algo_las.calculate_grade(data, answers, shs)
    except Exception as e:
        return jsonify({"error": f"Non possible de générer output : {e}"}), 500

    return jsonify({"output": output})
    


@app.route("/")
def homescreen():
    return render_template("grillelas.html")

if __name__ == "__main__":
    app.run(debug=True)