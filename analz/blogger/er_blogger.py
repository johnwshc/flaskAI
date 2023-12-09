from googleapiclient import sample_tools
from oauth2client import client

from analz.utils.podbeanapi import Podbean
from config import Config


class ERBlogger:
    sample_post_data = {
        'blogname': 'Enlighten Radio',
        'email': 'jcase4218@gmail.com',
        'template': 'er_post_content.html',
        'title': 'A big Deal',
        'post': '<h1> One Hell of a big deal occurred in timezone 0, shaking the foundations of the universe.</h1>',
        'imagelink': "https://pbs.twimg.com/media/FF_n1lPX0AcM207.jpg"
    }
    BlogNames = ['Enlighten Radio Player', 'Enlighten Radio', 'socialist-economics',
                 'The Storytelling Hour with Fanny Crawford and Stas Ziolkowski',
                 'ER Warehouse Reporter', 'Enlighten Radio Podcasts', 'Recovery Radio',
                 'The Poetry Show with Janet Harrison']

    wp_post_id = '6424181253444860473'
    # google_analytics_acct_id = '17860178'
    my_avatar_url = "https://lh3.googleusercontent.com/a/ALm5wu25FWOeBFYnxDZtT0lNqzXu7LuhftYzOaU5aZixIg=s360-p-rw-no"
    my_profile_page = "https://myaccount.google.com/profile/profiles-summary"

    def __init__(self):

        self.argv = ['analz\\\\blogger\\\\er_blogger.py', '--logging_level=DEBUG']
        self.scope = 'https://www.googleapis.com/auth/blogger'
        self.version = 'v3'
        self.doc = 'enlighten radio blogger app'
        self.API = 'blogger'
        self.service, self.flags = sample_tools.init(self.argv,
                                                     self.API,
                                                     self.version,
                                                     self.doc,
                                                     __file__,
                                                     scope=self.scope)
        try:
            self.user = self.service.users().get(userId='self').execute()
            self.display_name = self.user['displayName']
            self.blogs = self.service.blogs().listByUser(userId='self').execute()
            self.blogs_idx = {b['name']: b['id'] for b in self.blogs['items']}
            self.BlogNames = self.blogs_idx.keys()
            self.er_blog_id = self.blogs_idx['Enlighten Radio']
            self.plr_blog_id = self.blogs_idx['Enlighten Radio Player']
            self.posts = self.service.posts()
            self.pages = self.service.pages()
        except client.AccessTokenRefreshError:
            print('The credentials have been revoked or expired, please re-run'
                  'the application to re-authorize')

    def get_er_pages(self):
        pages = self.service.pages()
        request = pages.list(blogId=self.er_blog_id)
        pages_list = []
        while request != None:
            pages_doc = request.execute()
            if 'items' in pages_doc and not (pages_doc['items'] is None):
                for page in pages_doc['items']:
                    # print('  %s (%s)' % (post['title'], post['url']))
                    pages_list.append(page)
            request = pages.list_next(request, pages_doc)
        return pages_list

        # if id and len(ids) > 0:
        #     posts_by_id = []
        #     for p in posts_list:
        #         if p['id'] in ids:
        #             posts_by_id.append(p)
        #     return posts_by_id
        # else:
        #     return posts_list

    def get_player_posts(self, ids=[]):
        posts = self.service.posts()
        request = posts.list(blogId=self.plr_blog_id)
        posts_list = []
        while request != None:
            posts_doc = request.execute()
            if 'items' in posts_doc and not (posts_doc['items'] is None):
                for post in posts_doc['items']:
                    # print('  %s (%s)' % (post['title'], post['url']))
                    posts_list.append(post)
            request = posts.list_next(request, posts_doc)
        if id and len(ids) > 0:
            posts_by_id = []
            for p in posts_list:
                if p['id'] in ids:
                    posts_by_id.append(p)
            return posts_by_id
        else:
            return posts_list


class BloggerPost:
    wp_id = ''

    def __init__(self, erb: ERBlogger, post_obj: dict = None):
        self.props = post_obj

        self.post_obj_template = {
            'blogname': str,
            'title': str,
            'content': str,  # HTML
        }
        self.erb = erb

        self.author_id = '01595792808567356923'

        self.creator_url = "https://lh3.googleusercontent.com/a/ALm5wu25FWOeBFYnxDZtT0lNqzXu7LuhftYzOaU5aZixIg=s360-p-rw-no"

        self.test_content = "<h2>A New -- communist -- Post and image on the Player Blog</h2>"
        if post_obj:
            self.content = post_obj['post']
        else:
            self.content = self.test_content

    def insert_new_post(self):
        # insert(blogId, body=None, fetchBody=None, fetchImages=None, isDraft=None, x__xgafv=None)
        # Inserts a post.
        #
        # Args:
        # blogId: string, A parameter(required)
        # body: object, The request body.
        blogid = self.erb.blogs_idx[self.props['blogname']]
        body_obj = self.buildBodyObj()
        return self.erb.posts.insert(blogId=blogid,
                                     body=body_obj,
                                     fetchBody=None,
                                     fetchImages=None,
                                     isDraft=True,
                                     x__xgafv='2').execute()

    def buildBodyObj(self):

        return {
            "kind": "blogger#post",
            "title": self.props['title'],
            "content": self.content,

        }


class BloggerPages:
    sample_page_obj = {
        'blogname': 'Enlighten Radio',
        'title': 'Test Page',
        'post': '<div><H1> test page </h1></div>'
    }

    @staticmethod
    def log_playlist_post(res: dict):
        import json
        import threading
        log_fn = Config.PL_JSON_LOG
        evt = dict()
        evt['status'] = res['status']
        evt['url'] = res['url']
        evt['id'] = res['id']
        title = res['title']
        lock = threading.Lock()
        try:
            lock.acquire()
            with open(log_fn) as f:
                dlog = json.load(f)
                dlog[title] = evt

            with open(log_fn,"w") as f:
                json.dump(dlog, f)
            lock.release()
        except Exception as inst:
            print(f"got exception: {inst}")





    def __init__(self, erb: ERBlogger, page_obj: dict = None):
        if page_obj:
            self.props = page_obj
        else:
            self.props = BloggerPages.sample_page_obj

        self.post_obj_template = {
            'blogname': str,
            'title': str,
            'content': str,  # HTML
        }
        self.erb = erb

        self.author_id = '01595792808567356923'

        self.creator_url = "https://lh3.googleusercontent.com/a/ALm5wu25FWOeBFYnxDZtT0lNqzXu7LuhftYzOaU5aZixIg=s360-p-rw-no"

        self.test_content = "<h2>A New -- communist -- Page and image on the Player Blog</h2>"
        self.content = self.props['post']


    def insert_new_page(self):
        # {
        #     "kind": "blogger#page",
        #     "id": string,
        #     "status": string,
        #     "blog": {
        #         "id": string
        #     },
        #     "published": datetime,
        #     "updated": datetime,
        #     "url": string,
        #     "selfLink": string,
        #     "title": string,
        #     "content": string,
        #     "author": {
        #         "id": string,
        #         "displayName": string,
        #         "url": string,
        #         "image": {
        #             "url": string
        #         }
        #     }
        # }
        blogid = self.erb.blogs_idx[self.props['blogname']]
        body_obj = self.buildBodyObj()
        print(f"insert new page: body: {body_obj}")
        return self.erb.pages.insert(blogId=blogid,
                                     body=body_obj,
                                     # fetchBody=None,
                                     #
                                     # fetchImages=None,isDraft=True,
                                     x__xgafv='2').execute()

    def buildBodyObj(self):

        return {
            "kind": "blogger#page",
            "title": self.props['title'],
            "content": self.content,

        }


class PodcastPosts:
    def __init__(self, max=7):
        self.pods = []
        self.pb = Podbean()

        self.recent_posts, self.msg = self.pb.getEpisodes(max)
        self.episodes = self.recent_posts['episodes']
        for e in self.episodes:
            pod = PodcastPost(e, email=Config.ADMIN_EMAIL)
            self.pods.append(pod)


class PodcastPost:
    def __init__(self, eprops: dict, email):
        from app.jinjatuils import JinjaUtils as JU
        self.ju = JU()
        self.eprops = eprops
        self.erb = self.ju.erb
        self.pbid = eprops['id']
        self.blogid = self.erb.blogs_idx['Enlighten Radio Podcasts']
        self.email = email
        self.title = eprops['title']
        self.logo = eprops['logo']
        self.media_url = eprops['media_url']
        self.player_url = eprops['player_url']
        # self.player_html = requests.get(self.player_url)
        self.post = eprops['content']
        self.permalink_url = eprops['permalink_url']
        self.publish_time = eprops['publish_time']
        self.status = eprops['status']
        self.type = eprops['type']
        self.duration = eprops['duration']
        self.content_explicit = eprops['content_explicit']
        self.template = 'podbeanpost.html'
        self.bprops = {
            'blogname': 'Enlighten Radio Podcasts',
            'email': self.email,
            'template': Config.ERPOD_POST_TEMPLATE,
            'title': self.title,
            'post': self.post,
            'player_url': self.player_url,
        }

    def renderPodTemplate(self):
        self.post = self.ju.getPodcastPostTemplate(self)
        # self.post = self.template_render

    @staticmethod
    def get_podcast_post_by_id(pid):
        pb = Podbean()
        eps = pb.getPodcast_by_id(pid)
        pp = PodcastPost(eps, Config.ADMIN_EMAIL)
        return pp

    @staticmethod
    def get_podcast_post_by_title(title):
        pb = Podbean()
        id, tit, eps = pb.get_podcast_by_title(title)
        pp = PodcastPost(eps, Config.ADMIN_EMAIL)
        return pp

    def insert_new_podcast(self):
        # insert(blogId, body=None, fetchBody=None, fetchImages=None, isDraft=None, x__xgafv=None)
        # Inserts a post.
        #
        # Args:
        # blogId: string, A parameter(required)
        # body: object, The request body.

        body_obj = self.buildBodyObj()
        return self.erb.posts.insert(blogId=self.blogid,
                                     body=body_obj,
                                     fetchBody=None,
                                     fetchImages=None,
                                     isDraft=True,
                                     x__xgafv='2').execute()

    def buildBodyObj(self):
        return {
            "kind": "blogger#post",
            "title": self.title,
            "content": self.post,

        }
