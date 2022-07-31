from ordered_set import OrderedSet


# Only letters that are easy to differentiate
base22_symbol_space = "abcdefghjkmnpqrstuwxyz"

base16_symbol_space = "0123456789ABCDEF"


class IntBaseX:
    def __init__(self, value, symbol_set=base22_symbol_space):
        self._value = value
        self._symbol_set = None
        if symbol_set is not None:
            self._set_symbols(symbol_set)

    def _set_symbols(self, symbol_set):
        ss = OrderedSet(symbol_set)
        assert "".join(c for c in symbol_set) == "".join(c for c in ss), "Your symbol set has duplicates"
        self._symbol_set = ss

    def as_base(self, symbol_set=None, pad_zero=None):
        if symbol_set is not None:
            self._set_symbols(symbol_set)
        if self._symbol_set is None:
            return str(self)
        symbol_set = "".join(self._symbol_set)
        ret = self._to_int_basex(self._value, symbol_set)
        if pad_zero is not None and len(ret) < pad_zero:
            ret = (symbol_set[0] * (pad_zero-len(ret))) + ret
        return ret

    def __int__(self):
        return self.as_int()

    def as_int(self, value=None, case_sensitive=False):
        if self._symbol_set is None:
            return float('nan')
        if value is None:
            value = self._to_int_basex(self._value, self._symbol_set)
        else:
            self._value = self._from_int_basex(value, self._symbol_set)

        symbol_set = "".join(self._symbol_set)
        if not case_sensitive:
            value = value.upper()
            symbol_set = symbol_set.upper()
        return self._from_int_basex(value, symbol_set)

    @classmethod
    def _to_int_basex(cls, number, symbol_set):
        d, m = divmod(number, len(symbol_set))
        if d > 0:
            return cls._to_int_basex(d, symbol_set) + symbol_set[abs(m)]
        return symbol_set[abs(m)]

    @classmethod
    def _from_int_basex(cls, s, symbol_set):
        res = 0
        for c in s:
            res *= len(symbol_set)
            try:
                res += symbol_set.index(c)
            except (ValueError, KeyError):
                print(f"Symbol {c} not in {''.join(symbol_set)}")
                raise
        return res

    def __str__(self):
        if self._symbol_set is None:
            return "Empty symbol set"
        return self.as_base()


if __name__ == "__main__":
    # Very big number in hex for readability
    val = 0x2754fad5bc1
    ibx = IntBaseX(val, base16_symbol_space)
    print(ibx.as_base())
    ret = hex(ibx.as_int())[2:].upper()
    print(ret)

    expect = hex(val)[2:].upper()
    assert ret == expect, f"got {ret} expected {expect}"

    # From the original example
    val = 1399871903
    ss = '_HELOWRD'
    ibx = IntBaseX(val, ss)
    print(ibx)
    ret2 = ibx.as_int()
    print(ret2)

    expect = 'hello_world'
    assert ret2 == val, f"got {ret2} expected {val}"

    # Using base 22, and padding
    ibx = IntBaseX(val)
    print(ibx.as_base(pad_zero=10))
    ret2 = ibx.as_int()
    print(ret2)

    assert ret2 == val, f"got {ret2} expected {val}"

    print(IntBaseX(1).as_base(pad_zero=10).upper())