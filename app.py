from flask import Flask, render_template, request, redirect, url_for
from main import get_random_video_id
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        channel_name = request.form.get("channel_name")
        random_video_id = get_random_video_id(channel_name)
        if random_video_id:
            video_url = f"https://www.youtube.com/watch?v={random_video_id}"
            return render_template('result.html', channel_name=channel_name, random_video_id=random_video_id,
                                   video_url=video_url)
        else:
            error_message = f"No videos found for the channel '{channel_name}'."
            return render_template('result.html', error_message=error_message)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
