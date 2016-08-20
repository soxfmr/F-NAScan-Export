import re
import sys
from os.path import abspath

TAG_START   = 'adinfo='
TAG_END     = '"}];'
# javascript:view('0.0.0.0:80');
PATTERN_PORT = 'javascript:view\(\'(\d+\.\d+\.\d+\.\d+):%d\'\)'

def export(hosts, filename):
    bRet = False
    with open(filename, 'w+') as handle:
        for host in hosts:
            handle.write(host + '\n')
        bRet = True

    return bRet

def main():
    argv = sys.argv
    if len(argv) < 3:
        print 'Usage: export.py <file> <port> [-o <filename>]'
        sys.exit(0)

    try:
        port = int(argv[2])
        if port <= 0 and port > 65536:
            raise ValueError('Invalid service port.')

        with open(argv[1], 'r') as handle:
            data = handle.read()
            start_offset = data.find(TAG_START)
            end_offset = data.find(TAG_END)

            if not start_offset or not end_offset:
                raise Exception('No tags found.')

            start_offset += len(TAG_START)
            end_offset += len(TAG_END)

            data = data[start_offset:end_offset]

            hosts = re.findall(PATTERN_PORT % port, data)
            if not hosts:
                print '[-] No result matched.'
                sys.exit(0)

            for host in hosts:
                print host

            if len(argv) == 5:
                if export(hosts, argv[4]):
                    print '\n[+] Totally %d results saved to %s' % \
                        (len(hosts), abspath(argv[4]))
                else:
                    print '\n[-] Export failed.'
    except Exception as e:
        print e

if __name__ == '__main__':
    main()
