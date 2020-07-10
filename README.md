> ### 项目架构

项目基于python3+mysql进行搭建的一个web爬虫，主要用于爬取天眼通的企业数据。
架子已经基本搭建起来，git clone之后修改配置即可运行，在此基础上可进行二次开发。

  - python 开发语言，基于python3
  - mysql 数据库

关于python方面，主要使用了requests、sqlalchemy、xlwt

项目主要运行于Linux系统上，本人使用测试机Mac，线上服务器为Centos7.0。

> ### 问题

1、需要在etc/config.yaml进行配置相关信息，cookie建议填写，否则爬取的数据电话、邮箱等信息是带有**号的。
2、未注册的用户只能查找遍历5页，目前这个没什么好的方案解决

> ### 已完善功能

1、数据爬取
2、数据写入入excel

> ### 开发中功能

1、添加代理ip池


> ### 特别声明

项目部分代码借鉴了我的web脚手架代码（https://github.com/GIS90/base_webframe）