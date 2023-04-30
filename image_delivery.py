#! /usr/bin/env python3

import os
import sys
import json
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
    except:
        print('[!] Empty pool of images!')
        sys.exit(0)

    img_cover_list = []
    img_support_list = []

    for image in image_names:
        # print(image)
        if image.startswith('_'):
            img_cover_list.append(image)
        else:
            img_support_list.append(image)

    try:
        # img_amt = random.choice([1, 3]) if len(image_names) != 3 else 3
        img_amt = 3
        if img_amt == 1:
            push_images = random.sample(img_cover_list, img_amt)
        else:
            if len(img_cover_list) == 0:
                push_images = random.sample(img_support_list, img_amt)
            if len(img_support_list) == 0 and len(img_cover_list) > 5:
                push_images = random.sample(img_cover_list, img_amt)
            if len(img_cover_list) > 0:
                push_images = random.sample(img_cover_list, 1)
                push_images += random.sample(img_support_list, img_amt-1)
            else:
                push_images = random.sample(img_support_list, img_amt)
    except Exception as e:
        # print(e)
        if len(image_names) == 2:
            push_images = sorted(image_names, reverse=True)
        else:
            push_images = [img_cover_list[0]] if len(img_cover_list) > 0 else [image_names[0]]
    print(f'[+] Pushing {len(push_images)} images from {image_path}')
    for i in push_images:
        print(f'\t[+] {i}')

    push_images = [os.path.join(image_path, image_name) for image_name in push_images]
    pool_folder_path = os.path.join(pool_path, pool_folder)

    data = None
    try:
        with open(os.path.join(image_path, 'data.json'), 'r') as f:
            data = json.load(f)
    except Exception as e:
        print(f'[!] No custom json for selected image path: {e}')

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

    extra_tags = ''
    if data:
        extra_tags = ' '.join(data["tags"])
    tweet_text = f'''{text}{" ".join(generic_tags)} {extra_tags}'''
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
