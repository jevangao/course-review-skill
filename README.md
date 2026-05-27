# Course Slide Study Guide

`course-slide-study-guide` 是一个将课程、讲座、培训或复习课件转化为可核验学习资料的 Codex skill。

它不仅提取幻灯片文字，还要求对图解、公式、表格、流程动画和示例过程进行视觉核验，并区分：

- `课件口径`：课件本身采用的定义、符号或限制条件。
- `通用补充`：有助于学习者理解的标准背景知识。
- `待核验`：疑似笔误、图示歧义、无法渲染内容或存在冲突的表述。

## 适用场景

- 根据一学期的 PPT/PDF 课件生成 Markdown 复习讲义。
- 为考试准备速查表、公式表、易错点清单或自测题。
- 从培训课件整理行动手册、术语表和流程检查清单。
- 为算法、数学、工程、法律、语言、人文或职业培训课件建立可追溯知识资料。

## 核心能力

- 清点 `.pptx`、`.ppt`、`.pdf` 课件来源并统计覆盖范围。
- 从 `.pptx` 中按真实播放顺序抽取逐页文字和真实备注正文。
- 输出 Markdown 与 JSON 页级语料，便于搜索、定位和后续生成。
- 标记需要人工视觉核验的图片、图表、连接线或无文本页面。
- 生成覆盖校验报告，避免遗漏来源或页数不一致。
- 引导生成详细讲义、速查版、公式/术语表、题库素材和学习检查单。

## 目录结构

```text
.
├── SKILL.md
├── agents/
│   └── openai.yaml
├── docs/
│   └── SKILL.zh-CN.md
├── references/
│   ├── output-modes.md
│   └── visual-review.md
└── scripts/
    ├── inventory_slides.py
    ├── extract_pptx_corpus.py
    └── check_coverage.py
```

## 使用方式

在 Codex 中调用本 skill，并提供课件目录或文件，例如：

```text
Use $course-slide-study-guide to read the slides in this directory and create a detailed Chinese Markdown study guide with a rapid-review sheet.
```

处理 `.pptx` 的核心证据流程如下：

```bash
python3 scripts/inventory_slides.py --output-dir outputs/evidence <课件目录>
python3 scripts/extract_pptx_corpus.py --output-dir outputs/evidence <课件目录>
python3 scripts/check_coverage.py \
  --inventory outputs/evidence/source-inventory.json \
  --corpus outputs/evidence/pptx-corpus.json \
  --output outputs/evidence/coverage-report.md
```

文字抽取不能替代视觉检查。对于图示、公式、表格、动画过程页，应使用可用的 PPT/PDF 渲染工作流生成页面预览或联系表，再完成讲义总结。

## 已验证样本

该 skill 最初基于一套数据结构课程课件提炼和验证：

- `28` 份 PPTX
- `1049` 页幻灯片
- 清点与文本抽取覆盖报告为 `PASS`
- 抽取器修正了备注页中的幻灯片编号占位符误收问题

## 中文文档

主入口 [SKILL.md](SKILL.md) 保持标准可执行说明；完整中文配套说明见 [docs/SKILL.zh-CN.md](docs/SKILL.zh-CN.md)。
