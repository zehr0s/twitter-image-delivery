#! /usr/bin/env python3

import os
import sys
import time
import json
import shutil
import random
import datetime
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

    # Define the path where logs are stored
    logs_path = '/path/to/logs/'
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

def delete_old_file(file_path, retention_period=7):
    # Check if the file exists
    if os.path.isfile(file_path):
        # Get the current time and file's modification time
        current_time = time.time()
        file_modification_time = os.path.getmtime(file_path)

        # Calculate the file's age in days
        file_age_days = (current_time - file_modification_time) / (60 * 60 * 24)

        # If the file's age is greater than the retention period, delete it
        if file_age_days > retention_period:
            os.remove(file_path)
            print(f"Deleted file: {file_path}")
    else:
        raise Exception(f"File '{file_path}' not found.")

if __name__ == '__main__':
    try:
        log_retention_period = 7
        info_log_file = os.path.join(logs_path, 'info.log')
        # try:
        #     delete_old_file(info_log_file, log_retention_period)
        # except:
        #     print(f'[!] Log file doesn\'t exists yet!')
        today_tweets = 0

        last_tweet_data = None
        current_tweet_data = {
            f'{datetime.datetime.now()}':
                {
                    'status': 'ERROR',
                    'message': '',
                    'images': 1,
                }
        }

        try:
            with open(info_log_file, 'r') as f:
                last_tweet_data = json.loads(f.read())
        except:
            pass

        last_tweet_date = None
        last_tweet_imgs = 0
        if last_tweet_data:
            for tweet_date, values in last_tweet_data.items():
                if values['status'] == 'OK' and datetime.datetime.fromisoformat(tweet_date).date() == datetime.date.today():
                    today_tweets += 1
                if values['status'] == 'OK':
                    last_tweet_date = datetime.datetime.fromisoformat(tweet_date)
                    last_tweet_imgs = values['images']

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

        if today_tweets == 0:
            for k in list(image_data.items()):
                image_path_aux, image_names_aux = k
                for i in image_names_aux:
                    if i.startswith('+'):
                        image_path = image_path_aux
                        image_names = image_names_aux
                        break

        img_cover_list = []
        img_single_list = []
        img_support_list = []

        for image in image_names:
            # print(image)
            if image.startswith('_'):
                img_cover_list.append(image)
            elif image.startswith('+'):
                img_single_list.append(image)
            else:
                img_support_list.append(image)

        print('[+] Selected image path status:')
        print(f'\t[+] Cover: {len(img_cover_list)}')
        print(f'\t[+] Single: {len(img_single_list)}')
        print(f'\t[+] Support: {len(img_support_list)}')

        try:
            # img_amt = random.choice([1, 3]) if len(image_names) != 3 else 3
            if today_tweets == 0 and len(img_single_list)>0:
                img_amt = 1
                push_images = random.sample(img_single_list, img_amt)
            else:
                img_amt = 3
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
                if len(img_single_list) > 0:
                    push_images = [img_single_list[0]]
                elif len(img_cover_list) > 0:
                    push_images = [img_cover_list[0]]
                else:
                    push_images = [image_names[0]]

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
            raise Exception(f'[!] Something failed: {e}')

        for push_image in push_images:
            image_name = push_image
            image_file = os.path.join(image_path, image_name)
            mark_as_posted(image_file, posted_path, pool_folder_path)

        # Log successful tweet data
        current_tweet_data[list(current_tweet_data.keys())[-1]]['images'] = len(push_images)
        current_tweet_data[list(current_tweet_data.keys())[-1]]['status'] = 'OK'
        current_tweet_data[list(current_tweet_data.keys())[-1]]['tweet'] = tweet_text
        current_tweet_data[list(current_tweet_data.keys())[-1]]['image_paths'] = ', '.join(push_images)
        if last_tweet_data:
             last_tweet_data.update(current_tweet_data)
             current_tweet_data = last_tweet_data
        with open(info_log_file, 'w') as f:
            f.write(json.dumps(current_tweet_data))
        print(f'[!] Done')

    except Exception as e:
        # Log unsuccessful tweet data
        current_tweet_data[list(current_tweet_data.keys())[-1]]['message'] = str(e)
        current_tweet_data[list(current_tweet_data.keys())[-1]]['tweet'] = tweet_text
        current_tweet_data[list(current_tweet_data.keys())[-1]]['image_paths'] = ', '.join(push_images)
        if last_tweet_data:
             last_tweet_data.update(current_tweet_data)
             current_tweet_data = last_tweet_data
        with open(info_log_file, 'w') as f:
            f.write(json.dumps(current_tweet_data))
        raise Exception(e)
