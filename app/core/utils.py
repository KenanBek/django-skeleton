import datetime
import uuid

import os


def get_file_filename(instance, filename, folder):
    current_date = datetime.date.today()
    path = u"{}/{}/{}/".format(folder, current_date.year, current_date.month)  # It is real path address

    file_uuid = str(uuid.uuid4())
    file_name, file_extension = os.path.splitext(filename)
    name = u"{}{}".format(file_uuid, file_extension)

    full_filename = unicode(os.path.join(path, name).lower())

    return full_filename

