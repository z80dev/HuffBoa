#!/usr/bin/env python3
import boa
from boa.environment import abi, register_precompile
import subprocess
import binascii

# Adder smart contract source stub to use as interface
adder_source = """
@external
def addnums(x: uint256, y: uint256) -> uint256:
    return x + y
"""

# Load the Adder contract from source code
AdderContract = boa.loads_partial(adder_source, "Adder")

@boa.precompile("def huff(filename: String[128]) -> address")
def huff(filename: str):
    compilation_process = subprocess.run(["huffc", "-b", filename], capture_output=True)

    contract_address = boa.env.generate_address()
    contract_bytecode = binascii.unhexlify(compilation_process.stdout)
    boa.env.deploy_code(deploy_to=contract_address, bytecode=contract_bytecode)

    return contract_address


HUFF_PRECOMPILE_ADDRESS = bytes.fromhex("0000000000000000000000000000000068756666") # "huff" in bytes
register_precompile(HUFF_PRECOMPILE_ADDRESS, huff)

huff_deployer = boa.load("contracts/HuffDeployer.vy")
huff_user = boa.load("contracts/HuffUser.vy")

huff_adder_address = huff_deployer.compile_huff("contracts/HuffAdder.huff")
huff_adder_instance = AdderContract.at(huff_adder_address)

print(huff_adder_instance.addnums(6, 4))
print(huff_user.useHuff(huff_adder_instance))
