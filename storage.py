import hashlib
import os

from django.core.files.storage import FileSystemStorage
from django.db import models

class FileStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        if max_length and len(name) > max_length:
            raise(Exception("name's length is greater than max_length"))
        return name

    def _save(self, name, content):
        if self.exists(name):
            # if the file exists, do not call the superclasses _save method
            return name
        # if the file is new, DO call it
        return super(FileStorage, self)._save(name, content)


def media_file_name(instance, filename):
    h = instance.md5sum
    basename, ext = os.path.splitext(filename)
    return os.path.join('mediafiles', h[0:1], h[1:2], h + ext.lower())


class Media(models.Model):
    # use the custom storage class fo the FileField
    orig_file = models.FileField(
        upload_to=media_file_name, storage=FileStorage())
    md5sum = models.CharField(max_length=36)
    # ...

    def save(self, *args, **kwargs):
        if not self.pk:  # file is new
            md5 = hashlib.md5()
            for chunk in self.orig_file.chunks():
                md5.update(chunk)
            self.md5sum = md5.hexdigest()
        super(Media, self).save(*args, **kwargs)