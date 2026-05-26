# Changelog

## [0.2.0] - 2026-05-23

### Added
- `slugify(s)` —— 将字符串转为 URL 友好的 slug：转小写、空格替换为连字符、去除非 `[a-z0-9-]` 字符
- `slugifyUnique(strs)` —— 对字符串数组每项调用 `slugify`，重复结果依次加 `-2`、`-3` 等后缀以保证唯一
