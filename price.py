import requests
from bs4 import BeautifulSoup

url = "https://www.futbin.com/23/player/53762/sadio-mane"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
}

response = requests.get(url, headers=headers)


if response.status_code == 200:
    soup = BeautifulSoup(response.content, "html.parser")

    span_element = soup.find("span", {"id": "ps-lowest-1"})

    data_price = span_element.get("data-price")

else:
    print("Failed to retrieve the page. Status code:", response.status_code)

print(data_price)
