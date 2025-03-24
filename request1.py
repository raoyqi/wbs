import requests

# 这是您提供的 URL
url = "https://webofscience.clarivate.cn/api/gateway?GWVersion=2&SrcAuth=OpenURL&SrcApp=UA&DestURL=http%3A%2F%2FMK4ZC2TA5G.search.serialssolutions.com%3Furl_ver%3DZ39.88-2004%26url_ctx_fmt%3Dinfo%3Aofi%2Ffmt%3Akev%3Amtx%3Actx%26rft.atitle%3DHand%2BGesture%2BRecognition%2BApplied%2Bto%2Bthe%2BInteraction%2Bwith%2BVideo%2BGames%26rft.aufirst%3DLorena%2BIsabel%26rft.auinit%3DLIB%26rft.aulast%3DBarona%2BLopez%26rft.btitle%3DLecture%2BNotes%2Bin%2BArtificial%2BIntelligence%26rft.date%3D2024%26rft_id%3Dinfo%3Adoi%2F10.1007%252F978-3-031-47765-2_3%26rft.eissn%3D1611-3349%26rft.epage%3D52%26rft.genre%3Dproceeding%26rft.isbn%3D978-3-031-47765-2%26rft.eisbn%3D978-3-031-47765-2%26rft.issn%3D2945-9133%26rft_val_fmt%3Dinfo%3Aofi%2Ffmt%3Akev%3Amtx%3Abook%26rft.pages%3D36-52%26rft.series%3DLecture%2BNotes%2Bin%2BArtificial%2BIntelligence%26rfr_id%3Dinfo%3Asid%2Fwebofscience.com%3AWOS%3AALLDB%26rft.spage%3D36%26rft.tpages%3D17%26rft.volume%3D14391%26rft.au%3DL%25C3%25B3pez%252C%2BLIB%26rft.au%3DCifuentes%252C%2BCIL%26rft.au%3DBenalc%25C3%25A1zar%252C%2BME&DestApp=OTHER_OpenURL&SrcAppSID=USW2EC0CECXDZ8C4WtcOrBwEkWIXs&SrcJTitle=ADVANCES+IN+COMPUTATIONAL+INTELLIGENCE%2C+MICAI+2023%2C+PT+I&SrcPubType=MD_FORMAT&HMAC=lzbaRsaO47Ns2CJaKVHQOR88FeY8%2BCM61FK2ywb%2B6g0%3D"

# 发送 GET 请求
response = requests.get(url)

# 检查响应状态码
if response.status_code == 200:
    print("请求成功!")

    # 将响应内容保存到本地文件
    with open("response_content.html", "w", encoding="utf-8") as file:
        file.write(response.text)
    print("内容已成功保存到 'response_content.html' 文件中")
else:
    print(f"请求失败，状态码: {response.status_code}")
