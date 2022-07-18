import keras.models
import alhudood
import bbc_en
import bbc_scrap
import interior_affairs
import newyorker
import presidency
import sports
import telecom
import zamalek
import numpy as np
import pandas as pd
import pickle
import requests
import re
import nltk
import gc
from keras.models import load_model
from azure.storage.blob import BlobClient
from textblob import TextBlob
from nltk.corpus import stopwords
from keras.utils.data_utils import pad_sequences
# from keras.preprocessing.sequence import pad_sequences
from nltk.stem import SnowballStemmer
from arabert.preprocess import ArabertPreprocessor
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from sklearn.model_selection import train_test_split
import tensorflow as tf
import gensim
import schedule
import time

nltk.download('stopwords')
nltk.download('punkt')

con_str = 'DefaultEndpointsProtocol=https;AccountName=detect0rnews;AccountKey=+T/vwDH865hqfCeAZsSooIPtaLgH+fXwUbfMqT7t8i0dXjgEG1yvfIj83EKCwzVqCwxINo3yRtIz+AStID/rlg==;EndpointSuffix=core.windows.net'
arabert_model_name = "aubmindlab/bert-base-arabertv2"
arabert_prep = ArabertPreprocessor(model_name=arabert_model_name, )
stops = set(stopwords.words("arabic"))
port_stem = SnowballStemmer('english')


def scrap_all():
    ar_news = []
    ar_fake_flag = []
    en_news = []
    en_fake_flag = []
    news, fake_flag = zamalek.scrap()
    ar_news.extend(news)
    ar_fake_flag.extend(fake_flag)
    news, fake_flag = bbc_scrap.scrap()
    ar_news.extend(news)
    ar_fake_flag.extend(fake_flag)
    news, fake_flag = bbc_en.scrap()
    en_news.extend(news)
    en_fake_flag.extend(fake_flag)
    news, fake_flag = alhudood.scrap()
    ar_news.extend(news)
    ar_fake_flag.extend(fake_flag)
    news, fake_flag = interior_affairs.scrap()
    ar_news.extend(news)
    ar_fake_flag.extend(fake_flag)
    news, fake_flag = newyorker.scrap()
    en_news.extend(news)
    en_fake_flag.extend(fake_flag)
    news, fake_flag = presidency.scrap()
    ar_news.extend(news)
    ar_fake_flag.extend(fake_flag)
    news, fake_flag = sports.scrap()
    ar_news.extend(news)
    ar_fake_flag.extend(fake_flag)
    news, fake_flag = telecom.scrap()
    ar_news.extend(news)
    ar_fake_flag.extend(fake_flag)
    return ar_news, ar_fake_flag, en_news, en_fake_flag


def remove_stop_words(text):
    zen = TextBlob(text)
    words = zen.words
    return " ".join([w for w in words if not w in stopwords.words('english') and len(w) >= 2])


def split_hashtag_to_words(tag):
    tag = tag.replace('#', '')
    tags = tag.split('_')
    if len(tags) > 1:
        return tags
    pattern = re.compile(r"[A-Z][a-z]+|\d+|[A-Z]+(?![a-z])")
    return pattern.findall(tag)


def clean_hashtag(text):
    words = text.split()
    text = list()
    for word in words:
        if is_hashtag(word):
            text.extend(extract_hashtag(word))
        else:
            text.append(word)
    return " ".join(text)


def is_hashtag(word):
    if word.startswith("#"):
        return True
    else:
        return False


def extract_hashtag(text):
    hash_list = ([re.sub(r"(\W+)$", "", i) for i in text.split() if i.startswith("#")])
    word_list = []
    for word in hash_list:
        word_list.extend(split_hashtag_to_words(word))
    return word_list


def clean_tweet(text):
    text = re.sub('#\d+K\d+', ' ', str(text))  # years like 2K19
    text = re.sub('http\S+\s*', ' ', str(text))  # remove URLs
    text = re.sub('RT|cc', ' ', str(text))  # remove RT and cc
    text = re.sub('@[^\s]+', ' ', str(text))
    text = clean_hashtag(str(text))
    return text


def clean_text(text):
    text = clean_tweet(text)
    text = re.sub('[%s]' % re.escape("""!"#$%&'()*+,،-./:;<=>؟?@[\]^_`{|}~"""), ' ', text)  # remove punctuation
    text = re.sub('\s+', ' ', text)
    text = text.lower()
    text = remove_stop_words(text)
    # text = re.sub("\d+", " ", text)
    text = re.sub(r'\\u[A-Za-z0-9\\]+', ' ', text)
    text = re.sub('\s+', ' ', text)
    zen = TextBlob(text)
    words = zen.words
    text = [port_stem.stem(word) for word in words]
    text = ' '.join(text)
    text = arabert_prep.preprocess(text)
    text = re.sub('(\w+\+)|(\+\w+)', '', text)
    text = re.sub('\s+', ' ', text)
    return text


def download_item(item_name):
    blob_client = BlobClient.from_connection_string(con_str, blob_name=item_name, container_name='newcontainer')
    downloader = blob_client.download_blob(0)
    f = downloader.readall()
    item = pickle.loads(f)
    return item


def upload_item(item, item_name):
    blob_service_client = BlobServiceClient.from_connection_string(con_str)
    blob_client = blob_service_client.get_blob_client(container='newcontainer', blob=item_name)
    pickled = pickle.dumps(item, 0)
    blob_client.upload_blob(pickled, overwrite=True)


def download_csv(name):
    blob_service_client = BlobServiceClient.from_connection_string(con_str)
    csv_blob = blob_service_client.get_blob_client(container='newcontainer', blob=name)
    df = pd.read_csv(csv_blob.url)
    return df


def upload_csv(df,name):
    blob_service_client = BlobServiceClient.from_connection_string(con_str)
    csv_blob = blob_service_client.get_blob_client(container='newcontainer', blob=name)
    output = df.to_csv(index=False)
    csv_blob.upload_blob(output, overwrite=True)

# en_tokenizer = download_item('en_tokenizer')
# en_model_weights = download_item('english_weights.pickle')
# en_model_json = download_item('english_json.pickle')
#
# ar_tokenizer = download_item('ar_tokenizer.pickle')
# ar_model_weights = download_item('ar_weights.pickle')
# ar_model_json = download_item('ar_json.pickle')


def add_dataset():
    try:
        ar_news, ar_fake_flag, en_news, en_fake_flag = scrap_all()

        ar_fake_flag = np.array(ar_fake_flag)
        ar_news = np.array(clean_text(x) for x in ar_news)
        df = pd.DataFrame({'claim_s': ar_news, 'fake_flag': ar_fake_flag})
        ar_df = download_csv('arabic_stemmed.csv')
        ar_df = pd.concat([ar_df, df], ignore_index=True)
        upload_csv(ar_df, 'arabic_stemmed.csv')
        # ar_df.to_csv('ar_stemmed_all.csv',index=False)

        en_fake_flag = np.array(en_fake_flag)
        en_news = np.array(clean_text(x) for x in en_news)
        df = pd.DataFrame({'text': en_news, 'target': en_fake_flag})
        en_df = download_csv('english_stemmed.csv')
        en_df = pd.concat([en_df, df], ignore_index=True)
        upload_csv(en_df, 'english_stemmed.csv')
        # en_df.to_csv('en_stemmed_all.csv',index=False)
    except:
        return


def train_models():
    try:
        print('in training')
        en_tokenizer = download_item('en_tokenizer')
        en_model_weights = download_item('english_weights$1.pickle')
        en_model_json = download_item('english_json.pickle')

        en_model = keras.models.model_from_json(en_model_json)
        en_model.compile(loss="binary_crossentropy", optimizer="adam", metrics=['acc'])
        en_model.set_weights(en_model_weights)

        en_df = download_csv('english_stemmed.csv')
        en_tokens = en_tokenizer.texts_to_sequences(en_df.text)
        en_tokens = pad_sequences(en_tokens, maxlen=1000)
        en_y = en_df.target

        en_train_x, en_test_x, en_train_y, en_test_y = train_test_split(en_tokens, en_y, test_size=0.2, stratify=en_y)

        en_model.fit(en_train_x, en_train_y, epochs=1, batch_size=128, validation_data=(en_test_x, en_test_y))

        en_model_weights = en_model.get_weights()
        en_model_json = en_model.to_json()

        upload_item(en_model_weights, 'english_weights$1.pickle')
        upload_item(en_model_json, 'english_json.pickle')

        del en_model
        del en_tokenizer
        del en_model_weights
        del en_model_json
        del en_df
        del en_train_x, en_test_x, en_train_y, en_test_y
        gc.collect()

        ar_tokenizer = download_item('ar_tokenizer.pickle')
        ar_model_weights = download_item('ar_weights_2.pickle')
        ar_model_json = download_item('ar_json_2.pickle')

        ar_model = keras.models.model_from_json(ar_model_json)
        ar_model.compile(loss="binary_crossentropy", optimizer="adam", metrics=['acc'])
        ar_model.set_weights(ar_model_weights)

        ar_df = download_csv('arabic_stemmed.csv')
        ar_tokens = ar_tokenizer.texts_to_sequences(ar_df.text)
        ar_tokens = pad_sequences(ar_tokens, maxlen=1000)
        ar_y = ar_df.target

        ar_train_x, ar_test_x, ar_train_y, ar_test_y = train_test_split(ar_tokens, ar_y, test_size=0.2, stratify=ar_y)

        ar_model.fit(ar_train_x, ar_train_y, epochs=1, batch_size=128, validation_data=(ar_test_x, ar_test_y))

        ar_model_weights = ar_model.get_weights()
        ar_model_json = ar_model.to_json()
        upload_item(ar_model_weights, 'ar_weights_2.pickle')
        upload_item(ar_model_json, 'ar_json_2.pickle')

        del ar_model
        del ar_tokenizer
        del ar_df
        del ar_model_weights
        del ar_model_json
        del ar_train_x, ar_test_x, ar_train_y, ar_test_y

        gc.collect()

        url = 'https://fake-news-detector.azurewebsites.net/update'
        x = requests.post(url)
    except:
        return


schedule.every().day.at("23:30").do(add_dataset)
schedule.every().tuesday.at("12:00").do(train_models)

while True:
    schedule.run_pending()
    time.sleep(60)  # wait one minute






