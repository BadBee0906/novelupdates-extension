from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MultiLabelBinarizer, MinMaxScaler
import numpy as np
import ast  # For safely evaluating Python literals
import re  # For cleaning slugs

app = Flask(__name__)
CORS(app)  # Allow CORS requests for browser extensions or frontend clients

# Load dataset
df = pd.read_csv('novel_data.csv')

# Add missing columns (for older versions, e.g., v0.14 or earlier)
if "novel_type" not in df.columns:
    df.insert(2, "novel_type", None)
if "cover_url" not in df.columns:
    df.insert(3, "cover_url", None)

# Rename columns to match the expected schema
df = df.rename(columns={'name': 'title', 'activity_all_time_rank': 'rank'})

# Create a 'slug' column from 'title' (lowercase, spaces -> '-', remove non-alphanumeric characters)
df['slug'] = df['title'].str.lower().str.replace(' ', '-').str.replace(r'[^a-z0-9-]', '', regex=True)

# Parse genres and tags (convert stringified lists to Python lists)
df['genres'] = df['genres'].apply(lambda x: ast.literal_eval(x) if pd.notna(x) else [])
df['tags'] = df['tags'].apply(lambda x: ast.literal_eval(x) if pd.notna(x) else [])

# Encode genres and tags
mlb = MultiLabelBinarizer()
genres_encoded = mlb.fit_transform(df['genres'])
tags_encoded = mlb.fit_transform(df['tags'])

# Normalize rating and rank values
scaler = MinMaxScaler()
ratings_scaled = scaler.fit_transform(df[['rating', 'rank']].fillna(0))

# Combine all feature vectors
features = np.hstack([genres_encoded, tags_encoded, ratings_scaled])

@app.route('/api/recommend', methods=['GET'])
def recommend():
    novel_slug = request.args.get('url')  # Novel slug (e.g., 'coiling-dragon')
    top_n = int(request.args.get('top_n', 10))  # Number of recommendations to return
    w1 = float(request.args.get('w1', 1.0))  # Weight for similarity
    w2 = float(request.args.get('w2', 0.4))  # Weight for rating
    w3 = float(request.args.get('w3', 0.3))  # Weight for rank

    # Find the novel index by slug
    try:
        idx = df.index[df['slug'] == novel_slug].tolist()[0]
    except IndexError:
        return jsonify({'recommendations': []}), 404  # Return empty if not found

    target_feature = features[idx].reshape(1, -1)

    # Compute cosine similarity between the target and all others
    sim_scores = cosine_similarity(target_feature, features)[0]
    
    # Weight similarity by rating and rank
    sim_scores = w1 * sim_scores + w2 * df['rating'] + w3 * (1 / (df['rank'] + 1))

    # Get top N most similar novels (excluding the target itself)
    indices = sim_scores.argsort()[-top_n-1:-1][::-1]
    recommendations = []
    for i in indices:
        recommendations.append({
            'url': df['slug'][i],  # Slug used for frontend linking
            'similarity': float(sim_scores[i]),
            'score': float(sim_scores[i])  # Same as similarity (for compatibility with frontend)
        })

    return jsonify({'recommendations': recommendations})

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
