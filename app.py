from flask import Flask, render_template, request, jsonify, Response
from database import (
    check_and_create_database,
    get_topics,
    get_story_elements,
    get_quiz_data,
)
from story_generator import generate_story

app = Flask(__name__)


@app.route("/")
def index():
    check_and_create_database()
    story_topics, learn_topics = get_topics()
    return render_template(
        "index.html", story_topics=story_topics, learn_topics=learn_topics
    )


@app.route("/generate_adventure", methods=["GET"])
def generate_adventure():
    story_topic = request.args.get("story_topic")
    learn_topic = request.args.get("learn_topic")

    story_elements = get_story_elements(story_topic)
    quiz_data = get_quiz_data(learn_topic)

    def generate():
        yield "data: Starting story...\n\n"
        for chunk in generate_story(story_elements, quiz_data):
            if chunk:
                yield f"data: {chunk}\n\n"
        yield "data: [DONE]\n\n"

    return Response(
        generate(),
        mimetype="text/event-stream",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive"},
    )


if __name__ == "__main__":
    app.run(debug=True)
