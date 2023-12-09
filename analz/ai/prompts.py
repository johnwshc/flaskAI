from analz.ai.socgpt import Chunk, Prompt


class NRPrompts(Prompt):

    def __init__(self, chnk: Chunk):
        super().__init__(chnk)
        self.prompt = NRPrompts.prompt_1(self.txt)

    @staticmethod
    def prompt_1(etext):
        p = f"""
        Your task is to generate a detailed summary of text selected from an article \
                on an economics website named "Michael Roberts Blog" at \
                 the link "https://www.thenextrecession.wordpress.com". The text \
                 is delimited by triple backticks.\
                 Use at at least 100 and at most 300 words. \
                 Describe the two most important topics in the selected text.\
                Use at most 500 words. \
                article: ```{etext}```
                """
        return p

class GenSEPrompt:

    @staticmethod
    def prompt_1(etext):
        p = f"""
        Your task is to generate a detailed summary of an article \
                on an economics website. The text \
                 is delimited by triple backticks.\
                 Describe the  most important topics or facts in the article.\
                 Note mentions and context of these key words:\
                 - Marx\
                 - unions\
                 - socialism\
                 - communism\
                 - imperialism\
                 - capitalism\
                 - Marxism\
                Use at most 500 words in your summary. \
                Here is the selected text : ```{etext}```
                """
        return p

    @staticmethod
    def prompt_combine_summaries(etext):
        p = f"""
               Your task is to generate a detailed summary this extracted from a\
               text selected from a longer article \
                       on an economics website. The text \
                        is delimited by triple backticks.\
                        Describe the  most important topics or facts in the selected text.\
                        Note mentions of the key words below and include how many\
                        many times each were mentioned. Use a simple straightforward style.\
                        The key words are:\
                        - Marx\
                        - unions\
                        - socialism\
                        - communism\
                       Use at most 500 words in your summary. \
                       Here is the selected text : ```{etext}```
                       """
        return p













