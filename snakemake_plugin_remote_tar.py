from snakemake.common.remote import AbstractRemoteProvider, AbstractRemoteObject
import tarfile
from functools import cached_property
from pathlib import Path
from contextlib import contextmanager

from meta import *


snakemake_submodule_name = "tar"


class RemoteProvider(AbstractRemoteProvider):
    def remote(self, value, *args, **kwargs):
        # As the value will be used for saving files locally, and
        # the tar file is locally (because this is for demonstration purposes)
        # We remove the `.tar` sequence and add it back later in RemoteObject.
        value = "/".join(value.split(".tar/"))
        return super().remote(value, *args, **kwargs)

    @property
    def default_protocol(self):
        return "tar://"

    @property
    def default_protocols(self):
        return [self.default_protocol]


class RemoteObject(AbstractRemoteObject):
    @cached_property
    def archive_file(self):
        # Find the tar file
        f = Path(self.local_file())
        while not f.with_suffix(".tar").exist():
            f = f.parent
        return f.with_suffix(".tar")

    @cached_property
    def file_in_archive(self):
        return self.local_file()[(len(self.archive_file) - 3) :]

    @contextmanager
    def open(self, mode="r"):
        t = tarfile.open(self.archive_file, mode)
        try:
            yield t
        finally:
            t.close()

    def exists(self):
        with self.open() as t:
            try:
                t.get_member(self.file_in_archive)
                return True
            except KeyError:
                return False

    @cached_property
    def tarinfo(self):
        with self.open() as t:
            return t.getmember(self.file_in_archive)

    def mtime(self):
        return self.tarinfo.mtime

    def get_inventory_parent(self):
        return self.archive_file

    def size(self):
        return self.tarinfo.size

    def name(self):
        return self.file_in_archive

    def _download(self):
        with self.open() as t, open(self.local_file(), "rw") as f:
            f.write(t.extractfile(self.file_in_archive).read())

    def _upload(self):
        with self.open("w") as t, open(self.local_file(), "rb") as f:
            t.addfile(t.gettarinfo(fileobj=f, arcname=self.file_in_archive), fileobj=f)

    @property
    def list(self):
        with self.open() as t:
            return t.getnames()
