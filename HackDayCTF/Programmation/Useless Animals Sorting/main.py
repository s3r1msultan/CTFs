from pwn import *
import base64
import PIL.Image
import PIL.ExifTags

animals_list = {
                "0000": "butterfly",
                "0001": "cat",
                "0010": "chicken",
                "0011": "cow",
                "0100": "dog",
                "0101": "elephant",
                "0111": "sheep",
                "1000": "spider",
                "0110": "horse",
                "1001": "squirrel"
                }

def process_image(base64_image):
    try:
        image_data = base64.b64decode(base64_image)
        img = PIL.Image.open(BytesIO(image_data))
        model = img.getexif().get(272)
        return animals_list[model]

    except Exception as e:
        print(f"Error processing image {i}: {e}")
        return animals_list[0]


host = "challenges.hackday.fr"
port = 51259
conn = remote(host, port)

conn.recv()
conn.sendline('')

n = 100
for i in range(n):
    try:
        line = conn.recvline().decode().strip()
        base64_image = conn.recvline().decode()
        conn.recvline()

        result = process_image(base64_image)

        conn.sendline(result.encode())
        print(conn.recvline().decode())

    except EOFError:
        print("Server closed the connection.")
        break

conn.interactive()
conn.close()
