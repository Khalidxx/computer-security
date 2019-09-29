import numpy as np

# set print option for numpy to print all int as hex
np.set_printoptions(formatter={'int':hex})


def encrypt(plain_text, key, pdc='x', subByte = None, mix_const=None, RCon=None):
    if(subByte is None): 
        sub_byte = np.array([[0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76],
                            [0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0],
                            [0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15],
                            [0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75],
                            [0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84],
                            [0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF],
                            [0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8],
                            [0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2],
                            [0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73],
                            [0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB],
                            [0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79],
                            [0xE7, 0xCB, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08],
                            [0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A],
                            [0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E],
                            [0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF],
                            [0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16]])
    if(mix_const is None):
        mix_const = np.array([[0x02, 0x03, 0x01, 0x01],
                             [0x01, 0x02, 0x03, 0x01],
                             [0x01, 0x01, 0x02, 0x03],
                             [0x03, 0x01, 0x01, 0x02]])
    
    if(RCon is None):
        RCon = np.array([[0x01, 0x00, 0x00, 0x00],
                        [0x02, 0x00, 0x00, 0x00],
                        [0x04, 0x00, 0x00, 0x00],
                        [0x08, 0x00, 0x00, 0x00],
                        [0x10, 0x00, 0x00, 0x00],
                        [0x20, 0x00, 0x00, 0x00],
                        [0x40, 0x00, 0x00, 0x00],
                        [0x80, 0x00, 0x00, 0x00],
                        [0x1B, 0x00, 0x00, 0x00],
                        [0x36, 0x00, 0x00, 0x00]])
    round_key = key
    plain_text = plain_text.upper()

    # Initial state matrix
    state = np.empty([4, 4],  dtype=int)


    # Remove spaces and other characters to shorten Plain Text
    short_text = ''
    for c in plain_text:
        if ord(c) >= 65 and ord(c) <= 90:
            short_text += c

    # Add padding if necessery
    msg_length = len(short_text)
    for i in range(16 - msg_length):
        short_text += pdc.upper()

    # Convert the plain text to the initial state matrix
    rows = state.shape[0]
    cols = state.shape[1]

    for i in range(rows):
        for j in range(cols):
            state[j][i] = ord(short_text[i * rows + j])


    # 0. Add  pre-round key

    state = np.bitwise_xor(state, key)

    for round_no in range(10):
        # 1. SubByte

        for i in range(rows):
            for j in range(cols):
                x = state[i,j] % 0x10
                y = int(state[i,j] / 0x10)
                state[i][j] = sub_byte[y, x]


        # 2. Shift rows

        shifted = np.empty([rows, cols],  dtype=int)

        for i in range(rows):
            for j in range(cols):
                shifted[i, j] = state[i, (j + i) % cols]

        # 3. Mix columns
        if round_no < 9:
            mixed = np.matmul(mix_const, shifted) % 0xff


        # 4. Add round key

        # Rotate key
        temp = round_key.transpose()[cols-1]
        t = np.empty(cols, dtype=int)

        for i in range(cols):
            t[i] = temp[(i + 1) % cols]
        # SubByte key
        for i in range(cols):
            x = t[i] % 0x10
            y = int(t[i] / 0x10)
            t[i] = sub_byte[y, x]

        # X-OR with RCon
        t = np.bitwise_xor(t, RCon[round_no])

        # X-OR t and words from previous key
        current_key = np.empty([rows, cols], dtype=int)
        current_key[0] = np.bitwise_xor(t, round_key.transpose()[0])
        for i in range(1, cols):
            current_key[i] = np.bitwise_xor(current_key[i-1], round_key.transpose()[i])

        round_key = np.array(current_key.transpose())

        # Add roundKey to state
        final_state = np.bitwise_xor(mixed, round_key)

    return final_state.flatten('F')


def decrypt(cipher_text, key, subByte = None, inv_mix=None, RCon=None):
    
    if(subByte is None): 
        sub_byte = np.array([[0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76],
                            [0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0],
                            [0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15],
                            [0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75],
                            [0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84],
                            [0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF],
                            [0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8],
                            [0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2],
                            [0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73],
                            [0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB],
                            [0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79],
                            [0xE7, 0xCB, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08],
                            [0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A],
                            [0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E],
                            [0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF],
                            [0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16]])
    if(inv_mix is None):
        inv_mix = np.array([[0x0E, 0x0B, 0x0D, 0x09],
                             [0x09, 0x0E, 0x0B, 0x0D],
                             [0x0D, 0x09, 0x0E, 0x0B],
                             [0x0B, 0x0D, 0x09, 0x0E]])

    
    if(RCon is None):
        RCon = np.array([[0x01, 0x00, 0x00, 0x00],
                        [0x02, 0x00, 0x00, 0x00],
                        [0x04, 0x00, 0x00, 0x00],
                        [0x08, 0x00, 0x00, 0x00],
                        [0x10, 0x00, 0x00, 0x00],
                        [0x20, 0x00, 0x00, 0x00],
                        [0x40, 0x00, 0x00, 0x00],
                        [0x80, 0x00, 0x00, 0x00],
                        [0x1B, 0x00, 0x00, 0x00],
                        [0x36, 0x00, 0x00, 0x00]])
    
    # convert cipher text to state
    state = np.empty([4, 4],  dtype=int)
    
    rows = state.shape[0]
    cols = state.shape[1]

    for i in range(rows):
        for j in range(cols):
            state[j][i] = cipher_text[i*cols + j]
    
    # create Round Key
    round_key = np.empty([11, 4, 4], dtype=int)
    round_key[0] = key
    
    for round_n in range(1, 11):
        # Rotate key
        temp = round_key[round_n-1].transpose()[cols-1]
        t = np.empty(cols, dtype=int)

        for i in range(cols):
            t[i] = temp[(i + 1) % cols]
        # SubByte key
        for i in range(cols):
            x = t[i] % 0x10
            y = int(t[i] / 0x10)
            t[i] = sub_byte[y, x]

        # X-OR with RCon
        t = np.bitwise_xor(t, RCon[round_n-1])
        # X-OR t and words from previous key
        current_key = np.empty([rows, cols], dtype=int)
        current_key[0] = np.bitwise_xor(t, round_key[round_n-1].transpose()[0])
        for i in range(1, cols):
            current_key[i] = np.bitwise_xor(current_key[i-1], round_key[round_n-1].transpose()[i])

        round_key[round_n] = np.array(current_key.transpose())
        
    # 0. Add initial Round Key
    state = np.bitwise_xor(state, round_key[10])
    
    for round_n in range(10):
        
        # 1. Inverse shift rows
        
        state_1 = np.empty([rows, cols],  dtype=int)

        for i in range(rows):
            for j in range(cols):
                state_1[rows-i-1, j] = state[rows-i-1, (j + i + 1) % cols]
        
        # 2. Inverse SubByte
        
        for i in range(rows):
            for j in range(cols):
                pos = np.where(sub_byte == state_1[i][j])
                state_1[i][j] = pos[0][0] * 0x10 + pos[1][0]
        
        # 3. Add Round Key
        
        state_2 = np.bitwise_xor(state_1, round_key[9 - round_n])
        
        # 4. Inverse Mix Column
        
        if round_n < 9:
            state_3 = np.matmul(inv_mix, state_2) % 0xff
    
    final_state = state_3.flatten('F')
    
    return final_state

