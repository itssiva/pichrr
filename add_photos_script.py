import os
import random
os.environ['DJANGO_SETTINGS_MODULE'] = 'pichrr.settings'
import django
from django.conf import settings

if __name__ == '__main__':
    django.setup()

from post.models import Post
from post.views import get_ref_id
from utils.image_utils import reduce_quality_and_make_thumbs
import shutil
from django.contrib.auth.models import User
from utils.common_utils import txt2set
from post.views import upload_photo


def upload_photo(photo, ext, photo_size, attribution):
    sub_folder_name = str(random.randint(0,100))
    path = os.path.join(settings.MEDIA_ROOT, sub_folder_name)
    # If the folder does not exist, create a folder
    if not os.path.exists(path):
        os.mkdir(path)
    import time
    filename = str(time.time()).replace('.','_') + str(random.randrange(0,99999,1)) + ext
    ret_filename = os.path.join(sub_folder_name, filename)
    filename = os.path.join(path, filename)
    shutil.copy2(photo, filename)
    type, width, height = reduce_quality_and_make_thumbs(filename, path, photo_size, attribution)
    return (ret_filename.replace("\\", "/")), type, width, height


languages = ['ENGLISH', 'HINDI', 'TELUGU', 'TAMIL', 'KANNADA', 'ENGLISH HINDI', 'ENGLISH TELUGU', 'ENGLISH TAMIL',
             'ENGLISH KANNADA', 'HINDI TELUGU', 'HINDI TAMIL', 'HINDI KANNADA', 'TELUGU TAMIL', 'TAMIL KANNADA']
lang12 = ['10', '20', '30', '40', '50', '12', '13', '14', '15', '23', '24', '25', '34', '45']
usernames = ['theHulk', 'tonyStark', 'capt_America', 'Thor', 'blackWidow', 'hawkEye', 'loki', 'deadPool']

for lang in range(0, len(languages)):

    for i in range(len(usernames)):
        user = User.objects.get(username = usernames[i])
        ref_id = get_ref_id()
        title = "This is the title for image in " + languages[lang] + " " + str(i)
        #image = '/home/sponugot/Desktop/images/image' + str(i) + '.jpg';
        if settings.DEBUG:
            image = '/home/sponugot/Desktop/images/image' + str(i) + '.jpg'
        else:
            image = '/home/itssiva/env/images/image' + str(i) + '.jpg'
        photo_url, type, width, height = upload_photo(image, '.jpg', os.stat(image).st_size, '')
        photo_type = photo_url.split('.')[-1]
        txt_tags = "tag1, tag2, tag3"
        language1 = int(lang12[lang][0])
        language2 = int(lang12[lang][1])
        is_anonymous = False
        creator = ' '
        ip = '127.0.0.1'
        post = Post.objects.create(ref_id=ref_id, user=user, title=title, photo_url=photo_url, post_type=type,
                                   txt_tags=txt_tags, language1=language1, language2=language2,
                                   is_anonymous=is_anonymous, width=width, height=height,
                                   attribution=creator, uploaded_ip=ip)
        post.save()
        post.add_txt_tags(txt2set(txt_tags))
        post.save()
