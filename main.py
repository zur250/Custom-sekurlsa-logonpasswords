import io
import os
import re
import struct
import logging
import traceback
import json
import ntpath

# from pypykatz.pypykatz import pypykatz
from katz import katz
from commons.common import UniversalEncoder


def main():
    import argparse
    import glob
    parser = argparse.ArgumentParser(
        description='Pure Python sekurlsa::logonpasswords implementation of Mimikatz \n Usage: python main.py [path to lsass.dmp]')

    parser.add_argument('minidumpfile', type=str, help='Path to lsass dump file')

    args = parser.parse_args()

    ##### Common obj
    results = {}
    files_with_error = []

    ###### Minidump
    logging.info('Parsing file %s' % args.minidumpfile)
    try:
        mimi = katz.parse_minidump_file(args.minidumpfile)
        results[args.minidumpfile] = mimi
        for result in results:
            print('FILE: ======== %s =======' % result)
            if isinstance(results[result], str):
                print(results[result])
            else:
                for luid in results[result].logon_sessions:
                    print(str(results[result].logon_sessions[luid]))

                if len(results[result].orphaned_creds) > 0:
                    print('== Orphaned credentials ==')
                    for cred in results[result].orphaned_creds:
                        print(str(cred))
    except Exception as e:
        logging.exception('Error while parsing file %s' % args.minidumpfile)
        if args.halt_on_error == True:
            raise e
        else:
            traceback.print_exc()

    return None


if __name__ == '__main__':
    main()
