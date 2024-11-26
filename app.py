# -*- coding: utf-8 -*-

from flask import Flask, render_template, request

# Initialize Flask app
app = Flask(__name__)

# Define point values
POINTS = {
    "textbook": 40,
    "mid_book": 20,
    "normal_book": 10,
    "degree": 40,
    "published_work": 40,
    "unique_activity": 20,
    "journal_article": 5,
    "movie_game": 2.5
}

# Badge thresholds
BADGE_LEVELS = {
    "Platinum": "Requires unique contribution or 2+ years of consistent engagement.",
    "Gold": 90,
    "Silver": 60,
    "Bronze": 40
}

def calculate_points(details):
    total = 0

    # Calculate book points (including journal articles) and apply cap
    book_points = (
        POINTS["textbook"] * details.get("textbook", 0) +
        POINTS["mid_book"] * details.get("mid_book", 0) +
        POINTS["normal_book"] * details.get("normal_book", 0) +
        POINTS["journal_article"] * details.get("journal_article", 0)
    )
    book_points = min(book_points, 75)

    # Calculate movie/game points and apply cap
    movie_points = POINTS["movie_game"] * details.get("movie_game", 0)
    movie_points = min(movie_points, 10)

    # Assign points for unique activity (True/False)
    unique_activity_points = POINTS["unique_activity"] if details.get("unique_activity", False) else 0

    # Add other points
    for category, count in details.items():
        if category not in ["textbook", "mid_book", "normal_book", "movie_game", "unique_activity", "journal_article"]:
            total += POINTS.get(category, 0) * count

    # Add capped book, movie, and unique activity points
    total += book_points + movie_points + unique_activity_points

    return total

def determine_badge(points, platinum_criteria=False):
    if platinum_criteria:
        return "Platinum"
    elif points >= BADGE_LEVELS["Gold"]:
        return "Gold"
    elif points >= BADGE_LEVELS["Silver"]:
        return "Silver"
    elif points >= BADGE_LEVELS["Bronze"]:
        return "Bronze"
    else:
        return "No Badge"

@app.route("/", methods=["GET", "POST"])
def badge_form():
    if request.method == "POST":
        # Get data from form
        user_details = {
            "textbook": int(request.form.get("textbook", 0)),
            "mid_book": int(request.form.get("mid_book", 0)),
            "normal_book": int(request.form.get("normal_book", 0)),
            "degree": int(request.form.get("degree", 0)),
            "published_work": int(request.form.get("published_work", 0)),
            "unique_activity": request.form.get("unique_activity") == "on",
            "journal_article": int(request.form.get("journal_article", 0)),
            "movie_game": int(request.form.get("movie_game", 0))
        }
        platinum_criteria = request.form.get("platinum_criteria") == "on"

        # Calculate points and badge
        total_points = calculate_points(user_details)
        badge = determine_badge(total_points, platinum_criteria)

        return render_template("result.html", points=total_points, badge=badge)

    return render_template("form.html")

if __name__ == "__main__":
    app.run(debug=True)

