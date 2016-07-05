# ----------------------------------------------------------------------------
# Copyright (c) 2016--, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
# ----------------------------------------------------------------------------

import abc
import zipfile
import tempfile

import qiime.core.archiver


class ResultBase(metaclass=abc.ABCMeta):
    """ABC for QIIME 2 result/output classes."""

    @classmethod
    @abc.abstractmethod
    def _assert_valid_type(cls, type_):
        raise NotImplementedError

    @classmethod
    def load(cls, filepath):
        result = cls.__new__(cls)
        result._archiver = qiime.core.archiver.Archiver.load(filepath)
        result._assert_valid_type(result.type)
        return result

    @classmethod
    def extract(cls, filepath, output_dir=None):
        if output_dir is None:
            output_dir = tempfile.gettempdir()
        with zipfile.ZipFile(filepath, mode='r') as zf:
            zf.extractall(output_dir)
        return output_dir

    @property
    def type(self):
        return self._archiver.type

    @property
    def provenance(self):
        return self._archiver.provenance

    @property
    def uuid(self):
        return self._archiver.uuid

    def __init__(self):
        class_name = self.__class__.__name__
        raise NotImplementedError(
            "%s constructor is private, use `%s.load`." %
            (class_name, class_name))

    def __new__(cls):
        result = object.__new__(cls)
        result._archiver = None
        return result

    def _orphan(self, pid):
        self._archiver.orphan(pid)

    def save(self, filepath):
        self._archiver.save(filepath)
