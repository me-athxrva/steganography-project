def lsb_encode(img, text):
    from routes.aes import toBinary
    user_binary_text = toBinary(text) + '1111111111111110'
    data_index = 0
    rows, cols, channels = img.shape

    if len(user_binary_text) > rows * cols * 3:
        return {"error": "Message too long to fit in image!"}, 500

    for row in range(rows):
        for col in range(cols):
            for channel in range(3):  # Modify R, G, B channels
                if data_index < len(user_binary_text):
                    img[row, col, channel] = (img[row, col, channel] & 0xFE) | int(user_binary_text[data_index])
                    data_index += 1
                else:
                    break
    return img


def lsb_decode(img):
    binary_data = ""
    rows, cols, channels = img.shape
    for row in range(rows):
        for col in range(cols):
            for channel in range(3):
                lsb = img[row, col, channel] & 1
                binary_data += str(lsb)

                if binary_data.endswith("1111111111111110"):
                    binary_data = binary_data[:-16]
                    from routes.aes import toAscii
                    message = toAscii(binary_data)
                    return message

    return "No hidden message found!"