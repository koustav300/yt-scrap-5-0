import os
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import app
import time
from other_functions import UDF_connections as new_conn


# # Not in use
def extract_vdo_comment(ui_link, ui_thumbnail_url): # Not in use
    options = Options()
    options.add_argument("start-maximized")

    # path to chrome driver
    driver = webdriver.Chrome(options=options, executable_path='../chromedriver.exe')
    driver.get(ui_link)

    wait = WebDriverWait(driver, 15)

    # going to end of page to ensure all comments are loaded
    for item in range(25):
        wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body"))).send_keys(Keys.END)
        # for comment in wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#content"))):

    # Getting the source formatted html
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # extracting no of likes
    total_likes = soup.find_all("div", id="top-level-buttons-computed")[0].find_all("yt-formatted-string")[0].text
    print('The total likes for this vdo is - ', total_likes)

    # Scrapping the comment info
    no_of_comments = 0
    comments_list = []
    commenter_name_list = []

    comment_mainContainer = soup.find_all("ytd-comment-thread-renderer")
    for comment_div in comment_mainContainer:
        comment_text = comment_div.find_all(id="content-text")[0].text
        commenter_name = comment_div.find_all(id='author-text')[0].find_all('span')[0].text
        comments_list.append(comment_text)
        commenter_name_list.append(commenter_name.strip())
        no_of_comments = no_of_comments + 1

    # downloading thubnail img
    img_content = requests.get(ui_thumbnail_url).content

    target_path = '../images'
    target_folder = os.path.join(target_path, '_'.join('test'))
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    counter = 1
    f = open(os.path.join(target_folder, 'jpg' + "_" + str(counter) + ".jpg"), 'wb')
    f.write(img_content)
    f.close()

    return [int(total_likes), int(no_of_comments), comments_list, commenter_name_list]


# -----------------------------------------------------------------------------------------------

from googleapiclient.discovery import build
api_key = 'AIzaSyC5vrAqcbk1QcdXJBx1zXsChV4EgPnDFhQ'

def video_info_comments(video_id: str):
    """
    This function extract youtube comments & replies with a help API id.
    this returns a dict  to be loaded in mongoDb

    Args:
        video_id: id of the video comments will be extracted.

    Returns:
        a dict  to be loaded in mongoDb.

    Raises:
        KeyError: Raises an exception .
    """

    fname = 'video_info_comments'
    try:
        # empty list for storing reply
        comment_list = {}

        # creating youtube resource object
        youtube = build('youtube', 'v3',
                        developerKey=api_key)
        app.logger.debug('Youtube resource object created with APi')

        # retrieve youtube video comments results
        try:
            video_response = youtube.commentThreads().list(
                part='snippet,replies',
                videoId=video_id
            ).execute()
            app.logger.debug('Youtube comment extracted')
        except Exception as e:
            app.logger.warning('Youtube comment count be extracted for %s, Reason: %s' %(video_id, str(e)))
            return comment_list

        # iterate video response
        comment_counter = 0
        while video_response:

            # extracting required info
            # from each result object

            for item in video_response['items']:

                # Extracting comments
                comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
                commeter = item['snippet']['topLevelComment']['snippet']['authorDisplayName']

                # append to output dict
                # adding the counter as one per may comment multiple times
                comment_list[str(comment_counter)] = {
                    'comment': {commeter: comment},
                    'reply': {}
                }

                # counting number of reply of comment
                replycount = item['snippet']['totalReplyCount']
                does_have_reply = 'N'
                for key in list(item.keys()):
                    if key == 'replies':
                        does_have_reply = 'Y'

                # if reply is there
                reply_list = []
                replycounter = 0
                if replycount > 0 and does_have_reply == 'Y':
                    # iterate through all reply
                    for reply in item['replies']['comments']:
                        # Extract reply
                        reply_text = reply['snippet']['textDisplay']
                        replyer = reply['snippet']['authorDisplayName']

                        # Adding replies to the output comment
                        comment_list[str(comment_counter)]['reply'].update({str(replycounter): {} })
                        comment_list[str(comment_counter)]['reply'][str(replycounter)].update({replyer: reply_text})
                        replycounter = replycounter +1
                # increasing the counter
                comment_counter = comment_counter + 1

            # Again repeat
            if 'nextPageToken' in video_response:
                video_response = youtube.commentThreads().list(
                    part='snippet,replies',
                    videoId=video_id,
                    pageToken=video_response["nextPageToken"],
                ).execute()
            else:
                break
    except Exception as e:
        app.logger.error('ERROR from file-- UDF_func, Func-name: %s, Error-mag: %s' %(fname ,str(e)))
        raise


    return comment_list


def video_info_basic(video_id):
    """
    This function extract youtube details of a video with a help API id.

    Args:
        video_id: id of the video comments will be extracted.

    Returns:
        a dict with all the details of the video

    Raises:
        KeyError: Raises an exception .
    """


    fname = 'video_info_basic'

    try:
        # creating youtube resource object
        youtube = build('youtube', 'v3',
                        developerKey=api_key)

        # retrieve youtube video results
        video_response = youtube.videos().list(
            part='snippet, statistics, contentDetails',
            id=video_id
        ).execute()

        title = video_response['items'][0]['snippet']['title']
        channel_id = video_response['items'][0]['snippet']['channelId']
        thumbnail_url = video_response['items'][0]['snippet']['thumbnails']['high']['url']  # default
        channel_title = video_response['items'][0]['snippet']['channelTitle']
        like_count = video_response['items'][0]['statistics']['likeCount']
        view_count = video_response['items'][0]['statistics']['viewCount']
        comment_count = video_response['items'][0]['statistics']['commentCount']
        duration = video_response['items'][0]['contentDetails']['duration']

        output_dict = {
            'title': title,
            'channel_id': channel_id,
            'thumbnail_url': thumbnail_url,
            'channel_title': channel_title,
            'like_count': like_count,
            'view_count': view_count,
            'comment_count': comment_count,
            'duration': duration
        }
    except Exception as e:
        app.logger.error('ERROR from file-- UDF_func, Func-name: %s, Error-mag: %s' % (fname ,str(e)))
        raise

    return output_dict





def delete_mysql_chhnlData(input_channel_id: str):
    """
    This function runs a server side sql query to delete data from mySql based on Channel_id .

    Args:
        input_channel_id: id of the Youtube channel user wants to clean the data for.

    Returns: Nothing

    Raises:
        KeyError: Raises an exception .
    """

    fname = 'delete_mysql_chhnlData'

    try:
        # creating pySQL conncetion
        conn = new_conn.create_pysql_connction()

        # creating query string
        sql_sqtring = f"DELETE from basic_scrap_info where channel_id = '{input_channel_id}';"
        print(sql_sqtring)
        # create cursor  & Execute query
        cursor = conn.cursor()
        cursor.execute(sql_sqtring)
        conn.commit()
    except Exception as e:
        app.logger.error('ERROR from file-- UDF_func, Func-name: %s, Error-mag: %s' % (fname, str(e)))
        raise

    return 'Successful'


def fetch_scrapped_info_frmMysql(input_channel_id: str):
    """
       This function runs a server side sql query to collect data from mySql based on Channel_id .
       With fetched data it creates a html table text that can be added(innerhtml) in a <tbody> to get a table

       Args:
           input_channel_id: id of the Youtube channel user wants to clean the data for.

       Returns: html table text that can be added(innerhtml) in a <tbody> to get a table

       Raises:
           KeyError: Raises an exception .
    """



    fname = 'fetch_scrapped_info_frmMysql'

    try:
        # creating pySQL conncetion
        conn = new_conn.create_pysql_connction()

        # creating query string
        sql_sqtring = f"Select * from yt_scrape.basic_scrap_info where channel_id = '{input_channel_id}'"

        # create cursor  & Execute query
        cursor = conn.cursor()
        cursor.execute(sql_sqtring)

        # Fetch all the records
        result = cursor.fetchall()

        app.logger.debug('Basic info data collected from mysql ..... Proceed to html table text creation')


        html_text = ""
        for row in result:
            html_text += "<tr class='tr_type_1'>"  # opening the row

            for row_value in range(0, len(row)):
                if row_value == 8:
                    html_text += f"<td class='td_thumbnail'> <img src='{row[row_value]}' alt='thumbnail' srcset=''> </td>"
                elif row_value == 6 or row_value == 9:
                    asd =0
                else:
                    html_text += f"<td>{row[row_value]}</td>"  # creating tds

            html_text += "</tr>"  # closing the row
        conn.close()
        app.logger.debug('HTML table text for created for basic info data')

    except Exception as e:
        app.logger.error('ERROR from file-- UDF_func, Func-name: %s, Error-mag: %s' % (fname, str(e)))
        raise
    return html_text

def delete_comment_info_byChannel(input_channel_name: str):
    """
       This function delete the documents of a channel by Name from MongoDb

       Args:
           input_channel_name: Name of the Youtube channel user wants to clean the data for.

       Returns: Nothing

       Raises:
           KeyError: Raises an exception .
    """

    fname = 'delete_comment_info_byChannel'
    try:
        # connecting to mongoDb
        client = new_conn.create_mongodb_conn()
        db = client['mongotest']
        collection = db['testLoadtest7']
        collection.delete_many({'channel_name': input_channel_name})
        app.logger.debug('Data deleted from MongoDb --- for the Channel')

    except Exception as e:
        app.logger.error('ERROR from file-- UDF_func, Func-name: %s, Error-mag: %s' % (fname, str(e)))
        raise

def fetch_scrapped_info_frmMongoDb(input_channel_name: str):
    """
        This function collect data from mongoDb based on Channel_Name .
        With fetched data it creates a html table text that can be added(innerhtml) in a <tbody> to get a table

        Args:
            input_channel_name: Name of the Youtube channel user wants to fetch the data for.

        Returns: a list with 3 entries
            [ html table text that can be added(innerhtml) in a <tbody> to get a table: (Youtube Comment info),
              a list thumbnail url ,
              a list of vdo ids
            ]
        Raises:
            KeyError: Raises an exception .
    """

    fname = 'fetch_scrapped_info_frmMongoDb'

    try:
        # connecting to mongoDb
        client = new_conn.create_mongodb_conn()
        db = client['mongotest']
        collection = db['testLoadtest7']
        cursor = collection.find({'channel_name': input_channel_name})
        app.logger.debug('data collected from mongo db')

        html_text = ''
        img_url_list  = []
        vdo_id_list=[]
        for chnl in cursor:
            # getting the record of this channel
            all_vdo_info = chnl['list_of_vdos']  # return arry with object-per-vdo
            vdo_ids = list(all_vdo_info.keys())

            # for each vdo-id in the channel
            for vdo_id in vdo_ids:
                comments = all_vdo_info[vdo_id]['comments']
                images   = all_vdo_info[vdo_id]['thumbnail_url']
                img_url_list.append(images)
                vdo_id_list.append(vdo_id)
                # for each comment in among the comments
                for key in comments:
                    comment = comments[key]['comment']
                    replies = comments[key]['reply']

                    commenter = list(comment.items())[0][0]
                    commentText = list(comment.items())[0][1]
                    # print(commenter, ' - ', commentText)
                    html_text += f"<tr> <td>{vdo_id}</td> <td>{commenter}</td> <td>{commentText}</td> <td>Comment</td> <td>-</td> <td>-</td>"

                    for key in replies:
                        reply = replies[key]
                        replyer = list(reply.items())[0][0]
                        replyText = list(reply.items())[0][1]

                        html_text += f"<tr class='tr_reply> <td>-</td> <td>-</td> <td>-</td> <td>Reply</td> <td>{replyer}</td> <td>{replyText}</td>"

                    html_text += '</tr>'

        app.logger.debug('HTML text for comment table created')

    except Exception as e:
        app.logger.error('ERROR from file-- UDF_func, Func-name: %s, Error-mag: %s' % (fname, str(e)))
        raise

    return [html_text, img_url_list, vdo_id_list]





