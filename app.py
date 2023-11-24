from flask import Flask, request, render_template, send_file
import requests
from bs4 import BeautifulSoup
import os
import uuid

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/scrape", methods=["POST"])
def scrape():
    url = request.form["url"]

    if not url.strip():  # Check if the URL is empty or contains only whitespace
        return "Please provide a valid URL."

    # Generate a unique filename for the scraped data
    filename = str(uuid.uuid4()) + "_scraped_data.txt"
    filepath = os.path.join(app.root_path, filename)

    # Perform web scraping
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        text_data = soup.get_text()

        # Save scraped data to a text file with a unique filename
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(text_data)

        # Send the file for download
        return send_file(filepath, as_attachment=True)

    except Exception as e:
        return str(e)

    finally:
        # Delete the temporary file after it's been sent for download
        if os.path.exists(filepath):
            os.remove(filepath)


if __name__ == "__main__":
    app.run(debug=True)
