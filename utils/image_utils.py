from PIL import Image, ImageDraw, ImageFont
import os
from django import forms
from post.tasks import make_thumbnail
import subprocess


# Upload pictures check the legality max_size The maximum size, the unit K. 0 means unlimited
def check_image(value, max_size):
    try:
        img = Image.open(value)
        try:
            if img.format not in ['JPEG', 'GIF', 'PNG']:
                raise forms.ValidationError('Only supports JPEG, GIF, PNG files')
        except:
            raise forms.ValidationError('Image does not have a format')
    except:
        raise forms.ValidationError('Invalid Graphic file')

    if img.format == 'GIF':

        if value.size > 2 * max_size * 1024:
            raise forms.ValidationError('Image greater than %s kb size ' % max_size * 2)
    else:
        if value.size > max_size * 1024:
            raise forms.ValidationError('Image greater than %s kb size' % max_size)



def reduce_quality_and_make_thumbs(filename, path, photo_size, attribution=''):
    """
    reduce the quality of uploadeded image and make thumbnails
    """

    try:
        im = Image.open(filename)

        width, height = im.size
        ratio = (width + 1.0) / height
        if width > 650:
            width = 650
        height = (width) / ratio
        if not im.format == 'GIF':
            im.thumbnail((width, height))
            to_quality = 100 if photo_size <200 else 90
            im.save(filename, quality=to_quality, optimize=True)
            """
            # To draw text on the image
            draw = ImageDraw.Draw(im)
            fontsFolder = '/usr/share/fonts/truetype/dejavu'  # e.g. 'Library/Fonts'
            arialFont = ImageFont.truetype(os.path.join(fontsFolder, 'DejaVuSerif.ttf'), 16)
            if attribution != '':
                draw.text((10, 10), attribution, fill='black', font=arialFont)
            else:
                draw.text((10, 10), 'website', fill='black', font=arialFont)
            im.save(filename)
            """
            # Thumbnails
            thumb_big_filename = filename.replace('.', '_thumb_big.')
            thumb_small_filename = filename.replace('.', '_thumb_small.')
            thumb_big_filename = os.path.join(path, thumb_big_filename)
            thumb_small_filename = os.path.join(path, thumb_small_filename)
            # Size for the big and main thumbnail
            big_width = 500
            big_height = max(((big_width + 1.0) / ratio), 600)
            print big_width, big_height
            # big_height = big_height if big_height > 450 else 450
            make_thumbnail.delay(filename, out_filename=thumb_big_filename, size=(big_width, big_height))
            # Small Thumbnail
            make_thumbnail.delay(filename, out_filename=thumb_small_filename, size=(48, 48))
            return 0, width, int(height)
        else:
            name = filename.split('.')[0]
            process = subprocess.Popen(['ffmpeg', '-i', filename, '-crf', '30', '-b:v', '500k', '-y', name + '.mp4'])
            while process.poll() < 0:
                continue
            process = subprocess.Popen(['ffmpeg', '-i', filename, '-crf', '30', '-b:v', '500k', '-y', name + '.webm'])
            while process.poll() < 0:
                continue
            return 1, width, int(height)

    except IOError:
        print "Couldn't reduce quality"

    except Exception, e:
        print "EXception occurred", str(e)
