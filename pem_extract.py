#!/usr/bin/env python

from __future__ import print_function
import hashlib
import re
import shlex
import subprocess
import sys


class OpenSSLWrapper(object):
    """Class containing helper methods for using OpenSSL."""

    @staticmethod
    def _exec_openssl(args, indata):
        args = shlex.split(args)
        proc = subprocess.Popen(
            ['openssl'] + args, stdin=subprocess.PIPE,
            stdout=subprocess.PIPE, close_fds=True)
        stdout, _ = proc.communicate(indata)
        return stdout.strip()

    @classmethod
    def openssl_hash(cls, pemdata):
        options = 'x509 -noout -hash'
        return cls._exec_openssl(options, pemdata)

    @classmethod
    def openssl_fingerprint(cls, pemdata):
        options = 'x509 -noout -fingerprint'
        return cls._exec_openssl(options, pemdata).split('=', 1)[-1]


class PEMExtractor(object):
    """Hunt for PEM files within another file or file-like object."""

    _pem_re = re.compile(
        r'-----BEGIN ([^-]+)-----'
        r'[A-Za-z0-9+/\n\r]+=*[\r\n]*'
        r'-----END \1-----')

    def __init__(self, source, block_size=5*1024*1024):
        self.block_size = block_size
        if isinstance(source, basestring):
            self.source = open(source, 'rb')
        else:
            try:
                getattr(source, 'read')
            except AttributeError:
                raise ValueError(
                    'source must be a filename or file-like object.')
            self.source = source

    def walk(self, callback, unique=True):
        chunk = ''
        seen = set()
        while True:
            tail = len(chunk)
            tmp = self.source.read(self.block_size)
            if not tmp:
                break
            chunk += tmp
            for m in self._pem_re.finditer(chunk):
                tail = max(tail, m.end())
                cert = m.group()
                fp = OpenSSLWrapper.openssl_fingerprint(cert)
                if not unique or fp not in seen:
                    callback(cert)
                    seen.add(fp)
            chunk = chunk[tail:]

    def save_certs(self):
        def save_single_cert(cert):
            cert_hash = OpenSSLWrapper.openssl_hash(cert)
            filename = '{}.pem'.format(cert_hash)
            with open(filename, 'wb') as fp:
                fp.write(cert)
            print('Wrote {}'.format(filename))
        self.walk(save_single_cert)


if __name__ == '__main__':
    try:
        source = sys.argv[1]
    except IndexError:
        source = sys.stdin
    extractor = PEMExtractor(source)
    extractor.save_certs()
