from flask_admin.contrib.sqla import ModelView
from app import admin, db
from app.models import Author, Authorship, Usage, Book


admin.add_view(ModelView(Author, db.session))
admin.add_view(ModelView(Authorship, db.session))
admin.add_view(ModelView(Usage, db.session))

from flask_admin.contrib import sqla
from flask_admin import form

import random
import os


class StorageAdminModel(sqla.ModelView):
    form_extra_fields = {
        'file': form.FileUploadField('file')
    }

    def _change_path_data(self, _form):
        try:
            storage_file = _form.file.data

            if storage_file is not None:
                hash = random.getrandbits(128)
                ext = storage_file.filename.split('.')[-1]
                path = '%s.%s' % (hash, ext)
                from config import Config
                storage_file.save(
                    os.path.join(Config.BOOKSDIR, path)
                )

                _form.path.data = path
                del _form.file

        except Exception as ex:
            pass

        return _form

    def edit_form(self, obj=None):
        return self._change_path_data(
            super(StorageAdminModel, self).edit_form(obj)
        )

    def create_form(self, obj=None):
        return self._change_path_data(
            super(StorageAdminModel, self).create_form(obj)
        )


admin.add_view(StorageAdminModel(Book, db.session))