# -*- coding: utf-8 -*-

class BaseX(object):
    def __init__(self, charset="0123456789"):
        self.base = len(charset)
        self.n_c = charset
        self.c_n = {}
        for n, c in enumerate(charset):
            self.c_n[c] = n

    def encode(self, n):
        if n == 0:
            return self.n_c[0]
        l = []
        while n:
            n, m = divmod(n, self.base)
            l.append(self.n_c[m])
        return ''.join(reversed(l))

    def decode(self, s):
        n = 0
        for c in s:
            n = n * self.base + self.c_n[c]
        return n

base2 = BaseX('01')
base16 = BaseX('0123456789ABCDEF')
base36 = BaseX('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ')
base62 = BaseX('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz')

if __name__ == '__main__':
    import random
    ascii = ''.join(map(chr, xrange(256)))

    for i in xrange(1000):
        charset = ascii[:random.randint(2, 256)]
        base = BaseX(charset)
        if i != base.decode(base.encode(i)):
            assert False

    for i in xrange(1000):
        s = base16.encode(i)
        assert i == base16.decode(s) == int(s, 0x10)

    base62_data = [
        (0,     "0"),
        (1,     "1"),
        (10,     "A"),
        (35,     "Z"),
        (36,     "a"),
        (61,     "z"),
        (62,     "10"),
        (3844,     "100"),
        (238328,     "1000"),
        (14776336,     "10000"),
        ]

    for n, s in base62_data:
        assert base62.encode(n) == s
        assert base62.decode(s) == n
