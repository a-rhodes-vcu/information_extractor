
question = "when does a baby situp"

from nltk.corpus import stopwords
import ssl
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
count_vectorizer = CountVectorizer()
from nltk.stem import WordNetLemmatizer

new_dict = {}
new_list= []
lemmatizer = WordNetLemmatizer()

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

sw_nltk = stopwords.words('english')

def create_dataframe(matrix, tokens):
    doc_names = [f'doc_{i + 1}' for i, _ in enumerate(matrix)]
    df = pd.DataFrame(data=matrix, index=doc_names, columns=tokens)
    return (df)

def get_response(situp_text):

    text = situp_text.replace(". ",".")
    text = text.split(".")

    for j in text:
        words = [ lemmatizer.lemmatize(word.lower()) for word in j.split() if word.lower() not in sw_nltk ]
        string = " ".join(words)

        words2 = [ lemmatizer.lemmatize(word1.lower()) for word1 in question.split() if word1.lower() not in sw_nltk ]
        string2 = " ".join(words2)

        new_dict[string] = j
        new_list.append([string,string2])

    max_dict = {}
    return_string = "Here are some info:\n"
    for j in new_list:
        vector_matrix = count_vectorizer.fit_transform(j)
        tokens = count_vectorizer.get_feature_names_out()
        vector_matrix.toarray()

        create_dataframe(vector_matrix.toarray(), tokens)

        cosine_similarity_matrix = cosine_similarity(vector_matrix)
        de = create_dataframe(cosine_similarity_matrix, ['doc_1', 'doc_2'])

        column = de["doc_1"]
        max_value = column.min()

        max_dict[max_value] = j[0]

    print(question + "\n")

    max_key_list = sorted(max_dict)[-3:]

    for key in max_key_list:

        if key != 0.0:
            value = max_dict[key]
            return_string += new_dict[value] + "."
    return (return_string)


situp_text = """Babies must be able to hold their heads up without support and have enough upper body strength before being able to sit up on their own. Babies often can hold their heads up around 2 months, and begin to push up with their arms while lying on their stomachs.

At 4 months, a baby typically can hold his/her head steady without support, and at 6 months, he/she begins to sit with a little help. At 9 months he/she sits well without support, and gets in and out of a sitting position but may require help. At 12 months, he/she gets into the sitting position without help.

Tummy time helps strengthen the upper body and neck muscles that your baby needs to sit up. Around 6 months, encourage sitting up by helping your baby to sit or support him/her with pillows to allow him/herher to look around."""


#get_response(situp_text)


