from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Replace 'your_postgres_url' with your PostgreSQL connection URL
app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{username}:{pwd}@{hostname}:{port_id}/{database}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Define your models here (User, GPC, Game, Region, ...)
class User(db.Model):
    User_ID = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(255), unique=True, nullable=False)
    Password = db.Column(db.String(255), nullable=False)
    Language = db.Column(db.String(255))
    Age = db.Column(db.Integer)
    Email_ID = db.Column(db.String(255), unique=True, nullable=False)


# GPC model
class GPC(db.Model):
    GPC_ID = db.Column(db.Integer, primary_key=True)
    GPC_Name = db.Column(db.String(255))
    Email_ID = db.Column(db.String(255))


# Game model
class Game(db.Model):
    Game_ID = db.Column(db.Integer, primary_key=True)
    Game_Name = db.Column(db.String(255))
    Price = db.Column(db.DECIMAL(10, 2))
    GPC_ID = db.Column(db.Integer, db.ForeignKey("gpc.GPC_ID"))
    Game_Release_Date = db.Column(db.DATE)
    Age_Limit = db.Column(db.Integer)
    Status = db.Column(db.String(10))


# Region model
class Region(db.Model):
    RegionID = db.Column(db.Integer, primary_key=True)
    Region_Name = db.Column(db.String(255))


# User_Region model
class User_Region(db.Model):
    RegionID = db.Column(db.Integer, db.ForeignKey("region.RegionID"), primary_key=True)
    User_Name = db.Column(db.String(255), primary_key=True)


# Game_Region model
class Game_Region(db.Model):
    RegionID = db.Column(db.Integer, db.ForeignKey("region.RegionID"), primary_key=True)
    Game_Name = db.Column(db.String(255), primary_key=True)


# UnderReview_WE model
class UnderReview_WE(db.Model):
    Status = db.Column(db.String(10), primary_key=True)


# AvailableGames model
class AvailableGames(db.Model):
    Game_ID = db.Column(db.Integer, db.ForeignKey("game.Game_ID"), primary_key=True)
    Game_Name = db.Column(db.String(255))


# Review model
class Review(db.Model):
    User_ID = db.Column(db.Integer, db.ForeignKey("user.User_ID"), primary_key=True)
    Game_ID = db.Column(db.Integer, db.ForeignKey("game.Game_ID"), primary_key=True)
    Posted_Time = db.Column(db.DATETIME)
    Edited_Time = db.Column(db.DATETIME)
    Content = db.Column(db.String(100))


# Genre model
class Genre(db.Model):
    Genre_ID = db.Column(db.Integer, primary_key=True)
    Genre_Name = db.Column(db.String(50))


# Game_Genre model
class Game_Genre(db.Model):
    Genre_ID = db.Column(db.Integer, db.ForeignKey("genre.Genre_ID"), primary_key=True)
    Game_ID = db.Column(db.Integer, db.ForeignKey("game.Game_ID"), primary_key=True)


# Language model
class Language(db.Model):
    Lang_ID = db.Column(db.Integer, primary_key=True)
    Lang_Name = db.Column(db.String(50))


# Game_Language model
class Game_Language(db.Model):
    Lang_ID = db.Column(db.Integer, db.ForeignKey("language.Lang_ID"), primary_key=True)
    Game_ID = db.Column(db.Integer, db.ForeignKey("game.Game_ID"), primary_key=True)


# Routes for user registration and login
@app.route("/register", methods=["POST"])
def register_user():
    data = request.json
    new_user = User(**data)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"}), 201


@app.route("/login", methods=["POST"])
def login_user():
    data = request.json
    username = data.get("Username")
    password = data.get("Password")
    user = User.query.filter_by(Username=username, Password=password).first()

    if user:
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401


# Routes for handling game purchases
@app.route("/purchase_game", methods=["POST"])
def purchase_game():
    data = request.json
    user_id = data.get("user_id")
    game_id = data.get("game_id")

    # Check if the user and game exist
    user = User.query.get(user_id)
    game = Game.query.get(game_id)

    if user and game:
        # Perform the purchase logic
        # Example: Add the game to the user's purchased games
        user.purchased_games.append(game)
        db.session.commit()

        return jsonify({"message": "Game purchased successfully"}), 201
    else:
        return jsonify({"message": "User or game not found"}), 404


# Route for handling game reviews
@app.route("/post_review", methods=["POST"])
def post_review():
    data = request.json
    user_id = data.get("user_id")
    game_id = data.get("game_id")
    content = data.get("content")

    # Check if the user and game exist
    user = User.query.get(user_id)
    game = Game.query.get(game_id)

    if user and game:
        # Create a new review
        new_review = Review(User_ID=user_id, Game_ID=game_id, Content=content)
        db.session.add(new_review)
        db.session.commit()

        return jsonify({"message": "Review posted successfully"}), 201
    else:
        return jsonify({"message": "User or game not found"}), 404

#get request to show all reviews of a game
@app.route("/game/<int:game_id>/reviews", methods=["GET"])
def get_game_reviews(game_id):
    game = Game.query.get(game_id)

    if game is None:
        return jsonify({"message": "Game not found"}), 404

    reviews = Review.query.filter_by(Game_ID=game_id).all()

    # Optional: You can customize the format of the reviews before returning them
    formatted_reviews = [
        {
            "user_id": review.User_ID,
            "username": User.query.get(review.User_ID).Username,
            "posted_time": str(review.Posted_Time),
            "content": review.Content,
        }
        for review in reviews
    ]

    return jsonify({"game_name": game.Game_Name, "reviews": formatted_reviews})

# Route for displaying all genres
@app.route("/genres", methods=["GET"])
def get_all_genres():
    genres = Genre.query.all()

    # Optional: You can customize the format of the genres before returning them
    formatted_genres = [{"genre_id": genre.Genre_ID, "genre_name": genre.Genre_Name} for genre in genres]

    return jsonify({"genres": formatted_genres})


# Route for showing all games of a particular genre
@app.route("/genre/<int:genre_id>/games", methods=["GET"])
def get_games_by_genre(genre_id):
    genre = Genre.query.get(genre_id)

    if genre is None:
        return jsonify({"message": "Genre not found"}), 404

    games = Game_Genre.query.filter_by(Genre_ID=genre_id).all()

    # Optional: You can customize the format of the games before returning them
    formatted_games = [
        {"game_id": game.Game_ID, "game_name": Game.query.get(game.Game_ID).Game_Name}
        for game in games
    ]

    return jsonify({"genre_name": genre.Genre_Name, "games": formatted_games})

# ... Existing code ...
if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
