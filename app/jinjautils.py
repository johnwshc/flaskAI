
 from jinja2 import Environment, FileSystemLoader
from analz.blogger.er_blogger import ERBlogger as ERB, BloggerPost, BloggerPages, PodcastPost
# from analz.utils.podbeanapi import Podbean, PBPoetry as PBP, PBLabor as PBL, PBRecovery as PBR
# from analz.utils.podbeanapi import PBWNL as PBW, PBSports as PBS
from PIL import Image
from config import Config
from analz.ai.socgpt import Summary, Summaries
import requests

class JinjaUtils:


    def socEconSummarySection(self, summs: list, props: dict):
        tmpl = 'se_ai_post_content.html'
        summaries = summs


        self.sample_lenin_imagelnk = "https://pbs.twimg.com/media/FF_n1lPX0AcM207.jpg"
        try:

            im = Image.open(requests.get(props['imagelink'], stream=True).raw)
            print("got image: image width == ", im.width)
            w, h = im.size
            props['width'] = 450
            props['height'] = 350
            # print("template: ", props['template'])
            template = self.environment.get_template(tmpl)
            print("got template")
            print(f"type of summaries: {type(summaries)}")
            # dsumms = [s.to_dict() for s in summaries]

            html_content = template.render(summaries=summaries, props=props)

            props['post'] = html_content
            props['blogname'] = 'socialist-economics'
            bp = BloggerPost(self.erb, post_obj=props)
            res = bp.insert_new_post()

            return res


        except Exception as inst:
            print(inst)
            raise(inst)

    @staticmethod
    def get_ERPostTemplate(prps: dict):
        print(f" in get_ERPostTemplate")
        props = prps
        # print(f"props in jinjautils getERPostTemplate: {props}")
        # print("getting jinja utils")
        ju = JinjaUtils()
        erb = ju.erb
        print('getting image...')
        try:
            im = Image.open(requests.get(props['imagelink'], stream=True).raw)
            print("got image: image width == ", im.width)
            w, h = im.size
            props['width'] = w
            props['height'] = h
            # print("template: ", props['template'])
            template = ju.environment.get_template(props['template'])
            html_content = template.render(props=props)
            print(html_content)
            props['post'] = html_content
            bp = BloggerPost(erb, post_obj=props)
            res = bp.insert_new_post()
            return res

        except Exception as inst:
            print("got exception", str(inst))
            raise Exception(f"post of template to blogger fails: {inst}")

    def __init__(self):
        self.environment = Environment(loader=FileSystemLoader("f:/python_apps/flaskAI/app/templates/"))
        self.erb = ERB()

    @staticmethod
    def get_ERPagesTemplate(prps: dict):
        print(f" in get_ERPageTemplate")
        props = prps
        # print(f"props in jinjautils getERPageTemplate: {props}")
        # print("getting jinja utils")
        ju = JinjaUtils()
        erb = ju.erb
        print('getting image...')
        try:
            im = Image.open(requests.get(props['imagelink'], stream=True).raw)
            print("got image: image width == ", im.width)
            w, h = im.size
            props['width'] = w
            props['height'] = h
            print("template: ", props['template'])
            template = ju.environment.get_template(props['template'])
            html_content = template.render(props=props)
            # print(html_content)
            props['post'] = html_content
            bp = BloggerPages(erb, props)
            res = bp.insert_new_page()
            BloggerPages.log_playlist_post(res)

            print(f'response from blogger: \n {res}')
            # return props

        except Exception as inst:
            print("got exception", str(inst))
            raise Exception(f"post of template to blogger fails: {inst}")


    def getPodcastPostTemplate(self, ppost:PodcastPost):
            title = ppost.title
            bprops = ppost.bprops
            print("bprops incoming: ", bprops)
            print("invoking tmplate: ", bprops['template'])
            template = self.environment.get_template(bprops['template'])
            html_content = template.render(props=bprops)
            print(html_content)
            self.post = html_content
            # try:
            #     bp = BloggerPost(self.erb, post_obj=bprops)
            #     res = bp.insert_new_post()
            #     return res
            # except Exception as inst:
            #     raise Exception(f"insert to blogger failed: {inst}")
            # return bprops



    def socEconPostHTML2Blogger(self, props):
        ju = JinjaUtils()
        erb = ju.erb
        template = self.environment.get_template(props['template'])
        print('getting image...')
        try:
            im = Image.open(requests.get(props['imagelink'], stream=True).raw)
            print("got image: image width == ", im.width)
            w, h = im.size
            props['width'] = w
            props['height'] = h
            html_content = template.render(props=props)
            # print(html_content)
            props['post'] = html_content
            props['post'] = html_content
            bp = BloggerPost(erb, post_obj=props)
            res = bp.insert_new_post()
            return res

        except Exception as inst:
            print("got exception", str(inst))
            raise Exception(f"post of template to blogger fails: {inst}")






