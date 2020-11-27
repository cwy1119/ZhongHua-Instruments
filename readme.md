# "中华器乐"管理系统



## 1.  环境依赖

1.  python3.6即以上
2. MySQL



## 2.运行方法

> (以下操作皆为windows命令,linux或者mac os请用相应的命令)

1. 安装python和MySQL环境
2. cd 项目文件夹

3. 安装python依赖 `pip install requirements.txt`

4. 在本地MySQL数据库中新建数据库, 例如dam(只需创建一个空库就行, 不用创建表)

5. 修改项目配置文件,以下修改都在项目根目录的config.py文件

   + 修改数据库配置, 修改SQLALCHEMY_DATABASE_URI, 格式: `mysql+pymysql://username:password@host/database`

   + 修改邮箱配置

     ![image-20201127150215000](.\image-20201127150215000.png) 

6. 运行项目 `python manage.py` 

   > 第一次启动时,程序会自动初始化数据库表

7. 启动成功后, 访问http://127.0.0.1:5000/即可访问项目主页

   > 第一次访问时, 本地会没有数据,需要访问管理系统上传数据



## 3. 数据初始化

1. 访问http://127.0.0.1:5000/manage即可访问管理页<img src=".\image-20201127151344286.png" alt="image-20201127151344286" style="zoom:50%;" />

2. 按照指导注册登陆后, 进行数据初始化(提供了一个上传文件样例(根目录erhu.zip)<img src=".\image-20201127151746389.png" alt="image-20201127151746389" style="zoom:50%;" />

   

## 4. 上传文件说明

> 上传的文件主要包括一个乐器的资源文件, 其中包括乐器的名字, 缩略图, 乐器相关的名人, 代表作品和演奏音符,所以需要管理员将相关的资源放在一个文件夹下, 并在该文件夹中提供一个json文件(命名为source.json),样例如下. 最后将整个文件夹打包成一个zip压缩包. 在管理界面上传压缩包即可

```json
{
    "name": "二胡",
    "image": "./img/eh.png",
    "briefInfo": {
        "title": "二胡简介",
        "text": "./richtext/briefInfo.md"
    },
    "Famous": [{
            "name": "阿炳",
            "photo": "./img/musicianimage/阿炳.jpg",
            "intro": {
                "title": "阿炳",
                "text": "./richtext/musicianinfo/阿炳.md"
            }
        },
        {
            "name": "邓建栋",
            "photo": "./img/musicianimage/邓建栋.jpg",
            "intro": {
                "title": "邓建栋",
                "text": "./richtext/musicianinfo/邓建栋.md"
            }
        },
        {
            "name": "刘天华",
            "photo": "./img/musicianimage/刘天华.jpg",
            "intro": {
                "title": "刘天华",
                "text": "./richtext/musicianinfo/刘天华.md"
            }
        },
        {
            "name": "闵惠芬",
            "photo": "./img/musicianimage/闵惠芬.jpg",
            "intro": {
                "title": "闵惠芬",
                "text": "./richtext/musicianinfo/闵惠芬.md"
            }
        },
        {
            "name": "宋飞",
            "photo": "./img/musicianimage/宋飞.jpg",
            "intro": {
                "title": "宋飞",
                "text": "./richtext/musicianinfo/宋飞.md"
            }
        },
        {
            "name": "孙凰",
            "photo": "./img/musicianimage/孙凰.jpg",
            "intro": {
                "title": "孙凰",
                "text": "./richtext/musicianinfo/孙凰.md"
            }
        },
        {
            "name": "于红梅",
            "photo": "./img/musicianimage/于红梅.jpg",
            "intro": {
                "title": "于红梅",
                "text": "./richtext/musicianinfo/于红梅.md"
            }
        }

    ],
    "Masterwork": [{
            "name": "二泉映月",
            "mp3": "./music/阿炳 - 二泉映月.mp3",
            "image": "./img/musicimage/二泉映月.jpg",
            "intro": {
                "title": "二泉映月",
                "text": "./richtext/musicinfo/二泉映月.md"
            }
        },
        {
            "name": "兰花花叙事曲",
            "mp3": "./music/魏晓冬 - 兰花花叙事曲.mp3",
            "image": "./img/musicimage/兰花花叙事曲.jpg",
            "intro": {
                "title": "兰花花叙事曲",
                "text": "./richtext/musicinfo/兰花花叙事曲.md"
            }
        },
        {
            "name": "赛马",
            "mp3": "./music/陈军 - 赛马.mp3",
            "image": "./img/musicimage/赛马.jpg",
            "intro": {
                "title": "赛马",
                "text": "./richtext/musicinfo/赛马.md"
            }
        },
        {
            "name": "听松",
            "mp3": "./music/于红梅 - 听松.mp3",
            "image": "./img/musicimage/听松.jpg",
            "intro": {
                "title": "听松",
                "text": "./richtext/musicinfo/听松.md"
            }
        },
        {
            "name": "一枝花",
            "mp3": "./music/于红梅 - 一枝花.mp3",
            "image": "./img/musicimage/一枝花.jpg",
            "intro": {
                "title": "一枝花",
                "text": "./richtext/musicinfo/一枝花.md"
            }
        },
        {
            "name": "战马奔腾",
            "mp3": "./music/陈军 - 战马奔腾.mp3",
            "image": "./img/musicimage/战马奔腾.jpg",
            "intro": {
                "title": "战马奔腾",
                "text": "./richtext/musicinfo/战马奔腾.md"
            }
        },
        {
            "name": "长城随想",
            "mp3": "./music/宋飞 - 二胡协奏曲《长城随想》.mp3",
            "image": "./img/musicimage/长城随想.jpg",
            "intro": {
                "title": "长城随想",
                "text": "./richtext/musicinfo/长城随想.md"
            }
        }
    ],
    "Gamut": [{
            "index": 3,
            "c": "notes/3/C3.mp3",
            "db": "notes/3/Db3.mp3",
            "d": "notes/3/D3.mp3",
            "eb": "notes/3/Eb3.mp3",
            "e": "notes/3/E3.mp3",
            "f": "notes/3/F3.mp3",
            "gb": "notes/3/Gb3.mp3",
            "g": "notes/3/G3.mp3",
            "ab": "notes/3/Ab3.mp3",
            "a": "notes/3/A3.mp3",
            "bb": "notes/3/Bb3.mp3",
            "b": "notes/3/B3.mp3"
        },
        {
            "index": 4,
            "c": "notes/4/C4.mp3",
            "db": "notes/4/Db4.mp3",
            "d": "notes/4/D4.mp3",
            "eb": "notes/4/Eb4.mp3",
            "e": "notes/4/E4.mp3",
            "f": "notes/4/F4.mp3",
            "gb": "notes/4/Gb4.mp3",
            "g": "notes/4/G4.mp3",
            "ab": "notes/4/Ab4.mp3",
            "a": "notes/4/A4.mp3",
            "bb": "notes/4/Bb4.mp3",
            "b": "notes/4/B4.mp3"
        },
        {
            "index": 5,
            "c": "notes/5/C5.mp3",
            "db": "notes/5/Db5.mp3",
            "d": "notes/5/D5.mp3",
            "eb": "notes/5/Eb5.mp3",
            "e": "notes/5/E5.mp3",
            "f": "notes/5/F5.mp3",
            "gb": "notes/5/Gb5.mp3",
            "g": "notes/5/G5.mp3",
            "ab": "notes/5/Ab5.mp3",
            "a": "notes/5/A5.mp3",
            "bb": "notes/5/Bb5.mp3",
            "b": "notes/5/B5.mp3"
        }
    ]
}
```



