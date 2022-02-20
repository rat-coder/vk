import vk_api
import random
import time
import cv2
import requests
import json
from message import *


token = 'c7638e0261d3787e2a157a87b9bd1ceb0afd6e72635c67b5f1b464f42735b4c6759941977398d09dc68ae'

def write_json(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=2, ensure_ascii=False)

def captcha_handler(captcha):
    response = requests.get(captcha.get_url())
    img_bytes = response.content
    fname = 'captcha.png'
    with open(fname, 'wb') as f:
        f.write(img_bytes)
    # Обработка картинки
    img = cv2.imread(fname)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    cv2.imshow(fname, img)
    cv2.waitKey(1000)
    code = input('Введите капчу: ')
    cv2.destroyAllWindows()
    return captcha.try_again(code)

session = vk_api.VkApi(token=token, captcha_handler=captcha_handler)
vk = session.get_api()

def get_user_friends_info(user_id):
    try:
       friends = session.method("friends.get", {"user_id": user_id})
       for friend in friends['items']:
           user = session.method("users.get", {"user_ids": friend})
           print(f"Имя: {user[0]['first_name']} Id: {user[0]['id']} Фамилия: {user[0]['last_name']}")
    except Exception as e:
       print(e)

def add_comment_to_post(owner_id, post_id, count):
    while count > 0:
        message = random.random()
        try:
            message = session.method("wall.createComment", {"owner_id": owner_id, "post_id": post_id, "message": message})
            print(message)
        except Exception as e:
            print(e)
        count -= 1

def add_friends(user_id):
    try:
        friends = session.method("friends.get", {"user_id": user_id})
        for friend in friends['items']:
            user_info = session.method("users.get", {"user_ids": friend})
            id = user_info[0]['id']
            name = user_info[0]['first_name']
            l_name = user_info[0]['last_name']
            try:
                vk.friends.add(user_id=id, text=message_sub_on_community)
                time.sleep(1)
            except Exception as e:
                print(e)
                continue
            print(f'Заявка отправлена: {name, l_name}   id: {id}')
    except Exception as e:
        print(e)

def delete_friends(user_id):
    try:
        friends = vk.friends.get(user_id=user_id)
        for friend in friends['items']:
            user_info = vk.users.get(user_ids=friend)
            id = user_info[0]['id']
            name = user_info[0]['first_name']
            l_name = user_info[0]['last_name']
            try:
                vk.friends.delete(user_id=friend)
                print(f'Пользователь: {name, l_name} удалён! Id: {id}')
            except Exception as e:
                print(e)
                continue
    except Exception as e:
        print(e)

def delete_requests_to_friend(user_id):
    try:
        req_to = vk.friends.getRequests(user_id=user_id, out=1)
        for nofriend in req_to['items']:
            user_info = vk.users.get(user_ids=nofriend)
            id = user_info[0]['id']
            name = user_info[0]['first_name']
            l_name = user_info[0]['last_name']
            try:
                vk.friends.delete(user_id=nofriend)
                print(f'Заявка для: {name, l_name} отменена! Id: {id}')
            except Exception as e:
                print(e)
                continue
    except Exception as e:
        print(e)

def send_message_to_friends():
    friends = vk.friends.get(order='random')
    try:
        for friend in friends['items']:
            vk.messages.send(user_id=friend, message=message_sub_on_community, random_id=random.randint(1, 999999))
    except Exception as e:
        print(e)

def add_group_members(group_id):
    try:
        x = 1
        group_members = vk.groups.getMembers(group_id=group_id)
        for friend in group_members['items']:
            user_info = vk.users.get(user_ids=friend)
            id = user_info[0]['id']
            name = user_info[0]['first_name']
            l_name = user_info[0]['last_name']
            try:
                vk.friends.add(user_id=id)
                time.sleep(0.5)
                print(f'Заявка [{x}] отправлена: {name, l_name} id: {id}')
                x += 1
            except Exception as e:
                print(e)
                continue
        print(group_members)
    except Exception as e:
        print(e)

def add_send_group_members(group_id):
    try:
        x = 1
        group_members = vk.groups.getMembers(group_id=group_id)
        for friend in group_members['items']:
            user_info = vk.users.get(user_ids=friend)
            id = user_info[0]['id']
            name = user_info[0]['first_name']
            l_name = user_info[0]['last_name']
            try:
                vk.friends.add(user_id=id, text=message_sub_on_community)
                time.sleep(0.5)
                print(f'Заявка [{x}] отправлена: {name, l_name} id: {id}')
                x += 1
            except Exception as e:
                print(e)
                continue
        print(group_members)
    except Exception as e:
        print(e)

def change_user_photo(user_id):
    try:
        upload_s = vk.photos.getOwnerPhotoUploadServer(owner_id=user_id)
        url = upload_s['upload_url']
        photo = {'file1': open(r'img\nobody.png', 'rb')}
        ur = requests.post(url, files=photo).json()
        res = vk.photos.saveOwnerPhoto(server=ur['server'], hash=ur['hash'], photo=ur['photo'])
        print(res)
    except Exception as e:
        print(e)

def create_album(group_id, file_name):
    cr_alb = vk.photos.createAlbum(title='alb', group_id=group_id)
    album_id = cr_alb['id']
    upload_s = vk.photos.getUploadServer(album_id=album_id, group_id=group_id)
    url = upload_s['upload_url']
    photo = {'file1': open(fr'img\{file_name}', 'rb')}
    ur = requests.post(url, files=photo).json()
    res = vk.photos.save(album_id=album_id, group_id=group_id, server=ur['server'], photos_list=ur['photos_list'], hash=ur['hash'])
    return res[0]['id']

def edit_albums(group_id, file_name):
    photo = {'file1': open(fr'img\{file_name}', 'rb')}
    result = vk.photos.getAlbums(owner_id='-'+str(group_id))
    count_alboms = result['count']
    if count_alboms == 0:
        return create_album(group_id, file_name)
    else:
        alboms = result['items']
        rand_albom = random.randint(0, (count_alboms - 1))
        albom = result['items'][rand_albom]['id']
        upload_s = vk.photos.getUploadServer(album_id=albom, group_id=group_id)
        url = upload_s['upload_url']
        ur = requests.post(url, files=photo).json()
        res = vk.photos.save(album_id=albom, group_id=group_id, server=ur['server'],photos_list=ur['photos_list'], hash=ur['hash'])
        return res[0]['id']

def create_post(group_id):
    i = 1
    x = 1
    while i != 11111111:
        try:
            myfile = open('posts.txt', 'a')
            group_id = int(group_id) + 1
            photo_id = edit_albums(group_id)
            pt = vk.wall.post(owner_id='-'+str(group_id), filter='suggests', message=post_sweek_promo, attachments=f'photo-{group_id}_{photo_id}')
            print(f'Запись номер [{x}] опубилкована Id Сообщества: {group_id} Id Записи: {pt["post_id"]}')
            myfile.write(f'Запись номер [{x}] опубилкована Id Сообщества: {group_id} Id Записи: {pt["post_id"]}\n')
            myfile.close()
            x += 1
        except Exception as e:
            # print(e)
            continue
        i += 1

def check_post_in_community(community_id, post_id):
    r1 = vk.wall.getById(posts='-'+str(community_id)+'_'+str(post_id))
    answer = r1[0]['post_type']
    return answer

def read_file(file_name):
    txt_file = open(file_name, 'r')
    last_line = txt_file.readlines()[-1]
    last_community_id = last_line.split('/')[-1].split('public')[-1]
    txt_file.close()
    return last_community_id

def find_open_community(file_name, txt_file_name):
    i = 1
    x = 1
    community_id = read_file(txt_file_name)
    while i != 11111111:
        try:
            myfile = open(txt_file_name, 'a+')
            community_id = int(community_id) + 1
            photo_id = edit_albums(community_id, file_name)
            pt = vk.wall.post(owner_id='-' + str(community_id), filter='suggests', message=post_sweek_promo, attachments=f'photo-{community_id}_{photo_id}')
            print(f'https://vk.com/public{community_id}')
            answer = check_post_in_community(community_id, pt['post_id'])
            if answer == 'post':
                myfile.write(f'https://vk.com/public{community_id}\n')
            else:
                continue
            x += 1
        except Exception as e:
            # print(e)
            continue
        myfile.close()
        i += 1

# find_open_community('nobody.png', 'communities.txt')
# send_message_to_friends()
# change_user_photo()
# add_send_group_members(40418917)
