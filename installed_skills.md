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
| 29 | `stock-sdk`（JS 股票行情 SDK） | chengzuopeng/stock-sdk | 纯 JavaScript 股票行情 SDK（零依赖，Browser + Node.js）。无需 API key，直接获取 A股/港股/美股/基金实时行情与 K 线数据。**用法**: `npm install stock-sdk` → `new StockSDK()` → `sdk.quotes.cnSimple(['sh600519'])`. CLI: `npx stock-sdk quote 600519`. 内置 MCP server: `npx stock-sdk mcp`. 支持技术指标/选股/回测。参考：https://github.com/chengzuopeng/stock-sdk |
| 30 | `huashu-nuwa`（女娲·造人术） | alchaincyf/nuwa-skill | 输入人名/主题/模糊需求，自动深度调研→思维框架提炼→生成可运行的人物 Skill。捕捉 HOW they think，不是 WHAT they said。**用法**: 安装后直接说「蒸馏一个XX」让 AI 自动蒸馏新人，或直接使用已蒸馏好的 14 个牛人视角技能（乔布斯/马斯克/芒格/费曼/纳瓦尔/塔勒布/PG/特朗普/MrBeast/Ilya/Karpathy/张一鸣/张雪峰/孙宇晨）。参考：https://github.com/alchaincyf/nuwa-skill |
| 31 | `mistery-perspective`（Mistery 视角） | 源：自建（书籍+推文蒸馏） | 基于 710页《Mistery股市理论》+ 183条推文（7天）蒸馏的炒股思维框架 Skill。提炼 8 个核心心智模型：增量资金思维 / 结构性行情 / 远离大多数人 / 筹码优先于技术面 / 等待主升浪 / 认知深度决定持仓 / 情绪钟摆 / 主力行为学 + 10条决策启发式 + 完整表达DNA。**触发方式**:• 显式：「用Mistery视角分析」「Mistery会怎么看」「切换到Mistery模式」「mistery perspective」• 隐式：提及「增量资金」「筹码结构」「情绪钟摆」「主升浪」「认知深度」等Mistery自创概念• 英文：「how would Mistery think」「in Mistery's view」**使用方法**: 直接问投资决策/市场分析问题，Skill会以Mistery身份回答（条件化表达/不给代码/逻辑优先）。文件位置：`/data/hermes/workspace/.claude/skills/mistery-perspective/SKILL.md` |
| 32 | `book-to-skill`（书籍→Skill） | virgiliojr94/book-to-skill | 把技术书籍/PDF/EPUB/DOCX 转成 AI Agent Skill 的工具。24-51倍 fewer tokens 比直接塞进 context（约 $1/本书）。生成 SKILL.md + 每章 Markdown + 术语表 + 模式库 + 速查表。**用法**: `npx skills add virgiliojr94/book-to-skill` → `/book-to-skill ./my-book.pdf my-slug`。支持 Claude Code / Codex / Cursor / OpenClaw / Hermes 等 50+ runtime。适用：技术书籍/内部文档/研究论文。参考：https://github.com/virgiliojr94/book-to-skill |
| 33 | `seedance-20`（导演 Skill OS） | Emily2040/seedance-2.0 | ✅ 已安装：`/data/hermes/.hermes/skills/seedance-2.0/`（category: seedance-2.0，28个子skill）。AI视频生成导演技能包，35种内容类型（产品/恐怖/音乐MV/动漫/动作/纪录片/时尚/Sci-Fi），支持中/日/韩/俄/西六语言，对接 Seedance/Dreamina/Jimeng/Doubao/Runway/Volcengine 等平台。核心原则："导演场景，不是装饰画面"。**用法**：说「帮我用Seedance生成一个XX视频」或触发子skill（seedance-prompt/seedance-camera/seedance-lighting等）。参考：https://github.com/Emily2040/seedance-2.0 |
| 34 | `video-use`（AI 视频剪辑） | browser-use/video-use | 用 AI Agent 剪辑视频的工具，丢原始素材进文件夹，聊天得到 `final.mp4`。功能：自动删除 filler words / 音频淡入淡出 / 自动调色 / 烧录字幕 / 自我评估。原理：LLM 通过 ElevenLabs Scribe 读取词级时间戳转录（~12KB）+ 按需可视化时间线，不逐帧处理。**用法**: `git clone` 后配置 `ELEVENLABS_API_KEY`，依赖 ffmpeg（必须）。**注意**：这是视频剪辑工具，不是生成工具（生成用 seedance）。参考：https://github.com/browser-use/video-use |
| 35 | `wechat-account-launch-expert`（公众号起号） | chenjin-cmd/agent-skills-launch-pack | 微信公众号起号专家 Skill，覆盖账号定位、主页框架、对标拆解、选题库、文章简报、发布节奏、流量主实验和周复盘。**触发**: 用户询问公众号起号、新号冷启动、流量主、公众号定位、对标账号、爆款标题、30天起号计划或公众号内容策略时。**使用方法**: 直接说「帮我规划公众号起号」「分析下我的公众号定位」「30天起号计划」。**安装**: `./install.sh wechat-account-launch-expert` 或直接 clone skills 目录。参考：https://github.com/chenjin-cmd/agent-skills-launch-pack_ |
| 36 | `xiaohongshu-account-launch-expert`（小红书起号） | chenjin-cmd/agent-skills-launch-pack | 小红书起号专家 Skill，覆盖账号定位、笔记简报、内容日历、转化路径、主页诊断、选题库、对标分析和 30/60/90 天起号计划。**触发**: 用户需要创建/诊断/优化小红书账号，包括起号、涨粉、引流、账号定位、个人IP、选题库、笔记简报、内容日历、主页诊断、转化路径时。**使用方法**: 直接说「帮我做小红书起号规划」「分析账号定位」「30天起号计划」。参考：https://github.com/chenjin-cmd/agent-skills-launch-pack_ |
| 37 | `douyin-account-launch-expert`（抖音起号） | chenjin-cmd/agent-skills-launch-pack | 抖音新号起号与涨粉 Skill，覆盖账号定位、观看理由、标签校准、搜索流量预埋、3秒钩子、人格化表达、评论互动、私域冷启动、合集运营、9条视频小样本实验、数据复盘和30天执行计划。**触发**: 用户询问抖音起号、涨粉、新号冷启动、账号定位、低播放量、对标账号、短视频选题、完播率、评论互动、合集策略、私域启动或抖音内容复盘时。**使用方法**: 直接说「帮我规划抖音起号」「分析账号问题」「新号冷启动计划」。参考：https://github.com/chenjin-cmd/agent-skills-launch-pack_ |
| 38 | `channels-account-launch-expert`（视频号起号） | chenjin-cmd/agent-skills-launch-pack | 微信视频号起号专家 Skill，覆盖账号定位、人设打造、选题策划、视频脚本、私域承接、9条视频小样本实验、数据复盘和30天执行计划。**触发**: 用户询问视频号起号、视频号涨粉、新号冷启动、账号定位、低播放量、对标账号、视频号脚本、完播率、评论互动或视频号内容复盘时。**使用方法**: 直接说「帮我规划视频号起号」「分析视频号数据」「30天起号计划」。参考：https://github.com/chenjin-cmd/agent-skills-launch-pack_ |
| 39 | `x-twitter-cold-start-expert`（X起号） | chenjin-cmd/agent-skills-launch-pack | 中文 X/Twitter 冷启动专家 Skill，覆盖账号定位、内容主题、回复区曝光、主贴/Thread 转化、7天执行计划、周复盘表和增长诊断。**触发**: 用户想做X账号冷启动、推特起号、500粉以内增长、个人IP定位、内容矩阵、互动回复策略、将真实工作流转成内容、复盘X数据，或要求基于账号/选题/截图制定可执行起号方案时。**使用方法**: 直接说「帮我做X起号规划」「分析推特账号」「7天冷启动计划」。参考：https://github.com/chenjin-cmd/agent-skills-launch-pack_ |
| 40 | `female-portrait-director`（女性人像导演） | liyue-aigc/female-portrait-director | ✅ 已安装：`/data/hermes/.hermes/skills/female-portrait-director-skill/`（name: female-portrait-director）。AI 人像图像 Prompt 优化工具，将零散参数扩展为摄影导演级 Prompt。20 种视觉风格路线（CCD/古风/电商/法式/港风/新车/新中式/低暗光等），含冲突检测/安全边界/参考图锁重/参数推荐等工具链。**用法**: 说「生成一张XX风格人像」「优化这个人像Prompt」「帮我写CCD曲线风格人像」。参考：https://github.com/liyue-aigc/female-portrait-director |

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
- JS 股票 SDK：https://github.com/chengzuopeng/stock-sdk
- nuwa-skill（女娲）：https://github.com/alchaincyf/nuwa-skill （14 个预蒸馏人物 skills）
- Mistery 视角：自建（书籍+推文蒸馏）→ `/data/hermes/workspace/.claude/skills/mistery-perspective/SKILL.md`
- 书籍→Skill：https://github.com/virgiliojr94/book-to-skill
- Seedance 2.0 导演 OS：https://github.com/Emily2040/seedance-2.0
- Video-Use AI 剪辑：https://github.com/browser-use/video-use
- 起号专家套装（5平台）：https://github.com/chenjin-cmd/agent-skills-launch-pack_

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

---

## 新增 Skills（追加）

### 2026-07-02: guizang-social-card-skill (本地已安装)

| # | Skill 名称 | 来源 | 说明 |
|---|-----------|------|------|
| 11 | `guizang-social-card-skill` | guizang-ppt-skill | 生成小红书/公众号封面图，Magazine Editorial 风格，支持 3:4 竖版、1:1 方版、21:9 横版，含 6 套调色板、15 种布局模板、WebGL 氛围背景 |

- 来源: https://github.com/guizang/ppt-skill/tree/main/skills
- 用法: 加载 skill `guizang-social-card-skill`，复制模板到工作目录，替换主题和海报内容，用 Playwright 渲染 PNG
- 模板: `assets/template-editorial-card.html`，WebGL: `assets/magazine-bg-webgl.js`
- 布局模板: M01-M15 (封面/清单/账本/对比/引用等)
- 调色板: ink-classic / indigo-porcelain / forest-ink / kraft-paper / dune / midnight-ink

### 2026-07-17: handdraw-story-video（手绘故事视频生成）

| # | 项目名称 | 来源 | 说明 |
|---|---------|------|------|
| 29 | `handdraw-story-video` | xiejunjie524/handdraw-story-video | 把 7–9 幅手绘故事母图制作成 35–45 秒竖屏短视频：先从左到右显现黑白线稿，再沿相同方向逐步填入低饱和色彩。基于 HyperFrames + GSAP，输出 720×960 / 30fps 竖屏视频。兼容任意生图模型（不绑定 API），支持字幕、道具文字、时长/素材自动校验。适合小红书/抖音暖心故事/励志短片内容批量生产 |

- 来源: https://github.com/xiejunjie524/handdraw-story-video
- 环境: Python 3.10+ / Node.js 18+ / FFmpeg / HyperFrames / GSAP
- 安装: `git clone → pip install -r requirements.txt → npm install gsap`
- 核心流程:
  1. 复制模板 `cp templates/story-template.json story.json`，填写故事配置
  2. 每幕生成一张 1K 彩色母图，用 `python scripts/make_lineart.py` 提取对齐线稿
  3. 准备 HyperFrames: `mkdir -p hyperframes/assets/vendor && cp node_modules/gsap/dist/gsap.min.js hyperframes/assets/vendor/`
  4. 放入图片和 BGM 到 `hyperframes/assets/`，路径与 `story.json` 一致
  5. 生成页面: `python scripts/build_story.py story.json hyperframes/index.html --check-assets`
  6. 校验: `npx hyperframes check hyperframes/index.html --json`
  7. 渲染: `npx hyperframes render hyperframes/index.html --output renders/story-v1.mp4 --workers 1`
- 画面原则: 8 幕各约 5 秒，主体占下方 45%–55%，纸白留白，单帧最多 2–3 人
- Codex Skill: 可将仓库链接到 `$CODEX_HOME/skills/handdraw-good-deed-story`，用"做一个 40 秒线稿逐渐上色的暖心故事"触发

### 2026-07-17: equity-research（机构级投研报告）

| # | Skill 名称 | 来源 | 说明 |
|---|-----------|------|------|
| 30 | `equity-research` | rollingSirius/equity-research-skill | 机构级个股投研报告 Agent Skill：九章结构 + 多方法估值交叉验证（DCF/相对估值/情景加权）。覆盖美股/港股/A股，含 A/H 双重上市溢价对比。触发词：公司名/代码 + 任何投研意图。IBKR/Morningstar/联网三路并行采集，降级自动标注 |

- 来源: https://github.com/rollingSirius/equity-research-skill
- 触发词: "研究/分析一下某只股票"、"值不值得买"、"写投研报告"、"is this stock a buy"
- 工作流: 明确标的 → 并行采集(IBKR+Morningstar+联网) → 对账时间戳 → 九章报告 → DCF估值(≥3种方法)
- 核心文件: `references/report-template.md`（九章模板）/ `references/valuation-methods.md`（标定规则）/ `scripts/dcf.py`（计算器）
- 质量要求: 结论低估/合理/高估必须由规则产出，DCF 全用脚本计算，"未获取到"诚实标注

### 2026-07-17: InStock（A股量化系统）

| # | 项目名称 | 来源 | 说明 |
|---|---------|------|------|
| 31 | `InStock`（myhhub/stock） | myhhub/stock | 全功能 A 股量化投资平台：200+ 维度综合选股、32 种技术指标（与同花顺/通达信一致）、61 种 K 线形态识别、筹码分布（CYQ，与东方财富一致）、策略选股、回测、自动交易（仅 Windows）。Docker 一键部署，Web UI（9988端口）。Apache-2.0 |

- 来源: https://github.com/myhhub/stock
- Docker: `docker run -dit --name InStock -p 9988:9988 -e db_host=localhost ... mayanghua/instock:latest`
- 访问: http://localhost:9988/
- 技术: Python + talib + pandas + MySQL，指标和筹码计算结果与商业软件对标
- ⚠️ 自动交易仅支持 Windows；需一定量化基础，非 AI 选股工具

### 2026-07-20: story-to-handdrawn-video（手绘日记漫画动画）

| # | Skill 名称 | 来源 | 说明 |
|---|-----------|------|------|
| 32 | `story-to-handdrawn-video` | gnipbao/story-to-handdrawn-video | 将中文故事文案或有序手绘图片，转换成 3:4 竖屏手绘日记漫画动画：手写字幕、"文字→黑白画稿→彩色插画"从左到右揭示、可选右下角卷页翻书转场。基于 Remotion，输出无声 H.264 画面轨。Codex/Agent Skill 分发版在 `skill-package/` 目录下 |

- 来源: https://github.com/gnipbao/story-to-handdrawn-video
- 技术栈: Remotion (React/TypeScript) + H.264 MP4
- 输出规格: 1080×1440 正式渲染 / 720×960 快速预览
- 动画阶段: 文字 → 黑白画稿 → 彩色插画（均从左到右揭示）
- 可选转场: 右下角卷页翻书（纸背保留淡化原页纹理）
- 环境: Node.js / npx remotion preview / npx remotion render

### 2026-07-22: free-stockdb（本地A股量化数据引擎）

| # | 项目名称 | 来源 | 说明 |
|---|---------|------|------|
| 33 | `free-stockdb` | hello245m/free-stockdb | 本地 A 股量化数据引擎：日K / 分钟K / ETF / tick 数据同步、清洗、复权；内置 39 种指标 + 5 种指数；支持 Python SDK / HTTP API / Excel / HTML / MCP 五种调用方式。Windows exe 可直接运行，增量同步，Zstd 压缩存储 |

- 来源: https://github.com/hello245m/free-stockdb
- 下载: https://github.com/hello245m/free-stockdb/releases （Windows exe 版）
- 数据: A股日K、分钟K（1/5/15/30分钟）、ETF、tick 级，Zstd 压缩，本地存储
- 内置指标: 39 种技术指标 + 5 种指数（Rust 计算核心，比 pandas 快 3 倍）
- 复权: 内置完整复权因子，查询时写时计算
- 板块: 申万一二三级 + 1200 概念板块，毫秒查询

---

## 使用方法

### 前提（Windows）

下载 [Releases](https://github.com/hello245m/free-stockdb/releases) 的 Windows exe 包，解压后：

1. **双击 `数据更新.exe`** → 等待数据同步完成（可多次退出/重启直到同步完）
2. **双击 `stockdb.exe`** → 启动本地数据库服务（监听 7899 端口）

> ⚠️ 数据更新前先退出 stockdb.exe

### 方式一：Python SDK（推荐）

```bash
# 1. 运行一次安装脚本（将 pybao 模块写入 Python 全局路径）
python pybao/安装.py

# 2. 启动数据库后，任何位置均可导入
python
>>> from stockdb import init, rd
>>> from stock_sdk import StockDBClient
>>>
>>> client = StockDBClient(host="127.0.0.1", port=7899)
>>> df = client.get_data("日K", "000001", start="2024-01-01", end="2024-12-31")
>>> print(df)
```

> `stockdb.pyd` 需要与 Python 版本匹配（3.8+ 非自由线程 / 3.14t+ 自由线程）

### 方式二：HTTP API

```bash
# 启动后访问 http://127.0.0.1:7899
python 调用方式/http/http_api.py
```

直接浏览器打开 `数据网页版.html` 可可视化查看行情数据。

### 方式三：Excel / WPS

```bash
# 使用 WPS 宏脚本
# 见 调用方式/excel/wps_js_macro.js
```

### 方式四：AI MCP（Claude Desktop / Cursor 等）

1. 先运行一次 `pybao/安装.py`
2. 编辑 Claude Desktop 配置 `claude_desktop_config.json`，添加：

```json
{
  "mcpServers": {
    "stockdb-native": {
      "command": "python",
      "args": ["-u", "C:/path/to/ai_mcp/stock_mcp_server.py"]
    }
  }
}
```

3. 重启 Claude Desktop，确保 stockdb.exe 在后台运行

> MCP Server 依赖 `native_mcp.py`，零第三方依赖

---

### Linux 服务器用法（直接调用本地数据文件）

该项目本质是本地数据文件 + C++ 时序引擎，数据路径在 `./data/`。在没有 stockdb.exe 的 Linux 端，可以直接读取 `./data/` 下的 Zstd 压缩文件自己解包分析（不依赖 exe）。
