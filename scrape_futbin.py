import requests
from bs4 import BeautifulSoup

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

        # Print the player name and price
        print(f"Player Name: {player_name_text}")
        print(f"Player Price: {player_price_text}")
        print()
else:
    print("Failed to retrieve the page. Status code:", response.status_code)
