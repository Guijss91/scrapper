from flask import Flask, request, jsonify
import asyncio
from scraper.crawler import crawl

app = Flask(__name__)

@app.route('/')
def index():
    return 'A API está funcionando!'

@app.route('/scrap', methods=['POST'])
def scrap():
    data = request.json
    url = data.get('url')
    fields = data.get('fields')
    follow_links = data.get('follow_links', 0)
    ignore_external = data.get('ignore_external', True)
    depth = data.get('depth', 1)

    if not url:
        return jsonify({'error': 'URL é obrigatória'}), 400

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(
        crawl(url, fields=fields, follow_links=follow_links, ignore_external=ignore_external, depth=depth)
    )
    loop.close()

    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
