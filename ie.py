from nltk.corpus import stopwords
import ssl
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
import re
count_vectorizer = CountVectorizer()

from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

sw_nltk = stopwords.words('english')

sw_nltk.append('child')

def create_dataframe(matrix, tokens):
    
    # create row names
    doc_names = [f'doc_{i + 1}' for i, _ in enumerate(matrix)]
    # create data frame where tokens are the words in the sentence and matrix is the count
    df = pd.DataFrame(data=matrix, index=doc_names, columns=tokens)
    return (df)


def get_cs(content_and_question):
    cosine_sim_dict = {}


    for item in content_and_question:
        # transform the words in each inner list into a matrix that looks like this:
        # (0, 1)  1 (sentence index, word index) count of word appearing in that location.
        # vector_matrix = count_vectorizer.fit_transform(item)
        vectorizer = TfidfVectorizer()
        vector_matrix = vectorizer.fit_transform(item)
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
        # exclude values if they are 0.0

        if item[0] and "\\" not in item[0]:
            if min_value not in cosine_sim_dict:
                cosine_sim_dict[min_value] = [item[0]]
            else:
                cosine_sim_dict[min_value].append(item[0])

    return cosine_sim_dict

def get_response(content,question):
    content_dict = {}
    content_and_question = []

    """
    :param content: string of the article content
    :param question: string of the question from the user
    :return: string that contains most relevant sentences from article
    """

    # first process text
    text = content.replace(". ",".").replace("\n","").replace("\"","").replace("U.S.", "US").strip()
    token_text = text.split(".")
    # remove punc from question
    question = re.sub(r'[^\w\s]', '', question)


    for index,sentence in enumerate(token_text):
        #sentence = ".".join(token_text[index:index+3])
        if sentence:

            # tokenizing the content and getting the lemma of each word. saving text back into a string
            content_as_list = [ lemmatizer.lemmatize(word.lower()) for word in sentence.split() if word.lower() not in sw_nltk ]
            content_as_string = " ".join(content_as_list)

            # tokenizing the question and getting the lemma of each word. saving text back into a string
            question_as_list = [ lemmatizer.lemmatize(word.lower()) for word in question.split() if word.lower() not in sw_nltk]
            question_as_string = " ".join(question_as_list)

            # create a dictionary, this will be used later on to product the responses
            content_dict[content_as_string] = sentence
            # create a list of lists, each inner list is a sentence from the content and question
            content_and_question.append([content_as_string,question_as_string])

    #print(content_and_question)
    cosine_sim_dict = get_cs(content_and_question)
    #print(cosine_sim_dict)

    response_string_dict = {
        'data': []
    }

    for key, value in cosine_sim_dict.items():
       if len(value) > 4:
           cosine_sim_dict.pop('key', None)
    try:
        # sort dict so smallest number is first, use only first three sentences
        sorted_cs_dict = sorted(cosine_sim_dict)[0:3] # [0.0, 0.17512808619292852, 0.18068688270171662]

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

    except:
        return "Sorry, unable to process question"

# comments it out for testing
#content = "In this personal essay, a parent shares their experience of switching from breastfeeding to formula. When my daughter was 6 months old, I made the hard decision to wean her from breastfeeding. I had struggled to conceive her. During the infertility process, my reproductive endocrinologist had told me that if I wanted to have another child I should consider weaning at 6 months to get my cycle back on track and set up my body for another round of fertility treatment. Specifically, I had a low ovarian reserve, so my biological clock had less time on it than most people my age.  When I was pregnant, six months seemed like a reasonable time to breastfeed. I wasn't too concerned about having to give it up at that point. After giving birth, I had a relatively easy time getting breastfeeding going, despite some real pain in the first few weeks. My daughter latched easily and we had a good thing going.  At 5 months, the weaning deadline started to loom in my mind. I couldn't imagine the idea of stopping breastfeeding and would try to push it from my mind. Then, I got mastitis, I believe from taking too long to pump while I was away from her working. The extreme nausea and pain came over me quickly, but the antibiotics helped me feel better in a day. This would have been a manageable blip in our journey, but it did give me the first glimpse that there might actually be an upside to switching to formula. At 6 months, I continued to push away the idea of ending breastfeeding. But I did let my husband start to research formulas. He found an organic formula he felt good about. One night, I left the house for dinner out with my friends and he gave our daughter her first bottle of formula. For the next month, we slowly started to supplement breast feedings with formula. At her daycare, she got formula.  Eventually, we were down to just the morning feed. I still can remember the last time I nursed her. When it was done, I made a list of all the specific nursing moments I could remember. We had turned a page. That night, we left her at my parents' house for the first time and had an overnight alone. It felt like a reward and silver lining ending our 7-month breastfeeding journey.  After a hard week with many emotions, I adjusted to the idea that I was no longer feeding my daughter from my own body. Here are some positive things I wish I had known before:  I could still bond with my child during bottle feedings. Just like with nursing, she would cuddle in my arms and look into my eyes.  I could now wear whatever I wanted. No more baggy shirts or button downs. Dresses were back in the mix! I underestimated how much this made me feel more like myself.  My hormones took a turn for the better. Lower levels of estrogen associated with breastfeeding can make sex painful. When you wean, sex can get easier and more pleasurable. It feels good to say goodbye to pumping. Let's be honest, hooking yourself up to a machine and having the wash all those parts can be a drag. It doesn't have to be all or nothing. For family planning reasons, I had to eventually stop nursing completely. But for many families, it's possible to give your baby some breastmilk after introducing formula.  Commercial formula cannot perfectly replace breastmilk and it has been overmarketed to parents, especially in communities of color. Today, many medical and birth support professionals rightfully emphasize the importance of breastfeeding. But this can also leave some parents nervous and uninformed about how to start feeding their children if and when they cannot produce milk themselves. If you're in this situation know this: how you feed your baby is not a reflection of your love or care for them. '"
#question = "how do i breastfeed"

#content = """Loss is an unfortunate part of life. As a parent, it is usually your first instinct to shield your children from the emotional pain that is caused by loss. It is important to remember that in order for your children to learn to deal with pain and the emotions that come along with it, parents must guide children through what they are feeling, and show them healthy ways to cope. Often when parents shelter children from these feelings, the child never truly learns how to deal with big emotions.  Children react to loss differently. Some might become withdrawn or quiet, while others may lash out in anger or frustration. Feelings of guilt, sadness, or even quick changes in mood can all be a typical part of the grieving process for a child; any emotion or reaction that your child may experience is valid. It is our responsibility to acknowledge those feelings as normal and guide your child as they navigate the immense pain that can come from a loss.  Here are some ways you can support your child as they deal with loss in their lives.   Follow their lead. If your child is asking a lot of questions or choosing to take some space, understand what your child needs from you to best help them understand what has happened and process their feelings. Listen to your child as they communicate and allow your child to feel heard as they let out the emotions that they are feeling. Open-ended questions such as, "What's one question you would like to ask me today?" can be a great way to encourage your child to openly communicate with you.  Be honest with your child. Explain what happened and use clear language that helps them to understand. Make sure that you are using age-appropriate language in doing so. Acknowledge your child's feelings. When parents validate the emotions their children are having, it often helps the child to understand that these feelings are normal. Statements such as, "I can see that you are feeling really sad today. I wonder if you would like to ask any questions or talk about what you are feeling more?" can help children to feel heard and understood.  Create a memorial for the person who died. Creating and decorating a "memory box" with your child can be a great way to celebrate a loved one's life while allowing your child to acknowledge that they are gone. Model healthy ways to grieve. Ultimately the goal is to teach your children how to process the loss of a loved one. By modeling strategies for grief, your child will learn how to manage these feelings. Make your child aware of your own feelings, e.g., "I am having a really hard time today, I miss the person who died. Today I am going to look at some old pictures of them and then get outside for a walk. Would you like to do that with me?"  As hard as it is to see children grieving, it is crucial that parents/caregivers give them the tools to deal with grief in a positive way. As parents begin to show their children how to move through grief, they are setting their children up with the tools to become emotionally healthy individuals. – Cleo Guide, Saga Pappas """
#question = "How do I cope with child loss?"

#print(get_response(content,question))


