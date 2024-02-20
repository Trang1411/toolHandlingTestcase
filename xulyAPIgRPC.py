import os
import asyncio

import requests
import random
import time

from telegram import Bot


async def send_mess_format_text(api_key, _chat_id, _from, _mess="Hello world", _file=None):
    # api_key = "5579530637:AAHiJONsPHZ0bTsiHANWBrfqvE4QoRv0BlM"
    bot = Bot(token=api_key)
    if _file:
        try:
            document = open(_file, "rb")
            await bot.send_document(chat_id=_chat_id,
                                    filename=_file,
                                    document=document,
                                    caption=_mess)
        except Exception as e:
            print(e)
    else:
        await bot.send_message(chat_id=_chat_id,
                               text=f"From [{_from}]\n{_mess}")


def generate_random_number():
    """Tạo số ngẫu nhiên 11 chữ số."""
    digits = [str(i) for i in range(10)]
    random_number = "".join(random.choices(digits, k=11))
    return "clientSession" + random_number


def load_file(url, headers, payload, client_session):
    url = "https://api.idg.vnpt.vn/stt-service/v1/grpc/async/standard"
    response = requests.post(url, headers=headers, data=payload)
    return response


def upload_file(file_name_upload, url, headers, payload, client_session):
    files = [
        ('audioFile',
         (file_name_upload, open(file_name_upload, 'rb'), 'audio/mpeg'))
    ]
    response = requests.post(url, files=files, headers=headers, data=payload)
    return response


response_status = ""
if __name__ == '__main__':
    count = 0
    api_key = "5579530637:AAHiJONsPHZ0bTsiHANWBrfqvE4QoRv0BlM"
    chat_id = "-419391239"
    client_session = generate_random_number()
    file_long = "phatbieu_10p.mp3"
    file_short = "file_25MB.mp3"
    url_long = "https://api.idg.vnpt.vn/stt-service/v1/grpc/async/standard"
    url_short = "https://api.idg.vnpt.vn/stt-service/v1/grpc/standard."
    headers = {
        'Token-id': '0d529657-bb56-0c28-e063-62199f0a7303',
        'Token-key': 'MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBAL4++WhQ+xUR9C3ljwc0s5hFJtuIigiXQrDd2E9JYq2CFg7zI1zKW7+j7UtIvO/gDAfEcDF9RILZQAqwpGjFwOECAwEAAQ==',
        'Authorization': 'bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIwZDUyOTM5ZS0yYTlmLTdiYTEtZTA2My02MzE5OWYwYTVjZTYiLCJhdWQiOlsicmVzdHNlcnZpY2UiXSwidXNlcl9uYW1lIjoidGVzdHZucHRzdjJAZ21haWwuY29tIiwic2NvcGUiOlsicmVhZCJdLCJpc3MiOiJodHRwczovL2xvY2FsaG9zdCIsIm5hbWUiOiJ0ZXN0dm5wdHN2MkBnbWFpbC5jb20iLCJ1dWlkX2FjY291bnQiOiIwZDUyOTM5ZS0yYTlmLTdiYTEtZTA2My02MzE5OWYwYTVjZTYiLCJhdXRob3JpdGllcyI6WyJVU0VSIl0sImp0aSI6ImIyMjRhOWUwLWI2OTctNGQwYy04NmYzLTcyMzE4ZmEwMzVhYSIsImNsaWVudF9pZCI6ImFkbWluYXBwIn0.cT_I4SZ1w7SC6KvexG5EOxYsZ6O9CRi1Y1QxnKm2HHR6jjvr2RVWninubYR0mzKIJKqv8pG3fJMgzjDCF3VKXA47oGCDomSx7Q1glpdkEsw8SGjO8wyjNIWR3O8x7HyjeaGuD5eCOkWIZysfKaASAYSXk4jXG4bMWO2asKOHR4AuJSWJe-6n-qoDfMLxl0R7yIxNvNx5DXG7zQu_aJG4KC0MW_EU2iW_NbVGcDpgOE6r_krw-cspPToqqHxzbVaUER32rciYpHlfDXJSAOvQl7w7RbcpZVDy4V_xGlDqEb-g50heGwMNLd0_9isbLFBi84GlTmx-vf6MuZDMgBht7w'
    }
    payload = {'clientSession': client_session}

    response_short = upload_file(file_short, url_short, headers, payload, client_session)
    response_long = upload_file(file_long, url_long, headers, payload, client_session)
    response_status = response_long.json()["object"]["status"]

    if response_short.status_code != 200:
        print(response_short.json())
        message_err = f"❌❌❌ Speech to Text (gRPC) - SHORT FILE \n Status: {response_short.json()['statusCode']} \n Error: {response_short.json()['error']} \n @caothanhha9, @ngocson124, @thuynt112"
        asyncio.run(send_mess_format_text(api_key, chat_id, "BOT SYSTEM", message_err))
    else:
        count += 1

    if response_long.status_code != 200:
        message_err = f"❌❌❌ Speech to Text Async (gRPC) - LONG FILE \n Status: {response_long.status_code} \n Error: {response_short.json()['error']} \n @caothanhha9, @ngocson124, @thuynt112"
        asyncio.run(send_mess_format_text(api_key, chat_id, "BOT SYSTEM", message_err))
    else:
        count += 1
        while response_status != "OK":
            time.sleep(2)
            # gọi đến api để tiếp tục upload
            uploading = load_file(url_long, headers, payload, client_session)
            response_status = uploading.json()["object"]["status"]
            print(response_status)
            print("====>>", uploading.json())
            results = uploading.json()["object"]
    if count == 2:
        message = f"✅✅✅ 2/2 Speech to Text (gRPC) SUCCESS!!! "
    else:
        message = f"❌❌❌ {count}/2 SUCCESS!!!"
    print(message)
    asyncio.run(send_mess_format_text(api_key, chat_id, "BOT SYSTEM", message))
