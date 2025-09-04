import os
import cocotb
import random
from pathlib import Path
from cocotb_tools.runner import get_runner
from cocotb.triggers import RisingEdge
from cocotb.clock import Clock


N = 3233  # modulus
e = 17  # public exponent



def encrypt():
    random_plaintext = "".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@£$%^&*()-=_+'\"|,./<>?`~§±", k=20))
    datafile = "./data/message.hex"
    plaintext_file = "./data/plaintext.txt"
    with open(datafile, "w") as f:
        for ch in random_plaintext:
            m = ord(ch)
            c = pow(m, e, N)
            f.write(f"{c:X}\n")

    with open(plaintext_file, "w") as f:
        f.write(random_plaintext)

    print(f"\nPlaintext: {random_plaintext}\n")
    return random_plaintext


@cocotb.test()
async def test_decryptor(dut):

    clk=Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clk.start())

    dut.reset.value = 1
    dut.encrypted_char.value = 0
    await RisingEdge(dut.clk)
    dut.reset.value = 0

    hex_path = Path(__file__).parent.parent / "data" / "message.hex"
    plaintext_path = Path(__file__).parent.parent / "data" / "plaintext.txt"
    with open(hex_path) as f:
        encrypted_message = [int(line.strip(), 16) for line in f if line.strip()]
    with open(plaintext_path) as f:
            random_plaintext = f.read().strip()

    decrypted_chars = []
    for cipher in encrypted_message:
        dut.encrypted_char.value = cipher
        for _ in range(15):
            await RisingEdge(dut.clk)
        decrypted_chars.append(chr(dut.decrypted_char.value.integer))

    result = "".join(decrypted_chars)
    if result == random_plaintext:
        cocotb.log.info(f"Decrypted message: {result}\n")
    else:
        cocotb.log.error(f"Decryption failed: {result}\n")


def test_my_design_runner():
    sim = os.getenv("SIM", "icarus")

    proj_path = Path(__file__).resolve().parent

    sources = [proj_path / "decryptor.v"]

    runner = get_runner(sim)
    runner.build(
        sources=sources,
        hdl_toplevel="decryptor",
        timescale=("1ns", "1ns")
    )

    runner.test(hdl_toplevel="decryptor", test_module="test_decryptor", timescale=("1ns", "1ns"))


if __name__ == "__main__":
    for i in range(1):
        encrypt()
        test_my_design_runner()