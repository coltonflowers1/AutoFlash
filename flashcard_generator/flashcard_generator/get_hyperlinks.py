from collections import defaultdict
from typing import Dict, Iterable, List, Optional, Tuple
import spacy
import requests
from bs4 import BeautifulSoup as bs
from spacy import displacy
from spacy.ml import Doc
from spacy.tokens import SpanGroup
import spacy
import wikipedia
import wikipediaapi

def get_wiki_title(url):
    base_url = "https://en.wikipedia.org/w/api.php"
    page = url.replace("/wiki/", "")
    params = {
        "action": "query",
        "prop": "extracts",
        "format": "json",
        "exintro": True,
        "titles": page
    }
    response = requests.get(base_url, params=params)
    data = response.json()
    page_id = list(data['query']['pages'].keys())[0]
    title = data['query']['pages'][page_id]['title']
    return title

def get_offsets_and_title(paragraph)->List[Tuple[Tuple[int,int],str]]:
    paragraph_text = paragraph.get_text()
    offsets = []
    for link in paragraph.find_all("a"):
        url = link.get("href", "")
        if url[:6] == "/wiki/":
            link_text = link.string
            link_title = url
            if link_text:
                if link_text!= "citation needed":
                    start_offset = paragraph_text.index(link_text)
                    end_offset = start_offset + len(link_text)
                    offsets.append(((start_offset, end_offset),link_title))
    return offsets

def map_chars_to_tokens(doc:Doc)->Dict[int,int]:
    char_to_token = {}
    for token in doc:
        for char_idx in range(token.idx,token.idx+len(token)+1):
            char_to_token[char_idx] = token.i
    return char_to_token
        
        
def get_sentences_and_hyperlinks(soup)->List[List[Tuple[str,List[Tuple[str,str,Tuple[int,int]]]]]]:
    nlp = spacy.load("en_core_web_sm")
    paragraphs = soup.find_all("p")
    docs = nlp.pipe(paragraph.get_text() for paragraph in paragraphs)
    results = []
    for paragraph,doc in zip(paragraphs,docs):
        offsets_and_titles = get_offsets_and_title(paragraph)
        sentences_with_links=defaultdict(list)
        char_to_token = map_chars_to_tokens(doc)
        # print(paragraph.get_text())
        # print(list(doc.sents))
        for ((start,end),title) in offsets_and_titles :
            title = get_wiki_title(title)
            token_start = char_to_token[start]
            token_end = char_to_token[end]
            # print(doc[token_start].sent.text)
            if doc[token_start].sent == doc[token_end].sent:
                sent = doc[token_start].sent
                char_start = start - sent.start_char
                char_end = end - sent.start_char
                # print(char_start,char_end)
                # sentence_with_links = sent.text[:char_start] + "[" + sent.text[char_start:char_end] + "]" + sent.text[char_end:]
                sentences_with_links[sent.text].append((sent.text[char_start:char_end],title,(char_start,char_end)))
        for sentence in doc.sents:
            if sentence.text not in sentences_with_links:
                sentences_with_links[sentence.text] = []
        # print(sentences_with_links)
        results.append(sentences_with_links)
    
    return [[(key, values) for key,values in result.items()] for result in results]

def get_hyperlinked_page(topic)->List[List[Tuple[str,List[Tuple[str,str,Tuple[int,int]]]]]]:
    soup = get_beautiful_soup_for_wikipedia_page(topic)
    if soup:
        return get_sentences_and_hyperlinks(soup)
    else:
        raise ValueError("No page found for topic")
    
def get_beautiful_soup_for_wikipedia_page(topic)->Optional[bs]:
    page = get_page(topic)
    if page.fullurl:
        res = requests.get(page.fullurl)
        soup = bs(res.text, "html.parser")
        return soup
    else:
        return None

def get_page(topic):
    pages = wikipedia.search(topic)
    page = pages[0]
    wiki_html = wikipediaapi.Wikipedia('en')
    page = wiki_html.page(title=page)
    return page

    
def generate_html(sentences_with_offsets):
    html_sentences = []
    for sent_text, span_text, _ in sentences_with_offsets:
        span_html = f"<span style='color: red;'>{span_text}</span>"
        sent_html = sent_text.replace(span_text, span_html)
        html_sentences.append(sent_html)


# print(sentences)
# filtered_sentences = [sentence for sentence in sentences if len(sentence.text) < 500]

# links = set()
# urls = []
# for link in soup.find_all("a"):
#     url = link.get("href", "")
#     if "/wiki" in url:
#         urls.append(url)
#         links.add(link.text.strip())
# print(list(zip(links,urls))[:50])
# print(naval_battles)

# def get_texts(topic):
#     pages = wikipedia.search(topic)
#     page = pages[0]
#     # page = wikipedia.page(page,auto_suggest=False)
#     wiki_html = wikipediaapi.Wikipedia('en')
#     page = wiki_html.page(title=page)
#     # for link,page in page.links.items():
#     #     wiki_html.page(title=link.)
#     print(page.links)
    # texts = [page.summary]
    # for section in page.sections:
    #     if section.title not in ["See also","References","External links","Further reading","Selected works"]:
    #         texts.extend(get_html(section))
    # return texts
    # docs = nlp.pipe(texts)
    #     sentences = []
    #     for doc in docs:
    #         for sent in doc.sents:
    #             if len(sent.text) < 500:
    #                 sentences.append(sent.text)
    #     return sentences

# def get_html(section):
#     text = [section.text]
#     for section in section.sections:
#         text.extend(get_html(section))
#     return text
# # def parse_html(html):
    

# print(get_hyperlinked_page("Arizona"))