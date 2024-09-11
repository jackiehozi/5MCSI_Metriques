import requests
import json
from flask import Flask, render_template, jsonify
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('hello.html')  # commit8

# Nouvelle route pour la page de contact
@app.route("/contact/")
def contact():
    return render_template("contact.html")

# Nouvelle route pour afficher les données météo de Tawarano
@app.route('/tawarano/')
def meteo():
    response = requests.get('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    json_content = response.json()  # Décoder et charger en JSON
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

@app.route('/commits/')
def commits():
    response = requests.get('https://api.github.com/repos/jackiehozi/5MCSI_Metriques/commits')
    commits_data = response.json()
    
    # Extraire les minutes des commits
    commit_minutes = {}
    for commit in commits_data:
        commit_time = commit['commit']['author']['date']
        date_object = datetime.strptime(commit_time, '%Y-%m-%dT%H:%M:%SZ')
        minute = date_object.minute
        commit_minutes[minute] = commit_minutes.get(minute, 0) + 1
    
    # Préparer les données pour le graphique
    results = [{'minute': minute, 'count': count} for minute, count in sorted(commit_minutes.items())]
    return jsonify(results=results)

if __name__ == "__main__":
    app.run(debug=True)
