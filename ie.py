from nltk.corpus import stopwords
import ssl
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
count_vectorizer = CountVectorizer()
from nltk.stem import WordNetLemmatizer
content_dict = {}
content_and_question = []
lemmatizer = WordNetLemmatizer()

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

sw_nltk = stopwords.words('english')

def create_dataframe(matrix, tokens):
    # create row names
    doc_names = [f'doc_{i + 1}' for i, _ in enumerate(matrix)]
    # create data frame where tokens are the words in the sentence and matrix is the count
    df = pd.DataFrame(data=matrix, index=doc_names, columns=tokens)
    return (df)

def get_response(content,question):

    """
    :param content: string of the article content
    :param question: string of the question from the user
    :return: string that contains most relevant sentences from article
    """

    # first process text
    text = content.replace(". ",".").replace("\n","").replace("","")
    token_text = text.split(".")

    for sentence in token_text:
        if sentence:
            # tokenizing the content and getting the lemma of each word. saving text back into a string
            content_as_list = [ lemmatizer.lemmatize(word.lower()) for word in sentence.split() if word.lower() not in sw_nltk ]
            content_as_string = " ".join(content_as_list)

            # tokenizing the question and getting the lemma of each word. saving text back into a string
            question_as_list = [ lemmatizer.lemmatize(word.lower()) for word in question.split() if word.lower() not in sw_nltk ]
            question_as_string = " ".join(question_as_list)

            # create a dictionary, this will be used later on to product the responses
            content_dict[content_as_string] = sentence
            # create a list of lists, each inner list is a sentence from the content and question
            content_and_question.append([content_as_string,question_as_string])

    cosine_sim_dict = {}
    response_string = "Here are some info:\n"
    for item in content_and_question:
        # transform the words in each inner list into a matrix that looks like this:
        # (0, 1)  1 (sentence index, word index) count of word appearing in that location.
        vector_matrix = count_vectorizer.fit_transform(item)
        vector_matrix.toarray()

        # if you were interested in seeing what this looks like under the hood. doc_1 refers to the content and doc_2 refers to the question
        # tokens = count_vectorizer.get_feature_names_out()
        # print(create_dataframe(vector_matrix.toarray(), tokens))
        #  able  baby  body  enough  head
        # doc_1     2     1     1       1     1
        # doc_2     0     1     0       0     0

        # calculate cosine similarity with the vector matrix
        cosine_similarity_matrix = cosine_similarity(vector_matrix)
        # create a data frame
        de = create_dataframe(cosine_similarity_matrix, ['doc_1', 'doc_2'])

        # for cosine similarity, we want the smallest number because that means the vectors are more similar
        min_value = min(de["doc_1"])
        # save min value in dictionary as key, value is single sentence from the content
        cosine_sim_dict[min_value] = item[0]

    print(question + "\n")

    try:
        # sort dict so smallest number is first, use only first three sentences
        sorted_cs_dict = sorted(cosine_sim_dict)[0:3]
        for key in sorted_cs_dict:
            # print dict contents by taking key to retrieve lemma sentence and using that to print out full sentence
            lemma_sentence = cosine_sim_dict[key]
            response_string += content_dict[lemma_sentence] + "."
        return (response_string)

    except:
        return "Sorry, unable to process question"

# comments it out for testing
# content = """Babies must be able to hold their heads up without support and have enough upper body strength before being able to sit up on their own. Babies often can hold their heads up around 2 months, and begin to push up with their arms while lying on their stomachs.
#
# At 4 months, a baby typically can hold his/her head steady without support, and at 6 months, he/she begins to sit with a little help. At 9 months he/she sits well without support, and gets in and out of a sitting position but may require help. At 12 months, he/she gets into the sitting position without help.
#
# Tummy time helps strengthen the upper body and neck muscles that your baby needs to sit up. Around 6 months, encourage sitting up by helping your baby to sit or support him/her with pillows to allow him/herher to look around."""
#
# question = "when does a baby situp"

#get_response(content,question)


