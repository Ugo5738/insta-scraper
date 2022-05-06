import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify


app = Flask(__name__)


@app.route('/scrape_instagram_data/<keyword>', methods=['POST'])
def scrape_instagram_data(keyword):
    result = requests.get(f"https://www.picuki.com/tag/{keyword}")

    src = result.content

    soup = BeautifulSoup(src, 'html.parser')

    links = soup.find_all('a')

    dict_ = {}
    urls = []
    ids = []
    desp = []
    for link in links:
        if 'media' in link.attrs['href'].split('/'):
            urls.append(link.attrs['href'])
            ids.append(link.attrs['href'].split('/')[-1])

    texts = soup.find_all("div", {"class": "photo-description"})
    for desp_text in texts:
        desp.append(desp_text.text)

    dict_['url'] = urls
    dict_['ids'] = ids
    dict_['desp'] = desp

    return jsonify(dict_)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
