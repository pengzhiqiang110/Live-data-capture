# 智能营销
## 0.ssh登录
ssh -i /Users/test/Desktop/baichuan/agent_lzh.pem ec2-user@ec2-18-183-89-226.ap-northeast-1.compute.amazonaws.com

## 1.创建虚拟环境
python -m venv xsale-env

## 2. 启动环境
mac和linux  
source sales-env/bin/activate

windows  
xsales-env/script/activate

# 3. 安装依赖包
pip install -r requrements.txt

# 4. 自动回复默认用openAI, terminal环境中执行
mac 和 linux  
export OPENAI_API_KEY=sk-xxxx

windows  
set OPENAI_API_KEY=sk-xxxx

# 5. 安装mysql
mac  
brew install mysql  
brew services start mysql  

# 6. 第一次部署，mysql -u root 登录后给mysql建立用户名，仓库，以及建表
'''云服务器上 sudo docker exec -it xagc-mysql mysql -u root -p '''   
CREATE USER 'xagc'@'localhost' IDENTIFIED BY '123456';  
CREATE DATABASE xSales_test;  
GRANT ALL PRIVILEGES ON xSales_test.* TO 'xagc'@'localhost';  
FLUSH PRIVILEGES;  

use xSales_test;  

CREATE TABLE `user` (  
  `id` int NOT NULL AUTO_INCREMENT,  
  `phone` varchar(4096) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,  
  `pwd` varchar(100) COLLATE utf8_bin DEFAULT NULL,  
  PRIMARY KEY (`id`) USING BTREE  
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;  

CREATE TABLE `bot` (  
  `id` int NOT NULL AUTO_INCREMENT,  
  `uid` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,  
  `shopper_id` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL, 
  `shopper_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,  
  `life_id` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,  
  `live_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,  
  `live_url` varchar(4096) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,  
  `live_doc` text CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,  
  `status` int,  
  `live_status` int,  
  PRIMARY KEY (`id`) USING BTREE  
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;  

# 7. 启动
python main.py

<!-- # 8. 本地提供公网服务
参考：https://natapp.cn/article/natapp_newbie  
Linux/Mac  
chmod a+x natapp  
./natapp   -->

# 测试post 
# 创建user
curl -X POST -H "Content-Type: application/json" -d '{"phone":"16619906311","pwd":"123456"}' http://ec2-18-183-133-123.ap-northeast-1.compute.amazonaws.com:8000/user/create

# 登录
curl -X GET http://ec2-18-183-133-123.ap-northeast-1.compute.amazonaws.com:8000/user/16619906311/123456
curl -X GET http://localhost:8080/user/16619906311/123456


# 获取信息
curl -X GET http://ec2-18-183-133-123.ap-northeast-1.compute.amazonaws.com:8000/user -H "token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwicGhvbmUiOiIxNjYxOTkwNjMxMSIsInB3ZCI6IjEyMzQ1NiJ9.1st772uNSzqloPpsDB35hrIjOFISUJ9og885eVu35ng"


# 创建bot
curl -X POST -H "Content-Type: application/json" -H "token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwicGhvbmUiOiIxNjYxOTkwNjMxMSIsInB3ZCI6IjEyMzQ1NiJ9.1st772uNSzqloPpsDB35hrIjOFISUJ9og885eVu35ng" -d '{"id":"1","shopper_id":"2088741204488103","shopper_name":"伯棠","live_name":"云服务验证","live_url":"https://b.alipay.com/page/live-console/detail/A202312314583467701001099?appId=2030093915638103","live_doc":"Q:伯棠测试 A:复现post"}' http://ec2-18-183-133-123.ap-northeast-1.compute.amazonaws.com:8000/bot/create 

curl -X POST -H "Content-Type: application/json" -H "token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwicGhvbmUiOiIxNjYxOTkwNjMxMSIsInB3ZCI6IjEyMzQ1NiJ9.1st772uNSzqloPpsDB35hrIjOFISUJ9og885eVu35ng" -d '{"id":"1","shopper_id":"2088741204488103","shopper_name":"伯棠","live_name":"云服务验证","live_url":"https://b.alipay.com/page/live-console/detail/A202312314583467701001099?appId=2030093915638103","live_doc":"Q:红包在哪领？A：亲亲，动动发财小手点点关注！红包就在左上角哦Q:优惠券在哪领A：动动发财小手点点关注！红包就在左上角哦亲！Q:拍了两个包能一起发吗?A:亲亲，我给您备注一下！包包都是今天发出，分开寄也不用担心哦！Q:已拍A: 感谢亲亲支持，给亲亲备注拍一发四！加急发出！Q 已经下单了A: 感谢亲亲支持，给亲亲备注拍一发四！加急发出！Q：己拍二个包，但有一个订单中没有显示，是什么情况？亲亲，刷新一下页面呀，您搜索小程序“我的订单”或者”中国袋鼠官方旗舰店“,小程序中查看订单呀Q: 怎么看订单？A:亲亲您搜索小程序“我的订单”或者”中国袋鼠官方旗舰店“,小程序中查看核对一下订单呀！直播间小蓝车点开，上方有客服，订单入口哦亲Q一号链接尺寸多少A 长宽高 23*10*15 再送130cm肩带哦亲亲Q：一号链接多重A：0.36kg，单肩背不压肩的哦亲亲Q：拍一发四发什么A亲亲，发袋鼠定制礼盒，袋鼠定制礼品袋，一条赠送的120cm肩带，您拍下的商品包包，直播间下单再额外送您袋鼠正品21位小卡包哦Q拍一发四都有啥？ 送什么？A姐姐，您稍等 主播马上给您展示，拍一发四发袋鼠定制礼盒，袋鼠定制礼品袋，一条赠送的120cm肩带，您拍下的商品包包，直播间下单再额外送您袋鼠正品21位小卡包哦Q:什么时候发货A:亲亲，我们承诺48h内发货哦，一般都是现货现发哦，当天拍当天发！Q:有运费险吗A:抱歉呐亲亲，没有运费险的哈Q:发什么快递A:袋鼠官方正品保证质量 三通一达快递为您送达！！！Q为什么还要运费A: 亲，二号链接小卡包单拍是需要付邮费的哈，您可以拍其他款哦，我们免费给您送一个！Q什么材质A 进口pvc人工革的哈亲，质感不输其他国际大牌哦亲Q质感怎么样A 质感很好的呦亲，我们是袋鼠官方正品，大牌优惠仅限新直播间哦！Q:3号链接尺寸多少A:亲，枕头包尺寸 :长宽高 23*10*15Q:三号链接多重A:3号链接枕头包净重0.45kg哈，单背不压肩哦！Q:保真吗A:亲，我们发出的每一款包包都是有唯一防伪码的哦，支持扫码、线下验真伪，假一罚十！Q是正品吗A:亲，我们发出的每一款包包都是有唯一防伪码的哦，支持扫码、线下验真伪，假一罚十！Q收到货不满意怎么办亲，收到货不满意7天无理由退换货哦亲Q收到货有质量问题怎么办亲，收到货有质量问题我们售后全包哦！我们出厂的每一款包包都是有专人一一检查的哈，都有数据记载的哈，不用担心哦！Q:哪个颜色好看A:奶茶色百搭时尚，卡其色高档大气！！！"}' http://localhost:8080/bot/create 


# 获取bot list
curl -X GET http://ec2-18-183-133-123.ap-northeast-1.compute.amazonaws.com:8000/bot/list -H "token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwicGhvbmUiOiIxNjYxOTkwNjMxMSIsInB3ZCI6IjEyMzQ1NiJ9.1st772uNSzqloPpsDB35hrIjOFISUJ9og885eVu35ng"

curl -X GET http://localhost:8080/bot/list -H "token:eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwicGhvbmUiOiIxNjYxOTkwNjMxMSIsInB3ZCI6IjEyMzQ1NiJ9.1st772uNSzqloPpsDB35hrIjOFISUJ9og885eVu35ng"

# 获取bot 
curl -X GET http://ec2-18-183-133-123.ap-northeast-1.compute.amazonaws.com:8000/bot/1

# update bot
curl -X POST -H "Content-Type: application/json" -H "token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwicGhvbmUiOiIxNjYxOTkwNjMxMSIsInB3ZCI6IjEyMzQ1NiJ9.1st772uNSzqloPpsDB35hrIjOFISUJ9og885eVu35ng" -d '{"id":"1","shopper_id":"2088741204488103","shopper_name":"伯棠","live_name":"云服务验证update bot","live_url":"https://b.alipay.com/page/live-console/detail/A202401104816580001001099?appId=2030093915638103","live_doc":"Q:红包在哪领？A：亲亲，动动发财小手点点关注！红包就在左上角哦Q:优惠券在哪领A：动动发财小手点点关注！红包就在左上角哦亲！Q:拍了两个包能一起发吗?A:亲亲，我给您备注一下！包包都是今天发出，分开寄也不用担心哦！Q:已拍A: 感谢亲亲支持，给亲亲备注拍一发四！加急发出！Q 已经下单了A: 感谢亲亲支持，给亲亲备注拍一发四！加急发出！Q：己拍二个包，但有一个订单中没有显示，是什么情况？亲亲，刷新一下页面呀，您搜索小程序“我的订单”或者”中国袋鼠官方旗舰店“,小程序中查看订单呀Q: 怎么看订单？A:亲亲您搜索小程序“我的订单”或者”中国袋鼠官方旗舰店“,小程序中查看核对一下订单呀！直播间小蓝车点开，上方有客服，订单入口哦亲Q一号链接尺寸多少A 长宽高 23*10*15 再送130cm肩带哦亲亲Q：一号链接多重A：0.36kg，单肩背不压肩的哦亲亲Q：拍一发四发什么A亲亲，发袋鼠定制礼盒，袋鼠定制礼品袋，一条赠送的120cm肩带，您拍下的商品包包，直播间下单再额外送您袋鼠正品21位小卡包哦Q拍一发四都有啥？ 送什么？A姐姐，您稍等 主播马上给您展示，拍一发四发袋鼠定制礼盒，袋鼠定制礼品袋，一条赠送的120cm肩带，您拍下的商品包包，直播间下单再额外送您袋鼠正品21位小卡包哦Q:什么时候发货A:亲亲，我们承诺48h内发货哦，一般都是现货现发哦，当天拍当天发！Q:有运费险吗A:抱歉呐亲亲，没有运费险的哈Q:发什么快递A:袋鼠官方正品保证质量 三通一达快递为您送达！！！Q为什么还要运费A: 亲，二号链接小卡包单拍是需要付邮费的哈，您可以拍其他款哦，我们免费给您送一个！Q什么材质A 进口pvc人工革的哈亲，质感不输其他国际大牌哦亲Q质感怎么样A 质感很好的呦亲，我们是袋鼠官方正品，大牌优惠仅限新直播间哦！Q:3号链接尺寸多少A:亲，枕头包尺寸 :长宽高 23*10*15Q:三号链接多重A:3号链接枕头包净重0.45kg哈，单背不压肩哦！Q:保真吗A:亲，我们发出的每一款包包都是有唯一防伪码的哦，支持扫码、线下验真伪，假一罚十！Q是正品吗A:亲，我们发出的每一款包包都是有唯一防伪码的哦，支持扫码、线下验真伪，假一罚十！Q收到货不满意怎么办亲，收到货不满意7天无理由退换货哦亲Q收到货有质量问题怎么办亲，收到货有质量问题我们售后全包哦！我们出厂的每一款包包都是有专人一一检查的哈，都有数据记载的哈，不用担心哦！Q:哪个颜色好看A:奶茶色百搭时尚，卡其色高档大气！！！"}' http://localhost:8080/bot/update




# 删除bot 
curl -X GET http://ec2-18-183-133-123.ap-northeast-1.compute.amazonaws.com:8000/bot/delete/19

# 启动bot
curl -X GET http://ec2-18-183-133-123.ap-northeast-1.compute.amazonaws.com:8000/run_bot/1
curl -X GET http://localhost:8080/run_bot/1

# 停止机器人
curl -X GET http://ec2-18-183-133-123.ap-northeast-1.compute.amazonaws.com:8000/bot/stop/1
curl -X GET http://localhost:8080/bot/stop/1

# 查询机器人状态
curl -X GET http://ec2-18-183-133-123.ap-northeast-1.compute.amazonaws.com:8000/bot/status/1

# 查询直播间状态
curl -X GET http://ec2-18-183-133-123.ap-northeast-1.compute.amazonaws.com:8000/bot/live_status/17

# 直播间信息

0. 直播间启动直播
1. 登录智能直播页面[没有账号先注册] http://hfv7be.natappfree.cc/。
2. 创建机器人，填商家自己的信息，示例：
  商家号：2088741204488103
  商户名称:武汉耀赢莱鑫电子科技有限公司
  直播间名称：袋鼠旗舰店
  直播间url：https://b.alipay.com/page/live-console/detail/A202312274530494201001099?appId=2030093915638103
  直播间doc:
3. Q:红包在哪领？A：亲亲，动动发财小手点点关注！红包就在左上角哦Q:优惠券在哪领A：动动发财小手点点关注！红包就在左上角哦亲！Q:拍了两个包能一起发吗?A:亲亲，我给您备注一下！包包都是今天发出，分开寄也不用担心哦！Q:已拍A: 感谢亲亲支持，给亲亲备注拍一发四！加急发出！Q 已经下单了A: 感谢亲亲支持，给亲亲备注拍一发四！加急发出！Q：己拍二个包，但有一个订单中没有显示，是什么情况？亲亲，刷新一下页面呀，您搜索小程序“我的订单”或者”中国袋鼠官方旗舰店“,小程序中查看订单呀Q: 怎么看订单？A:亲亲您搜索小程序“我的订单”或者”中国袋鼠官方旗舰店“,小程序中查看核对一下订单呀！直播间小蓝车点开，上方有客服，订单入口哦亲Q一号链接尺寸多少A 长宽高 23*10*15 再送130cm肩带哦亲亲Q：一号链接多重A：0.36kg，单肩背不压肩的哦亲亲Q：拍一发四发什么A亲亲，发袋鼠定制礼盒，袋鼠定制礼品袋，一条赠送的120cm肩带，您拍下的商品包包，直播间下单再额外送您袋鼠正品21位小卡包哦Q拍一发四都有啥？ 送什么？A姐姐，您稍等 主播马上给您展示，拍一发四发袋鼠定制礼盒，袋鼠定制礼品袋，一条赠送的120cm肩带，您拍下的商品包包，直播间下单再额外送您袋鼠正品21位小卡包哦Q:什么时候发货A:亲亲，我们承诺48h内发货哦，一般都是现货现发哦，当天拍当天发！Q:有运费险吗A:抱歉呐亲亲，没有运费险的哈Q:发什么快递A:袋鼠官方正品保证质量 三通一达快递为您送达！！！Q为什么还要运费A: 亲，二号链接小卡包单拍是需要付邮费的哈，您可以拍其他款哦，我们免费给您送一个！Q什么材质A 进口pvc人工革的哈亲，质感不输其他国际大牌哦亲Q质感怎么样A 质感很好的呦亲，我们是袋鼠官方正品，大牌优惠仅限新直播间哦！Q:3号链接尺寸多少A:亲，枕头包尺寸 :长宽高 23*10*15Q:三号链接多重A:3号链接枕头包净重0.45kg哈，单背不压肩哦！Q:保真吗A:亲，我们发出的每一款包包都是有唯一防伪码的哦，支持扫码、线下验真伪，假一罚十！Q是正品吗A:亲，我们发出的每一款包包都是有唯一防伪码的哦，支持扫码、线下验真伪，假一罚十！Q收到货不满意怎么办亲，收到货不满意7天无理由退换货哦亲Q收到货有质量问题怎么办亲，收到货有质量问题我们售后全包哦！我们出厂的每一款包包都是有专人一一检查的哈，都有数据记载的哈，不用担心哦！Q:哪个颜色好看A:奶茶色百搭时尚，卡其色高档大气！！！


代码目录
aliStreamRepaly.py 页面抓取
main.py fastapi交互
db.py mysql数据库
autoReply.py 自动回复

## 前端代码运行
1. setupProxy.js 里面的target是后端的网址
2. 下载Nodejs(官网下载最新版),里面集成了npm
3. npm --version 命令,显示出版本号说明下载成功
4. 确认您的项目中包含了 package.json 文件，其中应该包含了您的项目依赖和启动脚本等信息。
5. 使用命令 npm install 安装项目依赖。这个命令会根据 package.json 中的依赖信息，自动下载并安装所有需要的包。
6. 安装完成后，使用命令 npm start 启动项目。这个命令会执行 package.json 中的 start 脚本，通常这个脚本会启动一个本地开发服务器，并在浏览器中打开项目页面
7. 如果您需要在生产环境中运行项目，可以使用 npm run build 命令，这个命令会执行 package.json 中的 build 脚本，通常这个脚本会构建一个优化过的生产版本的项目，可以通过将构建后的文件部署到服务器来运行项目。

异步bot启动出错 4: Message: 'chromedriver' executable needs to be in PATH. Please see https://sites.google.com/a/chromium.org/chromedriver/home

启动实例的时候启动代码
cd xSales
vim start.sh
chmod +x start.sh
sudo vim /etc/systemd/system/xSales.service
sudo systemctl daemon-reload
sudo systemctl enable xSales.service
sudo systemctl start xSales.service
ps -aux | grep python
vim start.sh
./start.sh
ps -aux | grep python

关闭vscode的ssh连接代码还能执行
trap '' HUP
nohup python main.py &

直接连接实例,关闭连接代码的实例终端,代码继续执行
nohup python main.py &

查找nohub在后台执行的程序
ps -aux | grep python

杀死你正在执行的nohub 
kill -9 + “正在运行的id”

