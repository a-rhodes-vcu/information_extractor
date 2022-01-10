# Information Extractor
This bot returns relevant sentences from an article that pertains to the person's query

## Motivation
I love NLP and enjoy expanding my current knowledge and skill set on it. I was googling a question and the response was a segment from a paragraph, like the one below:
![image_1](https://github.com/a-rhodes-vcu/information_extractor/blob/main/images/Screen%20Shot%202022-01-07%20at%2011.28.01%20AM.png)
I thought this was so cool and the more I read about information extraction the more I became fascinated. In exploring this concept I hope the final product is one that can lower the barrier of entry for meaningful information and can produce accurate results that are pertinent to the query.

## Code walkthrough
Programs used:
<br>
[ie.py](https://github.com/a-rhodes-vcu/information_extractor/blob/main/ie.py)
<br>
[app.py](https://github.com/a-rhodes-vcu/information_extractor/blob/main/app.py)
<br>

In [ie.py](https://github.com/a-rhodes-vcu/information_extractor/blob/main/ie.py) a dictionary is made that contains the lemma as the key and the sentence as the value. This is used later to return the sentences from the article. A list is made that contains inner lists of the article sentence and the question, for example:
content_and_question = ['Babies are babies','What are babies?']

```
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

```
Then the cosine similarity is calculated. Cosine similarity is a measure of similarity between two non-zero vectors, and it is a common way of determining text similarity. The smallest cosine similarity is chosen.
```
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

```
Finally, the most relevant sentence is chosen from the list of sentences.
```
 try:
       for key, value in cosine_sim_dict.items():
       if len(value) > 4:
           cosine_sim_dict.pop('key', None)
    try:
        # sort dict so smallest number is first
        sorted_cs_dict = sorted(cosine_sim_dict)[-1:]

        # init data obj
        for cs in sorted_cs_dict:
            data_obj = {
                'score': cs,
                'sentences': []
            }

            # retrieve single sentence from content, store as value, key is cosine similarity
            lemma_sentence_list = cosine_sim_dict[cs]

            for lemma in lemma_sentence_list:
                respond_sentence = content_dict[lemma]
                # add lemma sentences to data obj
                respond_sentence =  "{}{}".format(respond_sentence,".")
                data_obj['sentences'].append(respond_sentence)
            response_string_dict['data'].append(data_obj)
        return response_string_dict

```


# Tech Spec
python 3.9 is a requirement
<br>
to download requirements:
*pip3 install -r requirements.txt
<br>
to run flask app:
*run 'flask run' in the ide terminal
<br>
*change flask port
flask run -h localhost -p 3000

