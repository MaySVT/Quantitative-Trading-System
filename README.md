# Quantitative-Trading-System
登辉项目：面向期货市场的教学科研一体化量化交易仿真系统的构建及优化
# Week 1
分别构建实现一个经典策略，用样本数据跑通代码。<br>
一方面，我们的系统承诺会提供经典策略的实现以便用户操作及优化；另一方面，也让大家更加了解量化策略编程，刚开始练练手。<br>
* 张鑫璨：海龟策略
* 吴忱松：Dual Thrust
* 刘润笛：R-Breaker
* 王思鳗：菲阿里四价<br>

## 总结反思
* 代码注释可以写得更清楚一些，以便自己和他人以后阅读理解
* 多思考如何将经典的、较为定型的策略，找到可以改善的余地，思考如何融入到系统中帮助用户优化（如调参优化）
* 后续可以继续完善细节，如手续费、保证金、仓位限制等
* 可以借鉴聚宽等网站上的代码，但最好还是手工操作一份能够跑通的代码，锻炼自身能力也不容易有版权之类的问题

# Week 2
搭建系统大致框架。
## 后端
+ 负责人：刘润迪、王思鳗
+ 目标：能够连上API数据，可以分别提取出high、low、close price等
+ 资源：后端主要以flask为框架
  * Framework的样本代码已上传，可供参考，主体部分在于Backend文件夹下的flask1.py文件
  * 之前看到的一个比较好的[flask教程](https://www.youtube.com/watch?v=CjYKrbq8BCw&list=PLXmMXHVSvS-CoYS177-UvMAQYRfL3fBtX)，可以学习参考。
  * 最后的最后，一切解释权在于[flask官网](https://flask.palletsprojects.com/en/2.2.x/)，利用好官网材料。
## 前端
+ 负责人：张鑫璨、吴忱松
+ 目标：能够将前端网页大致框架框出，设置好按钮可以跑通样本数据与样本经典策略并画图
+ 资源：前端主要以vue为框架
  * Framework的样本代码已上传，可供参考，主体部分在Frontend>src>components下的两个vue文件。
  * [Vue官网](https://vuejs.org/) Vue的官网也提供有不错的详细从0开始教程，可供学习参考。
  * Javascript一些基本语法可参考[w3school](https://www.w3school.com.cn/js/index.asp)，包括一些CSS、HTML的语法也可在这个网站上找到。
  * 可视化、画图的工具主要是[d3](https://github.com/d3/d3/blob/main/API.md)库，链接里很完整的API reference，可供参考。
  * Vue其他比较重要的，主要是掌握好整体框架，各部分之间的互动即可。常F12/右击检查来查看console以及Elements。Console.log当print用。
+ 运行Vue，命令行打开到Frontend文件夹，npm install(只有第一次需要运行，安装所有需要的配置)，npm run serve

## 总结反思
+ 后端：
  * 已完成与Tushare的基本连接，传输日线数据
  * 可以再研究一下更高频的数据传输，看看数据能够达到的最高频度是多少
  * 将数据格式、结构统一化
+ 前端：
  * 完成样本数据的后端读取与前端获取。
  * 已完成基本的框架搭建，实现按钮与画图功能
  * 继续完成策略在前端的实现
  
# Week 3
继续完善框架
## 策略
继续完善菲阿里四价策略，查错跑通。
## 后端
+ 目标：
  * 数据格式、结构统一化，整理一个Markdown文件总结API->数据格式
  * 连接更加高频的数据，Tushare是否可以达到需求，是否需要别的数据源
## 前端
+ 目标：
  * 完成样本经典策略的前端实现
  * 调整美化前端页面布局
  * 试着实现从后端获取Tushare的数据
 
