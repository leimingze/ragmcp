# RAGMCP

> 可扩展、可观测、易迭代的 RAG（检索增强生成）框架，集成 MCP（Model Context Protocol）支持

## 项目概述

RAGMCP 是一个基于 Python 3.12+ 构建的现代化 RAG 框架，采用**可插拔架构设计**。

### 核心特性

- 🔌 **可插拔组件**：LLM、Embedding、VectorStore、Reranker、Evaluator 均可配置切换
- 🔍 **混合检索**：稠密（语义）+ 稀疏（关键词）检索，RRF 融合
- 🖼️ **多模态支持**：图像理解与跨模态检索
- 📊 **可观测性**：结构化日志 + Streamlit 仪表板
- 🤖 **MCP 集成**：作为 MCP Server 无缝接入 Claude Desktop、GitHub Copilot 等

## 快速开始

### 安装

```bash
# 克隆仓库
git clone https://github.com/your-org/ragmcp.git
cd ragmcp

# 创建虚拟环境
python3.12 -m venv .venv
source .venv/bin/activate

# 安装依赖
pip install -e ".[dev]"

# 安装 pre-commit hooks
pre-commit install
```

### 运行测试

```bash
# 运行所有测试
pytest

# 运行测试并查看覆盖率
pytest --cov=src/ragmcp --cov-report=html

# 代码格式检查
ruff check .
```

## 项目结构

```
ragmcp/
├── src/ragmcp/           # 源代码
│   ├── llm/              # LLM 抽象接口
│   ├── embedding/        # Embedding 抽象接口
│   ├── vectorstore/      # 向量存储抽象接口
│   ├── reranker/         # 重排器抽象接口
│   └── evaluator/        # 评估器抽象接口
├── tests/                # 测试代码
├── .claude/              # Claude Code 命令和技能
│   ├── commands/         # 任务管理、工作流命令
│   └── skills/           # TDD 开发技能
├── devspec.md            # 技术设计文档
├── PROJECT_SCHEDULE.md   # TDD 开发排期
└── pyproject.toml        # 项目配置
```

## 开发规范

- **测试驱动开发 (TDD)**：所有功能先写测试
- **代码风格**：遵循 ruff 配置
- **类型提示**：使用 mypy 进行类型检查
- **提交前**：自动运行 pre-commit hooks

### TDD 闭环流程

使用 `/dev <ID>` 命令执行任务，会自动完成以下 6 个阶段：

```
┌─────────────────────────────────────────────────────────────┐
│  [1/6] PARSE   解析任务                                      │
│      └─ 从 PROJECT_SCHEDULE.md 读取任务详情                 │
├─────────────────────────────────────────────────────────────┤
│  [2/6] RED     写测试（预期失败）                            │
│      └─ 创建测试文件，运行 pytest 确认失败                   │
├─────────────────────────────────────────────────────────────┤
│  [3/6] GREEN   写代码（通过测试）                            │
│      └─ 实现功能，运行 pytest 直到通过                       │
├─────────────────────────────────────────────────────────────┤
│  [4/6] REFACTOR 代码优化                                     │
│      └─ ruff format + mypy check                            │
├─────────────────────────────────────────────────────────────┤
│  [5/6] VERIFY  验收检查                                      │
│      └─ 检查测试覆盖率和验收标准                             │
├─────────────────────────────────────────────────────────────┤
│  [6/6] UPDATE  更新状态                                      │
│      └─ PROJECT_SCHEDULE.md: ⏳ → ✅                         │
└─────────────────────────────────────────────────────────────┘
```

### 开发命令

```bash
# 执行指定任务
/dev 1.1.1

# 运行测试
/test              # 所有测试
/test phase1       # Phase 1 测试
/test 1.1.1        # 任务 1.1.1 测试
/test --coverage   # 带覆盖率
```

## 文档

- [设计规范](devspec.md) - 完整的技术设计文档
- [开发计划](PROJECT_SCHEDULE.md) - TDD 开发排期

## 技术栈

| 组件 | 技术选型 |
|------|----------|
| **框架** | LangChain & LangGraph |
| **LLM** | Azure OpenAI / OpenAI / Ollama / DeepSeek / Claude |
| **Embedding** | OpenAI / 本地模型 |
| **向量存储** | Milvus (主要) / Chroma / Qdrant / Pinecone |
| **Rerank** | Cross-Encoder / LLM-based |
| **PDF 解析** | markitdown |
| **MCP SDK** | Python 官方 MCP SDK |
| **可观测性** | Streamlit |

## License

MIT License

---

**Version**: 0.1.0
**Python**: 3.12+
**Status**: Alpha - 早期开发阶段
