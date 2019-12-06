- excel导出sql：
=CONCATENATE("INSERT INTO `tbl_customer_counselor` (`id`, `counselor_id`, `fullname`, `group_id`, `sort_in_group`, `config_id`) VALUES('"&A2&"','"&D2&"','"&C2&"','2','"&F2&"','"&E2&"');")

- VLOOKUP(A5,P:Q,2,FALSE)

```
VLOOKUP(查找值,查找范围起始:查找范围重点,填充查找范围的第几项(数字1开始),找不到是否展示(TRUE或者FALSE))
```
