#!/usr/bin/python

import lxml.etree as ET
import sys
import re
import string
from optparse import OptionParser


def create_lcc_filing_key(s, quiet=True):
    """Create a ALEPH style filing key for an lcc string

    >>> create_lcc_filing_key('KF12454.A45 J32 2011', quiet=True)
    'kf#12454 a45 j32 2011'
    >>> create_lcc_filing_key('Q4235.R4 N3256 2001a')
    'q#4235 r4 n3256 2001a'
    >>> create_lcc_filing_key('KF924.B32 1973')
    'kf"924 b32 1973'
    >>> create_lcc_filing_key('HV23.C32 1953z')
    'hv!23 c32 1953z'
    >>> create_lcc_filing_key('Z1.A9 T32')
    'z 1 a9 t32'
    >>> create_lcc_filing_key('382.532 T32 1999', quiet=False)
    Traceback (most recent call last):
        ...
    ValueError: Not a valid Library of Congress Call Number!
    >>> create_lcc_filing_key('GN923456.A43 T32', quiet=False)
    Traceback (most recent call last):
        ...
    ValueError: Not a valid Library of Congress Call Number!
    """

    blanks = string.ljust('', len(string.punctuation), ' ')
    table = string.maketrans(string.punctuation, blanks)
    lcc_re = re.compile('^([a-z]+)(\d+)(.*)')
    s = s.translate(table)
    s = re.sub('\s+', ' ', s)
    s = s.lower()
    s = s.strip()
    lcc_match = lcc_re.match(s)
    if lcc_match:
        (alpha, number, rest) = lcc_match.groups()
        if len(number) == 1:
            s = '%s %s%s' % (alpha, number, rest)
        elif len(number) == 2:
            s = '%s!%s%s' % (alpha, number, rest)
        elif len(number) == 3:
            s = '%s"%s%s' % (alpha, number, rest)
        elif len(number) == 4:
            s = '%s#%s%s' % (alpha, number, rest)
        elif quiet == True:
            s = '%s#%s%s' % (alpha, number, rest)
        else:
            raise ValueError('Not a valid Library of Congress Call Number!')
    elif quiet == True:
        pass
    else:
        raise ValueError('Not a valid Library of Congress Call Number!')
    return s

def main():
    """Open a ALEPH item output file and filter it based on a range of LC call
    numbers"""
    optionparser = OptionParser()
    optionparser.add_option('-f', '--file', dest='infile',
            help="file to read")
    optionparser.add_option('-o', '--output', dest='outfile',
            help="file to output")
    optionparser.add_option('-l', '--lower', dest='lbound',
            help="lower call number bound")
    optionparser.add_option('-u', '--upper', dest='ubound',
            help="upper call number bound")
    optionparser.add_option('-c', '--counter', type="int", dest='counter',
            help="progress counter")
    optionparser.set_defaults(counter=100)
    (options, args) = optionparser.parse_args()
    if not options.infile or not options.outfile or not options.lbound or \
        not options.ubound:
            print "Need to fill in all the options!"
            sys.exit()
    infile = open(options.infile, 'rb')
    outfile = open(options.outfile, 'w')
    parser = ET.iterparse(infile)

    begin = create_lcc_filing_key(options.lbound, quiet=False)
    end = create_lcc_filing_key(options.ubound, quiet=False)
    i = 0
    j = 0
    for (event, elem) in parser:
        if elem.tag == 'section-02':
            i += 1
            if i % options.counter == 0:
                sys.stdout.write("\rFound %s in %s records." % (j, i))
                sys.stdout.flush()
            call_no = elem.find('.//z30-call-no-key').text
            if call_no >= begin and call_no <= end:
                j += 1
                outfile.write(ET.tostring(elem, encoding='utf8').strip())
                outfile.write("\n")
            elem.clear()
    sys.stdout.write("\rFound %s in %s records.\n" % (j, i))

if __name__ == "__main__":
    main()
