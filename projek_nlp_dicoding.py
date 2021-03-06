# -*- coding: utf-8 -*-
"""Projek_NLP_Dicoding.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1h0e1IuZ9Qe9ZrTR5-LfWwlsYBxYbjVtu

# Proyek NLP 
Muhammad Fakhri Rahman

muhammad17031@mail.unpad.ac.id

## **Import Library**
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
import string
import matplotlib.pyplot as plt

import tensorflow as tf
from tensorflow.keras.callbacks import Callback
from tensorflow.keras import layers, Sequential
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import nltk
from nltk.corpus import stopwords

"""## **Hyperparameter Setting**"""

vocab_size = 7500
embedding_size = 64
trunc_type = 'post'
padding_type = 'post'
max_length = 100
oov_token = '<OOV>'

"""## **Data Preparation**

"""

df1 = pd.read_csv('/content/inshort_news_data-1.csv')
df2 = pd.read_csv('/content/inshort_news_data-2.csv')
df3 = pd.read_csv('/content/inshort_news_data-3.csv')
df4 = pd.read_csv('/content/inshort_news_data-4.csv')
df5 = pd.read_csv('/content/inshort_news_data-5.csv')
df6 = pd.read_csv('/content/inshort_news_data-6.csv')
df7 = pd.read_csv('/content/inshort_news_data-7.csv')

df = pd.concat([df1, df2, df3, df4, df5, df6, df7], ignore_index=True)
df.columns.str.match('Unnamed')
df.loc[:,~df.columns.str.match('Unnamed')]
df = df.drop('Unnamed: 0',axis=1)
df = df.drop(columns=['news_headline'])
df

"""### Exploratory data"""

plt.figure(figsize=(10,9))
sns.countplot(df['news_category'])
plt.title('News Category')
plt.show

"""### One-hot Encoding"""

category = pd.get_dummies(df.news_category)
new_df = pd.concat([df, category], axis=1)
new_df = new_df.drop(columns='news_category')
new_df

"""### Data Cleaning"""

def remove_punctuation(text):
    punctuationfree="".join([i for i in text if i not in string.punctuation])
    return punctuationfree

def tokenization(text):
    tokens = re.split('\s|(?<!\d)[,.]|[,.](?!\d)',text)
    return tokens

nltk.download('stopwords')
stopwords = stopwords.words('english')

def remove_stopwords(text):
    output= [i for i in text if i not in stopwords]
    return output

new_df['news_article'] = new_df['news_article'].apply(lambda x: remove_punctuation(x))
new_df['news_article'] = new_df['news_article'].apply(lambda x: x.lower())
new_df['stopwrds_removed_article'] = new_df['news_article'].apply(lambda x: ' '.join([word for word in x.split() if word not in (stopwords)]))
new_df

text = new_df['stopwrds_removed_article'].values
labels = new_df[['automobile', 'entertainment', 'politics', 'science', 'sports', 'technology', 'world']]
text_train, text_test, labels_train, labels_test = train_test_split(text, labels, test_size = 0.2)
print('Terdapat {} text untuk training'.format(len(text_train)))
print('Terdapat {} text untuk testing'.format(len(text_test)))

tokenizer = Tokenizer(num_words = vocab_size, oov_token = oov_token)
tokenizer.fit_on_texts(text_train)
word_index = tokenizer.word_index
dict(list(word_index.items())[0:20])

train_sequences = tokenizer.texts_to_sequences(text_train)

train_padded = pad_sequences(train_sequences, maxlen = max_length, padding=padding_type, truncating=trunc_type)

print(len(train_sequences[0]))
print(len(train_padded[0]))

print(len(train_sequences[1]))
print(len(train_padded[1]))

print(len(train_sequences[10]))
print(len(train_padded[10]))

validation_sequences = tokenizer.texts_to_sequences(text_test)
validation_padded = pad_sequences(validation_sequences, maxlen=max_length, padding=padding_type, truncating=trunc_type)

print(len(validation_sequences[0]))
print(len(validation_padded[0]))

print(len(validation_sequences[1]))
print(len(validation_padded[1]))

print(len(validation_sequences[10]))
print(len(validation_padded[10]))

"""## **Training**

### Model
"""

model = Sequential([
                    layers.Embedding(vocab_size, embedding_size),
                    layers.Bidirectional(layers.LSTM(embedding_size)),
                    layers.Dense(embedding_size, activation='relu'),
                    layers.Dense(7, activation='softmax')
])

model.summary()
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

"""### Callbacks"""

class myCallback(Callback):
  def on_epoch_end(self, epoch, logs={}):
    if(logs.get('accuracy')>0.965):
      print('\nAkurasi telah mencapai 96%"')
      self.model.stop_training = True

callbacks = myCallback()

"""### **Training model**"""

num_epochs = 20

history = model.fit(train_padded, labels_train, epochs=num_epochs, validation_data=(validation_padded, labels_test), callbacks=[callbacks], verbose=2)

"""### Plotting"""

def plot_graphs(history, string):
  plt.plot(history.history[string])
  plt.plot(history.history['val_'+string])
  plt.xlabel("Epochs")
  plt.ylabel(string)
  plt.legend([string, 'val_'+string])
  plt.show()

plot_graphs(history, "accuracy")
plot_graphs(history, "loss")