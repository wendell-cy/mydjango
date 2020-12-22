import bs4
import requests
import os
import threading
def ojue(i):
    req = requests.get(r"http://www.jj20.com/tx/katong/list_220_"+str(i)+".html")
    req.encoding = 'utf-8'
    bs = bs4.BeautifulSoup(req.text)
    # bs = bs4.BeautifulSoup(requests.get(r"http://www.jj20.com/tx/katong/list_220"+i+".html").text)
    #print(bs)
    print(r"http://www.jj20.com/tx/katong/list_220"+str(i)+".html")
    obj = bs.find_all("a", {"target": {"_blank"}})
    # print(obj)
    # return  ""
    objHtml=[]
    ImgObj=[]
    # for f in obj:
    #     objHtml.append(f.get("href"))
    for z in obj:
        # htmlText = bs4.BeautifulSoup(requests.get(z).text)
        Img = z.find_all("img")
        for c in Img:
            ImgObj.append(c.get("src"))
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    print(ImgObj)
    print("##################################################")
    # for img in ImgObj:
    #     with open("img_dir/"+os.path.basename(img),'wb') as f:
    #         f.write(requests.get(img).content)
    #     print(os.path.basename(img)+"保存成功")

for i in range(2): # range()从0开始取到627
    # print(i)
    threading.Thread(target=ojue, args=(i+1,)).start() # target 参数是对应的函数名称
