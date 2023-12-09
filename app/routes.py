import datetime

from app import app, sm, ju
from flask import render_template, redirect, url_for, flash, request, make_response
from analz.ai.socgpt import Summary, Summaries
from analz.forms.aiforms import (ReviewSESummaryForm as RSForm,
                                 PublishSummaryPageForm as PSForm,
                                 BuildMarxistSummariesForm as BMSForm
                                 )


# from analz.chatgpt.socgpt import NextRecessionPost, SocEconGPT, EContent

# ###############  index ER STATIC HOME   #################
@app.route('/')
@app.route('/index')
def index():
    return render_template('ai_class.html')

#  # Manage utilities
@app.route('/manage/build_marxist_summaries', methods=['GET', 'POST'])
def build_marxist_summaries():
    form = BMSForm()
    if form.validate_on_submit():
        data = request.form.to_dict()
        feed_ids = [data[k] for k in data.keys()]
        # for f in feed_ids:
        #     fid = f
        #     sm.setProdWorkFlow(fid,build=False)
        #     econtents = sm.econtents
        #     for e in econtents:
        #         print(e.title)
        return make_response(data, 207)

    return render_template('se_build_summaries.html', form=form)



@app.route('/manage')
def ai_mgmt():  # put application's code here
    return render_template('ai_manager.html', title='manager')

@app.route('/reporters', methods=['POST', 'GET'])
def reporters():
    return make_response("under construction", 200)

@app.route('/data', methods=['GET'])
def erdata():
    return make_response("under construction", 200)

@app.route('/manage/se_publish', methods=['GET', 'POST'])
def se_publish():
    form = PSForm()
    Summs: Summaries = sm.Summaries
    if form.validate_on_submit():
        props = request.form.to_dict()
        keys = props.keys()
        print('key val data from browser')
        for k in keys:
            print(f"key={k},  val={props[k]}")
        pub_summs = []
        print(f"db ids")
        for s in Summs.summaries:
            id = s.id
            print(f"db id: {id}")
            if id in keys:
                if props.get(id) == 'on':
                    pub_summs.append(s)

        sample_props = {
            'page_title': None,
            'about': None,
            'image_lnk': None
        }
        if pub_summs:
            props['title'] = props['page_title']
            res = ju.socEconSummarySection(pub_summs, props=props)
            for s in pub_summs:
                s.setPublished()
            Summs.saveSummaries()
            return make_response("success post to se_publish", 200)
        else:
            return make_response("No Summaries to publish", 207)
    else:
        return render_template('se_publish.html', summaries=Summs.summaries, form=form)


@app.route('/manage/review_summary', methods=['GET', 'POST'])
def se_review_summary():
    Summs: Summaries = sm.Summaries
    form = RSForm()
    if request.method == 'GET':
        sid = request.args.get('sid')
        if sid:
            summ = Summs.get_summary_by_id(sid)
            form.summary_text.data = summ.txt
            form.summary_id.data = summ.id
            return render_template('review_summary.html', form=form, summary=summ)
        else:
            return make_response("invalid summary id submitted", 403)
    else:
        dstr = ""
        data = request.form.to_dict()
        sid = data.get('sid')
        txt = data.get('summ_txt')
        summ = Summs.get_summary_by_id(sid)
        summ.txt = txt
        rsumm = Summs.remove_by_url(summ.url)
        Summs.add_summary(summ)
        Summs.saveSummaries()
        sm.Summaries = Summs

        return redirect('/manage/summaries')

@app.route('/manage/summaries', methods=['GET'])
def se_get_summaries():

    props = {
        'template':"se_summaries.html",
    }
    return render_template(props['template'], summaries=sm.Summaries.summaries)


# # ##############  Whats Playing from RDJ Web Export  ##############
@app.route('/manage/wprest', methods=['POST', 'GET'])
def wprest():
    print("in wprest")
    print(f"http method: {request.method}")
    content_type = request.headers.get('Content-Type')
    print(f"\nContent type: {content_type}")
    data = request.args.to_dict()
    print(f"wprest data: {data}")
    return redirect("/manage")

