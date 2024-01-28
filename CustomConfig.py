import os

logs_path = os.environ.get('TWITTER_IMG_DELIVERY_LOG_PATH_Z')
pool_path = os.environ.get('TWITTER_AI_GEN_PATH_Z')

posted_folder = 'posted'
pool_folder = 'pool'

username = os.environ.get('TWITTER_USERNAME_Z')
costumer_key = os.environ.get('TWITTER_COSTUMER_API_KEY_Z')
costumer_key_secret = os.environ.get('TWITTER_COSTUMER_API_KEY_SECRET_Z')
access_token = os.environ.get('TWITTER_ACCESS_TOKEN_Z')
access_token_secret = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET_Z')

generic_tags = [
    '#anime', '#animegirl', '#waifu',
    '#nsfwart', '#nsfwtwt', '#nsfw',
    '#AIart', '#aigenerated', '#stablediffusion',
    '#ChilloutMix', '#AIphoto','#AIArtworks',
]
