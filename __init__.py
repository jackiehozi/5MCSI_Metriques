from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
                                                                                                                                       
app = Flask(__name__)                                                                                                                  
                                                                                                                                       
@app.route('/')
def hello_world():
    return render_template('hello.html') #commit7

# Nouvelle route pour la page de contact
@app.route("/contact/")
def contact():
    return render_template("contact.html")

# Nouvelle route pour afficher les données météo de Tawarano
@app.route('/tawarano/')
def meteo():
    # URL de l'API avec les données météo de Tawarano
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()  # Lire le contenu brut
    json_content = json.loads(raw_content.decode('utf-8'))  # Décoder et charger en JSON
    results = []

    # Parcourir les éléments de la liste et extraire les dates et températures
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')  # Extraction du timestamp
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15  # Conversion en °C
        results.append({'Jour': dt_value, 'temp': temp_day_value})  # Ajouter les résultats à la liste

    # Retourner les résultats sous forme de JSON
    return jsonify(results=results)


# Nouvelle route pour le rapport graphique
@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")


# Route pour afficher l'histogramme
@app.route("/histogramme/")
def histogramme():
    return render_template("histogramme.html")

  
if __name__ == "__main__":
  app.run(debug=True)
