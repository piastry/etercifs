#!/bin/sh
# 2007 (c) Etersoft http://etersoft.ru
# Author: Vitaly Lipatov <lav@etersoft.ru>
# GNU Public License

# Build kernel modules for all kernel and all platforms

fatal()
{
    echo $@
    exit 1
}

DISTR_VENDOR=/usr/bin/distr_vendor

test -x $DISTR_VENDOR || fatal "Can't find distr_vendor"

get_sd()
{
    BASE_KERNEL_SOURCES_DIR=
    BASE_KERNEL_SOURCES_DIR=`grep -i $1 kernel_src.list | head -n1 | cut -d" " -f 2 2>/dev/null`
}

get_etercifs_sd()
{
    ETERCIFS_SOURCES_LIST=
    ETERCIFS_SOURCES_LIST=`grep -i $1 etercifs_src.list | head -n1 | cut -d" " -f 2 2>/dev/null`
}


get_src_dir()
{
    get_sd `$DISTR_VENDOR -e`
    [ -z "$BASE_KERNEL_SOURCES_DIR" ] && get_sd `$DISTR_VENDOR -d`
    [ -z "$BASE_KERNEL_SOURCES_DIR" ] && { echo "Unknown `$DISTR_VENDOR -d`, use Generic for kernel sources" ; get_sd Generic ; }
    [ -z "$BASE_KERNEL_SOURCES_DIR" ] && return 1
    return 0
}

get_etercifs_src_dir()
{
    get_etercifs_sd `$DISTR_VENDOR -e`
    [ -z "$ETERCIFS_SOURCES_LIST" ] && get_etercifs_sd `$DISTR_VENDOR -d`
    [ -z "$ETERCIFS_SOURCES_LIST" ] && { echo "Unknown `$DISTR_VENDOR -d`, use Generic for etercifs sources" ; get_etercifs_sd Generic ; }
    [ -z "$ETERCIFS_SOURCES_LIST" ] && return 1
    return 0
}

exit_handler()
{
    local rc=$?
    trap - EXIT
    [ -z "$tmpdir" ] || rm -rf -- "$tmpdir"
    exit $rc
}

#/lib/modules/$(shell uname -r)/build