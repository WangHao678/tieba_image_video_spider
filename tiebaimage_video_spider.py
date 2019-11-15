import requests
from urllib import parse
import time
import random
from lxml import etree

class TiebaImageSpider(object):
    def __init__(self):
        self.url = 'http://tieba.baidu.com/f?kw={}&pn={}'
        self.headers = {'User-Agent':'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 2.0.50727; SLCC2; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; Tablet PC 2.0; .NET4.0E)'}

    #功能函数1:请求
    def get_html(self,url):
        html = requests.get(url=url,
        headers=self.headers).content.decode('utf-8','ignore')
        return html

    #功能函数2:xpath解析
    def xpath_func(self,html,xpath_bds):
        p = etree.HTML(html)
        r_list = p.xpath(xpath_bds)
        return r_list

    def parse_html(self,page_url):
        page_html = self.get_html(page_url)
        #提取50个帖子链接['/p/2323','/p/23232']
        xpath_bds = '//li[@class=" j_thread_list clearfix"]/div/div/div/div/a/@href'
        tlink_list = self.xpath_func(page_html,xpath_bds)
        for tlink in tlink_list:
            t_url = 'http://tieba.baidu.com' + tlink
            #把1个帖子中所有的图片保存到本地
            self.save_image(t_url)

    #把t_url中所有的图片下载下来
    def save_image(self,t_url):
        t_html = self.get_html(t_url)
        #匹配视频+图片,此处视频xpath在响应内容中获取,作了修改
        # xpath_bds = '//div[@class="d_post_content j_d_post_content' \
        #             '  clearfix"]/img[@class="BDE_Image"]/@src'
	#只需切换路径即可
        xpath_bds = '//div[@class="video_src_wrapper"]/embed/@data-video'
        imalink_list = self.xpath_func(t_html,xpath_bds)
        #imglink_list:['http://xxx.jpg','','']
        for imglink in imalink_list:
            #保存1张图片到本地
            self.download_image(imglink)
            #下载1张图片随机休眠0-1秒钟
            time.sleep(random.uniform(0,1))

    def download_image(self,imglink):
        img_html = requests.get(
            url=imglink,
            headers=self.headers
        ).content
        filename = imglink[-10:]
        with open(filename,'wb') as f:
            f.write(img_html)

    def run(self):
        name = input('请输入贴吧名:')
        begin = int(input('请输入起始页:'))
        end = int(input('请输入终止页:'))
        params = parse.quote(name)
        for page in range(begin,end+1):
            pn = (page-1)*50
            url = self.url.format(params,pn)
            self.parse_html(url)

if __name__ == '__main__':
    spider = TiebaImageSpider()
    spider.run()





















