# akshare


ERROR 2013 (HY000): Lost connection to MySQL server at 'reading initial communication packet', system error: 102
   增加连接超时时间
set global max_allowed_packet=1024*1024*16;

