from flask import Flask, render_template, request
from search import search_for_toots
from plots import wordCloud_gen, temporal_gen, sentiment_graph, top_trending_words

app = Flask(__name__)


@app.route('/index', methods=['GET', 'POST']) 
def index():
    context = {
        'wordCloud': None,
        'temporal': None,
        'sentiment': None,
        'trending_words': None,
        'search_term': '',
        'search_results': [],
        'error_message': ''  
    }

    if request.method == 'POST':
        search_term = request.form.get('search_term', '').strip()
        if not search_term: 
            context['error_message'] = 'Please enter a search term.'
        else:
            search_results = search_for_toots(search_term)
            context.update({
                'wordCloud': wordCloud_gen(search_results),
                'temporal': temporal_gen(search_results),
                'sentiment': sentiment_graph(search_results),
                'trending_words': top_trending_words(search_results),
                'search_term': search_term,
                'search_results': search_results
            })

    return render_template('index.html', **context)

@app.route('/')
def about():
    return render_template('about.html')



    
if __name__ == '__main__':
    app.run(debug=True)
