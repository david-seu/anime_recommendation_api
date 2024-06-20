import faiss
import numpy as np
import pandas as pd
from flask import Blueprint, jsonify, request

# Load your data
df = pd.read_json('./similarity.json').astype('float32')
anime = pd.read_json('./anime-database.json')  # Assuming you have a separate JSON for anime metadata

# Ensure the array is C-contiguous
data_array = np.ascontiguousarray(df.values)

# Normalize the data
faiss.normalize_L2(data_array)

# Create the Faiss index
faiss_index = faiss.IndexFlatIP(data_array.shape[1])  # IP for inner product, use L2 for Euclidean distance
faiss_index.add(data_array)


def give_recommendations(index_value, data=anime):
    D, I = faiss_index.search(data_array[index_value].reshape(1, -1),
                              6)  # Search for 5 most similar items (excluding itself)
    index_recomm = I[0][1:]  # Exclude the first one since it's the same item
    anime_recomm = data['title'].iloc[index_recomm].values
    result = anime_recomm.tolist()
    return result


app = Blueprint('anime', __name__)


@app.route('/recommend', methods=['GET'])
def recommend():
    title = request.args.get('title')
    if title is None:
        return jsonify({'error': 'Title parameter is required'}), 400

    try:
        index = anime[anime['title'] == title].index[0]
    except IndexError:
        return jsonify({'error': 'Anime not found'}), 404

    recommendations = give_recommendations(index)
    return jsonify(recommendations)
