import os

BLOCK_SIZE = 8

IP = [
    58, 50, 42, 34, 26, 18, 10, 2,  60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6,  64, 56, 48, 40, 32, 24, 16, 8,
    57, 49, 41, 33, 25, 17, 9,  1,  59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5,  63, 55, 47, 39, 31, 23, 15, 7
]

IP_INV = [
    40, 8,  48, 16, 56, 24, 64, 32, 39, 7,  47, 15, 55, 23, 63, 31,
    38, 6,  46, 14, 54, 22, 62, 30, 37, 5,  45, 13, 53, 21, 61, 29,
    36, 4,  44, 12, 52, 20, 60, 28, 35, 3,  43, 11, 51, 19, 59, 27,
    34, 2,  42, 10, 50, 18, 58, 26, 33, 1,  41, 9,  49, 17, 57, 25
]

PC1 = [
    57, 49, 41, 33, 25, 17, 9,   1, 58, 50, 42, 34, 26, 18,
    10, 2,  59, 51, 43, 35, 27, 19, 11, 3,  60, 52, 44, 36,
    63, 55, 47, 39, 31, 23, 15,  7, 62, 54, 46, 38, 30, 22,
    14, 6,  61, 53, 45, 37, 29, 21, 13, 5,  28, 20, 12, 4
]

PC2 = [
    14, 17, 11, 24, 1,  5,  3,  28, 15, 6,  21, 10,
    23, 19, 12, 4,  26, 8,  16, 7,  27, 20, 13, 2,
    41, 52, 31, 37, 47, 55, 30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32
]

SHIFTS = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

E_TABLE = [
    32, 1,  2,  3,  4,  5,   4,  5,  6,  7,  8,  9,
    8,  9,  10, 11, 12, 13, 12, 13, 14, 15, 16, 17,
    16, 17, 18, 19, 20, 21, 20, 21, 22, 23, 24, 25,
    24, 25, 26, 27, 28, 29, 28, 29, 30, 31, 32, 1
]

P_TABLE = [
    16, 7,  20, 21, 29, 12, 28, 17, 1,  15, 23, 26, 5,  18, 31, 10,
    2,  8,  24, 14, 32, 27, 3,  9,  19, 13, 30, 6,  22, 11, 4,  25
]

S_BOXES = [
    [
        [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
        [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
        [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
        [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]
    ],
    [
        [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
        [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
        [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
        [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]
    ],
    [
        [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
        [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
        [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
        [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]
    ],
    [
        [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
        [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
        [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
        [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]
    ],
    [
        [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
        [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
        [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
        [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]
    ],
    [
        [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
        [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
        [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
        [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]
    ],
    [
        [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
        [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
        [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
        [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]
    ],
    [
        [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
        [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
        [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
        [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]
    ]
]


def bytes_to_bits(data):
    """Mengubah bytes menjadi list bit [0, 1]."""
    bits = []
    for byte in data:
        for i in range(7, -1, -1):
            bits.append((byte >> i) & 1)
    return bits

def bits_to_bytes(bits):
    """Mengubah list bit [0, 1] menjadi bytes."""
    if len(bits) % 8 != 0:
        raise ValueError("Jumlah bit harus merupakan kelipatan 8.")
    byte_array = bytearray()
    for i in range(0, len(bits), 8):
        byte = 0
        for bit in bits[i:i+8]:
            byte = (byte << 1) | bit
        byte_array.append(byte)
    return bytes(byte_array)

def permute(bits, table):
    """Melakukan permutasi bit berdasarkan tabel indeks (1-based)."""
    return [bits[p - 1] for p in table]

def xor_bits(bits1, bits2):
    """Operasi XOR antara 2 list bit."""
    if len(bits1) != len(bits2):
        raise ValueError("Kedua input XOR harus memiliki panjang yang sama.")
    return [b1 ^ b2 for b1, b2 in zip(bits1, bits2)]

def left_shift(bits, n):
    """Pergeseran bit ke kiri secara sirkular."""
    return bits[n:] + bits[:n]


def generate_subkeys(key_bytes):
    """Menghasilkan 16 subkey (masing-masing 48 bit) dari kunci 8 byte."""
    if not isinstance(key_bytes, bytes) or len(key_bytes) != BLOCK_SIZE:
        raise ValueError("Kunci DES harus tepat 8 byte (64 bit, 56 bit efektif).")
    key_bits = bytes_to_bits(key_bytes)
    permuted_key = permute(key_bits, PC1)
    
    C = permuted_key[:28]
    D = permuted_key[28:]
    
    subkeys = []
    for shift in SHIFTS:
        C = left_shift(C, shift)
        D = left_shift(D, shift)
        subkeys.append(permute(C + D, PC2))
        
    return subkeys


def feistel_function(r_bits, subkey):
    """Fungsi Feistel f(R, K): Expansion -> XOR -> S-Box -> Permutation P."""
    expanded_r = permute(r_bits, E_TABLE)
    xored = xor_bits(expanded_r, subkey)
    
    sbox_output = []
    for i in range(8):
        block = xored[i * 6 : (i + 1) * 6]
        row = (block[0] << 1) | block[5]
        col = (block[1] << 3) | (block[2] << 2) | (block[3] << 1) | block[4]
        val = S_BOXES[i][row][col]
        
        for shift in range(3, -1, -1):
            sbox_output.append((val >> shift) & 1)
            
    return permute(sbox_output, P_TABLE)


def des_process_block(block_bits, subkeys):
    """Memproses 1 blok (64-bit) melalui Initial Permutation, 16 Round, dan Final Permutation."""
    if len(block_bits) != 64:
        raise ValueError("Satu blok DES harus tepat 64 bit.")
    if len(subkeys) != 16 or any(len(subkey) != 48 for subkey in subkeys):
        raise ValueError("DES membutuhkan 16 subkey, masing-masing 48 bit.")
    permuted_block = permute(block_bits, IP)
    L = permuted_block[:32]
    R = permuted_block[32:]
    
    for subkey in subkeys:
        next_L = R
        f_result = feistel_function(R, subkey)
        next_R = xor_bits(L, f_result)
        L, R = next_L, next_R
        
    return permute(R + L, IP_INV)


def pkcs7_pad(data, block_size=BLOCK_SIZE):
    """Menambahkan padding PKCS#7."""
    if not 1 <= block_size <= 255:
        raise ValueError("Ukuran blok PKCS#7 harus berada di antara 1 dan 255 byte.")
    pad_len = block_size - (len(data) % block_size)
    return data + bytes([pad_len] * pad_len)


def pkcs7_unpad(data, block_size=BLOCK_SIZE):
    """Menghapus sekaligus memvalidasi padding PKCS#7."""
    if not data or len(data) % block_size != 0:
        raise ValueError("Data berpadding harus tidak kosong dan berukuran kelipatan blok.")

    pad_len = data[-1]
    if pad_len < 1 or pad_len > block_size:
        raise ValueError("Padding PKCS#7 tidak valid.")
    if data[-pad_len:] != bytes([pad_len]) * pad_len:
        raise ValueError("Padding PKCS#7 tidak valid.")
    return data[:-pad_len]


def _normalise_key(key):
    """Mengubah key teks/bytes menjadi key DES yang panjangnya tepat 8 byte."""
    if isinstance(key, str):
        key_bytes = key.encode("utf-8")
    elif isinstance(key, bytes):
        key_bytes = key
    else:
        raise TypeError("Kunci harus berupa str atau bytes.")

    if len(key_bytes) != BLOCK_SIZE:
        raise ValueError(
            "Kunci DES harus tepat 8 byte setelah encoding UTF-8; "
            "kunci tidak akan dipotong atau ditambah otomatis."
        )
    return key_bytes


def _xor_bytes(left, right):
    if len(left) != len(right):
        raise ValueError("Kedua input XOR harus memiliki panjang yang sama.")
    return bytes(a ^ b for a, b in zip(left, right))


def _crypt_block(block, subkeys):
    if len(block) != BLOCK_SIZE:
        raise ValueError("Satu blok DES harus tepat 8 byte.")
    result_bits = des_process_block(bytes_to_bits(block), subkeys)
    return bits_to_bytes(result_bits)


def encrypt(plaintext, key):
    """
    Mengenkripsi teks dengan DES-CBC dan padding PKCS#7.

    Nilai yang dikembalikan adalah hex dari IV || ciphertext. IV bukan key dan
    boleh dikirim bersama ciphertext. Implementasi DES dan CBC dibuat manual;
    os.urandom hanya digunakan untuk membuat IV acak.
    """
    if not isinstance(plaintext, str):
        raise TypeError("Plaintext harus berupa str.")

    key_bytes = _normalise_key(key)
    subkeys = generate_subkeys(key_bytes)
    iv = os.urandom(BLOCK_SIZE)
    padded_bytes = pkcs7_pad(plaintext.encode("utf-8"))
    ciphertext_bytes = bytearray()

    previous = iv
    for i in range(0, len(padded_bytes), BLOCK_SIZE):
        block = padded_bytes[i : i + BLOCK_SIZE]
        encrypted_block = _crypt_block(_xor_bytes(block, previous), subkeys)
        ciphertext_bytes.extend(encrypted_block)
        previous = encrypted_block

    return (iv + bytes(ciphertext_bytes)).hex()


def decrypt(ciphertext_hex, key):
    """Mendekripsi hex berformat IV || ciphertext dari fungsi encrypt()."""
    if not isinstance(ciphertext_hex, str):
        raise TypeError("Ciphertext harus berupa string hexadecimal.")

    key_bytes = _normalise_key(key)
    try:
        encrypted_data = bytes.fromhex(ciphertext_hex)
    except ValueError as exc:
        raise ValueError("Ciphertext bukan hexadecimal yang valid.") from exc

    # Minimal: 8 byte IV dan 8 byte ciphertext; total harus kelipatan blok.
    if len(encrypted_data) < 2 * BLOCK_SIZE or len(encrypted_data) % BLOCK_SIZE != 0:
        raise ValueError(
            "Ciphertext harus berisi IV 8 byte diikuti minimal satu blok 8 byte."
        )

    iv = encrypted_data[:BLOCK_SIZE]
    ciphertext_bytes = encrypted_data[BLOCK_SIZE:]
    subkeys = generate_subkeys(key_bytes)[::-1]
    decrypted_bytes = bytearray()

    previous = iv
    for i in range(0, len(ciphertext_bytes), BLOCK_SIZE):
        block = ciphertext_bytes[i : i + BLOCK_SIZE]
        decrypted_block = _xor_bytes(_crypt_block(block, subkeys), previous)
        decrypted_bytes.extend(decrypted_block)
        previous = block

    unpadded_bytes = pkcs7_unpad(bytes(decrypted_bytes))
    try:
        return unpadded_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Hasil dekripsi bukan teks UTF-8 yang valid.") from exc


if __name__ == "__main__":
    SECRET_KEY = "MYSECRET"
    MESSAGE = "Hello, World!"

    print(f"Plaintext   : {MESSAGE}")
    encrypted_hex = encrypt(MESSAGE, SECRET_KEY)
    print(f"Ciphertext  : {encrypted_hex}")
    decrypted_text = decrypt(encrypted_hex, SECRET_KEY)
    print(f"Decrypted   : {decrypted_text}")
