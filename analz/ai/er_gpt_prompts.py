
class NRPrompts:

    def __init__(self, p):

        self.para = p
        self.prompt_str_1 =  f"""Your task is to generate a summary of text selected from an article \
                on an economics website. The website is called "Michael Roberts Blog" at \
                 the link "https://www.thenextrecession.wordpress.com". The text \
                 is delimited by triple backticks.\
                 Include a list of the two most important topics in the selected text.\
                Use at most {int(self.para.num_words / 3)} words. \
                article: ```{p.txt}```
                """

class EQPrompts:
    def __init__(self, p):

        self.para = p
        self.prompt_str_1 =  f"""Your task is to generate a summary of text selected from an article \
                on an economics website. The website is called "Michael Roberts Blog" at \
                 the link "https://www.thenextrecession.wordpress.com". The text \
                 is delimited by triple backticks.\
                 Include a list of the two most important topics in the selected text.\
                Use at most {int(self.para.num_words / 3)} words. \
                article: ```{p.txt}```
                """
