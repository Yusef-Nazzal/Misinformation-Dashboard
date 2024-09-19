from helper import clean_text
import plotly.graph_objs as go
import plotly.io as pio
import pandas as pd
from wordcloud import WordCloud
import base64
from io import BytesIO
from matplotlib.colors import LinearSegmentedColormap
from wordcloud import WordCloud, STOPWORDS
from nltk.corpus import stopwords
from nltk.sentiment import SentimentIntensityAnalyzer




def top_trending_words(search_results):
    if not search_results:
        return
    combined_text = ' '.join(toot['content'] for toot in search_results if 'content' in toot)
    

    cleaned_text = clean_text(combined_text)

    tokens = cleaned_text.lower().split()
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word not in stop_words]

    word_freq = {}
    for word in filtered_tokens:
        if word in word_freq:
            word_freq[word] += 1
        else:
            word_freq[word] = 1

    sorted_word_freq = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]

    words, frequencies = zip(*sorted_word_freq)

    fig = go.Figure(data=[go.Bar(
        x=list(words),
        y=list(frequencies),
        marker_color='rgba(55, 128, 191, 0.7)'  
    )])

    fig.update_layout(
            title='Top 10 Trending Words',
            xaxis_title='Words',
            yaxis_title='Frequency',
            paper_bgcolor='#203354',
            plot_bgcolor='#203354',
            font_color='white', 
            xaxis=dict(tickangle=45)  
        )
    

    return pio.to_html(fig, full_html=False)

def temporal_gen(search_results):
    if not search_results:
        return ""
    
    timestamp_data = [pd.to_datetime(result["created_at"]) for result in search_results if isinstance(result, dict) and "created_at" in result]

    df = pd.DataFrame({'timestamp': timestamp_data})
    df['date'] = df['timestamp'].dt.date
    posts_over_time = df.groupby('date').size()

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=posts_over_time.index, y=posts_over_time.values, mode='lines+markers', name='Posts'))
    
    fig.update_layout(
        title='Posts Over Time',
        paper_bgcolor='#203354',
        plot_bgcolor='#203354',
        font_color='white',
        xaxis=dict(title='Date'),
        yaxis=dict(title='Number of Posts'),
        hovermode='x unified'
        )
   
    return pio.to_html(fig, full_html=False)

def sentiment_graph(search_results):
    if not search_results:
        return ""
    
    import nltk
    nltk.download('vader_lexicon')

    sia = SentimentIntensityAnalyzer()

    sentiments = [{
        'timestamp': pd.to_datetime(toot['created_at']),
        'sentiment': sia.polarity_scores(toot['content'])['compound']
    } for toot in search_results if 'content' in toot]
    df = pd.DataFrame(sentiments)

  
    df['date'] = df['timestamp'].dt.date
    sentiment_counts = df.groupby(['date', pd.cut(df['sentiment'], bins=[-1, -0.1, 0.1, 1], labels=['Negative', 'Neutral', 'Positive'])]).size().unstack(fill_value=0)

    fig = go.Figure()
    fig.add_trace(go.Bar(x=sentiment_counts.index, y=sentiment_counts['Negative'], name='Negative', marker_color='red'))
    fig.add_trace(go.Bar(x=sentiment_counts.index, y=sentiment_counts['Neutral'], name='Neutral', marker_color='blue'))
    fig.add_trace(go.Bar(x=sentiment_counts.index, y=sentiment_counts['Positive'], name='Positive', marker_color='green'))

    
    fig.update_layout(
            title='Sentiment Distribution Over Time',
            paper_bgcolor='#203354',
            plot_bgcolor='#203354',
            font_color='white',
            xaxis=dict(title='Date'),
            yaxis=dict(title='Number of Posts'),
            barmode='stack'
            )
    
   
    return pio.to_html(fig, full_html=False)


colors = ["red", "green", "#8dbdff"]
n_bins = 3 
cmap_name = 'rgbcustom'


cm = LinearSegmentedColormap.from_list(cmap_name, colors, N=n_bins)

def wordCloud_gen(search_results):
    if not search_results:
        return ""
    text = ' '.join(toot['content'] for toot in search_results if 'content' in toot)
    cleaned_text = clean_text(text) 
    stopwords = set(STOPWORDS)
    wordcloud = WordCloud(
        width=1200, height=600, 
        background_color="#203354", 
        stopwords=stopwords, 
        max_font_size=80,
        colormap=cm  
    ).generate(cleaned_text)

    image_bytes = BytesIO()
    wordcloud.to_image().save(image_bytes, format='PNG')
    encoded_image = base64.b64encode(image_bytes.getvalue()).decode('ascii')
    return encoded_image




    
