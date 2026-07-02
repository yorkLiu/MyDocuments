# installed_skills.md

已安装 skill 列表。

## 清单

| # | Skill 名称 | 来源 | 说明 |
|---|-----------|------|------|
| 1 | `frontend-design` | anthropics/skills | 前端 UI 设计：配色、字体、排版，拒绝模板味 |
| 2 | `docx` | anthropics/skills | Word 文档创建、编辑、格式化（docx-js） |
| 3 | `xlsx` | anthropics/skills | Excel 电子表格：公式、图表、格式化（openpyxl） |
| 4 | `pdf` | anthropics/skills | PDF 处理：读取、合并、分割、OCR、创建（pypdf/pdfplumber/reportlab） |
| 5 | `pptx` | anthropics/skills | PPT 演示文稿：创建、编辑、设计（pptxgenjs） |
| 6 | `web-access` | eze-is/web-access | 联网搜索 + 浏览器 CDP 操控（含本地 Chrome 登录态） |
| 7 | `pua` | tanweai/pua | AI 激励引擎：大厂 PUA 话术驱动的调试方法论 |

## 来源链接

- Frontend Design: https://github.com/anthropics/skills/tree/main/skills/frontend-design
- Docx/Xlsx/Pdf/Pptx: https://github.com/anthropics/skills/tree/main/skills
- Web Access: https://github.com/eze-is/web-access
- PUA: https://github.com/tanweai/pua

## 安装时间

2026-06-12

---

## 新增 Skills（追加）

| # | Skill 名称 | 来源 | 说明 |
|---|-----------|------|------|
| 8 | `huashu-nuwa`（女娲造人） | alchaincyf/nuwa-skill | 输入人名/主题/模糊需求，自动深度调研→思维框架提炼→生成可运行的人物 Skill。捕捉 HOW they think，不是 WHAT they said。触发词：「造 skill」「蒸馏 XX」「女娲」「做个 XX 视角」 |
| 9 | `a-stock-data` | simonlin1212/a-stock-data | A 股全栈数据工具包：七层数据架构（行情/研报/信号/资金面/新闻/基础数据/公告），27 个端点覆盖主板/中小板/科创板/ST。内置 mootdx/腾讯/东财等多源，含防封策略。适用于个股估值、龙虎榜跟踪、题材归因、融资融券跟踪等 |
| 10 | `Awesome-finance-skills` | RKiding/Awesome-finance-skills | AI 金融分析技能集：实时新闻聚合（10+ 源）、逻辑链可视化（市场影响传导图）、AI 预测（含新闻感知调整）。支持 alphaear-news、逻辑链图、预测模型等模块 |

## 新增来源链接

- 女娲造人：https://github.com/alchaincyf/nuwa-skill
- A股数据：https://github.com/simonlin1212/a-stock-data
- 金融技能：https://github.com/RKiding/Awesome-finance-skills

---

## 新增 Skills（2026-06-13）

| # | Skill 名称 | 来源 | 说明 |
|---|-----------|------|------|
| 11 | `DeepAnalyze` | ruc-datalab/DeepAnalyze | 首个 Agentic LLM 自主数据科学框架：自动完成数据准备、分析、建模、可视化、报告生成全流程。支持结构化/半结构化/非结构化多源数据研究，输出分析师级研究报告。配套 DeepAnalyze-8B 模型 + 500K 训练数据全开源 |
| 12 | `daily_stock_analysis` | ZhuLinsen/daily_stock_analysis | A 股/港股/美股个股深度分析引擎。22 维数据 + 52 评委量化裁决 + 6 种机构估值建模（D CF/Comps/LBO 等）。触发：个股走势预测、K 线复盘、多维度评分、估值对比 |
| 13 | `short-term-stock-picker` | online0001/short-term-stock-picker | 短线股票筛选工具，基于 AKShare 数据。条件：流通市值≤150亿、近20日有涨停、非ST、近3日主力净流入估算、换手率≤10%。输出 result.csv 含代码/名称/涨停次数/市值/换手率/封板资金/行业板块 |
| 14 | `UZI-Skill`（游资） | wbh604/UZI-Skill | A 股/港股/美股个股深度分析引擎。**66 位评审团 × 9 大流派 × 22 维数据 × 22 种机构方法**。零 API key，全免费数据源。触发命令：`/stock-deep-analyzer:analyze-stock 贵州茅台`（完整分析，5-8min）、`/stock-deep-analyzer:quick-scan 002217`（30秒速判）、`/stock-deep-analyzer:scan-trap 002217`（杀猪盘排查）、`/stock-deep-analyzer:dcf 600519`（DCF 估值专项）。输出 HTML 报告 + 朋友圈竖图 + 微信群战报 |

## 新增来源链接

- DeepAnalyze：https://github.com/ruc-datalab/DeepAnalyze
- 每日股票分析：https://github.com/ZhuLinsen/daily_stock_analysis
|- 短线选股：https://github.com/online0001/short-term-stock-picker
|- UZI 游资：https://github.com/wbh604/UZI-Skill

---

## 新增 Skills（2026-06-17）

| # | Skill 名称 | 来源 | 说明 |
|---|-----------|------|------|
| 15 | `guizang-ppt-skill`（归藏 PPT） | op7418/guizang-ppt-skill | 生成横向翻页网页 PPT（单 HTML 文件），提供两种风格：①「电子杂志 × 电子墨水」（衬线 + 流体 WebGL 背景 + 暖色调，适合人文分享/商业发布）②「瑞士国际主义」（无衬线 + 网格点阵 + IKB/柠檬黄/柠檬绿/安全橙高亮，适合科技产品/数据汇报）。内含 10+ 种布局模板（封面/幕封/数据大字报/左文右图/图片网格/流水线/对比页/收束页等）、5 套杂志风主题色 +4 套瑞士风主题色、WebGL 背景、Motion One 入场动效、Lucide 图标系统。**用法**:用户提到"杂志风 PPT"、"瑞士风 PPT"、"Swiss Style"、"horizontal swipe deck"、"网页 PPT"时触发。运行前需澄清：风格选择、受众场景、时长、素材、图片/截图处理需求、主题色、硬约束。 |
| 16 | `guizang-social-card-skill`（归藏社交卡片） | op7418/guizang-social-card-skill | 生成小红书/公众号等社交平台的图文卡片。支持小红书 3:4 轮播图、公众号 21:9+1:1 封面配对、单文件 HTML 直接转 PNG。含 28 套版式 +10 套主题，自动处理配图、排版、文字压缩。**用法**:用户提到"小红书图文"、"社交卡片"、"公众号封面"、"轮播图"、"Rednote images"时触发。运行前需澄清：目标平台、内容源（文章/脚本/截图）、Rednote 分类（旅行/职场/游戏等 11 类）、风格偏好（杂志风/瑞士风）。 |
| 17 | `humanizer-zh`（中文去 AI 味） | op7418/Humanizer-zh | 去除中文文本中的 AI 生成痕迹。基于维基百科"AI 写作特征"指南，检测并修复：夸大象征意义、宣传性语言、肤浅分析、模糊归因、破折号过度使用、三段式法则、AI 词汇、否定式排比、过多连接短语。**用法**:用户提到"去 AI 味"、"改回人话"、"去除 AI 痕迹"、"这篇太 AI 了"时触发。可直接输入文本或指定文件路径。 |
| 18 | `Deep-Research-skills`（深度研究） | Weizhena/Deep-Research-skills | 为 Agent 安装深度研究流程：先列研究大纲→分头上网查→汇成带出处的报告，全程可插手改方向。支持中文界面。**用法**:用户提到"深度研究"、"做个调研报告"、"查资料写报告"、"research outline"、"deep analysis"时触发。适合写干货长文前做资料收集。 |
| 19 | `qiaomu-anything-to-notebooklm`（乔木多源处理器） | joeseesun/qiaomu-anything-to-notebooklm | 多源内容智能处理器：支持微信公众号、网页、YouTube、播客（小宇宙/喜马拉雅）、PDF、Markdown 等，自动上传到 NotebookLM 并生成播客/PPT/思维导图/Quiz 等多种格式。支持深度分析模式和飞书文档自动创建。**用法**:用户提到"把这文章生成播客"、"做成 PPT"、"画思维导图"、"上传到 NotebookLM"、"深度分析这本书"时触发。需预先配置 MCP 和 NotebookLM 认证。 |
| 20 | `wewrite`（公众号一条龙） | oaker-io/wewrite | 微信公众号内容全流程助手：热点抓取→选题→框架→内容增强→写作→SEO→视觉 AI→排版推送草稿箱。支持 markdown 转微信格式、学习用户改稿风格、文章数据复盘、容器语法（`:::dialogue`/`:::timeline`/`:::callout`等）。**用法**:用户提到"公众号"、"写推文"、"微信文章"、"排版主题"、"封面图"、"推草稿箱"时触发。不适用于通用"写文章"、blog、邮件、PPT、抖音/短视频。 |
| 21 | `Youtube-clipper-skill`（YouTube 剪辑） | op7418/Youtube-clipper-skill | YouTube 视频智能剪辑工具。下载视频和字幕，AI 分析生成精细章节（2-5 分钟级别），用户选择片段后自动剪辑、翻译字幕为中英双语、烧录字幕到视频，并生成总结文案。**用法**:用户提到"剪辑 YouTube 视频"、"生成短视频片段"、"制作双语字幕"、"clip video"、"双语字幕"时触发。需安装 yt-dlp 和 ffmpeg-full（含 libass 字幕支持）。 |
| 22 | `oh-story-claudecode`（网文写作工具箱） | worldwonderer/oh-story-claudecode | 网络小说创作工具箱。支持长篇/短篇网文扫榜（起点/番茄/晋江/知乎等）、拆文分析（黄金三章/人设架构/爽点设计）、写作辅助（大纲→正文/日更/续写/修改）、去 AI 味、封面生成。自动路由到对应子 skill。**用法**:用户提到"写小说"、"写网文"、"扫榜"、"拆文"、"生成封面"、" fantasy story"、"web novel"时触发。子命令：`/story`、`/长篇扫榜`、`/短篇拆文`、`/story-cover`等。 |
| 23 | `marketingskills`（营销技能库） | coreyhaines31/marketingskills | GitHub star 最高的营销 skill 库（33k stars）。32 个 skill 覆盖文案、SEO、转化、品牌定位全流程。纯英文界面，适合做出海/外贸内容。包含：A/B测试、广告创意、投放策略、AI SEO、数据分析、邮件营销、竞品分析、内容策略、CRO、客户调研、定价策略等。**用法**:用户提到"marketing"、"SEO"、"copywriting"、"conversion optimization"、"go-to-market"、"marketing plan"、"出海营销"、"外贸文案"时触发。按具体需求路由到对应子 skill（如`cro`、`copywriting`、`seo-audit`等）。 |
| 24 | `awesome-gpt-image-2`（GPT-Image2 提示词库） | freestylefly/awesome-gpt-image-2 | GPT-Image2 工业级提示词引擎与模板库（7.3k stars）。470+ 爆款图逆向拆成提示词，20+ 套工业级模板，覆盖 UI 界面/信息可视化/海报排版/商品电商/品牌 logo/建筑空间/摄影写实/插画艺术/人物角色/场景叙事/历史古风等 11 类。**用法**:适合文章配图、海报、封面、创意生成场景。**注意**:本体是提示词模板库，需用可视化网站 (gpt-image2.canghe.ai) 或复制提示词；但已安装 Hermes skill `gpt-image-2-style-library` 可根据需求自动选择模板生成提示词。 |
| 25 | `AI-Content-Studio`（AI 内容自动化工作室） | naqashafzal/AI-Content-Studio | 100% 免费开源的 AI 内容自动化工具。自动完成：脚本撰写→语音合成→视频生成→自动上传全流程。基于 Gemini 等 LLM 的自主 Agent/Python 管道，适合无人值守的短视频批量生产（YouTube/TikTok/Reels）。**用法**:这是独立 Python 项目，非 Hermes skill。需克隆后自行配置 API keys 运行 (`run.sh`)。适合做 faceless YouTube 频道、自动化 content farm。参考：https://github.com/naqashafzal/AI-Content-Studio |
| 26 | `firecrawl`（Web 数据抓取 API） | firecrawl/firecrawl | Web 数据抓取与搜索 API（开源 Python 库）。支持 Search/Scrape/Crawl/Map/Agent 全套功能，可将任意 URL 转成干净 Markdown/JSON/截图，兼容 JS 渲染页面。支持 MCP server、Python SDK、CLI 三种接入方式。**用法**:这是 Python 库，非 Hermes skill。使用方式：① pip install firecrawl-py ② 配置 API key (firecrawl.dev 免费注册) ③ 调用 `app.scrape()`/`app.crawl()` 等方法。适合 RAG 数据清洗、竞品监控、内容聚合、agent 实时搜索场景。参考：https://github.com/firecrawl/firecrawl |
| 27 | `crawl4ai`（LLM 友好网页爬虫） | unclecode/crawl4ai | GitHub Trending #1 的开源 LLM 友好网页爬虫（12k+ stars）。无需 API key，直接 pip install 即可使用。生成干净 Markdown，支持 RAG/微调，自动处理 JS 渲染。支持 CSS/XPath/LLM 三种提取模式、多 URL 并行爬取、代理/Session 管理。**用法**:pip install -U crawl4ai && crawl4ai-setup（初始化浏览器）→ Python 调用 `AsyncWebCrawler()`。完全开源免费，无需 API key，适合 RAG 数据管道、竞品抓取、内容聚合。参考：https://github.com/unclecode/crawl4ai |
| 28 | `atutun-xhs-cover`（小红书封面提示词） | panggungunvibe/atutun-xhs-cover | 阿囤囤风格小红书封面提示词生成 skill（3:4 竖版）。真人出镜、超大浅黄(#FDFFA7)/白色中文标题、粗黑描边、人物抠图、绿色勾选清单、emoji贴纸、高对比高密度构图。8 种风格：爆款大字/巨字拆分/小白科普/教程清单/产品测评/种草推荐/贴纸拼贴/黑底工作流。**用法**:用户提到"小红书封面"、\"生成封面提示词\"、\"爆款封面\"时触发。逐步问答收集：风格→人物图→表情动作→素材图→背景色→字体→颜色→标题，最终输出可交给图片生成模型的提示词。需配合 GPT-Image-2 等使用。参考：https://github.com/panggungunvibe/atutun-xhs-cover |

## 新增来源链接

- 归藏 PPT: https://github.com/op7418/guizang-ppt-skill
- 归藏社交卡片：https://github.com/op7418/guizang-social-card-skill
- 中文 Humanizer: https://github.com/op7418/Humanizer-zh
- 深度研究：https://github.com/Weizhena/Deep-Research-skills
- 乔木多源处理器：https://github.com/joeseesun/qiaomu-anything-to-notebooklm
- 公众号一条龙：https://github.com/oaker-io/wewrite
- YouTube 剪辑：https://github.com/op7418/Youtube-clipper-skill
- 网文写作：https://github.com/worldwonderer/oh-story-claudecode
- 营销技能库：https://github.com/coreyhaines31/marketingskills
- GPT-Image2 提示词库：http://github.com/freestylefly/awesome-gpt-image-2
- AI 内容自动化：https://github.com/naqashafzal/AI-Content-Studio
- Web 数据抓取：https://github.com/firecrawl/firecrawl
- LLM 爬虫：https://github.com/unclecode/crawl4ai
- 小红书封面：https://github.com/panggungunvibe/atutun-xhs-cover

---

## 新增 Projects（2026-06-24）

| # | 项目名称 | 来源 | 说明 |
|---|---------|------|------|
| 26 | `Horizon`（AI 新闻雷达） | Thysrael/Horizon | 自建 AI 情报聚合系统：爬取 Hacker News、Reddit、Telegram、RSS、GitHub、X/Twitter、OpenBB 金融新闻等源，AI 评分去重 + 多源合并 + 背景增强 + 评论区摘要，支持英中双语简报。输出：静态网页（GitHub Pages）、邮件通讯（SMTP/IMAP）、飞书/钉钉/Slack/Discord 推送、Webhook。模型支持：Claude、GPT、Gemini、DeepSeek、Doubao、MiniMax、Ollama。**注意**: 此为独立 Python 项目（非 Hermes skill），需克隆后配置 uv 安装依赖、设置 .env、运行 `uv run python -m src.main`。适合构建个人情报系统、金融信息聚合、技术趋势监控。 |
| 27 | `agent-reach`（互联网 13 平台路由器） | Panniantong/Agent-Reach | **Hermes Skill + CLI 工具双重身份**。13 平台多后端路由：小红书/推特/B站/Reddit/V2EX/LinkedIn/YouTube/GitHub/小宇宙/雪球/RSS/网页/代码搜索。零配置可用 6 频道（V2EX/Web/RSS/GitHub/API/YouTube 基础），需登录态平台（小红书/Reddit/Twitter/LinkedIn）支持 OpenCLI/桌面 Cookie 复用或专用 MCP/CLI 后端。触发词：「调研/全网调研/搜一下/查一下/看看大家怎么说」或任意平台名/URL。**技能位置**: `agent_reach/skill/SKILL.md`，**命令**: `agent-reach doctor`（环境检查）、`agent-reach doctor --json`（机器可读）、`agent-reach install --env=auto`（自动安装工具）。 |
| 28 | `clone-website`（像素级网站克隆） | JCodesMore/ai-website-cloner-template | **Hermes Skill + Next.js 模板双重身份**。AI 驱动的网站反向工程流水线：自动提取 CSS/字体/颜色/SVG 图标/图片/视频/文案 → 生成组件规范文件 → 并行分发 builder agents 分别构建每个组件 → 验证构建 → 视觉 QA 对比。**核心特性**: 像素级精度（getComputedStyle() 提取精确值）、多状态提取（点击/滚动/悬停）、层级图像识别、滚动驱动交互识别、响应式断点提取。**触发词**:「克隆网站/复刻网站/反向工程/重建这个页面/这个网站照做一个」。**前置条件**: 需要浏览器 MCP（Chrome/Playwright 等），基于 Next.js 16 + shadcn/ui + Tailwind v4。**命令**: `npm run dev`、`npm run build`、`/clone-website <url1> [<url2> ...]`。 |

## 新增来源链接

- Horizon: https://github.com/Thysrael/Horizon
- Agent-Reach: https://github.com/Panniantong/Agent-Reach
- ai-website-cloner-template: https://github.com/JCodesMore/ai-website-cloner-template


# AI 算命 （NOT INSTALL)
- 紫微斗数 + 八字： https://github.com/DestinyLinker/MingLi-Bench
- 紫微斗数排盘工具： https://github.com/SylarLong/iztro
- 紫微斗数排盘工具说明：https://docs.iztro.com/learn/pattern.html



# Not Install
想用Hermes和Openclaw白嫖全网数据又不想被反爬的收藏着10个仓库就够了！

1️⃣ Firecrawl：丢个URL进去，它自己把整站爬完，吐出来就是AI能直接吃的干净数据，JS渲染的页面也扛得住，14万★，进了GitHub Top 100。
🔗 https://github.com/firecrawl/firecrawl

2️⃣ Crawl4AI：把网站整成LLM能直接读的文本，不要API key不要钱。一个被16美元月费惹毛的程序员几天写出来的，7万★。
🔗 https://github.com/unclecode/crawl4ai

3️⃣ browser-use：让AI像真人一样点鼠标、登录、填表，ETH Zurich学生团队搞的，10万★。
🔗 https://github.com/browser-use/browser-use

4️⃣ Crawlee：自动换代理、重试、伪装指纹、管队列，一整套躲限制的家伙事儿全给你配齐。
🔗 https://github.com/apify/crawlee

5️⃣ Scrapy：干了十多年的老炮，几百万页面照样稳，永久免费。
🔗 https://github.com/scrapy/scrapy

6️⃣ MarkItDown：微软出的，PDF、Office、HTML、图片批量转文本，开源免费。
🔗 https://github.com/microsoft/markitdown

7️⃣ Scrapling：网站改版它自己适应，还能一直躲封禁，免费版能打付费的。
🔗 https://github.com/D4Vinci/Scrapling

8️⃣ scrcpy：用电脑远程操控安卓手机，专治那些只有App没网页的，14万★。
🔗 https://github.com/Genymobile/scrcpy

9️⃣ AutoScraper：给它一个样例，它自己学规律批量扒，不用写选择器，几行Python就跑。
🔗 https://github.com/alirezamika/autoscraper

🔟 curl-impersonate：把请求伪装成真Chrome指纹，看着就像真人在点，绕反爬不要太轻松。
🔗 https://github.com/lwthiker/curl-impersonate

工具都摆这了，能扒多少看你自己。
