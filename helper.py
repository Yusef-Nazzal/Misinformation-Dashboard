
import re

def clean_text(text):
    text = re.sub('<[^>]*>', ' ', text)
    text = re.sub(r'https?://\S+|www\.\S+', ' ', text)
    text = re.sub(r'\bhttps\b', '', text)
    text = re.sub('[^a-zA-Z]', ' ', text)
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    text = re.sub('\s+', ' ', text)
    
    
    text = ' '.join(word for word in text.lower().split() if len(word) > 1 and word != 've' and word != 're' and word != 'don')
    
    return text.lower()