#! /usr/bin/env python3

import os
import sys
import shutil
import random
from Module.TwitterAPIWrapper import TwitterAPI

try:
    from CustomConfig import *
except Exception as e:
    # Credentials
    username = 'TWITTER_USERNAME'
    costumer_key = 'TWITTER_COSTUMER_API_KEY'
    costumer_key_secret = 'TWITTER_COSTUMER_API_KEY_SECRET'
    access_token = 'TWITTER_ACCESS_TOKEN'
    access_token_secret = 'TWITTER_ACCESS_TOKEN_SECRET'

    # Define the path where the pool of images and the posted images are going to be stored
    pool_path = '/path/to/images/'
    # Posted images are going to be placed in '/path/to/images/' + 'posted'
    posted_folder = 'posted'
    # Place all the images inside the folder '/path/to/images/' + 'pool'
    pool_folder = 'pool'

    # Tags to be postes along with the images
    generic_tags = [
        '#twitter', '#bot',
    ]

def track_images(path, skip_folders=[], extensions=('.png', '.jpg', '.jpeg')):
    image_dict = {}
    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if d not in skip_folders]
        folder_name = os.path.relpath(root, path)
        image_files = [file for file in files if file.lower().endswith(extensions)]
        if image_files:
            image_dict[os.path.join(path,folder_name)] = image_files
    return image_dict

def mark_as_posted(image_file, posted_path, root_path):
    image_path = os.path.dirname(image_file)
    sub_folders = os.path.relpath(image_path, root_path)
    target_dir = os.path.join(posted_path, sub_folders)

    # print(f'{image_file}\n->\n{target_dir}')

    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    shutil.move(image_file, target_dir)

if __name__ == '__main__':
    api = TwitterAPI(
        username,
        costumer_key,
        costumer_key_secret,
        access_token,
        access_token_secret,
    )

    posted_path = os.path.join(pool_path, posted_folder)

    try:
        image_data = track_images(pool_path, skip_folders=[posted_folder])
        image_path, image_names = random.choice(list(image_data.items()))
        img_amt = random.choice([1, 3])
    except:
        print('[!] Empty pool of images!')
        sys.exit(0)
    try:
        push_images = random.sample(image_names, img_amt)
    except:
        push_images = [image_names[0]]

    push_images = [os.path.join(image_path, image_name) for image_name in push_images]
    pool_folder_path = os.path.join(pool_path, pool_folder)
    print(f'[+] Pushing {len(push_images)} images from {image_path}')

    metadata = image_path.replace(pool_folder_path, '').split('/')[1:]
    text = ''
    try:
        model = metadata[0]
        text += f''
    except:
        model = None
    try:
        category = metadata[1]
        text += f'Generated from {category.replace("-", " ").title()} category '
    except:
        category = None
    try:
        detail = metadata[2]
        text += f'with {detail.replace("-", " ").title()} as details '
    except:
        detail = None

    tweet_text = f'''{text}{" ".join(generic_tags)}'''
    print(f'[.] Tweeting: {tweet_text}')

    try:
        if len(push_images) > 1:
            api.tweet_image(
                push_images,
                tweet_text
            )
        else:
            api.tweet_image(
                push_images[0],
                tweet_text
            )
    except Exception as e:
        raise Exception(f'[!] Someting failed: {e}')

    for push_image in push_images:
        image_name = push_image
        image_file = os.path.join(image_path, image_name)
        mark_as_posted(image_file, posted_path, pool_folder_path)

    print(f'[!] Done')
