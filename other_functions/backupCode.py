
#-----------------------------------------------------------------------
#very Slow
import pafy

url = "https://www.youtube.com/watch?v=Pp6CO2_YEDE"
video = pafy.new(url)

streams = video.streams
for i in streams:
    print(i)

# get best resolution regardless of format
best = video.getbest()

print(best.resolution, best.extension)

# Download the video
best.download()


#--------------------------------------------------
# It is also slow--- but shows the progress bar
# #Download video
import youtube_dl
ydl_opts = {}

def dwl_vid():
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([zxt])

channel = 1
while (channel == int(1)):
    #link_of_the_video = input("Copy & paste the URL of the YouTube video you want to download:- ")
    link_of_the_video = test_link

    zxt = link_of_the_video.strip()
    dwl_vid()
    #channel = int(input("Enter 1 if you want to download more videos \nEnter 0 if you are done "))
    channel=0


   # comment_mainContainer = driver.find_elements(By.TAG_NAME, 'ytd-comment-thread-renderer')
    # for comment_div in comment_mainContainer:
    #     comment_text   = comment_div.find_elements(By.ID, 'content-text')[0].text
    #     commenter_name = comment_div.find_elements(By.ID, 'author-text')[0].find_elements(By.TAG_NAME, 'span')[0].text
    #
    #     print('----------------------------- ', commenter_name)
    #     print(comment_text)

from pytube import YouTube
def fetch_vdo_info(ui_link):
    yt = YouTube(ui_link)
    title = yt.title
    views = yt.views
    length = yt.length
    channel_id = yt.channel_id
    thumbnail_img_link = yt.thumbnail_url
    chnl_author = yt.author
    return [title, views, length, channel_id, thumbnail_img_link, chnl_author]


def download_thubnail_img(ui_thumbnail_url, img_name):
    fname = 'download_thubnail_img'
    from pathlib import Path

    try:
        # downloading thubnail img
        img_content = requests.get(ui_thumbnail_url).content
        IMAGE_FOLDER = '../static/images'
        app.config['IMAGE_FOLDER'] = IMAGE_FOLDER

        f = open(os.path.join(app.config['IMAGE_FOLDER'], img_name + ".jpg"), 'wb')
        f.write(img_content)
        f.close()
    except Exception as e:
        app.logger.error('ERROR from file-- UDF_func, Func-name: %s, Error-mag: %s' % (fname, str(e)))
        raise

    return img_content

def download_imgFrom_mongodb(mongoFetchRecords):
    fname = 'download_imgFrom_mongodb'

    try:
        pass

    except Exception as e:
        app.logger.error('ERROR from file-- UDF_func, Func-name: %s, Error-mag: %s' % (fname, str(e)))
        raise


def yt_video_len_in_sec(input_api_len):
    L = list(input_api_len)
    for i in range(len(L)):
        if L[i].isdigit():
            pass
        else:
            L[i] = "-"
    modified_string = ''.join(L).rstrip('-').lstrip('-')
    new_l = modified_string.split('-')

    # converting duration to Sec
    len_in_sec = 0
    if len(new_l) == 3:  # H+M+S
        len_in_sec = ((int(new_l[0]) * 60) * 60) + (int(new_l[1]) * 60) + int(new_l[2])
    elif len(new_l) == 2:  # M+S
        len_in_sec = (int(new_l[1]) * 60) + int(new_l[2])
    else:  # S
        len_in_sec = int(new_l[2])

    return len_in_sec


# not required functions
def getting_aws_credentials():
    import boto3
    # import base64
    from botocore.exceptions import NoCredentialsError
    from botocore.exceptions import ClientError

    secret_name = "new_user_sm"
    region_name = "us-east-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )
    print(client)
    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        print(e)
        if e.response['Error']['Code'] == 'DecryptionFailureException':
            # Secrets Manager can't decrypt the protected secret text using the provided KMS key.
            # Deal with the exception here, and/or rethrow at your discretion.

            raise e
        elif e.response['Error']['Code'] == 'InternalServiceErrorException':
            # An error occurred on the server side.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            # You provided an invalid value for a parameter.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            # You provided a parameter value that is not valid for the current state of the resource.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'ResourceNotFoundException':
            # We can't find the resource that you asked for.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
    else:
        # Decrypts secret using the associated KMS key.
        # Depending on whether the secret is a string or binary, one of these fields will be populated.
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
            # print(secret)
        else:
            # decoded_binary_secret = base64.b64decode(get_secret_value_response['SecretBinary'])
            pass

    return secret
