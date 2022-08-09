from django.core.files.storage import Storage


class DBBlobStorage(Storage):

    def exists(self, name):
        raise NotImplementedError()

    def size(self, name):
        raise NotImplementedError()

    def url(self, name):
        raise NotImplementedError()

    def delete(self, name):
        raise NotImplementedError()

    def listdir(self, path):
        raise NotImplementedError()
