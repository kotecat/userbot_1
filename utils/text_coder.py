zov_encode = {
    "00": "o",
    "01": "v",
    "10": "z",
    "11": " "
}

zov_decode = {v: k for k, v in zov_encode.items()}


def text_to_bits(text: str) -> str:
    byte_array = text.encode('utf-8')
    bit_string = ''.join(f'{byte:08b}' for byte in byte_array)
    return bit_string


def bits_to_text(bit_string):
    if len(bit_string) % 8 != 0:
        raise ValueError("The length of the bit string must be a multiple of 8")

    byte_array = bytearray(int(bit_string[i:i + 8], 2) for i in range(0, len(bit_string), 8))
    text = byte_array.decode('utf-8')
    return text


def bits_to_code(bits: str, d_ = zov_encode, step: int = 2) -> str:
    r = []
    for i in range(0, len(bits), step):
        part = bits[i:i+step]
        r.append(d_.get(part, "?"))
    return "".join(r)


def code_to_bits(code: str, d_ = zov_decode) -> str:
    return "".join([d_.get(l, "?") for l in code])
