interface Adder:
    def addnums(a: uint256, b: uint256) -> uint256: nonpayable

@external
def useHuff(adder: Adder) -> uint256:
    return adder.addnums(1, 2)
