# Pixiv_dailyranking
编程新手个人练习用写的一个脚本。。 使用selenium+requests模块下载Pixiv每日排行榜上的图片。 脚本包含:①登录               ②退出               ③下载单张图片               ④下载套图  关于Pixiv的人机验证功能，本萌新解决不了啊，不过手动验证一次后可以挺长一次时间不用再验证了。 开启脚本的时候要确保Pixiv没有账号自动登录的状态。 开启脚本后输入的数字指可以下载到排名第几位的图片，涩图模式只支持可以看R-18图片的账号。  本来一开始图片的定位用的是xpath，但后面发现Pixiv的图片的xpath是会变的，就改用了css，但估计css也会变化，我自己用的这几天还能用。 如果变了只要把脚本里面的图片定位改一改就好了。  还有这个脚本不支持gif的下载，遇到gif会报错。。。 图片是一张一张点开下载的，所以效率还挺低的。。主要是用来练习selenium写的脚本。
