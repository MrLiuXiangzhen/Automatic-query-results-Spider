# Automatic-query-results-spider
Research recruitment network automatic query results spider

## yzw_rearch.py
 用于循环检测成绩页面是否更新，如果更新，自动调用send_email模块发送邮件通知
 - 使用方法：
   实例化Detection对象，传入欲保存文件名列表，调用run方法
 - Detection中的参数说明：
        这里面网址已写死，其它学校可自行修改
      - SCORE_URL:主登录地址，成绩查询地址
      - RES_URL,RES_SCORE:备用地址
      - URL,URL_login:发送邮件内容的地址，没有什么用
      - SCORE_DATA:查询成绩需要输入验证的信息
      - RES_DATA:学信网登录验证信息，用于登录另一个查询成绩的地址（备胎）
 
## send_email.py
 用于发送邮件
 - 使用方法：
   实例化SendMail对象，传入参数，调用send_run方法
 - SendMail中的参数说明：
      - username: 用户名
      - passwd: 密码
      - recv: 收件人，可传list
      - title: 邮件标题
      - content: 邮件正文
      - file: 附件路径
      - ssl: 是否安全链接，默认为普通
      - email_host: smtp服务器地址
      - port: 非安全链接端口，默认为25
      - ssl_port: 安全链接端口，默认为465
 
