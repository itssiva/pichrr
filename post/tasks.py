from pichrr.celery import app
from PIL import Image


@app.task(name="make_thumb")
def make_thumbnail(filename, out_filename=None, size=(50,50)):
    try:
        im = Image.open(filename)
        im.thumbnail(size, Image.ANTIALIAS)
        im.save(out_filename)
    except IOError:
        print "cannot create thumbnail for '%s'" % filename