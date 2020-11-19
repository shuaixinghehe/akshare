
create table `akshare_run_log` (
  `time`  datetime  default CURRENT_TIMESTAMP,
  `namespace` varchar(100) COLLATE utf8mb4_bin DEFAULT NULL,
  `subtag` varchar(100) COLLATE utf8mb4_bin DEFAULT NULL,
  `extra` varchar(100) COLLATE utf8mb4_bin DEFAULT NULL,
  `value` INT
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

-- mysql 配置 grafana 参考网址：
-- 需要一个time字段，其他字段会被解析成数字类型