import os
from flask import Flask, render_template, request, send_from_directory, jsonify

app = Flask(__name__)

folder = "/home/scollins/motion_images"


@app.route("/images/<path:filename>")
def serve_image(filename):
    """Serve an image from the folder"""
    return send_from_directory(folder, filename)


def get_images(page=1, per_page=10):
    extensions = (".png", ".jpg", ".jpeg", ".gif", ".bmp")
    files = sorted([f for f in os.listdir(folder) if f.lower().endswith(extensions)], reverse=True)
    if not files:
        return []
    page = max(1, page)
    start = (page - 1) * per_page
    end = start + per_page
    return files[start:end]



def delete_image(filename):
    """Delete an image"""
    file_path = os.path.join(folder, filename)
    if os.path.exists(file_path):
        os.remove(file_path)


@app.route("/")
def index():
    """Render the images"""
    global folder
    page = int(request.args.get("page", 1))
    total_pages = (len(os.listdir(folder)) + 9) // 10
    images = get_images(page=page)
    selected_image = images[0] if images else ""
    return render_template("index.html", folder=folder, images=images, page=page, total_pages=total_pages, selected_image=selected_image)


@app.route("/delete/<path:filename>", methods=["DELETE"])
def delete(filename):
    """Handle image deletion"""
    delete_image(filename)
    return jsonify({"status": "success"}), 200


if __name__ == "__main__":
    app.run(debug=True)