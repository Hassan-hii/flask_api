from flask import Flask, jsonify, request
import pickle
import pandas as pd
import numpy as np

app = Flask(__name__)

# Load pickled data
# Open the file using 'with' statement
with open('popular1.pkl', 'rb') as f:
    popular_df = pd.read_pickle(f)
with open('pt1.pkl', 'rb') as fi:
    pt = pd.read_pickle(fi)
with open('banquet.pkl', 'rb') as fil:
    banquets = pd.read_pickle(fil)
with open('similarity_scores1.pkl', 'rb') as file:
    similarity_scores = pd.read_pickle(file)
# Define a route to get recommendations
@app.route('/recommend/<string:n>',methods=['GET'])
def recommend(n):
    # Get user input from request
   

    # Perform recommendation logic
    if n not in pt.index:
       return "Banquet not found in the index"

    index = np.where(pt.index == n)[0][0]
    similar_items = sorted(enumerate(similarity_scores[index]), key=lambda x: x[1], reverse=True)[1:5]

    data = []
    for i in similar_items:
        item = []
        temp_df = banquets[banquets['Hall-Name'] == pt.index[i[0]]]
        item.extend(temp_df.drop_duplicates('Hall-Name')['Hall-Name'].values)
        item.extend(temp_df.drop_duplicates('Hall-Name')['Address'].values)
        item.extend(temp_df.drop_duplicates('Hall-Name')['Contact'].values)
        item.extend(temp_df.drop_duplicates('Hall-Name')['Rating'].values)
        item.extend(temp_df.drop_duplicates('Hall-Name')['Jn12ke src'].values)
        data.append(item)

    return jsonify({'recommendations': data})

if __name__ == "__main__":
    app.run(debug=True)
