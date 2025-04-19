from flask import Flask, render_template, request
import requests
from googletrans import Translator

app = Flask(__name__)

API_KEY = 'd9fa95fc-69da-46f3-87bc-51385ea69805'

# URL برای دریافت اخبار از Guardian
def get_news():
    url = f'https://content.guardianapis.com/search?section=world&api-key={API_KEY}'
    response = requests.get(url)
    data = response.json()
    if data['response']['status'] == 'ok':
        return data['response']['results'][:15]  # نمایش 5 1خبر اول
    return []


def translate_to_persian(text):
    translator = Translator()
    translation = translator.translate(text, dest='fa')
    return translation.text

@app.route('/', methods=['GET', 'POST'])
def index():
    news_list = []
    if request.method == 'POST':
        articles = get_news()
        for i, article in enumerate(articles, 1):
            title = article.get('webTitle', '')
            newsDate = article.get('webPublicationDate', '')
            sectionName = article.get('sectionName', '')
            webUrl = article.get('webUrl','')
            title_trans = translate_to_persian(title)
            #desc_trans = translate_to_persian(description) if description else 'ندارد'
            news_list.append({
                'title': title,
                'title_trans': title_trans,
                'newsDate': newsDate,
                #'desc_trans': desc_trans
                'webUrl':webUrl,
                'section':sectionName
            })
    return render_template('index.html', news_list=news_list)

if __name__ == '__main__':
    app.run(debug=True)