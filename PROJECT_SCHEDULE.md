# RAGMCP 项目排期表 (TDD 模式)

> 严格按照 `devspec.md` 生成的项目规划排期表，采用测试驱动开发（TDD）模式
>
> 状态说明：⏳ 未开始 | 🔄 进行中 | ✅ 已完成
> 优先级说明：🔴 P0 (核心基础) | 🟡 P1 (重要功能) | 🟢 P2 (扩展功能)

---

## Phase 1: 可插拔架构层 - 接口定义

> **依赖分析**：此阶段为整个项目的基础，必须最先完成。所有后续功能都依赖这些抽象接口。

### Milestone 1.1: 核心接口定义完成

#### Module 1.1: LLM 与 Embedding 接口定义

- [x] ✅ **1.1.1 定义 LLMClient 抽象接口** 🔴 P0
  - **任务描述**: 定义 LLM 调用的统一抽象接口，屏蔽不同 Provider 的认证方式与请求格式差异
  - **测试先行步骤**:
    - 编写抽象类测试基类，验证子类必须实现 chat() 方法
    - 定义测试用例：验证 messages 格式、response 结构
  - **实现步骤**:
    - 定义抽象类 `LLMClient`
    - 定义抽象方法 `chat(messages: List[Message]) -> Response`
    - 定义 `Message` 和 `Response` 数据结构
  - **验收标准**:
    - 抽象类定义正确，无法直接实例化
    - 测试基类能验证子类的强制实现
    - 数据结构包含必需字段
  - **devspec 参考**: 第 262 行

- [x] ✅ **1.1.2 定义 EmbeddingClient 抽象接口** 🔴 P0
  - **任务描述**: 定义向量嵌入的统一抽象接口，统一处理批量请求与维度归一化
  - **测试先行步骤**:
    - 编写测试基类，验证子类必须实现 embed() 方法
    - 定义测试用例：验证批量文本输入、向量输出格式、维度归一化
  - **实现步骤**:
    - 定义抽象类 `EmbeddingClient`
    - 定义抽象方法 `embed(texts: List[str]) -> List[np.ndarray]`
    - 定义向量维度归一化逻辑
  - **验收标准**:
    - 抽象类定义正确
    - 批量处理接口设计合理
    - 向量归一化逻辑正确
  - **devspec 参考**: 第 263 行

- [x] ✅ **1.1.3 定义 BaseVisionLLM 抽象接口** 🔴 P0
  - **任务描述**: 定义多模态 LLM 接口，支持文本+图片的多模态输入
  - **测试先行步骤**:
    - 编写测试基类，验证子类必须处理多模态输入
    - 定义测试用例：验证文本+图片混合输入格式
  - **实现步骤**:
    - 定义抽象类 `BaseVisionLLM` (可继承自 `LLMClient`)
    - 定义多模态输入数据结构 `MultimodalMessage` (text + images)
    - 扩展 `chat()` 方法支持图片输入
  - **验收标准**:
    - 接口支持文本和图片混合输入
    - 数据结构清晰
  - **devspec 参考**: 第 265 行

#### Module 1.2: 向量存储接口定义

- [x] ✅ **1.2.1 定义 VectorStore 抽象接口** 🔴 P0
  - **任务描述**: 定义向量存储的统一接口，支持插入、查询、删除操作
  - **测试先行步骤**:
    - 编写测试基类，定义向量存储的基本操作测试
    - 定义测试用例：插入、查询、删除、upsert 操作
  - **实现步骤**:
    - 定义抽象类 `VectorStore`
    - 定义方法：`insert()`, `query()`, `delete()`, `upsert()`
    - 定义向量+payload 数据结构
  - **验收标准**:
    - 接口包含所有必需方法
    - upsert 语义明确（插入或更新）
  - **devspec 参考**: 第 269 行（检索策略抽象）

#### Module 1.3: Rerank 接口定义

- [x] ✅ **1.3.1 定义 Reranker 抽象接口** 🔴 P0
  - **任务描述**: 定义重排器的统一接口，支持对候选文档集进行相关性排序
  - **测试先行步骤**:
    - 编写测试基类，验证 rerank 方法签名
    - 定义测试用例：验证输入格式（query + chunks）、输出格式（排序后的 chunks + 分数）
  - **实现步骤**:
    - 定义抽象类 `Reranker`
    - 定义抽象方法 `rerank(query: str, chunks: List[Chunk]) -> List[RankedChunk]`
    - 定义 `RankedChunk` 数据结构（chunk + score）
  - **验收标准**:
    - 接口定义清晰
    - 输入输出格式明确
  - **devspec 参考**: 第 164 行

#### Module 1.4: 评估框架接口定义

- [x] ✅ **1.4.1 定义 Evaluator 抽象接口** 🔴 P0
  - **任务描述**: 定义评估器的统一接口，输出标准化的指标字典
  - **测试先行步骤**:
    - 编写测试基类，验证 evaluate 方法签名
    - 定义测试用例：验证输入参数（query, retrieved_chunks, generated_answer, ground_truth）
  - **实现步骤**:
    - 定义抽象类 `Evaluator`
    - 定义抽象方法 `evaluate(query, retrieved_chunks, generated_answer, ground_truth) -> Dict[str, float]`
  - **验收标准**:
    - 接口定义清晰
    - 返回值为标准化的指标字典
  - **devspec 参考**: 第 274 行

#### Module 1.5: RAG Pipeline 组件接口定义

- [ ] ⏳ **1.5.1 定义 Loader 抽象接口** 🔴 P0
  - **任务描述**: 定义文档解析器的统一接口
  - **测试先行步骤**:
    - 编写测试基类，验证 load 方法
    - 定义测试用例：验证输入（文件路径）、输出（Document 对象）
  - **实现步骤**:
    - 定义抽象类 `Loader`
    - 定义抽象方法 `load(file_path: str) -> Document`
    - 定义 `Document` 数据结构
  - **验收标准**:
    - 接口支持多种文档格式扩展
    - Document 包含 text 和 metadata 字段
  - **devspec 参考**: 第 76 行

- [ ] ⏳ **1.5.2 定义 Splitter 抽象接口** 🔴 P0
  - **任务描述**: 定义文档切分器的统一接口
  - **测试先行步骤**:
    - 编写测试基类，验证 split 方法
    - 定义测试用例：验证输入（Document）、输出（List[Chunk]）
  - **实现步骤**:
    - 定义抽象类 `Splitter`
    - 定义抽象方法 `split(document: Document) -> List[Chunk]`
    - 定义 `Chunk` 数据结构
  - **验收标准**:
    - 接口支持多种切分策略
    - Chunk 包含定位信息（source, chunk_index, offsets）
  - **devspec 参考**: 第 104 行

- [ ] ⏳ **1.5.3 定义 Transform 抽象接口** 🔴 P0
  - **任务描述**: 定义内容转换模块的统一接口
  - **测试先行步骤**:
    - 编写测试基类，验证 transform 方法
    - 定义测试用例：验证输入（Chunk）、输出（增强后的 Chunk）
  - **实现步骤**:
    - 定义抽象类 `Transform`
    - 定义抽象方法 `transform(chunk: Chunk) -> Chunk`
  - **验收标准**:
    - 接口支持多种转换模块（OCR、ImageCaption、HTML 清理等）
  - **devspec 参考**: 第 110 行

#### Module 1.6: 工厂模式接口定义

- [ ] ⏳ **1.6.1 定义 LLMFactory** 🔴 P0
  - **任务描述**: 实现 LLM 工厂，根据配置动态创建 Provider 实例
  - **测试先行步骤**:
    - 编写测试：验证根据不同配置返回正确的 Provider 类型
    - 定义测试用例：azure → AzureOpenAILLM, openai → OpenAILLM
  - **实现步骤**:
    - 实现 `LLMFactory.get_llm(config: Dict) -> LLMClient`
    - 支持的 provider: azure, openai, ollama, deepseek, claude, zhipu
  - **验收标准**:
    - 根据配置返回正确的 Provider 实例
    - 配置格式清晰
  - **devspec 参考**: 第 289 行（配置示例）

- [ ] ⏳ **1.6.2 定义 EmbeddingFactory** 🔴 P0
  - **任务描述**: 实现 Embedding 工厂，根据配置动态创建 Provider 实例
  - **测试先行步骤**:
    - 编写测试：验证根据配置返回正确的 Embedding Client
  - **实现步骤**:
    - 实现 `EmbeddingFactory.get_embedding(config: Dict) -> EmbeddingClient`
  - **验收标准**:
    - 根据配置返回正确的实例
  - **devspec 参考**: 第 295 行

- [ ] ⏳ **1.6.3 定义 VisionLLMFactory** 🔴 P0
  - **任务描述**: 实现 Vision LLM 工厂
  - **测试先行步骤**:
    - 编写测试：验证返回正确的 Vision LLM 实例
  - **实现步骤**:
    - 实现 `VisionLLMFactory.get_vision_llm(config: Dict) -> BaseVisionLLM`
  - **验收标准**:
    - 根据配置返回正确的实例
  - **devspec 参考**: 第 265 行

- [ ] ⏳ **1.6.4 定义 VectorStoreFactory** 🔴 P0
  - **任务描述**: 实现向量存储工厂
  - **测试先行步骤**:
    - 编写测试：验证根据配置返回正确的 VectorStore
  - **实现步骤**:
    - 实现 `VectorStoreFactory.get_vector_store(config: Dict) -> VectorStore`
    - 支持的 backend: milvus, chroma, qdrant, pinecone
  - **验收标准**:
    - 根据配置返回正确的实例
  - **devspec 参考**: 第 299 行

- [ ] ⏳ **1.6.5 定义 RerankerFactory** 🔴 P0
  - **任务描述**: 实现 Reranker 工厂
  - **测试先行步骤**:
    - 编写测试：验证根据配置返回正确的 Reranker
  - **实现步骤**:
    - 实现 `RerankerFactory.get_reranker(config: Dict) -> Reranker`
    - 支持的 backend: none, cross_encoder, llm
  - **验收标准**:
    - 根据配置返回正确的实例
    - none 时返回 NoOpReranker
  - **devspec 参考**: 第 305 行

#### Module 1.7: 配置管理实现

- [ ] ⏳ **1.7.1 实现 settings.yaml 配置文件** 🔴 P0
  - **任务描述**: 定义统一的配置文件格式
  - **测试先行步骤**:
    - 编写测试：验证配置文件格式解析
    - 定义测试用例：验证各配置项的默认值
  - **实现步骤**:
    - 创建 config/settings.yaml
    - 定义配置结构：llm, embedding, vector_store, retrieval, evaluation, observability
  - **验收标准**:
    - 配置文件结构清晰
    - 包含所有必需的配置项
  - **devspec 参考**: 第 288-309 行

- [ ] ⏳ **1.7.2 实现配置解析器** 🔴 P0
  - **任务描述**: 实现 YAML 配置文件解析
  - **测试先行步骤**:
    - 编写测试：验证配置解析正确性
    - 定义测试用例：正确配置、缺失配置、非法配置
  - **实现步骤**:
    - 实现 `ConfigParser` 类
    - 实现 `load_config(file_path: str) -> Config` 方法
    - 实现配置验证逻辑
  - **验收标准**:
    - 能够正确解析 YAML
    - 配置项映射正确
    - 缺失配置有合理默认值
  - **devspec 参考**: 第 287 行（配置管理与切换流程）

#### Module 1.8: 中间层实现

- [ ] ⏳ **1.8.1 实现重试中间层** 🟡 P1
  - **任务描述**: 为 LLM/Embedding 调用添加重试机制
  - **测试先行步骤**:
    - 编写测试：验证失败自动重试
    - 定义测试用例：网络错误重试、API 错误不重试、达到最大重试次数
  - **实现步骤**:
    - 实现装饰器 `@retry(max_retries, backoff)`
    - 应用到 LLMClient 和 EmbeddingClient 的方法
  - **验收标准**:
    - 失败请求能够自动重试
    - 重试策略可配置
    - 避免无限重试
  - **devspec 参考**: 第 264 行

- [ ] ⏳ **1.8.2 实现限流中间层** 🟡 P1
  - **任务描述**: 为 LLM/Embedding 调用添加限流机制
  - **测试先行步骤**:
    - 编写测试：验证请求速率限制
    - 定义测试用例：超过速率限制时等待、未超过时正常通过
  - **实现步骤**:
    - 实现装饰器 `@rate_limit(max_requests, time_window)`
    - 应用到 LLMClient 和 EmbeddingClient 的方法
  - **验收标准**:
    - 请求速率可控
    - 限流策略可配置
  - **devspec 参考**: 第 264 行

- [ ] ⏳ **1.8.3 实现日志中间层** 🟡 P1
  - **任务描述**: 为 LLM/Embedding 调用添加日志记录
  - **测试先行步骤**:
    - 编写测试：验证日志记录完整
    - 定义测试用例：验证日志包含输入、输出、耗时
  - **实现步骤**:
    - 实现装饰器 `@log_call`
    - 记录请求参数、响应、耗时
  - **验收标准**:
    - 所有调用有日志记录
    - 日志内容完整
  - **devspec 参考**: 第 264 行

### ✅ Milestone 1.1 验收标准
- [x] 所有核心抽象接口定义完成 (LLMClient, EmbeddingClient, BaseVisionLLM, VectorStore, Reranker, Evaluator)
- [ ] 所有工厂模式实现完成
- [ ] 配置文件和解析器实现完成
- [ ] 单元测试覆盖率 > 80% (当前: 35 个测试通过)
- [ ] 接口文档完整

---

## Phase 2: LLM 与 Embedding Provider 实现

> **依赖分析**：依赖 Phase 1 的接口定义。各 Provider 实现之间无依赖，可按需实现。

### Milestone 2.1: 核心 Provider 实现

#### Module 2.1: LLM Provider 实现

- [ ] ⏳ **2.1.1 实现 AzureOpenAILLM** 🔴 P0
  - **任务描述**: 实现 Azure OpenAI 的 LLMClient
  - **测试先行步骤**:
    - 编写 mock 测试：验证 API 调用格式
    - 编写集成测试：验证与真实 Azure OpenAI 的交互
    - 定义测试用例：正常调用、流式输出、错误处理
  - **实现步骤**:
    - 继承 LLMClient
    - 实现 `chat()` 方法，调用 Azure OpenAI API
    - 处理认证（API Key）
    - 处理错误和超时
  - **验收标准**:
    - 所有测试通过
    - API 调用格式符合 Azure 规范
    - 支持流式输出（如需要）
  - **devspec 参考**: 第 21 行、第 266 行

- [ ] ⏳ **2.1.2 实现 OpenAILLM** 🟡 P1
  - **任务描述**: 实现 OpenAI 官方 API 的 LLMClient
  - **测试先行步骤**:
    - 编写 mock 测试和集成测试
  - **实现步骤**:
    - 继承 LLMClient
    - 实现 `chat()` 方法
  - **验收标准**:
    - 所有测试通过
  - **devspec 参考**: 第 22 行

- [ ] ⏳ **2.1.3 实现 OllamaLLM** 🟡 P1
  - **任务描述**: 实现本地 Ollama 部署的 LLMClient
  - **测试先行步骤**:
    - 编写测试：验证本地 HTTP 通信
  - **实现步骤**:
    - 继承 LLMClient
    - 实现 `chat()` 方法，调用 Ollama HTTP API
  - **验收标准**:
    - 所有测试通过
  - **devspec 参考**: 第 23 行

- [ ] ⏳ **2.1.4 实现 DeepSeekLLM** 🟢 P2
  - **任务描述**: 实现 DeepSeek API 的 LLMClient
  - **测试先行步骤**:
    - 编写 mock 测试和集成测试
  - **实现步骤**:
    - 继承 LLMClient
    - 实现 `chat()` 方法
  - **验收标准**:
    - 所有测试通过
  - **devspec 参考**: 第 24 行

- [ ] ⏳ **2.1.5 实现 ClaudeLLM** 🟢 P2
  - **任务描述**: 实现 Anthropic Claude API 的 LLMClient
  - **测试先行步骤**:
    - 编写 mock 测试和集成测试
  - **实现步骤**:
    - 继承 LLMClient
    - 实现 `chat()` 方法
  - **验收标准**:
    - 所有测试通过
  - **devspec 参考**: 第 24 行

- [ ] ⏳ **2.1.6 实现 ZhipuLLM** 🟢 P2
  - **任务描述**: 实现智谱 API 的 LLMClient
  - **测试先行步骤**:
    - 编写 mock 测试和集成测试
  - **实现步骤**:
    - 继承 LLMClient
    - 实现 `chat()` 方法
  - **验收标准**:
    - 所有测试通过
  - **devspec 参考**: 第 24 行

#### Module 2.2: Embedding Provider 实现

- [ ] ⏳ **2.2.1 实现 OpenAIEmbedding** 🔴 P0
  - **任务描述**: 实现 OpenAI Embedding API 的 EmbeddingClient
  - **测试先行步骤**:
    - 编写 mock 测试：验证 API 调用格式
    - 编写集成测试：验证向量输出
    - 定义测试用例：单个文本、批量文本、维度归一化
  - **实现步骤**:
    - 继承 EmbeddingClient
    - 实现 `embed()` 方法
    - 处理批量请求
    - 实现维度归一化
  - **验收标准**:
    - 所有测试通过
    - 支持批量处理
    - 向量维度正确
  - **devspec 参考**: 第 27 行

- [ ] ⏳ **2.2.2 实现本地 Embedding** 🟡 P1
  - **任务描述**: 实现本地 Embedding 模型的 EmbeddingClient
  - **测试先行步骤**:
    - 编写测试：验证本地模型加载和调用
  - **实现步骤**:
    - 继承 EmbeddingClient
    - 实现 `embed()` 方法，调用本地模型
  - **验收标准**:
    - 所有测试通过
  - **devspec 参考**: 第 27 行

#### Module 2.3: Vision LLM 实现

- [ ] ⏳ **2.3.1 实现 AzureOpenAIVision** 🔴 P0
  - **任务描述**: 实现 Azure OpenAI Vision (GPT-4o/GPT-4-Vision) 的 BaseVisionLLM
  - **测试先行步骤**:
    - 编写 mock 测试：验证多模态输入格式
    - 编写集成测试：验证图像+文本输入
    - 定义测试用例：纯文本、图片+文本、多图片
  - **实现步骤**:
    - 继承 BaseVisionLLM
    - 实现 `chat()` 方法，支持 MultimodalMessage 输入
    - 处理图片编码（base64 或 URL）
  - **验收标准**:
    - 所有测试通过
    - 支持复杂图表解析
  - **devspec 参考**: 第 266 行

### ✅ Milestone 2.1 验收标准
- [ ] 至少实现一个 LLM Provider（推荐 Azure OpenAI）
- [ ] 至少实现一个 Embedding Provider（推荐 OpenAI）
- [ ] 实现 Azure OpenAI Vision
- [ ] 所有 Provider 通过单元测试和集成测试
- [ ] 工厂模式能正确创建各 Provider 实例

---

## Phase 3: 向量存储实现

> **依赖分析**：依赖 Phase 1 的 VectorStore 接口定义。

### Milestone 3.1: 向量存储实现

- [ ] ⏳ **3.1.1 实现 MilvusVectorStore** 🔴 P0
  - **任务描述**: 实现 Milvus 向量存储
  - **测试先行步骤**:
    - 编写集成测试：验证连接、插入、查询、删除、upsert
    - 定义测试用例：稠密向量+稀疏向量存储、混合查询
  - **实现步骤**:
    - 继承 VectorStore
    - 实现 `insert()`, `query()`, `delete()`, `upsert()`
    - 实现 All-in-One 策略（向量 + payload 存储）
    - 实现 chunk_id 幂等性设计
  - **验收标准**:
    - 所有测试通过
    - upsert 操作正确（插入或更新）
    - chunk_id 基于 hash(source_path + section_path + content_hash)
  - **devspec 参考**: 第 134 行、第 138 行

- [ ] ⏳ **3.1.2 实现 ChromaVectorStore** 🟡 P1
  - **任务描述**: 实现 Chroma 向量存储
  - **测试先行步骤**:
    - 编写集成测试
  - **实现步骤**:
    - 继承 VectorStore
    - 实现各方法
  - **验收标准**:
    - 所有测试通过
  - **devspec 参考**: 第 38 行

- [ ] ⏳ **3.1.3 实现 QdrantVectorStore** 🟢 P2
  - **任务描述**: 实现 Qdrant 向量存储
  - **测试先行步骤**:
    - 编写集成测试
  - **实现步骤**:
    - 继承 VectorStore
    - 实现各方法
  - **验收标准**:
    - 所有测试通过
  - **devspec 参考**: 第 38 行

- [ ] ⏳ **3.1.4 实现 PineconeVectorStore** 🟢 P2
  - **任务描述**: 实现 Pinecone 向量存储
  - **测试先行步骤**:
    - 编写集成测试
  - **实现步骤**:
    - 继承 VectorStore
    - 实现各方法
  - **验收标准**:
    - 所有测试通过
  - **devspec 参考**: 第 38 行

### ✅ Milestone 3.1 验收标准
- [ ] 至少实现一个 VectorStore（推荐 Milvus）
- [ ] upsert 幂等性正确实现
- [ ] chunk_id 生成算法正确
- [ ] 工厂模式能正确创建各 VectorStore 实例

---

## Phase 4: Reranker 实现

> **依赖分析**：依赖 Phase 1 的 Reranker 接口定义。

### Milestone 4.1: Reranker 实现

- [ ] ⏳ **4.1.1 实现 NoOpReranker** 🔴 P0
  - **任务描述**: 实现空操作 Reranker（直接返回输入）
  - **测试先行步骤**:
    - 编写测试：验证输出与输入相同
  - **实现步骤**:
    - 继承 Reranker
    - 实现 `rerank()` 方法，直接返回输入
  - **验收标准**:
    - 输入输出完全一致
  - **devspec 参考**: 第 166 行

- [ ] ⏳ **4.1.2 实现 CrossEncoderReranker** 🟡 P1
  - **任务描述**: 实现 Cross-Encoder 重排模型
  - **测试先行步骤**:
    - 编写 mock 测试：验证打分和排序
    - 编写集成测试：验证真实模型调用
    - 定义测试用例：正常排序、超时回退
  - **实现步骤**:
    - 继承 Reranker
    - 实现 `rerank()` 方法
    - 集成 cross-encoder 模型
    - 实现超时回退机制
  - **验收标准**:
    - 所有测试通过
    - 超时时回退到输入顺序
  - **devspec 参考**: 第 167 行

- [ ] ⏳ **4.1.3 实现 LLMReranker** 🟢 P2
  - **任务描述**: 实现基于 LLM 的重排
  - **测试先行步骤**:
    - 编写 mock 测试和集成测试
  - **实现步骤**:
    - 继承 Reranker
    - 实现 `rerank()` 方法，调用 LLM
  - **验收标准**:
    - 所有测试通过
  - **devspec 参考**: 第 168 行

### ✅ Milestone 4.1 验收标准
- [ ] NoOpReranker 实现
- [ ] 至少实现一个实际 Reranker（推荐 CrossEncoder）
- [ ] 超时回退机制正确
- [ ] 工厂模式能正确创建各 Reranker 实例

---

## Phase 5: 数据摄取流水线实现

> **依赖分析**：依赖 Phase 1 的 Loader/Splitter/Transform 接口，依赖 Phase 2 的 LLM/Embedding Provider，依赖 Phase 3 的 VectorStore。

### Milestone 5.1: Loader 实现

- [ ] ⏳ **5.1.1 实现文件去重机制** 🔴 P0
  - **任务描述**: 实现前置去重，计算文件 SHA256 哈希，查询 ingestion_history 表
  - **测试先行步骤**:
    - 编写测试：验证哈希计算、查询逻辑
    - 定义测试用例：新文件、已处理文件、内容相同但文件名不同
  - **实现步骤**:
    - 实现 `FileIntegrityCheck` 类
    - 实现 `calculate_file_hash(file_path) -> str`
    - 实现 `should_skip(file_hash) -> bool`
    - 实现 ingestion_history 表（可选用 SQLite）
  - **验收标准**:
    - 哈希计算正确
    - 已处理文件正确跳过
    - 内容相同但文件名不同的文件被识别为重复
  - **devspec 参考**: 第 91 行

- [ ] ⏳ **5.1.2 实现 PDFLoader** 🔴 P0
  - **任务描述**: 使用 markitdown 将 PDF 转换为 Markdown
  - **测试先行步骤**:
    - 编写测试：验证 PDF 解析正确性
    - 定义测试用例：纯文本 PDF、含图片 PDF、多页 PDF
  - **实现步骤**:
    - 继承 Loader
    - 集成 markitdown 库
    - 实现 `load()` 方法
    - 提取 metadata（source_path, doc_type, page, title, images）
  - **验收标准**:
    - 输出 Markdown 格式文本
    - Document 对象包含完整 metadata
    - images 列表包含图片引用
  - **devspec 参考**: 第 96 行、第 99 行

- [ ] ⏳ **5.1.3 实现 MarkdownLoader** 🟡 P1
  - **任务描述**: 实现 Markdown 文档解析器
  - **测试先行步骤**:
    - 编写测试：验证 Markdown 解析
  - **实现步骤**:
    - 继承 Loader
    - 实现 `load()` 方法
  - **验收标准**:
    - 正确解析 Markdown
  - **devspec 参考**: 第 32 行

- [ ] ⏳ **5.1.4 实现 CodeLoader** 🟡 P1
  - **任务描述**: 实现代码文件解析器
  - **测试先行步骤**:
    - 编写测试：验证代码解析
  - **实现步骤**:
    - 继承 Loader
    - 支持多种代码语言
  - **验收标准**:
    - 支持主流代码语言
  - **devspec 参考**: 第 32 行

### Milestone 5.2: Splitter 实现

- [ ] ⏳ **5.2.1 实现 RecursiveCharacterSplitter** 🔴 P0
  - **任务描述**: 使用 LangChain 的 RecursiveCharacterTextSplitter 进行切分
  - **测试先行步骤**:
    - 编写测试：验证切分质量
    - 定义测试用例：长文本、短文本、含代码块、含表格
  - **实现步骤**:
    - 继承 Splitter
    - 集成 LangChain RecursiveCharacterTextSplitter
    - 实现 `split()` 方法
    - 配置语义断点（标题、段落、列表、代码块）
  - **验收标准**:
    - 切分结果语义完整
    - 每个 chunk 包含 source, chunk_index, start_offset/end_offset
  - **devspec 参考**: 第 105 行

- [ ] ⏳ **5.2.2 实现定长切分策略** 🟢 P2
  - **任务描述**: 实现固定长度的切分
  - **测试先行步骤**:
    - 编写测试：验证定长切分
  - **实现步骤**:
    - 继承 Splitter
    - 实现 `split()` 方法
  - **验收标准**:
    - 切分长度符合配置
  - **devspec 参考**: 第 33 行

- [ ] ⏳ **5.2.3 实现语义切分策略** 🟢 P2
  - **任务描述**: 实现基于语义的切分
  - **测试先行步骤**:
    - 编写测试：验证语义切分
  - **实现步骤**:
    - 继承 Splitter
    - 使用 LLM 进行语义边界识别
  - **验收标准**:
    - 切分符合语义边界
  - **devspec 参考**: 第 33 行

### Milestone 5.3: Transform 实现

- [ ] ⏳ **5.3.1 实现智能重组 Transform** 🔴 P0
  - **任务描述**: 利用 LLM 对粗切分的片段进行二次加工
  - **测试先行步骤**:
    - 编写测试：验证重组逻辑
    - 定义测试用例：被切断的段落、含页眉页脚的片段
  - **实现步骤**:
    - 继承 Transform
    - 实现 `transform()` 方法
    - 调用 LLM 合并相关段落、移除噪音
  - **验收标准**:
    - 每个 chunk 是自包含的语义单元
    - 页眉页脚和乱码被移除
  - **devspec 参考**: 第 114 行

- [ ] ⏳ **5.3.2 实现语义元数据注入 Transform** 🔴 P0
  - **任务描述**: 利用 LLM 提取语义特征，生成 title、summary、tags
  - **测试先行步骤**:
    - 编写测试：验证元数据生成质量
    - 定义测试用例：技术文档、新闻文章、代码注释
  - **实现步骤**:
    - 继承 Transform
    - 实现 `transform()` 方法
    - 调用 LLM 生成元数据
    - 将元数据注入 chunk.metadata
  - **验收标准**:
    - title 准确反映 chunk 内容
    - summary 简洁准确
    - tags 相关且有用
  - **devspec 参考**: 第 117 行

- [ ] ⏳ **5.3.3 实现多模态增强 Transform** 🔴 P0
  - **任务描述**: 扫描图像引用，调用 Vision LLM 生成 caption
  - **测试先行步骤**:
    - 编写测试：验证图片处理流程
    - 定义测试用例：含图片的 chunk、多图片 chunk
  - **实现步骤**:
    - 继承 Transform
    - 扫描 chunk 中的 image_refs
    - 调用 Vision LLM 生成 caption
    - 将 caption 缝合到 chunk.text 或 chunk.metadata
  - **验收标准**:
    - 图片被正确识别
    - caption 准确描述图片内容
    - caption 被正确缝合
  - **devspec 参考**: 第 120 行

- [ ] ⏳ **5.3.4 实现 OCR Transform** 🟡 P1
  - **任务描述**: 实现 OCR 文字识别转换
  - **测试先行步骤**:
    - 编写测试：验证 OCR 准确性
  - **实现步骤**:
    - 继承 Transform
    - 集成 OCR 引擎
  - **验收标准**:
    - 能识别图片中的文字
  - **devspec 参考**: 第 34 行

- [ ] ⏳ **5.3.5 实现 HTML 清理 Transform** 🟡 P1
  - **任务描述**: 实现 HTML 标签清理转换
  - **测试先行步骤**:
    - 编写测试：验证 HTML 清理
  - **实现步骤**:
    - 继承 Transform
    - 移除 HTML 标签，保留内容
  - **验收标准**:
    - HTML 标签被正确移除
  - **devspec 参考**: 第 34 行

- [ ] ⏳ **5.3.6 实现原子化与幂等操作** 🟡 P1
  - **任务描述**: 确保 Transform 支持针对特定 chunk 的独立重试与增量更新
  - **测试先行步骤**:
    - 编写测试：验证幂等性
    - 定义测试用例：重复 transform 同一个 chunk、单个 chunk 失败重试
  - **实现步骤**:
    - 在 Transform 基类中实现幂等逻辑
    - 记录 chunk 的 transform 状态
  - **验收标准**:
    - 重复 transform 产生相同结果
    - 单个 chunk 失败不影响其他 chunk
  - **devspec 参考**: 第 124 行

### Milestone 5.4: Embedding 实现

- [ ] ⏳ **5.4.1 实现内容哈希计算** 🔴 P0
  - **任务描述**: 计算 chunk 的内容哈希
  - **测试先行步骤**:
    - 编写测试：验证哈希计算和去重
  - **实现步骤**:
    - 实现 `calculate_content_hash(chunk) -> str`
  - **验收标准**:
    - 相同内容产生相同哈希
    - 不同内容产生不同哈希
  - **devspec 参考**: 第 128 行

- [ ] ⏳ **5.4.2 实现向量复用机制** 🔴 P0
  - **任务描述**: 对内容未变的片段复用已有向量
  - **测试先行步骤**:
    - 编写测试：验证向量复用
  - **实现步骤**:
    - 查询数据库判断内容哈希是否已存在
    - 复用已有向量
  - **验收标准**:
    - 已存在的向量被复用
    - 不重复调用 embedding API
  - **devspec 参考**: 第 128 行

- [ ] ⏳ **5.4.3 实现双路向量化** 🔴 P0
  - **任务描述**: 对每个 chunk 并行执行 dense 和 sparse embedding
  - **测试先行步骤**:
    - 编写测试：验证双路向量和并行执行
  - **实现步骤**:
    - 实现 `dual_embed(chunks) -> Tuple[dense_vectors, sparse_vectors]`
    - 并行调用 dense embedding 和 sparse embedding
  - **验收标准**:
    - dense 和 sparse 向量都正确生成
    - 并行执行提高效率
  - **devspec 参考**: 第 129 行

- [ ] ⏳ **5.4.4 实现批处理优化** 🟡 P1
  - **任务描述**: 优化 embedding API 调用，支持批量处理
  - **测试先行步骤**:
    - 编写测试：验证批处理效率
  - **实现步骤**:
    - 实现 `batch_embed(chunks, batch_size)`
  - **验收标准**:
    - 批处理提高效率
  - **devspec 参考**: 第 132 行

### Milestone 5.5: Upsert & Storage 实现

- [ ] ⏳ **5.5.1 实现 Chunk ID 生成** 🔴 P0
  - **任务描述**: 为每个 chunk 生成全局唯一的 chunk_id
  - **测试先行步骤**:
    - 编写测试：验证 chunk_id 唯一性和稳定性
  - **实现步骤**:
    - 实现 `generate_chunk_id(source_path, section_path, content_hash) -> str`
  - **验收标准**:
    - chunk_id 全局唯一
    - 相同内容产生相同 chunk_id
  - **devspec 参考**: 第 138 行

- [ ] ⏳ **5.5.2 实现 Batch 事务性写入** 🔴 P0
  - **任务描述**: 以 batch 为单位进行事务性写入
  - **测试先行步骤**:
    - 编写测试：验证事务性
    - 定义测试用例：正常写入、部分失败回滚
  - **实现步骤**:
    - 实现 `batch_upsert(chunks, batch_size)`
  - **验收标准**:
    - batch 写入具有原子性
    - 失败的 batch 能够回滚
  - **devspec 参考**: 第 140 行

### Milestone 5.6: Dedup & Normalize 实现

- [ ] ⏳ **5.6.1 实现向量去重** 🟡 P1
  - **任务描述**: 在上载前运行向量去重
  - **测试先行步骤**:
    - 编写测试：验证向量去重
  - **实现步骤**:
    - 检测重复向量
    - 过滤重复向量
  - **验收标准**:
    - 重复向量被正确过滤
  - **devspec 参考**: 第 87 行

- [ ] ⏳ **5.6.2 实现文本去重** 🟡 P1
  - **任务描述**: 在上载前运行文本去重
  - **测试先行步骤**:
    - 编写测试：验证文本去重
  - **实现步骤**:
    - 检测重复文本
    - 过滤重复文本
  - **验收标准**:
    - 重复文本被正确过滤
  - **devspec 参考**: 第 87 行

### ✅ Milestone 5.1 验收标准
- [ ] PDFLoader 正常工作
- [ ] RecursiveCharacterSplitter 正常工作
- [ ] 核心 Transform 实现（智能重组、元数据注入、多模态增强）
- [ ] 双路向量化正常工作
- [ ] Milvus upsert 正常工作
- [ ] 端到端：PDF → Chunks → VectorStore 流程打通
- [ ] 单元测试覆盖率 > 70%

---

## Phase 6: 检索流水线实现

> **依赖分析**：依赖 Phase 5 的数据摄取（向量已存储），依赖 Phase 4 的 Reranker。

### Milestone 6.1: 查询预处理实现

- [ ] ⏳ **6.1.1 实现关键词提取** 🔴 P0
  - **任务描述**: 利用 NLP 工具提取 query 中的关键词
  - **测试先行步骤**:
    - 编写测试：验证关键词提取准确性
    - 定义测试用例：简单查询、含停用词查询、专业术语查询
  - **实现步骤**:
    - 实现 `KeywordExtractor`
    - 实现 `extract(query: str) -> List[str]`
    - 去除停用词
  - **验收标准**:
    - 关键词提取准确
    - 停用词被正确去除
  - **devspec 参考**: 第 147 行

- [ ] ⏳ **6.1.2 实现查询扩展** 🟡 P1
  - **任务描述**: 对查询进行同义词/别名/缩写扩展
  - **测试先行步骤**:
    - 编写测试：验证扩展效果
  - **实现步骤**:
    - 实现 `QueryExpander`
    - 同义词库（可选集成 WordNet 或自定义）
  - **验收标准**:
    - 扩展结果合理
  - **devspec 参考**: 第 148 行

- [ ] ⏳ **6.1.3 实现 Sparse Route 扩展策略** 🟡 P1
  - **任务描述**: 将关键词+扩展词合并，执行一次稀疏检索
  - **测试先行步骤**:
    - 编写测试：验证查询合并和权重
  - **实现步骤**:
    - 实现 `build_sparse_query(keywords, expansions)`
    - 原始关键词赋予更高权重
  - **验收标准**:
    - 查询表达式正确
    - 权重分配合理
  - **devspec 参考**: 第 150 行

- [ ] ⏳ **6.1.4 实现 Dense Route 策略** 🔴 P0
  - **任务描述**: 使用原始 query 进行稠密检索
  - **测试先行步骤**:
    - 编写测试：验证 query 处理
  - **实现步骤**:
    - 实现 `build_dense_query(query: str)`
  - **验收标准**:
    - 只进行一次稠密检索
  - **devspec 参考**: 第 151 行

### Milestone 6.2: 混合检索实现

- [ ] ⏳ **6.2.1 实现稀疏检索** 🔴 P0
  - **任务描述**: 实现 BM25 稀疏检索
  - **测试先行步骤**:
    - 编写测试：验证 BM25 检索结果
  - **实现步骤**:
    - 实现 `SparseRetriever`
    - 实现 `retrieve(query: str, top_k: int) -> List[ScoredChunk]`
    - 集成 BM25 算法
  - **验收标准**:
    - 返回 Top-N 候选及 BM25 分数
    - 关键词匹配准确
  - **devspec 参考**: 第 154 行

- [ ] ⏳ **6.2.2 实现稠密检索** 🔴 P0
  - **任务描述**: 实现语义向量检索
  - **测试先行步骤**:
    - 编写测试：验证向量检索结果
  - **实现步骤**:
    - 实现 `DenseRetriever`
    - 实现 `retrieve(query_vector, top_k: int) -> List[ScoredChunk]`
    - 调用 VectorStore.query()
  - **验收标准**:
    - 返回 Top-N 候选及相似度分数
    - 语义匹配准确
  - **devspec 参考**: 第 154 行

- [ ] ⏳ **6.2.3 实现 RRF 融合算法** 🔴 P0
  - **任务描述**: 采用 RRF 算法融合稀疏和稠密检索结果
  - **测试先行步骤**:
    - 编写测试：验证 RRF 融合结果
    - 定义测试用例：两路结果完全一致、完全不一致、部分重叠
  - **实现步骤**:
    - 实现 `RRFFusion`
    - 实现 `fuse(dense_results, sparse_results, k=60) -> List[ScoredChunk]`
    - 公式：Score = 1/(k+Rank_Dense) + 1/(k+Rank_Sparse)
  - **验收标准**:
    - 融合算法正确
    - 平滑单一模态缺陷
  - **devspec 参考**: 第 154 行

- [ ] ⏳ **6.2.4 实现并行召回** 🟡 P1
  - **任务描述**: 稀疏和稠密检索并行执行
  - **测试先行步骤**:
    - 编写测试：验证并行执行效率
  - **实现步骤**:
    - 使用并发执行（asyncio 或 threading）
  - **验收标准**:
    - 并行执行提高效率
  - **devspec 参考**: 第 154 行

### Milestone 6.3: Filter & Reranking 实现

- [ ] ⏳ **6.3.1 实现 Pre-filter 机制** 🟡 P1
  - **任务描述**: 在检索阶段应用硬约束过滤
  - **测试先行步骤**:
    - 编写测试：验证 pre-filter 效果
  - **实现步骤**:
    - 判断索引是否支持 pre-filter
    - 在检索前应用过滤条件
  - **验收标准**:
    - 硬约束在检索前应用
  - **devspec 参考**: 第 159 行

- [ ] ⏳ **6.3.2 实现 Post-filter 兜底机制** 🟡 P1
  - **任务描述**: 在 rerank 之前应用无法前置的过滤
  - **测试先行步骤**:
    - 编写测试：验证 post-filter 和宽松包含
  - **实现步骤**:
    - 对缺失字段默认宽松包含
  - **验收标准**:
    - 缺失字段时默认宽松包含
    - 避免误杀召回
  - **devspec 参考**: 第 160 行

- [ ] ⏳ **6.3.3 实现软偏好排序信号** 🟢 P2
  - **任务描述**: 软偏好作为排序信号在融合/重排序阶段加权
  - **测试先行步骤**:
    - 编写测试：验证软偏好加权
  - **实现步骤**:
    - 在融合或重排时应用软偏好权重
  - **验收标准**:
    - 软偏好不影响过滤
    - 软偏好在排序时加权
  - **devspec 参考**: 第 161 行

### ✅ Milestone 6.1 验收标准
- [ ] 查询预处理正常工作
- [ ] 混合检索正常工作
- [ ] RRF 融合正确
- [ ] Reranker 正常工作
- [ ] 端到端：Query → Preprocess → Hybrid Retrieve → Rerank 流程打通
- [ ] 单元测试覆盖率 > 70%

---

## Phase 7: 可观测性与追踪实现

> **依赖分析**：可贯穿全链路，但核心功能可在 Phase 6 后实现。

### Milestone 7.1: 追踪数据结构

- [ ] ⏳ **7.1.1 实现 TraceContext** 🔴 P0
  - **任务描述**: 实现追踪上下文对象
  - **测试先行步骤**:
    - 编写测试：验证 TraceContext 功能
    - 定义测试用例：记录各阶段、完成追踪
  - **实现步骤**:
    - 实现 `TraceContext` 类
    - 实现 `__init__(query, collection)` 生成 trace_id
    - 实现 `record_stage(stage_name, data)` 方法
    - 实现 `finish()` 方法序列化并写入日志
  - **验收标准**:
    - trace_id 唯一
    - 各阶段数据正确记录
    - 序列化格式正确
  - **devspec 参考**: 第 369-377 行

### Milestone 7.2: 阶段追踪实现

- [ ] ⏳ **7.2.1 实现 Query Processing 追踪** 🔴 P0
  - **任务描述**: 记录查询处理阶段的数据
  - **测试先行步骤**:
    - 编写测试：验证追踪记录
  - **实现步骤**:
    - 在查询处理完成后调用 `trace.record_stage('query_processing', data)`
  - **验收标准**:
    - 记录原始 Query、改写后 Query、关键词、耗时
  - **devspec 参考**: 第 326 行

- [ ] ⏳ **7.2.2 实现 Dense Retrieval 追踪** 🔴 P0
  - **任务描述**: 记录稠密检索阶段的数据
  - **测试先行步骤**:
    - 编写测试：验证追踪记录
  - **实现步骤**:
    - 在稠密检索完成后调用 `trace.record_stage('dense_retrieval', data)`
  - **验收标准**:
    - 记录 Top-N 候选、分数、耗时
  - **devspec 参考**: 第 327 行

- [ ] ⏳ **7.2.3 实现 Sparse Retrieval 追踪** 🔴 P0
  - **任务描述**: 记录稀疏检索阶段的数据
  - **测试先行步骤**:
    - 编写测试：验证追踪记录
  - **实现步骤**:
    - 在稀疏检索完成后调用 `trace.record_stage('sparse_retrieval', data)`
  - **验收标准**:
    - 记录 Top-N 候选、BM25 分数、耗时
  - **devspec 参考**: 第 328 行

- [ ] ⏳ **7.2.4 实现 Fusion 追踪** 🔴 P0
  - **任务描述**: 记录融合阶段的数据
  - **测试先行步骤**:
    - 编写测试：验证追踪记录
  - **实现步骤**:
    - 在融合完成后调用 `trace.record_stage('fusion', data)`
  - **验收标准**:
    - 记录融合后排名、耗时
  - **devspec 参考**: 第 329 行

- [ ] ⏳ **7.2.5 实现 Rerank 追踪** 🔴 P0
  - **任务描述**: 记录重排阶段的数据
  - **测试先行步骤**:
    - 编写测试：验证追踪记录
  - **实现步骤**:
    - 在重排完成后调用 `trace.record_stage('rerank', data)`
  - **验收标准**:
    - 记录最终排名、分数、Fallback 状态、耗时
  - **devspec 参考**: 第 330 行

### Milestone 7.3: 技术方案实现

- [ ] ⏳ **7.3.1 实现 JSON Formatter** 🔴 P0
  - **任务描述**: 基于 Python logging + JSON Formatter 实现结构化日志
  - **测试先行步骤**:
    - 编写测试：验证日志格式
  - **实现步骤**:
    - 实现 `JSONFormatter`
    - 配置 logging 模块
  - **验收标准**:
    - 日志格式为 JSON
    - 字段完整
  - **devspec 参考**: 第 366 行

- [ ] ⏳ **7.3.2 实现 JSON Lines 日志写入** 🔴 P0
  - **任务描述**: 将 Trace 数据以 JSON Lines 格式追加写入
  - **测试先行步骤**:
    - 编写测试：验证文件写入和格式
  - **实现步骤**:
    - 实现 `TraceLogger`
    - 追加写入 logs/traces.jsonl
  - **验收标准**:
    - 文件格式正确（每行一个 JSON）
    - 追加写入正常
  - **devspec 参考**: 第 366 行

- [ ] ⏳ **7.3.3 集成 Streamlit** 🔴 P0
  - **任务描述**: 使用 Streamlit 构建本地 Web UI
  - **测试先行步骤**:
    - 手动测试：验证 Streamlit 启动
  - **实现步骤**:
    - 安装 streamlit
    - 创建 dashboard/app.py
  - **验收标准**:
    - Streamlit 正确集成
    - 能够启动
  - **devspec 参考**: 第 367 行

- [ ] ⏳ **7.3.4 实现请求列表视图** 🔴 P0
  - **任务描述**: 按时间倒序展示历史请求，支持关键词筛选
  - **测试先行步骤**:
    - 手动测试：验证列表展示和筛选
  - **实现步骤**:
    - 实现 `RequestListView` 组件
    - 读取 traces.jsonl
    - 支持关键词筛选
  - **验收标准**:
    - 请求列表展示正确
    - 时间排序正确
    - 关键词筛选功能正常
  - **devspec 参考**: 第 386 行

- [ ] ⏳ **7.3.5 实现单请求详情页** 🔴 P0
  - **任务描述**: 按 trace_id 展示单次请求的完整追踪链路
  - **测试先行步骤**:
    - 手动测试：验证详情展示
  - **实现步骤**:
    - 实现 `RequestDetailView` 组件
    - 展示各阶段详情
  - **验收标准**:
    - 能够按 trace_id 查询
    - 详情展示完整
  - **devspec 参考**: 第 387 行

- [ ] ⏳ **7.3.6 实现耗时瀑布图** 🟡 P1
  - **任务描述**: 展示各阶段的时间分布
  - **测试先行步骤**:
    - 手动测试：验证瀑布图展示
  - **实现步骤**:
    - 使用 Streamlit/Plotly 绘制瀑布图
  - **验收标准**:
    - 瀑布图展示正确
    - 时间分布准确
  - **devspec 参考**: 第 388 行

- [ ] ⏳ **7.3.7 实现阶段详情展开** 🟡 P1
  - **任务描述**: 点击任意阶段，查看详细输入输出
  - **测试先行步骤**:
    - 手动测试：验证展开功能
  - **实现步骤**:
    - 使用 Streamlit expander
  - **验收标准**:
    - 详情展开功能正常
    - 输入输出展示完整
  - **devspec 参考**: 第 389 行

- [ ] ⏳ **7.3.8 实现召回结果表** 🟡 P1
  - **任务描述**: 展示 Top-K 候选在各阶段的排名与分数变化
  - **测试先行步骤**:
    - 手动测试：验证结果表展示
  - **实现步骤**:
    - 实现 `ResultsTable` 组件
  - **验收标准**:
    - 排名变化展示清晰
    - 分数变化展示准确
  - **devspec 参考**: 第 390 行

### Milestone 7.4: 配置实现

- [ ] ⏳ **7.4.1 实现 observability 配置项** 🔴 P0
  - **任务描述**: 实现可观测性相关配置
  - **测试先行步骤**:
    - 编写测试：验证配置加载
  - **实现步骤**:
    - 在 settings.yaml 中添加 observability 配置
    - 实现配置解析
  - **验收标准**:
    - enabled: true/false
    - logging 配置正确
    - detail_level 可配置：minimal | standard | verbose
    - dashboard 配置正确（enabled、port: 8501）
  - **devspec 参考**: 第 392-408 行

### ✅ Milestone 7.1 验收标准
- [ ] TraceContext 正常工作
- [ ] 所有阶段追踪正常记录
- [ ] JSON Lines 日志正常写入
- [ ] Streamlit Dashboard 正常运行
- [ ] 请求列表和详情页正常展示

---

## Phase 8: MCP 服务实现

> **依赖分析**：依赖 Phase 6 的检索流水线完成。

### Milestone 8.1: 传输协议实现

- [ ] ⏳ **8.1.1 实现 stdio transport** 🔴 P0
  - **任务描述**: 实现 stdio 作为 MCP 传输协议
  - **测试先行步骤**:
    - 编写测试：验证 stdin/stdout 通信
  - **实现步骤**:
    - 使用 Python MCP SDK
    - 配置 stdio transport
  - **验收标准**:
    - 能够通过 stdin/stdout 与 Client 通信
    - 正确实现 JSON-RPC 2.0 协议
  - **devspec 参考**: 第 179-187 行

- [ ] ⏳ **8.1.2 实现日志输出隔离** 🔴 P0
  - **任务描述**: 确保 stdout 仅输出 MCP 消息，日志输出到 stderr
  - **测试先行步骤**:
    - 编写测试：验证输出隔离
  - **实现步骤**:
    - 配置 logging 输出到 stderr
    - 确保无其他输出到 stdout
  - **验收标准**:
    - stdout 无污染
    - 日志正确输出到 stderr
  - **devspec 参考**: 第 186 行

### Milestone 8.2: 核心工具实现

- [ ] ⏳ **8.2.1 实现 query_knowledge_hub 工具** 🔴 P0
  - **任务描述**: 实现主检索入口工具
  - **测试先行步骤**:
    - 编写测试：验证工具调用
    - 定义测试用例：正常查询、指定 top_k、指定 collection
  - **实现步骤**:
    - 实现 `query_knowledge_hub(query, top_k, collection)` 函数
    - 调用检索流水线
    - 返回带引用的结构化结果
  - **验收标准**:
    - 执行完整的检索流程
    - 返回结果符合 MCP 工具规范
  - **devspec 参考**: 第 195-198 行

- [ ] ⏳ **8.2.2 实现 list_collections 工具** 🔴 P0
  - **任务描述**: 实现列举文档集合工具
  - **测试先行步骤**:
    - 编写测试：验证工具调用
  - **实现步骤**:
    - 实现 `list_collections()` 函数
    - 查询 VectorStore 获取集合信息
  - **验收标准**:
    - 返回集合名称、描述、文档数量
  - **devspec 参考**: 第 199 行

- [ ] ⏳ **8.2.3 实现 get_document_summary 工具** 🔴 P0
  - **任务描述**: 实现获取文档摘要工具
  - **测试先行步骤**:
    - 编写测试：验证工具调用
  - **实现步骤**:
    - 实现 `get_document_summary(doc_id)` 函数
    - 从 metadata 中获取摘要信息
  - **验收标准**:
    - 返回标题、摘要、创建时间、标签
  - **devspec 参考**: 第 200 行

### Milestone 8.3: 返回内容与引用透明设计

- [ ] ⏳ **8.3.1 实现 Citation 格式** 🔴 P0
  - **任务描述**: 实现统一的引用格式
  - **测试先行步骤**:
    - 编写测试：验证引用格式
  - **实现步骤**:
    - 定义 `Citation` 数据结构
    - 包含 source_file、page、chunk_id、score
  - **验收标准**:
    - 引用格式统一
    - 包含所有必需字段
  - **devspec 参考**: 第 210-220 行

- [ ] ⏳ **8.3.2 实现 Markdown 格式引用** 🔴 P0
  - **任务描述**: 在返回内容中以 Markdown 格式呈现引用
  - **测试先行步骤**:
    - 编写测试：验证 Markdown 格式
  - **实现步骤**:
    - 实现 `format_with_citations(answer, citations)` 函数
    - 生成 `[1]` 标注的 Markdown
  - **验收标准**:
    - Markdown 格式正确
    - 引用标注清晰
  - **devspec 参考**: 第 221 行

- [ ] ⏳ **8.3.3 实现 TextContent 返回** 🔴 P0
  - **任务描述**: 实现文本内容返回类型
  - **测试先行步骤**:
    - 编写测试：验证 TextContent 格式
  - **实现步骤**:
    - 遵循 MCP Content 规范
    - 返回 Markdown 格式文本
  - **验收标准**:
    - 格式符合 MCP 规范
  - **devspec 参考**: 第 225 行

- [ ] ⏳ **8.3.4 实现 ImageContent 返回** 🔴 P0
  - **任务描述**: 实现图像内容返回
  - **测试先行步骤**:
    - 编写测试：验证 ImageContent 格式
  - **实现步骤**:
    - 读取本地图片
    - Base64 编码
    - 返回 `{type: "image", data: "<base64>", mimeType: "image/png"}`
  - **验收标准**:
    - Base64 编码正确
    - 格式符合 MCP 规范
  - **devspec 参考**: 第 226-229 行

### Milestone 8.4: 扩展工具实现

- [ ] ⏳ **8.4.1 实现 search_by_keyword 工具** 🟢 P2
  - **任务描述**: 实现独立的关键词检索工具
  - **测试先行步骤**:
    - 编写测试：验证工具调用
  - **实现步骤**:
    - 实现 `search_by_keyword(query, top_k)` 函数
    - 仅调用稀疏检索
  - **验收标准**:
    - 返回关键词检索结果
  - **devspec 参考**: 第 203 行

- [ ] ⏳ **8.4.2 实现 search_by_semantic 工具** 🟢 P2
  - **任务描述**: 实现独立的语义检索工具
  - **测试先行步骤**:
    - 编写测试：验证工具调用
  - **实现步骤**:
    - 实现 `search_by_semantic(query, top_k)` 函数
    - 仅调用稠密检索
  - **验收标准**:
    - 返回语义检索结果
  - **devspec 参考**: 第 203 行

- [ ] ⏳ **8.4.3 实现 verify_answer 工具** 🟢 P2
  - **任务描述**: 实现事实核查工具
  - **测试先行步骤**:
    - 编写测试：验证核查逻辑
  - **实现步骤**:
    - 实现 `verify_answer(answer, retrieved_chunks)` 函数
  - **验收标准**:
    - 返回核查结果
  - **devspec 参考**: 第 204 行

- [ ] ⏳ **8.4.4 实现 list_document_sections 工具** 🟢 P2
  - **任务描述**: 实现浏览文档目录工具
  - **测试先行步骤**:
    - 编写测试：验证目录浏览
  - **实现步骤**:
    - 实现 `list_document_sections(doc_id)` 函数
  - **验收标准**:
    - 支持多级浏览
  - **devspec 参考**: 第 205 行

### ✅ Milestone 8.1 验收标准
- [ ] stdio transport 正常工作
- [ ] 核心工具正常工作
- [ ] 引用格式正确
- [ ] 多模态内容返回正常
- [ ] 能够与 MCP Client（如 Claude Desktop）通信

---

## Phase 9: 多模态图片处理实现

> **依赖分析**：依赖 Phase 5 的 Transform 和 Phase 7 的 MCP 服务。

### Milestone 9.1: 图片提取与引用收集

- [ ] ⏳ **9.1.1 在 PDFLoader 中实现图片提取** 🔴 P0
  - **任务描述**: 从 PDF 中提取嵌入图片
  - **测试先行步骤**:
    - 编写测试：验证图片提取
  - **实现步骤**:
    - 在 PDFLoader 中添加图片提取逻辑
    - 为每张图片生成唯一 image_id
    - 插入图片占位符
  - **验收标准**:
    - 图片被正确提取
    - image_id 唯一
    - 占位符正确插入
  - **devspec 参考**: 第 425-436 行

### Milestone 9.2: 图文关联保持

- [ ] ⏳ **9.2.1 在 Splitter 中保留图片引用** 🔴 P0
  - **任务描述**: 切分时保留图片引用标记
  - **测试先行步骤**:
    - 编写测试：验证引用保留
  - **实现步骤**:
    - 在 Splitter 中保留 image_refs
  - **验收标准**:
    - 切分后引用不丢失
  - **devspec 参考**: 第 440-444 行

### Milestone 9.3: 多模态理解与向量化

- [ ] ⏳ **9.3.1 实现 CLIP 风格多模态向量** 🔴 P0
  - **任务描述**: 使用多模态模型联合编码图像与上下文
  - **测试先行步骤**:
    - 编写测试：验证向量生成
  - **实现步骤**:
    - 集成多模态模型（如 CLIP）
    - 生成图像语义向量
  - **验收标准**:
    - 向量维度正确
    - 支持图文跨模态检索
  - **devspec 参考**: 第 418 行、第 448-452 行

### Milestone 9.4: 双轨存储

- [ ] ⏳ **9.4.1 在 Milvus 中存储图像向量** 🔴 P0
  - **任务描述**: 在向量库中存储图像向量
  - **测试先行步骤**:
    - 编写测试：验证图像向量存储和检索
  - **实现步骤**:
    - 扩展 VectorStore 支持图像向量
  - **验收标准**:
    - 图像向量正确存储
    - 可用于检索
  - **devspec 参考**: 第 456-459 行

- [ ] ⏳ **9.4.2 实现文件系统图片存储** 🔴 P0
  - **任务描述**: 存储原始图片到文件系统
  - **测试先行步骤**:
    - 编写测试：验证图片存储和读取
  - **实现步骤**:
    - 实现图片存储服务
  - **验收标准**:
    - 原始图片正确存储
    - 可按 ID 检索
  - **devspec 参考**: 第 456-459 行

### Milestone 9.5: 图文联合检索与返回

- [ ] ⏳ **9.5.1 实现混合检索图片支持** 🔴 P0
  - **任务描述**: 检索命中含图片的 Chunk
  - **测试先行步骤**:
    - 编写测试：验证图片检索
  - **实现步骤**:
    - 检索时识别图片引用
  - **验收标准**:
    - 能够检索含图片的 Chunk
  - **devspec 参考**: 第 463-468 行

- [ ] ⏳ **9.5.2 实现多模态内容返回** 🔴 P0
  - **任务描述**: 返回 TextContent + ImageContent
  - **测试先行步骤**:
    - 编写测试：验证多模态返回
  - **实现步骤**:
    - 在 MCP 工具中识别图片引用
    - 读取原图并编码
    - 返回 ImageContent
  - **验收标准**:
    - 图片正确返回
    - 格式符合 MCP 规范
  - **devspec 参考**: 第 463-468 行

### ✅ Milestone 9.1 验收标准
- [ ] 图片被正确提取和存储
- [ ] 图像向量正确生成和存储
- [ ] 支持图文跨模态检索
- [ ] MCP 工具能返回图片

---

## Phase 10: 评估框架实现

> **依赖分析**：依赖 Phase 1 的 Evaluator 接口定义。

### Milestone 10.1: Evaluator 实现

- [ ] ⏳ **10.1.1 实现 RagasEvaluator** 🟡 P1
  - **任务描述**: 实现 Ragas 评估框架集成
  - **测试先行步骤**:
    - 编写测试：验证 Ragas 指标计算
  - **实现步骤**:
    - 继承 Evaluator
    - 集成 Ragas 框架
    - 实现 `evaluate()` 方法
  - **验收标准**:
    - 支持 Faithfulness、Answer Relevancy、Context Precision 等指标
  - **devspec 参考**: 第 280 行

- [ ] ⏳ **10.1.2 实现 DeepEvalEvaluator** 🟡 P1
  - **任务描述**: 实现 DeepEval 评估框架集成
  - **测试先行步骤**:
    - 编写测试：验证 DeepEval 指标计算
  - **实现步骤**:
    - 继承 Evaluator
    - 集成 DeepEval 框架
    - 实现 `evaluate()` 方法
  - **验收标准**:
    - 支持 LLM-as-Judge 模式
    - 支持自定义评估标准
  - **devspec 参考**: 第 281 行

- [ ] ⏳ **10.1.3 实现 CustomMetricsEvaluator** 🟡 P1
  - **任务描述**: 实现自定义指标评估器
  - **测试先行步骤**:
    - 编写测试：验证指标计算
  - **实现步骤**:
    - 继承 Evaluator
    - 实现 Hit Rate、MRR、Latency P99 等指标
  - **验收标准**:
    - 指标计算正确
  - **devspec 参考**: 第 282 行

- [ ] ⏳ **10.1.4 实现组合执行** 🟡 P1
  - **任务描述**: 支持同时挂载多个 Evaluator
  - **测试先行步骤**:
    - 编写测试：验证组合执行
  - **实现步骤**:
    - 实现 `CompositeEvaluator`
    - 并行执行多个 Evaluator
  - **验收标准**:
    - 能够并行执行
    - 能够汇总结果
  - **devspec 参考**: 第 284-286 行

- [ ] ⏳ **10.1.5 实现评估指标追踪** 🟢 P2
  - **任务描述**: 在 Trace 中记录评估指标
  - **测试先行步骤**:
    - 编写测试：验证指标记录
  - **实现步骤**:
    - 在检索流水线中集成评估
    - 记录 context_relevance 和 answer_faithfulness
  - **验收标准**:
    - 指标正确记录到 Trace
  - **devspec 参考**: 第 337-340 行

### ✅ Milestone 10.1 验收标准
- [ ] 至少实现一个 Evaluator
- [ ] 评估框架可配置切换
- [ ] 评估指标正确记录

---

## 附录：DevSpec TODO 调研任务

> 以下为 `devspec.md` 中标注的 #TODO 项目，作为独立的调研/验证任务

### T1. 上下文感知调研
- [ ] ⏳ **调研为什么需要感知上下文** 🔴 P0
  - **任务描述**: devspec.md 第 8 行提到需要感知上下文，调研其必要性
  - **测试先行步骤**: N/A（调研任务）
  - **实现步骤**:
    - 阅读相关论文和文档
    - 理解上下文增强的价值
  - **验收标准**:
    - 能够解释为什么需要感知上下文
    - 输出调研报告
  - **devspec 参考**: 第 8 行

### T2. RRF 算法调研
- [ ] ⏳ **调研为什么 RRF 能保证查全率和查准率** 🔴 P0
  - **任务描述**: devspec.md 第 14 行提到 RRF，调研其原理
  - **测试先行步骤**: N/A（调研任务）
  - **实现步骤**:
    - 研究 RRF 算法原理
    - 理解排名融合的数学基础
  - **验收标准**:
    - 能够解释 RRF 如何平衡查全率和查准率
    - 输出调研报告
  - **devspec 参考**: 第 14 行

### T3. Azure OpenAI 调研
- [ ] ⏳ **调研 Azure OpenAI 是什么** 🟡 P1
  - **任务描述**: devspec.md 第 21 行提到 Azure OpenAI，调研其特点
  - **测试先行步骤**: N/A（调研任务）
  - **实现步骤**:
    - 研究 Azure OpenAI 与原生 OpenAI API 的区别
    - 了解企业级部署的优势
  - **验收标准**:
    - 理解 Azure OpenAI 的特点
    - 输出调研报告
  - **devspec 参考**: 第 21 行

### T4. Chunk ID 生成策略调研
- [ ] ⏳ **调研为什么要用 source_path + section_path + content_hash 组合生成 chunk_id** 🔴 P0
  - **任务描述**: devspec.md 第 138 行提到 chunk_id 生成算法，调研其设计理由
  - **测试先行步骤**: N/A（调研任务）
  - **实现步骤**:
    - 分析每个字段的作用
    - 理解组合策略的原理
  - **验收标准**:
    - 能够解释为什么这样组合能确保幂等性
    - 输出调研报告
  - **devspec 参考**: 第 138 行

### T5. 软硬偏好调研
- [ ] ⏳ **调研软偏好和硬偏好的区别** 🟡 P1
  - **任务描述**: devspec.md 第 162 行提到软偏好/硬偏好，调研其概念
  - **测试先行步骤**: N/A（调研任务）
  - **实现步骤**:
    - 理解软偏好和硬偏好的概念
    - 研究应用场景
  - **验收标准**:
    - 能够解释两者的区别
    - 能够举例说明应用场景
    - 输出调研报告
  - **devspec 参考**: 第 162 行

### T6. 数据追踪设计补充
- [ ] ⏳ **完善数据追踪设计** 🔴 P0
  - **任务描述**: devspec.md 第 319 行提到 #TODO:数据追踪，需要补充详细设计
  - **测试先行步骤**:
    - 编写测试：验证追踪数据结构
  - **实现步骤**:
    - 补充完整的追踪数据结构设计
    - 定义所有需要追踪的字段
  - **验收标准**:
    - 数据追踪设计完整
    - 覆盖所有关键阶段
  - **devspec 参考**: 第 319 行

---

**文档生成时间**: 2026-02-24
**依据文档**: devspec.md
**开发模式**: TDD (测试驱动开发)
