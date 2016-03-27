# douban-image.py
豆瓣电影 电影海报、壁纸自动下载程序  
python爬虫程序自动下载给定豆瓣电影地址的所有海报和壁纸  
使用requests，gevent，re模块编写

示例：
> python douban-image.py https://movie.douban.com/subject/19955769/photos?type=R  

![screenshots](https://github.com/iawia002/douban-image/raw/master/screenshots/1.png)

图片默认保存在当前文件夹下的**./1**目录（这个目录必须先存在）  
保存文件名就是豆瓣电影的命名，如遇同名文件会覆盖那个文件
