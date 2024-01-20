#ask questions wrt to the hyperlinks of a wikipedia page.
#include hyperlink with text in prompt and tell the llm to ask a question wrt to the hyperlink entity. 
#TODO: add a function to get the hyperlinks of a wikipedia page.

import itertools
import re
from langchain import FewShotPromptTemplate
from langchain.llms import LlamaCpp
from typing import Generator

from langchain.prompts import PromptTemplate
from langchain.schema.output_parser import StrOutputParser
import spacy
from flashcard_generator.sentence_retrieval_wiki import get_sentences
# Splitting the description into individual topics

llm = LlamaCpp(
    model_path="/Users/coltonflowers/LLAMA2/llama.cpp/models/llama-2-13b-chat/ggml-model.gguf.q4_0.bin",
    n_gpu_layers=1,
    n_batch=512,
    max_tokens=2048,
    verbose=False,
    f16_kv=True,
)


examples = [
    {
        "topic": "French Revolution",
        "previous_sentence": "Four years later in November 1799, the Consulate seized power in a military coup led by Napoleon Bonaparte.",
        "sentence": "This is generally seen as marking the end of the Revolutionary period.",
        "question": "What event marked the end of the Revolutionary period?",
        "answer":"The Consulate seizing power in a military coup led by Napoleon Bonaparte."
    },
    # {
    #     "topic": "French Revolution",
    #     "sentence": "The French Revolution[a] was a period of political and societal change in France that began with the Estates General of 1789, and ended with the coup of 18 Brumaire on November 1799 and the formation of the French Consulate.",
    #     "question": "When was the estates general formed?",
    #     "answer":"1789"
    # },
    # {
    #     "topic": "Jewish Autonomous Oblast",
    #     "wikipedia_sentence": "By 2010, according to census data, there were only approximately 1,600 people of Jewish descent remaining in the JAO (or just under 1% of the total population of the JAO and around 1% of Jews in the country), while ethnic Russians made up 93% of its population.[15] According to the 2021 census, there were only 837 ethnic Jews left in the JAO (0.6%).",
    #     "question": "In present day, what ethnic group mainly comprises the JAO?",
    #     "answer":"Russians"
    # },
    # {
    #     "topic": "Mary Shelley",
    #     "previous_sentence": "Shelley was the daughter of the political philosopher William Godwin and the writer Mary Wollstonecraft, who died a month after her birth.",
    #     "sentence": 'Until the 1970s, Shelley was known mainly for her efforts to publish her husband\'s works and for her novel Frankenstein, which remains widely read and has inspired many theatrical and film adaptations.',
    #     "question": "Until the 1970s, what was Mary Shelley mainly known for?",
    #     "answer":'Her efforts to publish her husband\'s works and for her novel Frankenstein.'
    # },
    {
        "topic": "Bell's Theorem",
        "previous_sentence": "Bell's theorem is a no-go theorem that draws an important distinction between quantum mechanics (QM) and the world as described by classical mechanics, particularly concerning quantum entanglement.",
        "sentence": 'The term is broadly applied to a number of different derivations, the first of which was introduced by Bell in a 1964 paper titled "On the Einstein Podolsky Rosen Paradox."',
        "question": "What was the title of Bell's 1964 paper?",
        "answer":'"On the Einstein Podolsky Rosen Paradox."'
    },

    # Additional decks can be added similarly
]

eg_template = """
topic: {topic}
previous_sentence: {previous_sentence}
sentence: {sentence}
question: {question}
answer: {answer}
[END]
"""
example_prompt = PromptTemplate(
    input_variables=["topic","previous_sentence", "sentence", "question","answer"], template=eg_template
)

prompt = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    suffix="topic: {topic}\nprevious_sentence:{previous_sentence}\nsentence:{sentence}\nquestion:",
    input_variables=["topic", "previous_sentence","sentence"],
)
# Generating flashcards
flashcards = []
llm_chain = prompt | llm.bind(stop=["[END]"]) | StrOutputParser()

def get_flashcard(topic, previous_sentence,sentence):
    response = llm_chain.invoke({"topic":topic,"previous_sentence":previous_sentence,"sentence":sentence}).strip()
    question = response.split("\n")[0]
    answer = response.split("\n")[1].split(":")[1].strip().strip(".")
    # return response
    return question, answer