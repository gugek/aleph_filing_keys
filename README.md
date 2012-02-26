## Synopsis

Create filing keys for Library of Congress Classification.

## Examples

    >>> create_lcc_filing_key('KF1245.A45 J32 2011')
    'kf#1245 a4500000 j3200000 20110000'
    >>> create_lcc_filing_key('Q4235.R4 N3256 2001a')
    'q#4235 r4000000 n3256000 2001a000'
    >>> create_lcc_filing_key('KF924.B32 1973')
    'kf"924 b3200000 19730000'
    >>> create_lcc_filing_key('HV23.C32 1953z')
    'hv!23 c3200000 1953z000'
    >>> create_lcc_filing_key('Z1.A9 T32')
    'z 1 a9000000 t3200000'
    >>> create_lcc_filing_key('KJC2100.2006 C9 2012')
    'kjc#2100 20060000 c9000000 20120000'
    >>> create_lcc_filing_key('JN23.42.S42 B43 1990c')
    'jn!23 42000000 s4200000 b4300000 1990c000'
    >>> create_lcc_filing_key('382.532 T32 1999', quiet=False)
    Traceback (most recent call last):
        ...
    ValueError: Not a valid Library of Congress Call Number!
    >>> create_lcc_filing_key('GN923456.A43 T32', quiet=False)
    Traceback (most recent call last):
        ...
    ValueError: Not a valid Library of Congress Call Number!
    """
