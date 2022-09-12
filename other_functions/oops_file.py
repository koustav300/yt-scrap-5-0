from other_functions import UDF_func as udf
import app
import requests

class vedio:
    """
        This is the class- get created with a YT vdo url.
        It extracts the information of the url
        Args:
            vdo_link: Youtube video link: .
            vdo_len_in_sec: Length of the video in secs
    """

    def __init__(self, vdo_link, vdo_len_in_sec):

        self.vdo_link = vdo_link
        self.vdo_id   = vdo_link.replace('https://www.youtube.com/watch?v=', "")

        # fetching the vdo information from youtube api with udf
        vdo_allInfo = udf.video_info_basic(self.vdo_id)

        self.title  = vdo_allInfo['title']
        self.channel_id = vdo_allInfo['channel_id']
        self.channel_name = vdo_allInfo['channel_title']
        self.views  = int(vdo_allInfo['view_count'])
        self.likes  = int(vdo_allInfo['like_count'])
        self.comment_count = int(vdo_allInfo['comment_count'])
        self.length = vdo_allInfo['duration']
        self.length_sec = vdo_len_in_sec
        self.thumbnail_url = vdo_allInfo['thumbnail_url']

    def create_sqlLoad_dict(self):
        """
            Just crate & Returns a dict with the Class object
        """

        output_dict = {
            'vdo_id' : self.vdo_id,
            'link' : self.vdo_link,
            'channel_name' : self.channel_name,
            'view_count' : self.views,
            'like_count' : self.likes,
            'comment_count' : self.comment_count,
            'length_in_sec' : self.length_sec,
            'length' : self.length,
            'thumbnail': self.thumbnail_url,
            'channel_id': self.channel_id
        }
        return output_dict


    def create_comment_info_dict(self):
        """
            it extarcts comment info with the vdo id of the Object
            Return a dict with all the comments & replies of the vdo ... This dict gets loaded in MongoDb
        """

        try:
            thumbnail_img   = requests.get(self.thumbnail_url).content
            comment_details = udf.video_info_comments(self.vdo_id)
            comment_details = {self.vdo_id : {"comments": comment_details,
                                              'thumbnail': thumbnail_img,
                                              'thumbnail_url': self.thumbnail_url} }
        except Exception as e:
           app.logger.error('Error inside vedio oops...func name: create_comment_info_dict... Error msg: %s' % (str(e)))

        return comment_details


