from flashcard_generator.get_hyperlinks import get_beautiful_soup_for_wikipedia_page, get_page


examples = [
    {
        "question": "A financial crisis and widespread social distress led to the convocation of what in May 1789?",
        "answer": "Estates General",
        "quality": 'true',
         
    },
    {
        "flashcard_front": "Who started the design of the first automatic mechanical calculator, his ___________, in 1822?",
        "flashcard_back": "Charles Babbage",
        "quality": 'false',
        "reason": "Answer does not match question"
    },
    {
        "question":"Who may be considered the first ___________ because of various reasons?",
        "answer":"computer scientist",
        "quality_question": 'false',
        "reason":"Too vague"
    },
    {   "question": "Machines for calculating fixed numerical tasks such as the __ have existed since antiquity?",
        "answer": "abacus",
        "quality": 'false',
        "reason": "Not a question"
    }
    # {
    #     "topic": "Computer Science",
    #     "previous_sentence": "Computer science is the study of computation, information, and automation.[1][2][3]",
    #     "sentence":'Computer science spans theoretical disciplines (such as algorithms, theory of computation, and information theory) to applied disciplines (including the design and implementation of hardware and software).[4][5][6] Though more often considered an academic discipline, computer science is closely related to computer programming.[7]',
    #     "answer": "theoretical disciplines",
    #     "question": "Besides theoretical disciplines, which other discipline is integral to computer science?",
    # }
    # {
    #     "topic": "Computer Science",
    #     "previous_sentence": "Computer architecture describes the construction of computer components and computer-operated equipment.",
    #     "sentence":'Artificial intelligence and machine learning aim to synthesize goal-orientated processes such as problem-solving, decision-making, environmental adaptation, planning and learning found in humans and animals.',
    #     "answer": "Artificial intelligence",
    #     "question": "Machine learning and which other discipline aim to synthesize goal-oriented processes found in humans and animals?",
    # }
]
soup = get_beautiful_soup_for_wikipedia_page("Panama Canal")
page = get_page("Panama Canal")
print(page.links)