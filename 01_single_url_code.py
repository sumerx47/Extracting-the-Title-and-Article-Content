

import requests
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import PorterStemmer
import re

# Download necessary NLTK resources
#nltk.download('punkt')79
#nltk.download('stopwords')

# Fetch HTML content from the URL
url = "https://insights.blackcoffer.com/how-google-fit-measure-heart-and-respiratory-rates-using-a-phone/"
response = requests.get(url)
html_content = response.text

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Extract the title
title = soup.title.string
print("Title:", title)

# Find the main article content
article = soup.find('article')  # Update with appropriate tag or element
if article:
    # Extract the title text from the <h1> tag inside <header> if it exists
    header = article.find('header')  # Find the <header> tag within the article
    if header:
        title_element = header.find('h1')  # Find the <h1> tag within the header
        if title_element:
            title_text = title_element.get_text()
            print("Header Title:", title_text)
        else:
            print("No <h1> tag found inside header.")
    else:
        print("Header element not found.")

    # Extract the text from the paragraph elements within the article
    paragraphs = article.find_all('p')
    article_text = ' '.join(paragraph.get_text(separator=' ') for paragraph in paragraphs)
    print("Article Text:", article_text)
else:
    print("Article element not found.")


# Specify the paths to positive, negative, and stop word files
positive_words_path = "C:/Users/sumair/OneDrive/Desktop/01-blackcoffer_nlp_code/dataset_nps/positive-words.txt"
negative_words_path = "C:/Users/sumair/OneDrive/Desktop/01-blackcoffer_nlp_code/dataset_nps/negative-words.txt"
stop_words_paths = [
    "C:/Users/sumair/OneDrive/Desktop/01-blackcoffer_nlp_code/dataset_nps/StopWords_Auditor.txt",
    "C:/Users/sumair/OneDrive/Desktop/01-blackcoffer_nlp_code/dataset_nps/StopWords_Currencies.txt",
    "C:/Users/sumair/OneDrive/Desktop/01-blackcoffer_nlp_code/dataset_nps/StopWords_DatesandNumbers.txt",
    "C:/Users/sumair/OneDrive/Desktop/01-blackcoffer_nlp_code/dataset_nps/StopWords_Generic.txt",
    "C:/Users/sumair/OneDrive/Desktop/01-blackcoffer_nlp_code/dataset_nps/StopWords_GenericLong.txt",
    "C:/Users/sumair/OneDrive/Desktop/01-blackcoffer_nlp_code/dataset_nps/StopWords_Geographic.txt",
    "C:/Users/sumair/OneDrive/Desktop/01-blackcoffer_nlp_code/dataset_nps/StopWords_Names.txt"
]


# Load positive and negative words
positive_words = set()
with open(positive_words_path, 'r') as file:
    positive_words.update(word.strip() for word in file)

negative_words = set()
with open(negative_words_path, 'r') as file:
    negative_words.update(word.strip() for word in file)

# Load stop words
stop_words = set()
for path in stop_words_paths:
    with open(path, 'r') as file:
        stop_words.update(word.strip() for word in file)

# Extracting Derived Variables
tokens = word_tokenize(article_text)
cleaned_tokens = [word.lower() for word in tokens if word.lower() not in stop_words]

positive_score = sum(1 for word in cleaned_tokens if word in positive_words)
negative_score = sum(1 for word in cleaned_tokens if word in negative_words)
polarity_score = (positive_score - negative_score) / (positive_score + negative_score + 0.000001)
subjectivity_score = (positive_score + negative_score) / (len(cleaned_tokens) + 0.000001)



# 2. Analysis of Readability
sentences = sent_tokenize(article_text)
num_sentences = len(sentences)
num_words = len(cleaned_tokens)
average_sentence_length = num_words / num_sentences

# 4. Complex Word Count
complex_words_count = 0
for word in cleaned_tokens:
    syllable_count = 0
    # Count the syllables in the word
    word = re.sub(r'[^a-zA-Z]', '', word)
    if len(word) > 2:
        if word.endswith(("es", "ed")):
            pass
        else:
            for vowel in ['a', 'e', 'i', 'o', 'u']:
                syllable_count += word.count(vowel)
    if syllable_count > 2:
        complex_words_count += 1

percentage_complex_words = complex_words_count / num_words
fog_index = 0.4 * (average_sentence_length + percentage_complex_words)

# 3. Average Number of Words Per Sentence
average_words_per_sentence = num_words / num_sentences

# 5. Word Count
word_count = len(cleaned_tokens)

# 6. Syllable Count Per Word
syllable_count_per_word = {}
for word in cleaned_tokens:
    syllable_count = 0
    # Count the syllables in the word
    word = re.sub(r'[^a-zA-Z]', '', word)
    if len(word) > 2:
        if word.endswith(("es", "ed")):
            pass
        else:
            for vowel in ['a', 'e', 'i', 'o', 'u']:
                syllable_count += word.count(vowel)
    syllable_count_per_word[word] = syllable_count
print("Syllable Count Per Word:", syllable_count_per_word)

# 7. Personal Pronouns
personal_pronouns = ['i', 'we', 'my', 'ours', 'us']
pronoun_count = sum(1 for word in cleaned_tokens if word.lower() in personal_pronouns)

# 8. Average Word Length
total_characters = sum(len(word) for word in cleaned_tokens)
average_word_length = total_characters / word_count

print()
# Print the derived variables
print("Positive Score:", positive_score)
print("Negative Score:", negative_score)
print("Polarity Score:", polarity_score)
print("Subjectivity Score:", subjectivity_score)
print("Average Sentence Length:", average_sentence_length)
print("Percentage of Complex Words:", percentage_complex_words)
print("Fog Index:", fog_index)
print("Average Number of Words Per Sentence:", average_words_per_sentence)
print("Complex Word Count:", complex_words_count)
print("Word Count:", word_count)
print("syllable_per_word :",syllable_count_per_word[word])
#print("Syllable Per Word:", syllable_count_per_word)
print("Personal Pronouns Count:", pronoun_count)
print("Average Word Length:", average_word_length)



