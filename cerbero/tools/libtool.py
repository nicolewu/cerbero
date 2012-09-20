#!/usr/bin/env python
# cerbero - a multi-platform build system for Open Source software
# Copyright (C) 2012 Andoni Morales Alastruey <ylatuya@gmail.com>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public
# License along with this library; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.

import os


class LibtoolLibrary(object):
    '''
    Helper class to create libtool libraries files (.la)
    '''

    LIBTOOL_HEADER = '''\
# %s - a libtool library file
# Generated by libtool (GNU libtool) 2.4.2 Debian-2.4.2-1ubuntu1\n'''

    LIBTOOL_LA = {
        'dlname': '',
        'library_names': '',
        'old_library': '',
        'inherited_linker_flags': '',
        'dependency_libs': '',
        'weak_library_names': '',
        'current': '',
        'age': '',
        'revision': '',
        'installed': 'yes',
        'shouldnotlink': 'no',
        'dlopen': '',
        'dlpreopen': '',
        'libdir': ''
        }

    def __init__(self, libname, major, minor, micro, libdir, deps=None):
        if not libname.startswith('lib'):
            libname = 'lib%s' % libname
        if deps is None:
            deps = ''
        self.libname = libname
        self.libdir = libdir
        self.laname = '%s.la' % libname
        dlname_base = '%s.so' % (libname)
        dlname = dlname_base
        dlname_all = dlname_base
        major_str = ''
        minor_str = ''
        micro_str = ''

        if major is not None:
            dlname = '%s.%s' % (dlname_base, major)
            major_str = major
            if minor is not None:
                dlname_all = '%s.%s' % (dlname, minor)
                minor_str = major
                if micro is not None:
                    dlname_all = '%s.%s' % (dlname, micro)
                    micro_str
        old_library = '%s.a' %  libname
        self.header = self.LIBTOOL_HEADER % self.laname
        self.change_value('dlname', dlname)
        self.change_value('library_name', '%s %s %s' % (dlname_all, dlname,
            dlname_base))
        self.change_value('old_library', old_library)
        self.change_value('current', major_str)
        self.change_value('age', minor_str)
        self.change_value('micro', micro_str)
        self.change_value('libdir', libdir)
        self.change_value('dependency_libs', deps)

    def save(self):
        path = os.path.join(self.libdir, self.laname)
        with open(path, 'w') as f:
            f.write(self.header)
            f.write('\n')
            for k, v in self.LIBTOOL_LA.iteritems():
                f.write("%s='%s'\n" % (k, v))

    def change_value(self, key, val):
        self.LIBTOOL_LA[key] = val