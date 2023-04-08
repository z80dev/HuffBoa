huffc_precompile: constant(address) = 0x0000000000000000000000000000000068756666

@external
def compile_huff(filename: String[128]) -> address:
    output: Bytes[32] = raw_call(huffc_precompile, _abi_encode(filename, method_id=method_id("compile_huff(string)")), max_outsize=32)
    huff_contract_address: address = _abi_decode(output, address)
    return huff_contract_address
