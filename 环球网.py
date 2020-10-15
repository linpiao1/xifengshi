import requests
from lxml import etree
import time
import xlwt

def main():
    Baseurl = 'https://weibo.cn/cctvnewsbeijing?page='
    # 1.爬取网页
    data_list = getdata(Baseurl)
    #IDlence = (len(datalist) - 1)
    savepath = "环球网1000.xls"
    # 3.保存数据
    saveData(data_list, savepath)

def getdata(Baseurl):
    data_list = []
    for i in range(500,1001):
        print('第'+str(i)+'页')
        url = Baseurl + str(i)
        time.sleep(2)
        html = askurl(url)
        #print(html)

        html_ele = etree.HTML(html.text.encode('utf-8'))
        #print(html_ele)
        item = html_ele.xpath('/html/body/div[@class="c"][contains(@id,"")]')
        #print(item)
        for i in item[:-2]:
            data = []
            #print(i)
            IDnumber = i.xpath('./@id')
            #print(IDnumber)
            if len(IDnumber) != 0:
                IDnumber = IDnumber[0]
                data.append(IDnumber)
            else:
                data.append('')

            try:

                title = i.xpath('./div/span[@class="ctt"]/a/text()')
                if len(title) != 0:
                    title = title[0]
                    data.append(title)
                else:
                    data.append('')
            except:
                    data.append("")


            try:

                link = i.xpath('./div/span[@class="ctt"]/a/@href')
                if len(link) != 0:
                    link = link[0]
                    data.append(link)
                else:
                    data.append('')
            except:
                    data.append("")

            try:

                like = i.xpath('./div[2]/a[3]/text()')
                if len(like) != 0:
                    like = like[0]
                    data.append(like)
                elif len(like) == 0:
                    like = i.xpath('./div[1]/a[1]/text()')
                    like = like[0]
                    data.append(like)
            except:
                    data.append('')

            try:

                forword = i.xpath('./div[2]/a[4]/text()')
                if len(forword) != 0:
                    forword = forword[0]
                    data.append(forword)
                elif len(forword) == 0:
                    forword = i.xpath('./div[1]/a[2]/text()')
                    forword = forword[0]
                    data.append(forword)
            except:
                    data.append('')



            try:

                comment = i.xpath('./div[2]/a[5]/text()')
                if len(comment) != 0:
                    comment = comment[0]
                    data.append(comment)
                elif len(comment) == 0:
                    comment = i.xpath('./div[1]/a[3]/text()')
                    comment = comment[0]
                    data.append(comment)
            except:
                    data.append('')


            url2 = 'https://weibo.cn/comment/'+str(IDnumber[2:])
            #print(url2)
            html2 = askurl(url2)
            #time.sleep(0.2)
            html_ele2 = etree.HTML(html2.text.encode('utf-8'))
            #print(html_ele2)
            try:
                c = html_ele2.xpath('//span[@class="ctt"]')[0]
                content = c.xpath('string(.)')


                if len(content) != 0 :
                    content = content
                    data.append(content)
                else:
                    data.append('')



            except:
                data.append('')




            data_list.append(data)
    X = len(data_list)
    data_list.append(X)
    print(data_list)
    print(data_list[-1])

    return data_list


def askurl(url):
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36",

        "cookie": "_T_WM=3e40e78e41c9df6f8f7e348ecb2b43d0; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhlIYCIji5f50-jfkch7n4y5JpX5KzhUgL.FoM7SK-41h-pS0z2dJLoIE5LxKMLB--L1KMLxKBLB.2L1hqLxK-L1K5LBKMNeoBc1Btt; SCF=AmvmEtdgbVNBLmY81b6nBUc87xPm36q8vSZjcyCgj68xqpzgSuQ4FbDSk7z5GrQF5i2SE4WSkzxvThn6_ftoHAI.; SUB=_2A25yhdDPDeRhGeFO7lcY-CvNzD6IHXVRifCHrDV6PUNbktAKLXLGkW1NQXWt35eq1acxAZMK7yH94HK9PDFVwq1x; SUHB=0u5Bp7gwLbKopm; SSOLoginState=1602330783; ALF=1604922783"
    }
    response = requests.get(url,headers = head)
    html = response
    return html


def saveData(data_list,savepath):
    print("save...")
    book = xlwt.Workbook(encoding="utf-8", style_compression=0)  # 创建workbook对象
    sheet = book.add_sheet('sheet1', cell_overwrite_ok=True)  # 创建工作表

    col = ('微博文章账号','标题','相关链接','点赞数','转发数','评论数','内容')
    for i in range(0, 7):
        sheet.write(0, i, col[i])  # 列名
    for i in range(0, data_list[-1]):
        print('第%d条' % (i + 1))
        data = data_list[i]  # 要保存的数据
        #print(data)
        for j in range(0, 7):
            sheet.write(i + 1, j, data[j])  # 数据


    book.save(savepath)  # 保存数据表



if __name__ == '__main__':  # 当程序执行时
    main()
    print("爬取完毕!")