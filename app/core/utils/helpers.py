import datetime
import uuid
import os

from slugify import slugify


def get_file_filename(instance, filename, folder):
    current_date = datetime.date.today()
    path = u"{}/{}/{}/".format(folder, current_date.year, current_date.month)  # It is real path address

    file_uuid = str(uuid.uuid4())
    file_name, file_extension = os.path.splitext(filename)
    name = u"{}{}".format(file_uuid, file_extension)

    full_filename = unicode(os.path.join(path, name).lower())

    return full_filename


def get_slug(title):
    slug = slugify(unicode(title))
    return slug


def get_dict_as_request_params(d, exclude=None):
    result = ""
    for i, v in enumerate(d):
        if (not exclude) or (exclude and exclude != v):
            result += "{}={}&".format(v, d.get(v))
    result = result[0:-1] if result else ""
    return result

