from flask import Flask,jsonify,render_template,request
import pickle
import pandas as pd
import pandas as pd
import numpy as np

# Open the file using 'with' statement
with open('popular1.pkl', 'rb') as f:
    popular_df = pd.read_pickle(f)
with open('pt1.pkl', 'rb') as fi:
    pt = pd.read_pickle(fi)
with open('banquet.pkl', 'rb') as fil:
    banquets = pd.read_pickle(fil)
with open('similarity_scores1.pkl', 'rb') as file:
    similarity_scores = pd.read_pickle(file)


app = Flask(__name__)

@app.route('/')
def index():
    return render_template(
        'index.html',
        banquet_img=list(popular_df['Jn12ke src'].values),
        banquet_name=list(popular_df['Hall-Name'].values),
        banquet_reviews=list(popular_df['num_ratings'].values),
        banquet_rating=list(popular_df['Rating_x'].values),
        

    )
@app.route('/recommend')
def recommend_ui():
    return render_template(

        'Recommend.html'
    )

@app.route('/banquet',methods=['post'])
def recommend(): 
    user_input=request.form.get('user-input')

    if user_input not in pt.index:
        return "Banquet not found in the index"

    index = np.where(pt.index ==user_input)[0][0]
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

    print(data)
 
    return jsonify({'recommendations': data})
    

if __name__=="__main__":
    app.run(debug=True)
  
 