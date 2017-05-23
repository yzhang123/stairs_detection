from datetime import date
from icrawler.builtin import FlickrImageCrawler
from icrawler.builtin import GoogleImageCrawler

#google_crawler = GoogleImageCrawler(parser_threads=2, downloader_threads=4, storage={'root_dir': 'your_image_dir'})
#google_crawler.crawl(keyword='stairs', max_num=1000, date_min=None, date_max=None, min_size=(200,200), max_size=None)

flickr_crawler = FlickrImageCrawler('9ec17606b35b36e913892f9c40b14374', storage={'root_dir': 'flickr'})
flickr_crawler.crawl(max_num=1000, tags='stairs', min_upload_date=date(1900, 5, 1))


'''
#from icrawler.examples import BingImageCrawler
#from icrawler.examples import BaiduImageCrawler
#from icrawler.examples import GoogleImageCrawler

#google_crawler = GoogleImageCrawler('/home/chris/Desktop/stairs/ic/google')
#google_crawler.crawl(keyword='stairs outside', offset=100, max_num=1000,
#                     date_min=None, date_max=None, feeder_thr_num=1,
#                     parser_thr_num=1, downloader_thr_num=4,
#                     min_size=(200,200), max_size=None)

#bing_crawler = BingImageCrawler('bing')
#bing_crawler.crawl(keyword='stairs outside', offset=0, max_num=2000,
#                   feeder_thr_num=1, parser_thr_num=1, downloader_thr_num=4,
#                   min_size=None, max_size=None)
#baidu_crawler = BaiduImageCrawler('/home/chris/Desktop/stairs/ic/baidu')
#baidu_crawler.crawl(keyword='stairs outside', offset=0, max_num=2000,
#                    feeder_thr_num=1, parser_thr_num=1, downloader_thr_num=4,
#                    min_size=None, max_size=None)

'''
