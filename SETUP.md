# GitHub 个人主页

发布目标：公开仓库 `openc2023/openc2023`。

仓库根目录的 `README.md` 是英文主版本；`README.zh-CN.md` 与 `README.ko.md` 是中文和韩文版本。三份文档互相链接，GitHub 个人资料会展示英文主版本。

## 资源

- `assets/tianhan-ascii-v2.gif`：960 × 360，48 帧，4.8 秒无缝循环。
- `assets/tianhan-static-v2.png`：静态替代图。
- `source/build_minimal.py`：本地生成脚本，使用 Windows 系统字体。

设计参考本人项目：https://openc2023.github.io/web-media/ 。横幅采用真实字形覆盖率生成 ASCII 字符，不依赖第三方图床或动态统计服务。

## 发布

1. 在 GitHub 新建公开仓库，名称填写 `openc2023`，勾选添加 README。
2. 将本文件夹的三个 README 和 assets 文件夹放到仓库根目录。
3. 提交后访问 https://github.com/openc2023 检查个人资料 README。

`preview*.html` 是本地排版预览，不代表 GitHub 网站的完整页面，也不需要发布。

## 后续更新

安装 `requirements.txt` 中的依赖，在 Windows 运行 `python source/build_minimal.py` 可重新生成横幅、文档和本地预览。介绍内容来自 web-media 现有公开资料；个人任职等易变内容没有写入。

建议手动固定展示仓库：web-media、7S、content。个人资料的固定仓库、头像和简介由 GitHub 账户设置管理，本包不更改这些账户设置。

当前采用极简版：动态横幅、一句身份、三个入口及语言链接。旧版图片和生成脚本保留在仓库历史与 assets 中，当前 README 不再使用。
