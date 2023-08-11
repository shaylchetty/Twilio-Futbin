from flask import Flask, render_template, request
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
from twilio.rest import Client

import sqlite3

app = Flask(__name__)
CORS(app)

# Set up the SQLite database connection


def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


# Create the database and players table if they don't exist


def create_database():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            score INTEGER
        )
    """
    )
    conn.commit()
    conn.close()


@app.route("/")
def home():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM players")
    players = cursor.fetchall()
    conn.close()
    return render_template("index.html", players=players)


@app.route("/update_score", methods=["GET", "POST"])
def update_score():
    if request.method == "POST" or request.method == "GET":
        scrapedarr = scrape()

        conn = get_db_connection()
        cursor = conn.cursor()

        for username, score in scrapedarr:
            # Check if the player already exists in the database
            cursor.execute("SELECT * FROM players WHERE username = ?", (username,))
            player = cursor.fetchone()

            if player is None:
                # Player does not exist, insert a new record
                cursor.execute(
                    "INSERT INTO players (username, score) VALUES (?, ?)",
                    (username, score),
                )
            else:
                db_score = player[
                    "score"
                ]  # Get the score from the retrieved player record
                print(username)
                print(score, db_score)
                if score != db_score:
                    message(f"{username}, {score}")
                    cursor.execute(
                        "UPDATE players SET score = ? WHERE username = ?",
                        (score, username),
                    )

        conn.commit()
        conn.close()

        return "Score updated successfully"


def message(content):
    account_sid = "ACb195434a2b3543eb1e7dfcca6ee4af3f"

    auth_token = "4e104623e4aa561756804e1e366091fd"

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=content,
        from_="+18668721725",  # Your Twilio phone number
        to="+14845027144",  # Your phone number
    )


def scrape():
    arr = []

    # Send a GET request to the Futbin popular page with headers
    url = "https://www.futbin.com/popular"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    }
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Create a BeautifulSoup object with the HTML content
        soup = BeautifulSoup(response.content, "html.parser")

        # Find the <ul> element that contains the player names
        player_list = soup.find("ul", {"class": "inline px-0"})

        # Find all <li> elements within the <ul> element
        player_names = player_list.find_all("li")

        # Extract the player names and additional information
        for player_name in player_names:
            # Find the nested divs to extract additional information
            divs = player_name.find_all("div", {"class": "pcdisplay-name"})
            spans = player_name.find_all(
                "span", {"class": "ut23 flat-price-ui ps_main_price"}
            )

            # Extract the player name from the div
            player_name_text = divs[0].get_text(strip=True)

            # Extract the player price from the span
            player_price_text = spans[0].get_text(strip=True)

            arr.append((player_name_text, player_price_text))

    else:
        print("Failed to retrieve the page. Status code:", response.status_code)

    return arr[:3]


if __name__ == "__main__":
    create_database()
    app.run(debug=True)
