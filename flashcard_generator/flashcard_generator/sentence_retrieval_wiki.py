import spacy
import wikipedia
import wikipediaapi

nlp = spacy.load("en_core_web_sm")

def get_text(section):
    text = [section.text]
    for section in section.sections:
        text.extend(get_text(section))
    return text

def get_sentences(topic):
    pages = wikipedia.search(topic)
    page = pages[0]
    # page = wikipedia.page(page,auto_suggest=False)
    wiki_wiki = wikipediaapi.Wikipedia('en')
    page = wiki_wiki.page(title=page)
    texts = [page.summary]
    for section in page.sections:
        if section.title not in ["See also","References","External links","Further reading","Selected works"]:
            texts.extend(get_text(section))
    docs = nlp.pipe(texts)
    sentences = []
    for doc in docs:
        for sent in doc.sents:
            if len(sent.text) < 500:
                sentences.append(sent.text)
    return sentences

# if __name__ == "__main__":
#     topic = "Frank Lloyd Wright"
#     print(get_sentences(topic))
#     print(page.section("Early life and education"))
#     [sent.text for sent in nlp(page.summary).sents]