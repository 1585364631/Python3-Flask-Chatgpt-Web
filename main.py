import time
import requests
import json
import uuid
import threading
from flask import Flask, request

app = Flask(__name__)

# https://chat.openai.com/api/auth/session
# 方式：GET请求
# cookie写请求cookie
# token写本地浏览器中cookie的__Secure-next-auth.session-token
# 如果目录下存在token.txt，直接把token写在文件中就行，确保有读写权限
cookie = "_ga=GA1.2.966573527.1670404819; __Host-next-auth.csrf-token=b5ade6f71cb02b4d3ed3fd521f9bf18619f90b924da0555931a23eff5940f95a%7Cec2171e26acc358863bc1d8b5c5463a37aa944d48a1313a47c8a1e81879490cb; __Secure-next-auth.callback-url=https%3A%2F%2Fchat.openai.com%2F; cf_clearance=q5Y9arN.TdUJdE.hIbX7TxFFgFHVW1u0anIyhw9cm14-1675826610-0-1-a023835a.3a48e41c.f722dcba-160; _cfuvid=QIyuK_LeV9kl.3iIulXg1mfnxL7nGLYjB_bzhokrqW8-1675826610183-0-604800000; __Secure-next-auth.session-token=eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..tQEC6kPeO2ZmUPZ5.XNxfGzE4mr6aFAUAm1uTUjd_hg7tES3BV73h2cFlNwj2sphMA1I-GWIBuB9rTokRJSwP8epg6H3aMyhuxWmbVFH_pjEFmfQL8sYxpxN-4ja8WkF5sAdjXfcmCmxB-1YxMx9dtZfLlvx2V69clcXr1W2S2txlnJGQOJnABpGy4EgltGqHAUeN2tPpdgTWVEiw1WWf0EVVsoqshNS9DnqCncQRALg4o7_YP6Q-6FEzdK89Kts2tqcTCp9yv6rxIkoUBIi0OKtRH6y3D6XKi5LxGst3BD_cHG7ihyKwdQjBoffKCeP2TWSj7G650DxK_nvOQRUFkuAaNczNUIXM7-24IHVNHX_OFyGe5JYX6ZurD_mfFHVDmxFnBTrv6w1a2q5ez3xo_XIRk11oCPdH_n57IzrEIMfTjNVFyX_JnrShW0HUbXXrXCp5rQxM5svZMBOJLikclGsw1i5LOiCk-swm5lKlqc40pjj9CtVZJbrmiaRlIFR2P32q7OyMCAFiYjOjVxaq4FuPI6JE0LL7K6wHGXUGCDg3WiAPJigBK9gqvbka6KhLFMut-mQyrwhh33Wvqd7NobBCziPmRXhS-aYtnoIp0lCM1VPN4NhQfkzJgMXBM94aSMD1TALU1SN5JpO9sLSs-ZierhWg0olJILL3bYIpH3BeE4hyMTW8Dyx-V5Zc1ttOLQW0WHfJHrco5gvjKrpZvaOTNNqZuqA6a10TAWCoHyEmt9ENYonCRo0gpiu1nOWfyAnbCQHKWu6S1Q7Iq4fzcqWa0ZFfBbWpudlz4T_GNXAItoiOgsQ7O5dPcNT9q1HorbkN46k3ZkEeliuxqtOStTAAj0RXIfCu9Ok3VoMtOg9WyDe99XkuhQSbyF5_Mjf0SAfvIuF-GdOzqlDCpGPNSYOD5DgoteHZJylOtfZs38EAn07kRUKNzpVhAvz1onO_KOsQsC1aB9nQ5XNao5MuR34G7jNXFG50Nk-7xh9Hslsf0j2tR7lDf-zl4KJ5Q4FAUnCWGJy5-wrYaq9iRbjHgDR-D28FMoUbl2ua2QM3A7EKFAAawoPAJUhHZ983NIer16LkdKlZBPFoH-miEdThcJkhkeEhYxrcI7ZQptxGQlGXc0QJfk1NRf0nuYNvfJrhOuc-gZxqMQwr-yskuHrqEaX2CXXBInBTrjXEpubov0wjJvrvyBBtAIMDxFC8Q_IEkDpx77hmLtv4lrzRUzzMPWMmltXghbibMj_0iEhy6VjqmdumEFNUozgi1uPnbHTYD40SJxD6cizhHo_M26zSWiAyipmesAFq6D5Eaq_BSpCTUYJm6D_dTyyjxhxOb3M4-CRVV-WwHiGTOO0dcPxF6JaJRg-61MAYIA3wAzBIUAQ9IPJfl9Ogz15t6G-jWtliKQTizWAqNrBHcqb_EtfIpMvHnzoJ_bN-jj63HpVmSAloqs3PHUDE9iWZPb3xt2WpjdMvl3KznsMUbsei1X8TOBEJiFHdZxFrVkV4qU7tdWeusQTaWjHE6iIXUjNrO_h_uQpE_MIO7uoiUoqRfvHWHmy2s2s7RpxY04ASG6_IuqKWPIbMvpgk6BhtHozhO8jDUz-IFx1-D5126RX0_rNTGCz41dk_FGUTp4h2j1E6yBqdtHt_a7KsU_pLwJ_RjPDli0pHgXdNOZ5qcmol5XEsmSGgB5qPnFD5-k2e3ASONycL2VGZ-S9SvNueUlKdSzPvLUJwKt90GbIDrm016Mv5asmTYYo5Y2c8JxbWQ5DEl9FKO7iEV3OQkeSWsHRZDGH509YRRnuBiFtmC7UI21ochGrWLKunp1pmPuFMyTihhQKDBYlgIlRKfpaDxPaAQbQA-GX9vDIbFiqtePTZSQ33i2hk4W_0Ibrs1kUPwEQbliLXzqWbvYEY6jRUHtbZ-JCL5_g86EEbrnjEc6wt4hZEZlnDxH9hogdTPmDiH1Gib5GD_pNEIjw7y05JPClaRI9WXhacg3V9FkXgt7CYaRItfaDSRx6MOPJO4vg3FPGZwTINl9E5kufWsrKzN4yTt5HCKDC8GuJ0GOQf7etcMtPE2b6_5PqjLQkBN5nXKt-7yTed3tHNe46sgZW_5bCXJMBkBHMAGbA2scEd-P9qh6In3erYQ1Wh_Mc_GKamkgrlFwGvVn0R6qgytw_5kRzvdrbcZnLLvH10xhTDrkgAqYnEZC9c1Jg60Tdbdz5egjYBB4LFIe5p6m-sZ9M5irUriSLvkLYYUqudOzbqbow690WeR_W_bjvKFhLYLgTbit6_-S80C-3UOyDkkuC9Nd29tau7VT1FmRSK_AGVp2w-waiykYXxmSmrpzjXHeR_MD7S5Qdq2JaqZeLuKHRl9iRWYZilLtQGMSZ0R2qWismMmWsKZ3pfdU19bc9YMOez9Vm1WhKiich4qgG82KnRetwi0uak63TrAInJEyR1jNFnyWjZd0dvIwdCcciPDwFZ5iQiJZMArRUPgYN_BxbZe_Ihnxp3UY6XK_lwyctVs6wLnKw8qQL2sYyQpeg09-skXWrmTne5HkSpfXKzE1Q4hrjuztSluca1XiI9XPSRDnRsB0rnmYv_GgyxXJjyC2T_6NNY8tgOMgIuozlZnryOiK1nrEyUBDfJTrHea_zouyQOOfmug6gNRllowizOBnsTzTjlWx-yjV_wdyqAZ1cHqoiVVbmgG072.1hDnpW1MagU8-VwDYvj-bw; __cf_bm=fhiF29gyJtBd9JMiwNMOcvDA_TS6bJAI_ba8JRVMM8A-1675827127-0-Adf3fWmnu8je0fz3umORtubovfimtjQr/ntLaIctcdforw5zc5jakivT+lu+FzlMEiowRtI0paX21nNlK6bcW4qgJtobduyHV2S7TfyWqS7U+USaZdYlnH0el9hWFypzNIspi12iUW9DMU76h0udm4hQbbAHliUvlbsWgvRIZ5pIOk9i9moFDF2ZwzfK+RZQ0w=="
token = "eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..tQEC6kPeO2ZmUPZ5.XNxfGzE4mr6aFAUAm1uTUjd_hg7tES3BV73h2cFlNwj2sphMA1I-GWIBuB9rTokRJSwP8epg6H3aMyhuxWmbVFH_pjEFmfQL8sYxpxN-4ja8WkF5sAdjXfcmCmxB-1YxMx9dtZfLlvx2V69clcXr1W2S2txlnJGQOJnABpGy4EgltGqHAUeN2tPpdgTWVEiw1WWf0EVVsoqshNS9DnqCncQRALg4o7_YP6Q-6FEzdK89Kts2tqcTCp9yv6rxIkoUBIi0OKtRH6y3D6XKi5LxGst3BD_cHG7ihyKwdQjBoffKCeP2TWSj7G650DxK_nvOQRUFkuAaNczNUIXM7-24IHVNHX_OFyGe5JYX6ZurD_mfFHVDmxFnBTrv6w1a2q5ez3xo_XIRk11oCPdH_n57IzrEIMfTjNVFyX_JnrShW0HUbXXrXCp5rQxM5svZMBOJLikclGsw1i5LOiCk-swm5lKlqc40pjj9CtVZJbrmiaRlIFR2P32q7OyMCAFiYjOjVxaq4FuPI6JE0LL7K6wHGXUGCDg3WiAPJigBK9gqvbka6KhLFMut-mQyrwhh33Wvqd7NobBCziPmRXhS-aYtnoIp0lCM1VPN4NhQfkzJgMXBM94aSMD1TALU1SN5JpO9sLSs-ZierhWg0olJILL3bYIpH3BeE4hyMTW8Dyx-V5Zc1ttOLQW0WHfJHrco5gvjKrpZvaOTNNqZuqA6a10TAWCoHyEmt9ENYonCRo0gpiu1nOWfyAnbCQHKWu6S1Q7Iq4fzcqWa0ZFfBbWpudlz4T_GNXAItoiOgsQ7O5dPcNT9q1HorbkN46k3ZkEeliuxqtOStTAAj0RXIfCu9Ok3VoMtOg9WyDe99XkuhQSbyF5_Mjf0SAfvIuF-GdOzqlDCpGPNSYOD5DgoteHZJylOtfZs38EAn07kRUKNzpVhAvz1onO_KOsQsC1aB9nQ5XNao5MuR34G7jNXFG50Nk-7xh9Hslsf0j2tR7lDf-zl4KJ5Q4FAUnCWGJy5-wrYaq9iRbjHgDR-D28FMoUbl2ua2QM3A7EKFAAawoPAJUhHZ983NIer16LkdKlZBPFoH-miEdThcJkhkeEhYxrcI7ZQptxGQlGXc0QJfk1NRf0nuYNvfJrhOuc-gZxqMQwr-yskuHrqEaX2CXXBInBTrjXEpubov0wjJvrvyBBtAIMDxFC8Q_IEkDpx77hmLtv4lrzRUzzMPWMmltXghbibMj_0iEhy6VjqmdumEFNUozgi1uPnbHTYD40SJxD6cizhHo_M26zSWiAyipmesAFq6D5Eaq_BSpCTUYJm6D_dTyyjxhxOb3M4-CRVV-WwHiGTOO0dcPxF6JaJRg-61MAYIA3wAzBIUAQ9IPJfl9Ogz15t6G-jWtliKQTizWAqNrBHcqb_EtfIpMvHnzoJ_bN-jj63HpVmSAloqs3PHUDE9iWZPb3xt2WpjdMvl3KznsMUbsei1X8TOBEJiFHdZxFrVkV4qU7tdWeusQTaWjHE6iIXUjNrO_h_uQpE_MIO7uoiUoqRfvHWHmy2s2s7RpxY04ASG6_IuqKWPIbMvpgk6BhtHozhO8jDUz-IFx1-D5126RX0_rNTGCz41dk_FGUTp4h2j1E6yBqdtHt_a7KsU_pLwJ_RjPDli0pHgXdNOZ5qcmol5XEsmSGgB5qPnFD5-k2e3ASONycL2VGZ-S9SvNueUlKdSzPvLUJwKt90GbIDrm016Mv5asmTYYo5Y2c8JxbWQ5DEl9FKO7iEV3OQkeSWsHRZDGH509YRRnuBiFtmC7UI21ochGrWLKunp1pmPuFMyTihhQKDBYlgIlRKfpaDxPaAQbQA-GX9vDIbFiqtePTZSQ33i2hk4W_0Ibrs1kUPwEQbliLXzqWbvYEY6jRUHtbZ-JCL5_g86EEbrnjEc6wt4hZEZlnDxH9hogdTPmDiH1Gib5GD_pNEIjw7y05JPClaRI9WXhacg3V9FkXgt7CYaRItfaDSRx6MOPJO4vg3FPGZwTINl9E5kufWsrKzN4yTt5HCKDC8GuJ0GOQf7etcMtPE2b6_5PqjLQkBN5nXKt-7yTed3tHNe46sgZW_5bCXJMBkBHMAGbA2scEd-P9qh6In3erYQ1Wh_Mc_GKamkgrlFwGvVn0R6qgytw_5kRzvdrbcZnLLvH10xhTDrkgAqYnEZC9c1Jg60Tdbdz5egjYBB4LFIe5p6m-sZ9M5irUriSLvkLYYUqudOzbqbow690WeR_W_bjvKFhLYLgTbit6_-S80C-3UOyDkkuC9Nd29tau7VT1FmRSK_AGVp2w-waiykYXxmSmrpzjXHeR_MD7S5Qdq2JaqZeLuKHRl9iRWYZilLtQGMSZ0R2qWismMmWsKZ3pfdU19bc9YMOez9Vm1WhKiich4qgG82KnRetwi0uak63TrAInJEyR1jNFnyWjZd0dvIwdCcciPDwFZ5iQiJZMArRUPgYN_BxbZe_Ihnxp3UY6XK_lwyctVs6wLnKw8qQL2sYyQpeg09-skXWrmTne5HkSpfXKzE1Q4hrjuztSluca1XiI9XPSRDnRsB0rnmYv_GgyxXJjyC2T_6NNY8tgOMgIuozlZnryOiK1nrEyUBDfJTrHea_zouyQOOfmug6gNRllowizOBnsTzTjlWx-yjV_wdyqAZ1cHqoiVVbmgG072.1hDnpW1MagU8-VwDYvj-bw"

# https://chat.openai.com/chat
# 随便发送一句话，改Authorization
Authorization = "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1UaEVOVUpHTkVNMVFURTRNMEZCTWpkQ05UZzVNRFUxUlRVd1FVSkRNRU13UmtGRVFrRXpSZyJ9.eyJodHRwczovL2FwaS5vcGVuYWkuY29tL3Byb2ZpbGUiOnsiZW1haWwiOiIxNTg1MzY0NjMxQHFxLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJnZW9pcF9jb3VudHJ5IjoiREUifSwiaHR0cHM6Ly9hcGkub3BlbmFpLmNvbS9hdXRoIjp7InVzZXJfaWQiOiJ1c2VyLVQ2c3FQT1JETnBHaDhqcmpxbDNQNUVvRCJ9LCJpc3MiOiJodHRwczovL2F1dGgwLm9wZW5haS5jb20vIiwic3ViIjoiYXV0aDB8NjM5MDVhM2JjMTA1NTA4ZmI2YTY3ODhjIiwiYXVkIjpbImh0dHBzOi8vYXBpLm9wZW5haS5jb20vdjEiLCJodHRwczovL29wZW5haS5vcGVuYWkuYXV0aDBhcHAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTY3NTgyNDY4NSwiZXhwIjoxNjc2NDI5NDg1LCJhenAiOiJUZEpJY2JlMTZXb1RIdE45NW55eXdoNUU0eU9vNkl0RyIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwgbW9kZWwucmVhZCBtb2RlbC5yZXF1ZXN0IG9yZ2FuaXphdGlvbi5yZWFkIG9mZmxpbmVfYWNjZXNzIn0.l1i-R1EageiM1jY5mmBdL3GUOH_4EHabyA1aaMbdiPz1D23xWCVZTbrtD6lal_-oV9i1Biq3KjH2n07BvbmbmIQ4jRoDqIb8km4o54O_K2UGqDdT9u4IhaMTR1DTQiGKLjjXzIpWi0LBeGTDHBqzwnkBviNJftTivAGeIcWpp4cJtIaCFTzwr0ZIAvAomHIbxQN6EzejSgaNGEPhtMYWlEQfGzGhdjG5lkB5iCVW6FVyAUiAjsQPrYgKSi17KaqRztMhUBhgPx1PbMrCXcIHBdYdn1bdD2t0vhY15kC_68C18xzhEdx6xekzzME4ZaqW30HfXIdprwwBcBiwwf_nKQ"



def cookie_to_dic(cookies):
    return {item.split('=')[0].strip(): item.split('=')[1].strip() for item in cookies.split(';')}


def json_to_cookie(data):
    cookies = ""
    for key, value in data.items():
        if key != "":
            cookies = cookies + f"{key}={value};"
    return cookies


def getChatGpt(text):
    global Authorization
    headers = {
        "Authorization": Authorization,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36", }

    body = {
        "action": "next",
        "messages": [
            {
                "id": str(uuid.uuid1()),
                "role": "user",
                "content": {
                    "content_type": "text",
                    "parts": [
                        text
                    ]
                }
            }
        ],
        "parent_message_id": str(uuid.uuid1()),
        "model": "text-davinci-002-render"
    }
    response = requests.post("https://chat.openai.com/backend-api/conversation", json=body, headers=headers, proxies={'https':'106.55.104.75:8118'})
    return response.text
    return json.loads(response.text.splitlines()[-4][6:])["message"]["content"]["parts"][0]


def getUUID():
    text = str(uuid.uuid1()).split("-")
    return f"{text[0]}{text[1]}{text[2][:2]}"


@app.route('/', methods=['POST'])
def chat():
    try:
        data = json.loads(request.data)['text']
        return getChatGpt(data)
    except:
        return "出故障了"


@app.route("/update", methods=["GET"])
def update():
    global token, cookie
    try:
        data = cookie_to_dic(cookie)
        data['__Secure-next-auth.session-token'] = token
        cookies = json_to_cookie(data)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
            "Cookie": cookies,
            "If-None-Match": getUUID()
        }
        text = requests.get("https://chat.openai.com/api/auth/session", headers=headers, proxies={'https':'106.55.104.75:8118'})
        token = text.headers.get("Set-Cookie").split("__Secure-next-auth.session-token=")[1].split(";")[0]
        f = open("token.txt", "w+")
        f.write(token)
        f.close()
        return str(json.loads(text.text)['expires']) + "----更新成功"
    except:
        return "更新失败，可能登入已过期"


def asyncUpdate():
    print("定时更新启动")
    while True:
        update()
        time.sleep(3600)


if __name__ == '__main__':
    try:
        f = open("token.txt", 'r', encoding="utf-8")
        token = str(f.read()).strip()
        f.close()
    except FileNotFoundError:
        print("token文件不存在")
    except PermissionError:
        print("文件存在但是无读写权限")

    # 多线程每一个小时更新一次token
    threading.Thread(target=asyncUpdate, name="asyncUpdate").start()

    app.run(host='0.0.0.0', port=8888, debug=False)
