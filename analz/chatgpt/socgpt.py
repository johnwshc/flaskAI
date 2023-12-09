import openai
from config import Config
from analz.feeds.entries import Entry
from analz.ai.prompts import NRPrompts

class EContent:

    shared_token_limit = 4097  # OPENAI tokens shared between prompt and completion.
    shared_words_limit = shared_token_limit * .75
    prompt_token_limit = 250
    prompt_word_limit = prompt_token_limit * .75
    para_word_limit = 750
    para_token_limit = int(para_word_limit / .75)

    @staticmethod
    def words2tokens(words: str):
        numchars = len(words) # length of words in chars
        numwords = len(words.split(' '))
        numtokens = int(numwords / .75)  # approx
        return numtokens, numwords, numchars

    def __init__(self, entry: Entry):
        self.entry = entry


class NextRecessionPost(EContent):

    NR_feed_id = 'feed/http://thenextrecession.wordpress.com/feed/'
    NR_about = """
    Michael Roberts worked in the City of London as an economist 
    for over 40 years. He has closely observed the machinations 
    of global capitalism from within the dragon’s den. At the 
    same time, he was a political activist in the labour m
    ovement for decades. Since retiring, he has written several 
    books.  The Great Recession – a Marxist view (2009); 
    The Long Depression (2016); Marx 200: a review of Marx’s economics (2018): 
    and jointly with Guglielmo Carchedi as editors of World in Crisis (2018).  
    He has published numerous papers in various academic economic 
    journals and articles in leftist publications.
    """

    def __init__(self, entry: Entry):
        super().__init__(entry)
        print(type(entry))
        self.entry_texts = [p.para_text for p in entry.paras]
        self.orig_summary = entry.summary if entry.summary else "unavailable"
        self.summaries = []
        self.prompts = []
        self.title = entry.title

    def initialize(self):
        self.prompts = [NRPrompts.prompt_1(et).gpt_prompt for et in self.entry_texts]

    def run_recursive_chat(self, prompts: list, res=''):
        print(f"calling run_recursive_chat, num propmpts = {len(prompts)}")
        if len(prompts) > 0:
            p = prompts.pop()
            p = f"{res} {p}"
            response = SocEconGPT.get_completion(p)
            self.summaries.append(response)
            self.run_recursive_chat(prompts,res=response)
        else:
            return

# class for making gpt queries for soc econ
class SocEconGPT:
    openai.api_key = Config.OPENAI_SECRET_KEY

    @staticmethod
    def get_completion(prompt, model="gpt-3.5-turbo"):
        # Andrew mentioned that the prompt completion paradigm
        #     is preferable for this class

            messages = [{"role": "user", "content": prompt}]
            response = openai.ChatCompletion.create(
                model=model,
                messages=messages,
                temperature=0,  # this is the degree of randomness of the model's output
            )
            return response.choices[0].message["content"]







