import bs4
import requests
import time
import os
import threading
# def ojue(i):
    # bs = bs4.BeautifulSoup(requests.get(r"http://www.umei.cc/bizhitupian/diannaobizhi/"+i+".htm").text)
    # bs = bs4.BeautifulSoup(requests.get(r"http://www.jj20.com/tx/katong/").text)
req = requests.get(r"http://www.jj20.com/tx/katong/list_220_3.html")
req.encoding = 'utf-8'
bs = bs4.BeautifulSoup(req.text)
# print(bs)
# print( "#################################################################" )
obj = bs.find_all("a", {"target": {"_blank"}})
print(obj)
print("#################################################################")
objHtml=[]
ImgObj=[]
# for f in obj:
#     objHtml.append(f.get("img"))
#     # print(objHtml)
for z in obj:
    # htmlText = bs4.BeautifulSoup(requests.get(z).text)
    Img = z.find_all("img")
    # print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    # print(Img)
    # print( "#################################################################" )
    for c in Img:
        ImgObj.append(c.get("src"))
        # print(ImgObj)
for img in ImgObj:
    with open("img_dir/"+os.path.basename(img), 'wb') as f:
        f.write(requests.get(img).content)
    time.sleep(1)
    print(os.path.basename(img)+"保存成功")

# for i in range(627):  # range()从0开始取到627g
#     threading.Thread(target=ojue,args=(i+1,)).start()  # target 参数是对应的函数名称
# i=0
# threading.Thread(target=ojue, args=(i+1,)).start()
