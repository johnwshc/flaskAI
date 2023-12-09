from flask_wtf import FlaskForm
from wtforms import (StringField, TextAreaField, HiddenField, IntegerField, BooleanField,
                     RadioField, SelectField, SelectMultipleField)
from wtforms.validators import InputRequired, Length
from app import sm
from config import Config
# import os
# from config import Config
# from analz.chatgpt.gpt_tests import SummaryManager as SM
# from analz.ai.socgpt import Summary, Summaries


class BuildMarxistSummariesForm(FlaskForm):
    gt = sm.gt
    m_feeds = gt.get_marxist_feed_ids()
    my_choices = [(v, k) for k, v  in m_feeds.items()]
    b_feeds = gt.get_mainstream_feed_ids()
    my_choices2 = [(v, k) for k, v in b_feeds.items()]
    feeds = SelectMultipleField('Marxist Feeds -- OpenAI Assisted Summarization',
                                  choices=my_choices
                                )
    ms_feeds = SelectMultipleField("Bourgeois Economic Feeds -- OpenAI Assisted Summarization",
                                   choices=my_choices2
                                   )


class PublishSummaryPageForm(FlaskForm):

    page_title = StringField('Summaries Page Title',
                             description='title for summaries post to Marxist Summaries',
                             validators=[InputRequired(),
                                         Length(min=5, max=100)])
    about = TextAreaField('About', description=f"Editor's Notes",
                          validators=[InputRequired(),
                                      Length(min=10, max=500)])
    imagelink = StringField("Page Image",
                            description="top image for Marxist Summaries",
                            validators=[InputRequired(), Length(min=10, max=200)]
                            )



class ReviewSESummaryForm(FlaskForm):
    summary_text = TextAreaField("Summary Text",
                                 description="Review/Edit summary text",
                                 validators=[InputRequired(),
                                             Length(min=10, max=40000)])
    summary_id = HiddenField("Summary_id", validators=[InputRequired(),
                                             Length(min=10, max=120)])


#
# class PBPoetryPublishForm(FlaskForm):
#     title = StringField('Title', validators=[InputRequired(),
#                                              Length(min=10, max=100)])
#     dir = Config.WNL_DIR
#     fnames = os.listdir(dir)
#     poetry_audio_names = [f for f in fnames if f.startswith('poet')]
#     choices_tuples = [(f, f) for f in poetry_audio_names]
#
#     filename = SelectField('Audio File', validators=[InputRequired()], choices=choices_tuples)
#     description = TextAreaField('Description',
#                                 validators=[InputRequired(),
#                                             Length(max=500)])
#     broadcast = StringField('Broadcast Info', validators=[InputRequired(), Length(max=80)])
#     rec_date = StringField('Recording Date', validators=[InputRequired(), Length(max=40)])
#     image_url = StringField("image url", validators=[InputRequired(), Length(max=160)])
#     headline = StringField("headline", validators=[InputRequired(), Length(max=160)])
#     hosts = StringField('Add Host(s) csv', validators=[Length(max=80)])
#     guests = StringField('Guests (csv)', validators=[Length(max=80)])
#     poem_names_dir = os.path.join(Config.basedir, 'show_resources/poetry')
#     poem_choices = [(f, f) for f in os.listdir(poem_names_dir) if f.startswith('poem')]
#     poem = SelectField('Poem of the Week', validators=[InputRequired()], choices=poem_choices)
#     poem_title = StringField('Poem Title', validators=[InputRequired(), Length(max=80)])
#     poet = StringField('Poet', validators=[InputRequired(), Length(max=80)], default="Homer")
