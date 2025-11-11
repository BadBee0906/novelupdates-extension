# A browser extension for novelupdates

A browser extension that adds a recommendation series and description for recommendation Lists.

## Demo
![Demo](image.png)

## Installation

## How to Test
1. Download and unzip the extension folder.
2. Install Python dependencies: `pip install -r requirements.txt`.
3. Run the backend: `python app.py` (starts at http://localhost:5000).
4. Load the extension in Chrome (`chrome://extensions/ > Load unpacked`).
5. Visit a NovelUpdates series page (e.g., https://www.novelupdates.com/series/coiling-dragon/).
6. Check the "Recommendations (AI)" section—should load from local backend.
7. Use the popup to adjust parameters (Top N, etc.) and save.

## Usage

Go to a novel page on [novelupdates.com](https://www.novelupdates.com/series/lord-of-the-mysteries/)
You should see a new section called `Recommendations (AI)` below the `Related Series` section.

## Advanced Usage

Click on the extension icon, and you will see a popup with the following options:

- Top N: Number of recommendations to show
- Similarity: How much similarity you want to consider
- Rating: If you want to consider the rating
- Rank: If you want to consider the rank
- Save: Save the settings

**NOTE**: You can set the rating and rank to `0` if you only want to consider similar novels.

## About

This is a small project created mainly to learn about Chrome extensions and recommendation systems. The recommendation system is a simple content-based system that uses the novel's description, genres, tags, rating, and rank to find similar novels. The similarity is calculated using cosine similarity. The recommendation system is running on [pythonanywhere](https://www.pythonanywhere.com/), and the extension is using a simple REST API to get the recommendations. Please note that since I'm using the free tier of Pythonanywhere, the API might be slow at times.
