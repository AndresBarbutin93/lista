from flask import Flask, render_template, request
import json, os

app = Flask(__name__)

DATA_FILE = "data.json"

# Restricciones ocultas
RESTRICCIONES = {
    "3137974506": ["3223392581", "3054051090", "3024142708"],
    "3223392581": ["3137974506"],
    "3054051090": ["3137974506"],
    "3024142708": ["3137974506"]
}

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    else:
        return {"usuarios": {}, "numeros": []}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

@app.route("/", methods=["GET", "POST"])
def index():
    mensaje = None
    asignacion = None
    if request.method == "POST":
        celular = request.form.get("celular")
        data = load_data()

        if celular in data["usuarios"]:
            asignacion = data["usuarios"][celular]
            mensaje = "Ya tienes un número asignado."
        else:
            # Buscar número libre que respete las restricciones
            libre = None
            for n in data["numeros"]:
                if not n["asignado"]:
                    # Revisar restricciones
                    if celular in RESTRICCIONES and n["numero"] in RESTRICCIONES[celular]:
                        continue
                    if n["numero"] in RESTRICCIONES and celular in RESTRICCIONES[n["numero"]]:
                        continue
                    libre = n
                    break
            if libre:
                libre["asignado"] = True
                data["usuarios"][celular] = libre
                save_data(data)
                asignacion = libre
                mensaje = "¡Se te asignó un número!"
            else:
                mensaje = "No hay números disponibles."

    return render_template("index.html", mensaje=mensaje, asignacion=asignacion)

if __name__ == "__main__":
    app.run()
