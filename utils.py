from Crypto.Cipher import AES
import base64


def decrypt(encrypted_text):
    key = 'GameKing2013AndroidGame'

    key = key.encode('utf-8')[:16].ljust(16, b'\0')

    try:
        encrypted_bytes = base64.b64decode(encrypted_text)

        cipher = AES.new(key, AES.MODE_CBC, iv=key)

        decrypted = cipher.decrypt(encrypted_bytes)

        padding_len = decrypted[-1]
        decrypted = decrypted[:-padding_len]

        return decrypted.decode('utf-8')

    except Exception as e:
        return f'Decryption failed: {str(e)}'


def encrypt(text):
    key = 'GameKing2013AndroidGame'
    key = key.encode('utf-8')[:16].ljust(16, b'\0')

    try:
        # Convert text to bytes and pad to multiple of 16 bytes
        text_bytes = text.encode('utf-8')
        padding_length = 16 - (len(text_bytes) % 16)
        padded_text = text_bytes + bytes([padding_length] * padding_length)

        # Create cipher and encrypt
        cipher = AES.new(key, AES.MODE_CBC, iv=key)
        encrypted_bytes = cipher.encrypt(padded_text)

        # Convert to base64 string
        encrypted_text = base64.b64encode(encrypted_bytes).decode('utf-8')
        return encrypted_text

    except Exception as e:
        return f'Encryption failed: {str(e)}'
    

# print(decrypt("Ihp7RWe2ONHgofQs/4h85ZbVzKM+xc9Pe9FhBrHTlGiXc6M2hPvy+EVZPX1N+/JXCTjZD0k50GeGZsLwvZnyHIl5ijTvX/F4vdF9vU7EKdw="))