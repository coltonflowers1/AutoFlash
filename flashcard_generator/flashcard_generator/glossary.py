#ask questions wrt to the hyperlinks of a wikipedia page.
#include hyperlink with text in prompt and tell the llm to ask a question wrt to the hyperlink entity. 
#TODO: add a function to get the hyperlinks of a wikipedia page.

import itertools
import re
from flashcard_generator.get_hyperlinks import get_hyperlinked_page
from langchain import FewShotPromptTemplate
from langchain.llms import LlamaCpp
from typing import Generator

from langchain.prompts import PromptTemplate
from langchain.schema.output_parser import StrOutputParser
import spacy
from flashcard_generator.sentence_retrieval_wiki import get_sentences
import spacy
import wikipedia
import wikipediaapi
# Splitting the description into individual topics

llm = LlamaCpp(
    model_path="/Users/coltonflowers/LLAMA2/llama.cpp/models/llama-2-13b-chat/ggml-model.gguf.q4_0.bin",
    n_gpu_layers=1,
    n_batch=512,
    n_ctx=1024,
    max_tokens=2048,
    verbose=False,
    f16_kv=True,
)


examples = [
    {
        "topic": "French Revolution",
        "previous_sentence": "Four years later in November 1799, the Consulate seized power in a military coup led by Napoleon Bonaparte.",
        "sentence": "A financial crisis and widespread social distress led, in May 1789, to the convocation of the Estates General which was converted into a National Assembly in June.",
        "answer": "Estates General",
        "question": "A financial crisis and widespread social distress led to the convocation of what in May 1789?"
         
    },
    {
        "topic": "Bell's Theorem",
        "previous_sentence": "Bell's theorem is a no-go theorem that draws an important distinction between quantum mechanics (QM) and the world as described by classical mechanics, particularly concerning quantum entanglement.",
        "sentence": 'The term is broadly applied to a number of different derivations, the first of which was introduced by Bell in a 1964 paper titled "On the Einstein Podolsky Rosen Paradox."',
        "answer":'Einstein Podolsky Rosen Paradox',
        "question": 'Bell introduced a derivation in a 1964 paper titled "On the __?',
    },
    # {
    #     "topic": "Functional group",
    #     "previous_sentence": "Functional groups can also be charged, e.g. in carboxylate salts (−COO−), which turns the molecule into a polyatomic ion or a complex ion.",
    #     "sentence":'For example, sugar dissolves in water because both share the hydroxyl functional group (−OH) and hydroxyls interact strongly with each other.',
    #     "answer": "hydroxyl",
    #     "question": "What functional group do sugar and water share?",
    # },
    # {
    #     "topic": "Computer Science",
    #     "previous_sentence": "Computer science is the study of computation, information, and automation.[1][2][3]",
    #     "sentence":'Computer science spans theoretical disciplines (such as algorithms, theory of computation, and information theory) to applied disciplines (including the design and implementation of hardware and software).[4][5][6] Though more often considered an academic discipline, computer science is closely related to computer programming.[7]',
    #     "answer": "theoretical disciplines",
    #     "question": "Besides theoretical disciplines, which other discipline is integral to computer science?",
    # }
    {
        "topic": "Computer Science",
        "previous_sentence": "Computer architecture describes the construction of computer components and computer-operated equipment.",
        "sentence":'Artificial intelligence and machine learning aim to synthesize goal-orientated processes such as problem-solving, decision-making, environmental adaptation, planning and learning found in humans and animals.',
        "answer": "Artificial intelligence",
        "question": "Machine learning and which other discipline aim to synthesize goal-oriented processes found in humans and animals?",
    }
]


eg_template = """
topic: {topic}
previous sentence: {previous_sentence}
sentence: {sentence}
answer: {answer}
question: {question}

[END]
"""
example_prompt = PromptTemplate(
    input_variables=["topic","previous_sentence","sentence", "answer","question"], template=eg_template
)

prompt = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    suffix="topic: {topic}\nprevious_sentence: {previous_sentence}\nsentence: {sentence}\nanswer: {answer}\nquestion:",
    input_variables=["topic","previous_sentence","sentence","answer"],
)
# Generating flashcards
flashcards = []
llm_chain = prompt | llm.bind(stop=["[END]"]) | StrOutputParser()


def get_flashcard(topic, previous_sentence,sentence,answer):
    response = llm_chain.invoke({"topic":topic,"previous_sentence":previous_sentence,"sentence":sentence,"answer":answer}).strip()
    question = response.split("\n")[0]
    return question, answer

# topic = "Barack Obama"
# previous_sentence = "Barack Obama served as the 44th President of the United States from 2009 to 2017."
# sentence = "He is a member of the Democratic Party and is known for his healthcare reform, foreign policy initiatives, and economic stimulus measures."
# answer = "Democratic Party"
# question, answer = get_flashcard(topic, previous_sentence, sentence, answer)
# print(f"Question: {question}")
# print(f"Answer: {answer}")


def _get_flashcards(topic)->Generator[tuple[str,str],None,None]:
    hyperlinked_page = get_hyperlinked_page(topic)
    for paragraph in hyperlinked_page:
        # print(paragraph)
        for i in range(len(paragraph)-1):
            previous_sentence = paragraph[i][0]
            sentence,hyperlinks = paragraph[i+1]
            if len(hyperlinks) > 0:
                hyperlink = hyperlinks[0]
                if sentence != "" and previous_sentence!="" and len(sentence) + len(previous_sentence) < 500:
                    try:
                        question,_ =  get_flashcard(topic,previous_sentence,sentence,hyperlink)
                        # print(question,hyperlink)
                        # print(question)
                        if "which of the following" not in question.lower() and "known for" not in question and "what is true" not in  question.lower() and "sentence" not in  question.lower() and "refers to" not in  question.lower() and "refered to" not in  question.lower() and "this" not in question.lower():
                            if hyperlink.lower() not in question.lower():
                                print(
                                      previous_sentence+"\n-------------------\n",
                                      sentence+"\n-------------------\n",
                                      question+"\n-------------------\n",
                                      hyperlink+"\n\n\n"
                                      )
                                yield question,hyperlink
                    except:
                        continue
                
                
                    
def get_flashcards(topic, num_flashcards=10):
    for flashcard in itertools.islice(_get_flashcards(topic),num_flashcards):
        yield {"front": flashcard[0], "back": flashcard[1]}

if __name__ == "__main__":
    flashcards = get_flashcards("Easter",num_flashcards=20)
    for flashcard in flashcards:
        pass
        # print(f"{flashcard["front"]}\n{flashcard["back"]}\n-------------------")