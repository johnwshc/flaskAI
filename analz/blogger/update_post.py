from analz.blogger.er_blogger import ERBlogger

class WPPost:
    sample_txt = """<div style="background-color: darkgreen; border: 2px solid black; color: bisque; padding-bottom: 50px; padding-left: 80px; padding-right: 30px; padding-top: 50px; padding: 50px 30px 50px 80px;">
 <h2 style="font-size: x-large; text-align: center;">Updated default test content</h2></div>"""

    def __init__(self, txt=sample_txt):
        self.post_obj = {
            "kind": "blogger#post",
            "id": UpdatePlayerPost.wp_post_id,
            "title": "What's Playing Now?",
            "content": txt

        }
    def getPostObj(self):
        return self.post_obj


class UpdatePlayerPost():
    # TODO update wp_post_id to get last post id from mongo
    wp_post_id = '6424181253444860473'
    wp_post_title = "What's Playing Now?"

    def __init__(self, erb:ERBlogger, post_id:str=wp_post_id, title:str=wp_post_title, post_obj:dict=None):

        if "wp" in list(post_obj.keys()):
            post_obj['content'] = post_obj['wp']

        print(f"init UpdatePlayerPost: post_id: {post_id}, title: {title}, post_obj: {str(post_obj)}")

        # init UPP:
        # post_id: 6424181253444860473,
        # title: What's Playing Now?,
        # post_obj: {'wp': 'BR549 - Too Lazy To Work, Too Nervous To Steal'}
        self.pid = post_id
        self.title = title
        self.erb = erb
        print(f"")
        self.body = self.buildUpdateObj(post_content=post_obj)

    def update(self):
        request = self.erb.posts.update(blogId=self.erb.plr_blog_id, postId=self.pid, body=self.body)
        print(f"in  update: ")
        res = request.execute()
        try:
            rres = self.log_response(res)
        except Exception as  inst:
            print(f"error logging update {inst}")
        return res

    def log_response(self, r:dict):
        return {
            'status': r.get('status', None),
            'post_id': r.get('post_id',None),
            'blog':r.get('blog', None),
            'published': r.get('published', None),
            'updated': r.get('updated', None),
            'url': r.get('url', None),
            'title': r.get('title', None),
            'content': r.get('content', None),
            'author_id': r.get('author', None),
        }

    def buildUpdateObj(self, post_content: dict=None):
        p_text = f"<div> <h2>updated default test content</h2></div>"
        if post_content:
            p_text = post_content['content']
        htm_content = f"""<p>Note: "What's playing" does not automatically refresh on Blogger....</p><div style="background-color: darkgreen; border: 3px solid rgb(115, 173, 33); color: ivory; margin: auto; padding: 10px; text-align: center; width: 80%;">
  <p style="font-size: large; font-weignt: bold;">{p_text}</p>
</div>"""
        return {
            "kind": "blogger#post",
            "id": self.pid,
            "title": self.title,
            "content": htm_content
        }


update_template = """
    update(blogId, postId, body=None, fetchBody=None, fetchImages=None, maxComments=None, publish=None, revert=None, x__xgafv=None)
Updates a post by blog id and post id.

Args:
  blogId: string, A parameter (required)
  postId: string, A parameter (required)
  body: object, The request body.
    The object takes the form of:

{
  "author": { # The author of this Post.
    "displayName": "A String", # The display name.
    "id": "A String", # The identifier of the creator.
    "image": { # The creator's avatar.
      "url": "A String", # The creator's avatar URL.
    },
    "url": "A String", # The URL of the creator's Profile page.
  },
  "blog": { # Data about the blog containing this Post.
    "id": "A String", # The identifier of the Blog that contains this Post.
  },
  "content": "A String", # The content of the Post. May contain HTML markup.
  "customMetaData": "A String", # The JSON meta-data for the Post.
  "etag": "A String", # Etag of the resource.
  "id": "A String", # The identifier of this Post.
  "images": [ # Display image for the Post.
    {
      "url": "A String",
    },
  ],
  "kind": "A String", # The kind of this entity. Always blogger#post.
  "labels": [ # The list of labels this Post was tagged with.
    "A String",
  ],
  "location": { # The location for geotagged posts.
    "lat": 3.14, # Location's latitude.
    "lng": 3.14, # Location's longitude.
    "name": "A String", # Location name.
    "span": "A String", # Location's viewport span. Can be used when rendering a map preview.
  },
  "published": "A String", # RFC 3339 date-time when this Post was published.
  "readerComments": "A String", # Comment control and display setting for readers of this post.
  "replies": { # The container of comments on this Post.
    "items": [ # The List of Comments for this Post.
      {
        "author": { # The author of this Comment.
          "displayName": "A String", # The display name.
          "id": "A String", # The identifier of the creator.
          "image": { # The creator's avatar.
            "url": "A String", # The creator's avatar URL.
          },
          "url": "A String", # The URL of the creator's Profile page.
        },
        "blog": { # Data about the blog containing this comment.
          "id": "A String", # The identifier of the blog containing this comment.
        },
        "content": "A String", # The actual content of the comment. May include HTML markup.
        "id": "A String", # The identifier for this resource.
        "inReplyTo": { # Data about the comment this is in reply to.
          "id": "A String", # The identified of the parent of this comment.
        },
        "kind": "A String", # The kind of this entry. Always blogger#comment.
        "post": { # Data about the post containing this comment.
          "id": "A String", # The identifier of the post containing this comment.
        },
        "published": "A String", # RFC 3339 date-time when this comment was published.
        "selfLink": "A String", # The API REST URL to fetch this resource from.
        "status": "A String", # The status of the comment (only populated for admin users).
        "updated": "A String", # RFC 3339 date-time when this comment was last updated.
      },
    ],
    "selfLink": "A String", # The URL of the comments on this post.
    "totalItems": "A String", # The count of comments on this post.
  },
  "selfLink": "A String", # The API REST URL to fetch this resource from.
  "status": "A String", # Status of the post. Only set for admin-level requests.
  "title": "A String", # The title of the Post.
  "titleLink": "A String", # The title link URL, similar to atom's related link.
  "trashed": "A String", # RFC 3339 date-time when this Post was last trashed.
  "updated": "A String", # RFC 3339 date-time when this Post was last updated.
  "url": "A String", # The URL where this Post is displayed.
}

  fetchBody: boolean, A parameter
  fetchImages: boolean, A parameter
  maxComments: integer, A parameter
  publish: boolean, A parameter
  revert: boolean, A parameter
  x__xgafv: string, V1 error format.
    Allowed values
      1 - v1 error format
      2 - v2 error format

Returns:
  An object of the form:

    {
  "author": { # The author of this Post.
    "displayName": "A String", # The display name.
    "id": "A String", # The identifier of the creator.
    "image": { # The creator's avatar.
      "url": "A String", # The creator's avatar URL.
    },
    "url": "A String", # The URL of the creator's Profile page.
  },
  "blog": { # Data about the blog containing this Post.
    "id": "A String", # The identifier of the Blog that contains this Post.
  },
  "content": "A String", # The content of the Post. May contain HTML markup.
  "customMetaData": "A String", # The JSON meta-data for the Post.
  "etag": "A String", # Etag of the resource.
  "id": "A String", # The identifier of this Post.
  "images": [ # Display image for the Post.
    {
      "url": "A String",
    },
  ],
  "kind": "A String", # The kind of this entity. Always blogger#post.
  "labels": [ # The list of labels this Post was tagged with.
    "A String",
  ],
  "location": { # The location for geotagged posts.
    "lat": 3.14, # Location's latitude.
    "lng": 3.14, # Location's longitude.
    "name": "A String", # Location name.
    "span": "A String", # Location's viewport span. Can be used when rendering a map preview.
  },
  "published": "A String", # RFC 3339 date-time when this Post was published.
  "readerComments": "A String", # Comment control and display setting for readers of this post.
  "replies": { # The container of comments on this Post.
    "items": [ # The List of Comments for this Post.
      {
        "author": { # The author of this Comment.
          "displayName": "A String", # The display name.
          "id": "A String", # The identifier of the creator.
          "image": { # The creator's avatar.
            "url": "A String", # The creator's avatar URL.
          },
          "url": "A String", # The URL of the creator's Profile page.
        },
        "blog": { # Data about the blog containing this comment.
          "id": "A String", # The identifier of the blog containing this comment.
        },
        "content": "A String", # The actual content of the comment. May include HTML markup.
        "id": "A String", # The identifier for this resource.
        "inReplyTo": { # Data about the comment this is in reply to.
          "id": "A String", # The identified of the parent of this comment.
        },
        "kind": "A String", # The kind of this entry. Always blogger#comment.
        "post": { # Data about the post containing this comment.
          "id": "A String", # The identifier of the post containing this comment.
        },
        "published": "A String", # RFC 3339 date-time when this comment was published.
        "selfLink": "A String", # The API REST URL to fetch this resource from.
        "status": "A String", # The status of the comment (only populated for admin users).
        "updated": "A String", # RFC 3339 date-time when this comment was last updated.
      },
    ],
    "selfLink": "A String", # The URL of the comments on this post.
    "totalItems": "A String", # The count of comments on this post.
  },
  "selfLink": "A String", # The API REST URL to fetch this resource from.
  "status": "A String", # Status of the post. Only set for admin-level requests.
  "title": "A String", # The title of the Post.
  "titleLink": "A String", # The title link URL, similar to atom's related link.
  "trashed": "A String", # RFC 3339 date-time when this Post was last trashed.
  "updated": "A String", # RFC 3339 date-time when this Post was last updated.
  "url": "A String", # The URL where this Post is displayed.
}
"""

response_ex = {'kind': 'blogger#post',
               'id': '6424181253444860473',
               'status': 'LIVE',
               'blog': {'id': '7248995940539759558'},
               'published': '2022-11-19T12:04:00-08:00',
               'updated': '2022-11-19T14:05:20-08:00',
               'url': 'http://player.enlightenradio.org/2022/11/player-post-test.html',
               'selfLink': 'https://blogger.googleapis.com/v3/blogs/7248995940539759558/posts/6424181253444860473',
               'title': "What's Playing Now?",
               'content': '<p>Note: "What\'s playing" does not automatically refresh on Blogger....</p><div style="background-color: darkgreen; border: 3px solid rgb(115, 173, 33); color: ivory; margin: auto; padding: 10px; text-align: center; width: 80%;">\n  <p style="font-size: large; font-weignt: bold;">Phil Lesh And Friends - Marker 3</p>\n</div>',
               'author':
                   {'id': '01595792808567356923',
                    'displayName': 'The Red Caboose',
                    'url': 'https://www.blogger.com/profile/01595792808567356923',
                    'image':
                        {'url': '//www.blogger.com/img/blogger_logo_round_35.png'}
                    },
               'replies':
                   {'totalItems': '0',
                    'selfLink': 'https://blogger.googleapis.com/v3/blogs/7248995940539759558/posts/6424181253444860473/comments'},
               'readerComments': 'DONT_ALLOW_HIDE_EXISTING',
               'etag': '"dGltZXN0YW1wOiAxNjY4ODk1NTIwNDIyCm9mZnNldDogLTI4ODAwMDAwCg"'
               }