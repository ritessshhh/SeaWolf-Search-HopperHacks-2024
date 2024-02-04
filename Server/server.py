from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from flask import Flask, request, jsonify, render_template
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
from werkzeug.utils import secure_filename
from flask_cors import CORS
import json
from flask import Flask, send_from_directory
import os
import tempfile

UPLOADS_FOLDER = os.path.join(os.getcwd(), 'uploaded_images')

app = Flask(__name__, static_url_path='', static_folder='uploaded_images')
CORS(app)

vectorizer = TfidfVectorizer()

# Initialize the BLIP model
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

# In-memory data storage
lost_items = {}  # This will store details about lost items
images_with_captions = {}  # This will store images' captions by image ID
next_id = 15 # Simple counter to act as ID

@app.route('/uploaded_images/<path:filename>')
def serve_image(filename):
    return send_from_directory(app.static_folder, filename)


def update_vectorizer():
    """Update the vectorizer based on current lost_items descriptions."""
    global vectorizer
    if lost_items:
        descriptions = [item['caption'] for item in lost_items.values()]
        vectorizer = TfidfVectorizer(ngram_range=(1, 2))  # Use bi-grams
        vectorizer.fit(descriptions)


def get_cosine_similarity(new_text):
    """Calculate cosine similarity of new_text against all lost item descriptions."""
    if not lost_items:  # Handle case with no items
        return []

    # Transform new text and all descriptions to vectors
    descriptions = [item['caption'] for item in lost_items.values()]
    all_vectors = vectorizer.transform(descriptions + [new_text])

    # Cosine similarity between new_text vector and all description vectors
    cos_sim = cosine_similarity(all_vectors[-1:], all_vectors[:-1]).flatten()

    return cos_sim

def generate_caption(image_bytes):
    with open(image_bytes, 'rb') as file:
        img = Image.open(file).convert('RGB')
        inputs = processor(img, return_tensors="pt").to("cpu")
        outputs = model.generate(**inputs)
        caption = processor.decode(outputs[0], skip_special_tokens=True)
        return caption


@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image provided"}), 400

    # Retrieve the image from the request
    image_file = request.files['image']
    if image_file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Save the uploaded image to a temporary file
    temp_dir = tempfile.gettempdir()  # Get the system temporary directory
    temp_filename = secure_filename(image_file.filename)
    temp_path = os.path.join(temp_dir, temp_filename)
    image_file.save(temp_path)

    try:
        # Generate caption for the saved image file
        caption = generate_caption(temp_path)
        print(caption)

        global next_id, images_with_captions, lost_items
        # Simulated logic for handling the uploaded image and caption
        image_id = next_id
        next_id += 1

        # Store the caption and image path in images_with_captions dictionary
        images_with_captions[image_id] = {"caption": caption, "image_path": temp_path}

        # Update the TF-IDF vectorizer and calculate cosine similarity
        update_vectorizer()  # Make sure the vectorizer is updated with current lost_items descriptions
        cos_sim = get_cosine_similarity(caption)

        # Find matches based on cosine similarity
        threshold = 0.2  # Define a threshold for similarity
        matches = [item_id for item_id, similarity in enumerate(cos_sim) if similarity > threshold]

    finally:
        # Clean up: Remove the temporary file after processing
        if os.path.exists(temp_path):
            os.remove(temp_path)

    # After finding matches based on cosine similarity
    matched_items = []
    for item_id in matches:
        if str(item_id + 1) in lost_items:  # Adjusting item_id to match the keys in lost_items
            matched_item = lost_items[str(item_id + 1)]  # Fetching the lost item details
            matched_items.append({
                "id": item_id + 1,
                "image_path": matched_item["image_path"],
                "contact": matched_item["contact"]
            })

    # Include matched_items in the response instead of just match IDs
    print(matched_items)
    return jsonify({"matches": matched_items}), 200

    # if matches:
    #     return jsonify({"matches": matches}), 200
    # else:
    #     return jsonify({"message": "No matches found"}), 404

def find_similar_captions(input_text):
    """Find lost items with descriptions similar to input_text."""
    update_vectorizer()  # Ensure vectorizer is up-to-date
    cos_sim = get_cosine_similarity(input_text)

    matches = []
    for index, similarity in enumerate(cos_sim):
        if similarity > 0.2:
            item_id = list(lost_items.keys())[index]
            item = lost_items[item_id]
            matches.append({
                "id": item_id,
                "contact": item["contact"],
                "image_path": item["image_path"]
            })

    return matches



@app.route('/find_matches', methods=['POST'])
def find_matches():
    input_text = request.json.get('text', '')
    print(input_text)
    if not input_text:
        return jsonify({"error": "Text input is required"}), 400

    matches = find_similar_captions(input_text)
    print(matches)
    # Instead of just printing matches, format them for JSON response
    if matches:
        return jsonify({"matches": matches}), 200
    else:
        return jsonify({"message": "No matches found"}), 404



@app.route('/add_lost_item', methods=['POST'])
def add_lost_item():
    global next_id
    # Ensure both an image and the required text fields are provided
    if 'image' not in request.files or 'title' not in request.form or 'contact' not in request.form:
        return jsonify({"error": "Missing data"}), 400

    image_file = request.files['image']
    title = request.form['title']
    contact = request.form['contact']

    # Define a directory for saving images
    temp = 'uploaded_images'
    os.makedirs(temp, exist_ok=True)  # Ensure the directory exists

    # Save the uploaded image to a file
    if image_file:
        filename = secure_filename(image_file.filename).replace('\0', '')
        temp_path = os.path.join(temp, filename)  # Save under a directory
        image_file.save(temp_path)

        # Generate the caption (assuming generate_caption works with file paths)
        caption = generate_caption(temp_path)

        # Store relative path instead of absolute to improve security and portability
        image_rel_path = os.path.join(temp, filename)
    else:
        caption = "No image provided."
        image_rel_path = None  # No image path to store

    lost_item_id = next_id
    lost_items[lost_item_id] = {
        "title": title,
        "contact": contact,
        "caption": caption,
        "image_path": image_rel_path,  # Store the relative path
        "status": "lost"
    }
    next_id += 1

    update_vectorizer()

    # Update the JSON file
    with open("lost_items.json", "w") as file:
        json.dump(lost_items, file, indent=4)

    return jsonify({"message": "Lost item added successfully", "item_id": lost_item_id}), 201




@app.route('/items', methods=['GET'])
def list_items():
    # Convert the dictionary to a list of items for display
    items_list = [{"id": k, **v} for k, v in lost_items.items()]
    return jsonify(items_list), 200


if __name__ == '__main__':
    # Load lost_items from JSON or database (if applicable)
    try:
        with open("lost_items.json", "r") as file:
            lost_items = json.load(file)
    except FileNotFoundError:
        lost_items = {}

    update_vectorizer()

    app.run(debug=True, port=8000)
