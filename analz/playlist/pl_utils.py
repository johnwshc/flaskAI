from config import Config
from app.jinjatuils import JinjaUtils as JU
from analz.playlist.plutils import PLUtils


class Test_pl:
    img_lnk = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS0LrvYDvdkcTCW_AGfWclc8yK6WEyxQlqEe5x7mTHYRQ&usqp=CAU&ec=48665701"
    plfn = f"{Config.PUBPL}/memday_pl.html"
    title = "The Memorial Day, 2023 Enlighten Radio Playlist"
    pl_props = {'playlist': plfn,
                'blogs': 'Enlighten Radio',
                'title': title,
                'image_url': img_lnk,
                'imagelink': img_lnk}

    @staticmethod
    def getPubPL():
        # props from this post should include:
        # playlist, title, blogs keys/values
        props = Test_pl.pl_props.copy()


        ju = JU()
        erb = ju.erb
        blogs = erb.blogs['items']
        blog_names = [b['name'] for b in blogs]

        props['post'] = PLUtils.RDJplaylist2BloggerHTML(props['playlist'])
        props['template'] = 'er_plpub_content.html'
        props['blogname'] =  props['blogs']
        res = ju.get_ERPostTemplate(props)

        # print(f"response from blogger to er post: : {res}")

        return res

        # res = ju.get_ERPostTemplate(props)

