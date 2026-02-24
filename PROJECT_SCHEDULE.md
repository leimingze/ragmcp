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

  - **TDD Cycle**:
    **Test 1: 抽象类无法直接实例化**
    - **RED**:
      - 编写 `test_cannot_instantiate_abstract_llm_client_directly()`
      - 断言: 尝试实例化 LLMClient 应抛出 TypeError
    - **Verify RED**: 运行测试，确认因 LLMClient 不存在而失败
    - **GREEN**: 定义抽象类 LLMClient 和抽象方法 chat()
    - **Verify GREEN**: 运行测试确认通过

    **Test 2: 子类必须实现 chat() 方法**
    - **RED**:
      - 编写 `test_subclass_without_chat_method_raises_error()`
      - 断言: 未实现 chat() 的子类实例化时抛出 TypeError
    - **Verify RED**: 运行测试确认失败
    - **GREEN**: 保持抽象类定义不变
    - **Verify GREEN**: 运行测试确认通过

    **Test 3: 实现了 chat() 的子类可实例化**
    - **RED**:
      - 编写 `test_subclass_with_chat_method_can_be_instantiated()`
      - 创建 MockLLMClient 实现 chat() 方法
      - 断言: 实例化成功，chat() 方法可调用
    - **Verify RED**: 运行测试确认失败
    - **GREEN**: 确保 LLMClient 抽象类设计正确
    - **Verify GREEN**: 运行测试确认通过

    **Test 4: Message 和 Response 数据结构**
    - **RED**:
      - 编写 `test_message_and_response_dataclass_structure()`
      - 断言: Message 有 role 和 content 字段，Response 有 content 字段
    - **Verify RED**: 运行测试确认失败
    - **GREEN**: 定义 Message 和 Response 数据类
    - **Verify GREEN**: 运行测试确认通过

  - **验收标准**:
    - [x] 每个测试都先失败（RED），观察失败原因正确
    - [x] 最小代码实现后所有测试通过（GREEN）
    - [x] 抽象类定义正确，无法直接实例化
    - [x] 数据结构包含必需字段
    - [x] 测试输出无警告/错误
  - **devspec 参考**: 第 262 行

- [x] ✅ **1.1.2 定义 EmbeddingClient 抽象接口** 🔴 P0
  - **任务描述**: 定义向量嵌入的统一抽象接口，统一处理批量请求与维度归一化

  - **TDD Cycle**:
    **Test 1: 抽象类无法直接实例化**
    - **RED**:
      - 编写 `test_cannot_instantiate_abstract_embedding_client()`
      - 断言: 尝试实例化 EmbeddingClient 应抛出 TypeError
    - **Verify RED**: 运行测试，确认因类不存在而失败
    - **GREEN**: 定义抽象类 EmbeddingClient 和抽象方法 embed()
    - **Verify GREEN**: 运行测试确认通过

    **Test 2: 子类必须实现 embed() 方法**
    - **RED**:
      - 编写 `test_subclass_without_embed_raises_error()`
      - 断言: 未实现 embed() 的子类实例化时抛出 TypeError
    - **Verify RED**: 运行测试确认失败
    - **GREEN**: 保持抽象类定义
    - **Verify GREEN**: 运行测试确认通过

    **Test 3: embed() 接受批量文本并返回向量列表**
    - **RED**:
      - 编写 `test_embed_accepts_batch_and_returns_vectors()`
      - 创建 MockEmbeddingClient 返回固定向量
      - 断言: 输入 ["text1", "text2"] 返回长度为 2 的列表
      - 断言: 每个元素是 numpy.ndarray 类型
    - **Verify RED**: 运行测试确认失败
    - **GREEN**: 确保 embed() 方法签名正确
    - **Verify GREEN**: 运行测试确认通过

    **Test 4: 向量归一化**
    - **RED**:
      - 编写 `test_vectors_are_l2_normalized()`
      - 断言: 返回的向量 L2 范数约等于 1.0
    - **Verify RED**: 运行测试确认失败
    - **GREEN**: 在基类中实现归一化逻辑或要求子类实现
    - **Verify GREEN**: 运行测试确认通过

  - **验收标准**:
    - [x] 每个测试都先失败，观察失败原因正确
    - [x] 批量处理接口设计合理
    - [x] 向量归一化逻辑正确
    - [x] 测试输出无警告/错误
  - **devspec 参考**: 第 263 行

- [x] ✅ **1.1.3 定义 BaseVisionLLM 抽象接口** 🔴 P0
  - **任务描述**: 定义多模态 LLM 接口，支持文本+图片的多模态输入

  - **TDD Cycle**:
    **Test 1: BaseVisionLLM 继承自 LLMClient**
    - **RED**:
      - 编写 `test_base_vision_llm_is_llm_client_subclass()`
      - 断言: BaseVisionLLM 是 LLMClient 的子类
    - **Verify RED**: 运行测试，确认因类不存在而失败
    - **GREEN**: 定义 BaseVisionLLM 继承 LLMClient
    - **Verify GREEN**: 运行测试确认通过

    **Test 2: MultimodalMessage 数据结构**
    - **RED**:
      - 编写 `test_multimodal_message_structure()`
      - 断言: MultimodalMessage 包含 text 和 images 字段
      - 断言: images 是列表类型
    - **Verify RED**: 运行测试确认失败
    - **GREEN**: 定义 MultimodalMessage 数据类
    - **Verify GREEN**: 运行测试确认通过

    **Test 3: chat() 接受 MultimodalMessage**
    - **RED**:
      - 编写 `test_chat_accepts_multimodal_message()`
      - 创建 MockVisionLLM 接收 MultimodalMessage
      - 断言: 可传入包含图片的消息
    - **Verify RED**: 运行测试确认失败
    - **GREEN**: 确保 chat() 方法支持多模态输入
    - **Verify GREEN**: 运行测试确认通过

  - **验收标准**:
    - [x] 每个测试都先失败，观察失败原因正确
    - [x] 接口支持文本和图片混合输入
    - [x] 数据结构清晰
    - [x] 测试输出无警告/错误
  - **devspec 参考**: 第 265 行

#### Module 1.2: 向量存储接口定义

- [x] ✅ **1.2.1 定义 VectorStore 抽象接口** 🔴 P0
  - **任务描述**: 定义向量存储的统一接口，支持插入、查询、删除操作

  - **TDD Cycle**:
    **Test 1: 抽象类定义**
    - **RED**:
      - 编写 `test_cannot_instantiate_abstract_vector_store()`
      - 断言: 尝试实例化 VectorStore 应抛出 TypeError
    - **Verify RED**: 运行测试，确认因类不存在而失败
    - **GREEN**: 定义抽象类 VectorStore
    - **Verify GREEN**: 运行测试确认通过

    **Test 2: insert() 方法签名**
    - **RED**:
      - 编写 `test_vector_store_has_insert_method()`
      - 断言: 子类必须实现 insert() 方法
    - **Verify RED**: 运行测试确认失败
    - **GREEN**: 定义抽象方法 insert(vectors, payloads)
    - **Verify GREEN**: 运行测试确认通过

    **Test 3: query() 方法签名**
    - **RED**:
      - 编写 `test_vector_store_has_query_method()`
      - 断言: 子类必须实现 query() 方法
    - **Verify RED**: 运行测试确认失败
    - **GREEN**: 定义抽象方法 query(query_vector, top_k)
    - **Verify GREEN**: 运行测试确认通过

    **Test 4: delete() 和 upsert() 方法**
    - **RED**:
      - 编写 `test_vector_store_has_delete_and_upsert_methods()`
      - 断言: 子类必须实现 delete() 和 upsert() 方法
    - **Verify RED**: 运行测试确认失败
    - **GREEN**: 定义抽象方法 delete() 和 upsert()
    - **Verify GREEN**: 运行测试确认通过

  - **验收标准**:
    - [x] 每个测试都先失败，观察失败原因正确
    - [x] 接口包含所有必需方法
    - [x] upsert 语义明确（插入或更新）
    - [x] 测试输出无警告/错误
  - **devspec 参考**: 第 269 行（检索策略抽象）

#### Module 1.3: Rerank 接口定义

- [x] ✅ **1.3.1 定义 Reranker 抽象接口** 🔴 P0
  - **任务描述**: 定义重排器的统一接口，支持对候选文档集进行相关性排序

  - **TDD Cycle**:
    **Test 1: 抽象类定义**
    - **RED**:
      - 编写 `test_cannot_instantiate_abstract_reranker()`
      - 断言: 尝试实例化 Reranker 应抛出 TypeError
    - **Verify RED**: 运行测试，确认因类不存在而失败
    - **GREEN**: 定义抽象类 Reranker
    - **Verify GREEN**: 运行测试确认通过

    **Test 2: rerank() 方法签名**
    - **RED**:
      - 编写 `test_reranker_has_rerank_method()`
      - 断言: 子类必须实现 rerank(query, chunks) 方法
    - **Verify RED**: 运行测试确认失败
    - **GREEN**: 定义抽象方法 rerank(query, chunks) -> List[RankedChunk]
    - **Verify GREEN**: 运行测试确认通过

    **Test 3: RankedChunk 数据结构**
    - **RED**:
      - 编写 `test_ranked_chunk_structure()`
      - 断言: RankedChunk 包含 chunk 和 score 字段
    - **Verify RED**: 运行测试确认失败
    - **GREEN**: 定义 RankedChunk 数据类
    - **Verify GREEN**: 运行测试确认通过

  - **验收标准**:
    - [x] 每个测试都先失败，观察失败原因正确
    - [x] 接口定义清晰
    - [x] 输入输出格式明确
    - [x] 测试输出无警告/错误
  - **devspec 参考**: 第 164 行

#### Module 1.4: 评估框架接口定义

- [x] ✅ **1.4.1 定义 Evaluator 抽象接口** 🔴 P0
  - **任务描述**: 定义评估器的统一接口，输出标准化的指标字典

  - **TDD Cycle**:
    **Test 1: 抽象类定义**
    - **RED**:
      - 编写 `test_cannot_instantiate_abstract_evaluator()`
      - 断言: 尝试实例化 Evaluator 应抛出 TypeError
    - **Verify RED**: 运行测试，确认因类不存在而失败
    - **GREEN**: 定义抽象类 Evaluator
    - **Verify GREEN**: 运行测试确认通过

    **Test 2: evaluate() 方法签名**
    - **RED**:
      - 编写 `test_evaluator_has_evaluate_method()`
      - 断言: 子类必须实现 evaluate() 方法
    - **Verify RED**: 运行测试确认失败
    - **GREEN**: 定义抽象方法 evaluate(query, retrieved_chunks, generated_answer, ground_truth) -> Dict[str, float]
    - **Verify GREEN**: 运行测试确认通过

    **Test 3: 返回值格式**
    - **RED**:
      - 编写 `test_evaluate_returns_metrics_dict()`
      - 创建 MockEvaluator 返回 {"precision": 0.5}
      - 断言: 返回值是 dict 类型，键为 str，值为 float
    - **Verify RED**: 运行测试确认失败
    - **GREEN**: 确保方法签名正确
    - **Verify GREEN**: 运行测试确认通过

  - **验收标准**:
    - [x] 每个测试都先失败，观察失败原因正确
    - [x] 接口定义清晰
    - [x] 返回值为标准化的指标字典
    - [x] 测试输出无警告/错误
  - **devspec 参考**: 第 274 行

#### Module 1.5: RAG Pipeline 组件接口定义

- [x] ✅ **1.5.1 定义 Loader 抽象接口** 🔴 P0
  - **任务描述**: 定义文档解析器的统一接口

  - **TDD Cycle**:
    **Test 1: 抽象类定义**
    - **RED**:
      - 编写 `test_cannot_instantiate_abstract_loader()`
      - 断言: 尝试实例化 Loader 应抛出 TypeError
    - **Verify RED**: 运行测试，确认因类不存在而失败
    - **GREEN**: 定义抽象类 Loader
    - **Verify GREEN**: 运行测试确认通过

    **Test 2: load() 方法签名**
    - **RED**:
      - 编写 `test_loader_has_load_method()`
      - 断言: 子类必须实现 load(file_path) 方法
    - **Verify RED**: 运行测试确认失败
    - **GREEN**: 定义抽象方法 load(file_path: str) -> Document
    - **Verify GREEN**: 运行测试确认通过

    **Test 3: Document 数据结构**
    - **RED**:
      - 编写 `test_document_has_text_and_metadata()`
      - 断言: Document 包含 text (str) 和 metadata (dict) 字段
    - **Verify RED**: 运行测试确认失败
    - **GREEN**: 定义 Document 数据类
    - **Verify GREEN**: 运行测试确认通过

  - **验收标准**:
    - [x] 每个测试都先失败，观察失败原因正确
    - [x] 接口支持多种文档格式扩展
    - [x] Document 包含 text 和 metadata 字段
    - [x] 测试输出无警告/错误
  - **devspec 参考**: 第 76 行

- [x] ✅ **1.5.2 定义 Splitter 抽象接口** 🔴 P0
  - **任务描述**: 定义文档切分器的统一接口

  - **TDD Cycle**:
    **Test 1: 抽象类定义**
    - **RED**:
      - 编写 `test_cannot_instantiate_abstract_splitter()`
      - 断言: 尝试实例化 Splitter 应抛出 TypeError
    - **Verify RED**: 运行测试，确认因类不存在而失败
    - **GREEN**: 定义抽象类 Splitter
    - **Verify GREEN**: 运行测试确认通过

    **Test 2: split() 方法签名**
    - **RED**:
      - 编写 `test_splitter_has_split_method()`
      - 断言: 子类必须实现 split(document) 方法
    - **Verify RED**: 运行测试确认失败
    - **GREEN**: 定义抽象方法 split(document: Document) -> List[Chunk]
    - **Verify GREEN**: 运行测试确认通过

    **Test 3: Chunk 数据结构**
    - **RED**:
      - 编写 `test_chunk_has_required_fields()`
      - 断言: Chunk 包含 text, source, chunk_index, start_offset, end_offset 字段
    - **Verify RED**: 运行测试确认失败
    - **GREEN**: 定义 Chunk 数据类
    - **Verify GREEN**: 运行测试确认通过

  - **验收标准**:
    - [x] 每个测试都先失败，观察失败原因正确
    - [x] 接口支持多种切分策略
    - [x] Chunk 包含定位信息
    - [x] 测试输出无警告/错误
  - **devspec 参考**: 第 104 行

- [x] ✅ **1.5.3 定义 Transform 抽象接口** 🔴 P0
  - **任务描述**: 定义内容转换模块的统一接口

  - **TDD Cycle**:
    **Test 1: 抽象类定义**
    - **RED**:
      - 编写 `test_cannot_instantiate_abstract_transform()`
      - 断言: 尝试实例化 Transform 应抛出 TypeError
    - **Verify RED**: 运行测试，确认因类不存在而失败
    - **GREEN**: 定义抽象类 Transform
    - **Verify GREEN**: 运行测试确认通过

    **Test 2: transform() 方法签名**
    - **RED**:
      - 编写 `test_transform_has_transform_method()`
      - 断言: 子类必须实现 transform(chunk) 方法
    - **Verify RED**: 运行测试确认失败
    - **GREEN**: 定义抽象方法 transform(chunk: Chunk) -> Chunk
    - **Verify GREEN**: 运行测试确认通过

    **Test 3: transform 返回增强后的 Chunk**
    - **RED**:
      - 编写 `test_transform_returns_enhanced_chunk()`
      - 创建 MockTransform 添加额外 metadata
      - 断言: 返回的 Chunk 包含增强信息
    - **Verify RED**: 运行测试确认失败
    - **GREEN**: 确保方法签名正确
    - **Verify GREEN**: 运行测试确认通过

  - **验收标准**:
    - [x] 每个测试都先失败，观察失败原因正确
    - [x] 接口支持多种转换模块（OCR、ImageCaption、HTML 清理等）
    - [x] 测试输出无警告/错误
  - **devspec 参考**: 第 110 行

#### Module 1.6: 工厂模式接口定义

- [x] ✅ **1.6.1 定义 LLMFactory** 🔴 P0
  - **任务描述**: 实现 LLM 工厂，根据配置动态创建 Provider 实例

  - **TDD Cycle**:
    **Test 1: azure 配置返回 AzureOpenAILLM**
    - **RED**:
      - 编写 `test_azure_config_returns_azure_openai_llm()`
      - 断言: LLMFactory.get_llm({"provider": "azure", ...}) 返回 AzureOpenAILLM 实例
    - **Verify RED**: 运行测试，确认因 LLMFactory 不存在而失败
    - **GREEN**: 实现 LLMFactory.get_llm() 方法
    - **Verify GREEN**: 运行测试确认通过

    **Test 2: openai 配置返回 OpenAILLM**
    - **RED**:
      - 编写 `test_openai_config_returns_openai_llm()`
      - 断言: 配置 provider="openai" 返回 OpenAILLM 实例
    - **Verify RED**: 运行测试确认失败
    - **GREEN**: 扩展工厂方法支持 openai
    - **Verify GREEN**: 运行测试确认通过

    **Test 3: 未知配置抛出异常**
    - **RED**:
      - 编写 `test_unknown_provider_raises_error()`
      - 断言: 未知 provider 抛出 ValueError
    - **Verify RED**: 运行测试确认失败
    - **GREEN**: 添加错误处理
    - **Verify GREEN**: 运行测试确认通过

  - **验收标准**:
    - [x] 每个测试都先失败，观察失败原因正确
    - [x] 根据配置返回正确的 Provider 实例
    - [x] 配置格式清晰
    - [x] 测试输出无警告/错误
  - **devspec 参考**: 第 289 行（配置示例）

- [x] ✅ **1.6.2 定义 EmbeddingFactory** 🔴 P0
  - **任务描述**: 实现 Embedding 工厂，根据配置动态创建 Provider 实例

  - **TDD Cycle**:
    **Test 1: openai 配置返回 OpenAIEmbedding**
    - **RED**:
      - 编写 `test_openai_config_returns_openai_embedding()`
      - 断言: EmbeddingFactory.get_embedding({"provider": "openai"}) 返回 OpenAIEmbedding
    - **Verify RED**: 运行测试，确认因类不存在而失败
    - **GREEN**: 实现 EmbeddingFactory.get_embedding()
    - **Verify GREEN**: 运行测试确认通过

  - **验收标准**:
    - [x] 每个测试都先失败，观察失败原因正确
    - [x] 根据配置返回正确的实例
    - [x] 测试输出无警告/错误
  - **devspec 参考**: 第 295 行

- [x] ✅ **1.6.3 定义 VisionLLMFactory** 🔴 P0
  - **任务描述**: 实现 Vision LLM 工厂

  - **TDD Cycle**:
    **Test 1: 返回 BaseVisionLLM 实例**
    - **RED**:
      - 编写 `test_vision_factory_returns_vision_llm()`
      - 断言: VisionLLMFactory.get_vision_llm() 返回 BaseVisionLLM 子类实例
    - **Verify RED**: 运行测试，确认因类不存在而失败
    - **GREEN**: 实现 VisionLLMFactory.get_vision_llm()
    - **Verify GREEN**: 运行测试确认通过

  - **验收标准**:
    - [x] 每个测试都先失败，观察失败原因正确
    - [x] 根据配置返回正确的实例
    - [x] 测试输出无警告/错误
  - **devspec 参考**: 第 265 行

- [x] ✅ **1.6.4 定义 VectorStoreFactory** 🔴 P0
  - **任务描述**: 实现向量存储工厂

  - **TDD Cycle**:
    **Test 1: milvus 配置返回 MilvusVectorStore**
    - **RED**:
      - 编写 `test_milvus_config_returns_milvus_store()`
      - 断言: VectorStoreFactory.get_vector_store({"backend": "milvus"}) 返回 MilvusVectorStore
    - **Verify RED**: 运行测试，确认因类不存在而失败
    - **GREEN**: 实现 VectorStoreFactory.get_vector_store()
    - **Verify GREEN**: 运行测试确认通过

  - **验收标准**:
    - [x] 每个测试都先失败，观察失败原因正确
    - [x] 根据配置返回正确的实例
    - [x] 测试输出无警告/错误
  - **devspec 参考**: 第 299 行

- [ ] ⏳ **1.6.5 定义 RerankerFactory** 🔴 P0
  - **任务描述**: 实现 Reranker 工厂

  - **TDD Cycle**:
    **Test 1: none 配置返回 NoOpReranker**
    - **RED**:
      - 编写 `test_none_config_returns_noop_reranker()`
      - 断言: RerankerFactory.get_reranker({"backend": "none"}) 返回 NoOpReranker
    - **Verify RED**: 运行测试，确认因类不存在而失败
    - **GREEN**: 实现 RerankerFactory.get_reranker()
    - **Verify GREEN**: 运行测试确认通过

  - **验收标准**:
    - [ ] 每个测试都先失败，观察失败原因正确
    - [ ] 根据配置返回正确的实例
    - [ ] none 时返回 NoOpReranker
    - [ ] 测试输出无警告/错误
  - **devspec 参考**: 第 305 行

#### Module 1.7: 配置管理实现

- [ ] ⏳ **1.7.1 实现 settings.yaml 配置文件** 🔴 P0
  - **任务描述**: 定义统一的配置文件格式

  - **TDD Cycle**:
    **Test 1: 配置文件可被解析**
    - **RED**:
      - 编写 `test_settings_yaml_is_valid_yaml()`
      - 断言: config/settings.yaml 可被 YAML 解析器解析
    - **Verify RED**: 运行测试，确认因文件不存在或格式错误而失败
    - **GREEN**: 创建 config/settings.yaml 定义配置结构
    - **Verify GREEN**: 运行测试确认通过

    **Test 2: 配置包含所有必需节**
    - **RED**:
      - 编写 `test_config_has_required_sections()`
      - 断言: 配置包含 llm, embedding, vector_store, retrieval, evaluation, observability 节
    - **Verify RED**: 运行测试确认失败
    - **GREEN**: 确保配置文件结构完整
    - **Verify GREEN**: 运行测试确认通过

  - **验收标准**:
    - [ ] 每个测试都先失败，观察失败原因正确
    - [ ] 配置文件结构清晰
    - [ ] 包含所有必需的配置项
    - [ ] 测试输出无警告/错误
  - **devspec 参考**: 第 288-309 行

- [ ] ⏳ **1.7.2 实现配置解析器** 🔴 P0
  - **任务描述**: 实现 YAML 配置文件解析

  - **TDD Cycle**:
    **Test 1: 正确配置解析成功**
    - **RED**:
      - 编写 `test_load_valid_config_succeeds()`
      - 创建有效配置文件，断言: load_config() 返回 Config 对象
    - **Verify RED**: 运行测试，确认因 ConfigParser 不存在而失败
    - **GREEN**: 实现 ConfigParser 和 load_config() 方法
    - **Verify GREEN**: 运行测试确认通过

    **Test 2: 缺失配置使用默认值**
    - **RED**:
      - 编写 `test_missing_config_uses_defaults()`
      - 创建部分缺失的配置，断言: 缺失项使用默认值
    - **Verify RED**: 运行测试确认失败
    - **GREEN**: 添加默认值逻辑
    - **Verify GREEN**: 运行测试确认通过

    **Test 3: 非法配置抛出异常**
    - **RED**:
      - 编写 `test_invalid_config_raises_error()`
      - 创建非法配置，断言: 抛出 ConfigError
    - **Verify RED**: 运行测试确认失败
    - **GREEN**: 添加验证逻辑
    - **Verify GREEN**: 运行测试确认通过

  - **验收标准**:
    - [ ] 每个测试都先失败，观察失败原因正确
    - [ ] 能够正确解析 YAML
    - [ ] 配置项映射正确
    - [ ] 缺失配置有合理默认值
    - [ ] 测试输出无警告/错误
  - **devspec 参考**: 第 287 行（配置管理与切换流程）

#### Module 1.8: 中间层实现

- [ ] ⏳ **1.8.1 实现重试中间层** 🟡 P1
  - **任务描述**: 为 LLM/Embedding 调用添加重试机制

  - **TDD Cycle**:
    **Test 1: 网络错误自动重试**
    - **RED**:
      - 编写 `test_retry_on_network_error()`
      - Mock 函数前两次抛出 ConnectionError，第三次成功
      - 断言: 函数被调用 3 次，最终返回成功结果
    - **Verify RED**: 运行测试，确认因装饰器不存在而失败
    - **GREEN**: 实现 @retry 装饰器
    - **Verify GREEN**: 运行测试确认通过

    **Test 2: 达到最大重试次数后抛出异常**
    - **RED**:
      - 编写 `test_max_retries_exceeded_raises_error()`
      - Mock 函数总是失败
      - 断言: 达到 max_retries 后抛出原异常
    - **Verify RED**: 运行测试确认失败
    - **GREEN**: 完善重试逻辑
    - **Verify GREEN**: 运行测试确认通过

  - **验收标准**:
    - [ ] 每个测试都先失败，观察失败原因正确
    - [ ] 失败请求能够自动重试
    - [ ] 重试策略可配置
    - [ ] 避免无限重试
    - [ ] 测试输出无警告/错误
  - **devspec 参考**: 第 264 行

- [ ] ⏳ **1.8.2 实现限流中间层** 🟡 P1
  - **任务描述**: 为 LLM/Embedding 调用添加限流机制

  - **TDD Cycle**:
    **Test 1: 超过速率限制时等待**
    - **RED**:
      - 编写 `test_rate_limit_waits_when_exceeded()`
      - Mock 时间，设置 max_requests=2, time_window=1
      - 断言: 第 3 次调用等待到下一个时间窗口
    - **Verify RED**: 运行测试，确认因装饰器不存在而失败
    - **GREEN**: 实现 @rate_limit 装饰器
    - **Verify GREEN**: 运行测试确认通过

  - **验收标准**:
    - [ ] 每个测试都先失败，观察失败原因正确
    - [ ] 请求速率可控
    - [ ] 限流策略可配置
    - [ ] 测试输出无警告/错误
  - **devspec 参考**: 第 264 行

- [ ] ⏳ **1.8.3 实现日志中间层** 🟡 P1
  - **任务描述**: 为 LLM/Embedding 调用添加日志记录

  - **TDD Cycle**:
    **Test 1: 日志包含输入输出**
    - **RED**:
      - 编写 `test_log_call_records_input_and_output()`
      - 使用 @log_call 装饰测试函数
      - 断言: 日志包含输入参数和返回值
    - **Verify RED**: 运行测试，确认因装饰器不存在而失败
    - **GREEN**: 实现 @log_call 装饰器
    - **Verify GREEN**: 运行测试确认通过

    **Test 2: 日志包含耗时**
    - **RED**:
      - 编写 `test_log_call_records_duration()`
      - 断言: 日志包含执行耗时（毫秒）
    - **Verify RED**: 运行测试确认失败
    - **GREEN**: 添加计时逻辑
    - **Verify GREEN**: 运行测试确认通过

  - **验收标准**:
    - [ ] 每个测试都先失败，观察失败原因正确
    - [ ] 所有调用有日志记录
    - [ ] 日志内容完整
    - [ ] 测试输出无警告/错误
  - **devspec 参考**: 第 264 行

### ✅ Milestone 1.1 验收标准
- [ ] 所有核心抽象接口定义完成
- [ ] 所有工厂模式实现完成
- [ ] 配置文件和解析器实现完成
- [ ] **TDD 验证**:
  - [ ] 每个方法都有先失败的测试
  - [ ] 观察到每个测试的预期失败
  - [ ] 所有测试通过
  - [ ] 测试输出无警告/错误
  - [ ] 单元测试覆盖率 > 80%
- [ ] 接口文档完整

---

## Phase 2: LLM 与 Embedding Provider 实现

> **依赖分析**：依赖 Phase 1 的接口定义。各 Provider 实现之间无依赖，可按需实现。

### Milestone 2.1: 核心 Provider 实现

#### Module 2.1: LLM Provider 实现

- [ ] ⏳ **2.1.1 实现 AzureOpenAILLM** 🔴 P0
  - **任务描述**: 实现 Azure OpenAI 的 LLMClient

  - **TDD Cycle**:
    **Test 1: 继承 LLMClient 抽象类**
    - **RED**:
      - 编写 `test_azure_openai_is_llm_client()`
      - 断言: AzureOpenAILLM 是 LLMClient 的实例
    - **Verify RED**: 运行测试，确认因类不存在而失败
    - **GREEN**: 创建 AzureOpenAILLM 类继承 LLMClient
    - **Verify GREEN**: 运行测试确认通过

    **Test 2: chat() 方法调用 Azure API**
    - **RED**:
      - 编写 `test_chat_calls_azure_openai_api()`
      - Mock Azure OpenAI API 响应
      - 断言: chat() 发送正确格式的请求
    - **Verify RED**: 运行测试确认失败
    - **GREEN**: 实现 chat() 方法调用 Azure API
    - **Verify GREEN**: 运行测试确认通过

    **Test 3: API Key 认证**
    - **RED**:
      - 编写 `test_azure_uses_api_key_authentication()`
      - 断言: 请求包含正确的 API Key
    - **Verify RED**: 运行测试确认失败
    - **GREEN**: 添加认证逻辑
    - **Verify GREEN**: 运行测试确认通过

    **Test 4: 错误处理**
    - **RED**:
      - 编写 `test_azure_api_error_is_propagated()`
      - Mock API 返回错误
      - 断言: 错误被正确传播
    - **Verify RED**: 运行测试确认失败
    - **GREEN**: 添加错误处理
    - **Verify GREEN**: 运行测试确认通过

  - **验收标准**:
    - [ ] 每个测试都先失败，观察失败原因正确
    - [ ] API 调用格式符合 Azure 规范
    - [ ] 支持流式输出（如需要）
    - [ ] 测试输出无警告/错误
  - **devspec 参考**: 第 21 行、第 266 行

- [ ] ⏳ **2.1.2 实现 OpenAILLM** 🟡 P1
  - **任务描述**: 实现 OpenAI 官方 API 的 LLMClient

  - **TDD Cycle**:
    **Test 1: 继承和基础实现**
    - **RED**:
      - 编写 `test_openai_is_llm_client()`
      - 断言: OpenAILLM 是 LLMClient 的实例
    - **Verify RED**: 运行测试确认失败
    - **GREEN**: 创建 OpenAILLM 类继承 LLMClient
    - **Verify GREEN**: 运行测试确认通过

    **Test 2: chat() 调用 OpenAI API**
    - **RED**:
      - 编写 `test_chat_calls_openai_api()`
      - Mock OpenAI API 响应
    - **Verify RED**: 运行测试确认失败
    - **GREEN**: 实现 chat() 方法
    - **Verify GREEN**: 运行测试确认通过

  - **验收标准**:
    - [ ] 每个测试都先失败，观察失败原因正确
    - [ ] 测试输出无警告/错误
  - **devspec 参考**: 第 22 行

- [ ] ⏳ **2.1.3 实现 OllamaLLM** 🟡 P1
  - **任务描述**: 实现本地 Ollama 部署的 LLMClient

  - **TDD Cycle**:
    **Test 1: 本地 HTTP 通信**
    - **RED**:
      - 编写 `test_ollama_communicates_via_http()`
      - Mock Ollama HTTP 端点
      - 断言: chat() 发送 HTTP 请求到正确端点
    - **Verify RED**: 运行测试确认失败
    - **GREEN**: 实现 OllamaLLM 类
    - **Verify GREEN**: 运行测试确认通过

  - **验收标准**:
    - [ ] 每个测试都先失败，观察失败原因正确
    - [ ] 测试输出无警告/错误
  - **devspec 参考**: 第 23 行

- [ ] ⏳ **2.1.4 实现 DeepSeekLLM** 🟢 P2
- [ ] ⏳ **2.1.5 实现 ClaudeLLM** 🟢 P2
- [ ] ⏳ **2.1.6 实现 ZhipuLLM** 🟢 P2
  - **任务描述**: 实现各 Provider 的 LLMClient（格式同上，遵循 TDD Cycle）
  - **TDD Cycle**: （参照 2.1.1 格式）
  - **验收标准**: 每个测试先失败，测试输出无警告/错误
  - **devspec 参考**: 第 24 行

#### Module 2.2: Embedding Provider 实现

- [ ] ⏳ **2.2.1 实现 OpenAIEmbedding** 🔴 P0
  - **任务描述**: 实现 OpenAI Embedding API 的 EmbeddingClient

  - **TDD Cycle**:
    **Test 1: 继承 EmbeddingClient**
    - **RED**:
      - 编写 `test_openai_embedding_is_embedding_client()`
      - 断言: OpenAIEmbedding 是 EmbeddingClient 的实例
    - **Verify RED**: 运行测试确认失败
    - **GREEN**: 创建 OpenAIEmbedding 类
    - **Verify GREEN**: 运行测试确认通过

    **Test 2: 单个文本嵌入**
    - **RED**:
      - 编写 `test_embed_single_text_returns_vector()`
      - Mock OpenAI Embedding API
      - 断言: embed(["text"]) 返回长度为 1 的向量列表
    - **Verify RED**: 运行测试确认失败
    - **GREEN**: 实现 embed() 方法
    - **Verify GREEN**: 运行测试确认通过

    **Test 3: 批量文本嵌入**
    - **RED**:
      - 编写 `test_embed_batch_texts_returns_vectors()`
      - 断言: embed(["text1", "text2"]) 返回长度为 2 的列表
    - **Verify RED**: 运行测试确认失败
    - **GREEN**: 确保批量处理正确
    - **Verify GREEN**: 运行测试确认通过

    **Test 4: 向量归一化**
    - **RED**:
      - 编写 `test_embedding_vectors_are_normalized()`
      - 断言: 返回的向量 L2 范数约等于 1.0
    - **Verify RED**: 运行测试确认失败
    - **GREEN**: 添加归一化逻辑
    - **Verify GREEN**: 运行测试确认通过

  - **验收标准**:
    - [ ] 每个测试都先失败，观察失败原因正确
    - [ ] 支持批量处理
    - [ ] 向量维度正确
    - [ ] 测试输出无警告/错误
  - **devspec 参考**: 第 27 行

- [ ] ⏳ **2.2.2 实现本地 Embedding** 🟡 P1
  - **任务描述**: 实现本地 Embedding 模型的 EmbeddingClient

  - **TDD Cycle**:
    **Test 1: 本地模型加载**
    - **RED**:
      - 编写 `test_local_embedding_loads_model()`
      - Mock 模型加载
      - 断言: 模型被正确加载
    - **Verify RED**: 运行测试确认失败
    - **GREEN**: 实现本地 Embedding 类
    - **Verify GREEN**: 运行测试确认通过

  - **验收标准**:
    - [ ] 每个测试都先失败，观察失败原因正确
    - [ ] 测试输出无警告/错误
  - **devspec 参考**: 第 27 行

#### Module 2.3: Vision LLM 实现

- [ ] ⏳ **2.3.1 实现 AzureOpenAIVision** 🔴 P0
  - **任务描述**: 实现 Azure OpenAI Vision (GPT-4o/GPT-4-Vision) 的 BaseVisionLLM

  - **TDD Cycle**:
    **Test 1: 继承 BaseVisionLLM**
    - **RED**:
      - 编写 `test_azure_vision_is_vision_llm()`
      - 断言: AzureOpenAIVision 是 BaseVisionLLM 的实例
    - **Verify RED**: 运行测试确认失败
    - **GREEN**: 创建 AzureOpenAIVision 类
    - **Verify GREEN**: 运行测试确认通过

    **Test 2: 纯文本输入**
    - **RED**:
      - 编写 `test_vision_accepts_text_only()`
      - Mock API 响应
      - 断言: 纯文本 MultimodalMessage 可正常处理
    - **Verify RED**: 运行测试确认失败
    - **GREEN**: 实现 chat() 方法
    - **Verify GREEN**: 运行测试确认通过

    **Test 3: 图片+文本输入**
    - **RED**:
      - 编写 `test_vision_accepts_image_and_text()`
      - 创建包含图片的 MultimodalMessage
      - 断言: 图片被正确编码和发送
    - **Verify RED**: 运行测试确认失败
    - **GREEN**: 添加图片处理逻辑
    - **Verify GREEN**: 运行测试确认通过

    **Test 4: 多图片输入**
    - **RED**:
      - 编写 `test_vision_accepts_multiple_images()`
      - 断言: 多个图片都被正确处理
    - **Verify RED**: 运行测试确认失败
    - **GREEN**: 确保多图片支持
    - **Verify GREEN**: 运行测试确认通过

  - **验收标准**:
    - [ ] 每个测试都先失败，观察失败原因正确
    - [ ] 支持复杂图表解析
    - [ ] 测试输出无警告/错误
  - **devspec 参考**: 第 266 行

### ✅ Milestone 2.1 验收标准
- [ ] 至少实现一个 LLM Provider（推荐 Azure OpenAI）
- [ ] 至少实现一个 Embedding Provider（推荐 OpenAI）
- [ ] 实现 Azure OpenAI Vision
- [ ] **TDD 验证**:
  - [ ] 每个方法都有先失败的测试
  - [ ] 所有测试通过
  - [ ] 测试输出无警告/错误
- [ ] 工厂模式能正确创建各 Provider 实例

---

## Phase 3: 向量存储实现

> **依赖分析**：依赖 Phase 1 的 VectorStore 接口定义。

### Milestone 3.1: 向量存储实现

- [ ] ⏳ **3.1.1 实现 MilvusVectorStore** 🔴 P0
  - **任务描述**: 实现 Milvus 向量存储

  - **TDD Cycle**:
    **Test 1: 继承 VectorStore**
    - **RED**:
      - 编写 `test_milvus_is_vector_store()`
      - 断言: MilvusVectorStore 是 VectorStore 的实例
    - **Verify RED**: 运行测试确认失败
    - **GREEN**: 创建 MilvusVectorStore 类
    - **Verify GREEN**: 运行测试确认通过

    **Test 2: insert() 插入向量**
    - **RED**:
      - 编写 `test_insert_stores_vectors_and_payloads()`
      - Mock Milvus 连接
      - 断言: 向量和 payload 被正确存储
    - **Verify RED**: 运行测试确认失败
    - **GREEN**: 实现 insert() 方法
    - **Verify GREEN**: 运行测试确认通过

    **Test 3: query() 查询向量**
    - **RED**:
      - 编写 `test_query_returns_top_k_results()`
      - Mock 查询响应
      - 断言: 返回 Top-K 结果及分数
    - **Verify RED**: 运行测试确认失败
    - **GREEN**: 实现 query() 方法
    - **Verify GREEN**: 运行测试确认通过

    **Test 4: upsert() 幂等性**
    - **RED**:
      - 编写 `test_upsert_is_idempotent()`
      - 断言: 相同 chunk_id 的 upsert 更新而非插入
    - **Verify RED**: 运行测试确认失败
    - **GREEN**: 实现 upsert() 方法
    - **Verify GREEN**: 运行测试确认通过

    **Test 5: delete() 删除向量**
    - **RED**:
      - 编写 `test_delete_removes_vectors()`
      - 断言: 指定向量被删除
    - **Verify RED**: 运行测试确认失败
    - **GREEN**: 实现 delete() 方法
    - **Verify GREEN**: 运行测试确认通过

    **Test 6: chunk_id 生成**
    - **RED**:
      - 编写 `test_chunk_id_is_hash_of_source_section_and_content()`
      - 断言: chunk_id = hash(source_path + section_path + content_hash)
    - **Verify RED**: 运行测试确认失败
    - **GREEN**: 实现 chunk_id 生成逻辑
    - **Verify GREEN**: 运行测试确认通过

  - **验收标准**:
    - [ ] 每个测试都先失败，观察失败原因正确
    - [ ] upsert 操作正确（插入或更新）
    - [ ] chunk_id 基于哈希生成
    - [ ] 测试输出无警告/错误
  - **devspec 参考**: 第 134 行、第 138 行

- [ ] ⏳ **3.1.2 实现 ChromaVectorStore** 🟡 P1
- [ ] ⏳ **3.1.3 实现 QdrantVectorStore** 🟢 P2
- [ ] ⏳ **3.1.4 实现 PineconeVectorStore** 🟢 P2
  - **任务描述**: 实现其他向量存储（格式同上）
  - **TDD Cycle**: （参照 3.1.1 格式）
  - **验收标准**: 每个测试先失败，测试输出无警告/错误
  - **devspec 参考**: 第 38 行

### ✅ Milestone 3.1 验收标准
- [ ] 至少实现一个 VectorStore（推荐 Milvus）
- [ ] upsert 幂等性正确实现
- [ ] chunk_id 生成算法正确
- [ ] **TDD 验证**:
  - [ ] 每个方法都有先失败的测试
  - [ ] 所有测试通过
  - [ ] 测试输出无警告/错误
- [ ] 工厂模式能正确创建各 VectorStore 实例

---

## Phase 4: Reranker 实现

> **依赖分析**：依赖 Phase 1 的 Reranker 接口定义。

### Milestone 4.1: Reranker 实现

- [ ] ⏳ **4.1.1 实现 NoOpReranker** 🔴 P0
  - **任务描述**: 实现空操作 Reranker（直接返回输入）

  - **TDD Cycle**:
    **Test 1: 继承 Reranker**
    - **RED**:
      - 编写 `test_noop_reranker_is_reranker()`
      - 断言: NoOpReranker 是 Reranker 的实例
    - **Verify RED**: 运行测试确认失败
    - **GREEN**: 创建 NoOpReranker 类
    - **Verify GREEN**: 运行测试确认通过

    **Test 2: 输入输出完全一致**
    - **RED**:
      - 编写 `test_noop_reranker_returns_input_unchanged()`
      - 创建测试 chunks 列表
      - 断言: rerank() 返回相同顺序的 chunks
    - **Verify RED**: 运行测试确认失败
    - **GREEN**: 实现 rerank() 直接返回输入
    - **Verify GREEN**: 运行测试确认通过

  - **验收标准**:
    - [ ] 每个测试都先失败，观察失败原因正确
    - [ ] 输入输出完全一致
    - [ ] 测试输出无警告/错误
  - **devspec 参考**: 第 166 行

- [ ] ⏳ **4.1.2 实现 CrossEncoderReranker** 🟡 P1
  - **任务描述**: 实现 Cross-Encoder 重排模型

  - **TDD Cycle**:
    **Test 1: 继承 Reranker**
    - **RED**:
      - 编写 `test_cross_encoder_reranker_is_reranker()`
      - 断言: CrossEncoderReranker 是 Reranker 的实例
    - **Verify RED**: 运行测试确认失败
    - **GREEN**: 创建 CrossEncoderReranker 类
    - **Verify GREEN**: 运行测试确认通过

    **Test 2: 正常打分和排序**
    - **RED**:
      - 编写 `test_cross_encoder_scores_and_ranks_chunks()`
      - Mock cross-encoder 模型返回分数
      - 断言: 返回按分数降序排列的 RankedChunk
    - **Verify RED**: 运行测试确认失败
    - **GREEN**: 实现 rerank() 方法
    - **Verify GREEN**: 运行测试确认通过

    **Test 3: 超时回退**
    - **RED**:
      - 编写 `test_cross_encoder_fallback_on_timeout()`
      - Mock 模型超时
      - 断言: 超时时返回原始输入顺序
    - **Verify RED**: 运行测试确认失败
    - **GREEN**: 添加超时和回退逻辑
    - **Verify GREEN**: 运行测试确认通过

  - **验收标准**:
    - [ ] 每个测试都先失败，观察失败原因正确
    - [ ] 超时时回退到输入顺序
    - [ ] 测试输出无警告/错误
  - **devspec 参考**: 第 167 行

- [ ] ⏳ **4.1.3 实现 LLMReranker** 🟢 P2
  - **任务描述**: 实现基于 LLM 的重排
  - **TDD Cycle**: （参照 4.1.2 格式）
  - **验收标准**: 每个测试先失败，测试输出无警告/错误
  - **devspec 参考**: 第 168 行

### ✅ Milestone 4.1 验收标准
- [ ] NoOpReranker 实现
- [ ] 至少实现一个实际 Reranker（推荐 CrossEncoder）
- [ ] 超时回退机制正确
- [ ] **TDD 验证**:
  - [ ] 每个方法都有先失败的测试
  - [ ] 所有测试通过
  - [ ] 测试输出无警告/错误
- [ ] 工厂模式能正确创建各 Reranker 实例

---

## Phase 5: 数据摄取流水线实现

> **依赖分析**：依赖 Phase 1 的 Loader/Splitter/Transform 接口，依赖 Phase 2 的 LLM/Embedding Provider，依赖 Phase 3 的 VectorStore。

### Milestone 5.1: Loader 实现

- [ ] ⏳ **5.1.1 实现文件去重机制** 🔴 P0
  - **任务描述**: 实现前置去重，计算文件 SHA256 哈希，查询 ingestion_history 表

  - **TDD Cycle**:
    **Test 1: 计算文件 SHA256 哈希**
    - **RED**:
      - 编写 `test_calculate_file_hash_returns_sha256()`
      - 创建测试文件
      - 断言: 返回 64 字符的十六进制字符串
    - **Verify RED**: 运行测试确认失败
    - **GREEN**: 实现 calculate_file_hash() 函数
    - **Verify GREEN**: 运行测试确认通过

    **Test 2: 相同内容相同哈希**
    - **RED**:
      - 编写 `test_same_content_same_hash()`
      - 创建内容相同但文件名不同的两个文件
      - 断言: 哈希值相同
    - **Verify RED**: 运行测试确认失败
    - **GREEN**: 确保哈希只基于内容
    - **Verify GREEN**: 运行测试确认通过

    **Test 3: 新文件不应跳过**
    - **RED**:
      - 编写 `test_should_skip_returns_false_for_new_file()`
      - Mock ingestion_history 查询返回空
      - 断言: should_skip(new_hash) 返回 False
    - **Verify RED**: 运行测试确认失败
    - **GREEN**: 实现 should_skip() 方法
    - **Verify GREEN**: 运行测试确认通过

    **Test 4: 已处理文件应跳过**
    - **RED**:
      - 编写 `test_should_skip_returns_true_for_processed_file()`
      - Mock ingestion_history 包含该哈希
      - 断言: should_skip(existing_hash) 返回 True
    - **Verify RED**: 运行测试确认失败
    - **GREEN**: 完善查询逻辑
    - **Verify GREEN**: 运行测试确认通过

  - **验收标准**:
    - [ ] 每个测试都先失败，观察失败原因正确
    - [ ] 哈希计算正确
    - [ ] 已处理文件正确跳过
    - [ ] 内容相同但文件名不同的文件被识别为重复
    - [ ] 测试输出无警告/错误
  - **devspec 参考**: 第 91 行

- [ ] ⏳ **5.1.2 实现 PDFLoader** 🔴 P0
  - **任务描述**: 使用 markitdown 将 PDF 转换为 Markdown

  - **TDD Cycle**:
    **Test 1: 继承 Loader**
    - **RED**:
      - 编写 `test_pdf_loader_is_loader()`
      - 断言: PDFLoader 是 Loader 的实例
    - **Verify RED**: 运行测试确认失败
    - **GREEN**: 创建 PDFLoader 类
    - **Verify GREEN**: 运行测试确认通过

    **Test 2: 纯文本 PDF 解析**
    - **RED**:
      - 编写 `test_load_returns_document_with_markdown_text()`
      - 使用测试 PDF 文件
      - 断言: 返回 Document 对象，text 是 Markdown 格式
    - **Verify RED**: 运行测试确认失败
    - **GREEN**: 实现 load() 方法集成 markitdown
    - **Verify GREEN**: 运行测试确认通过

    **Test 3: metadata 包含必需字段**
    - **RED**:
      - 编写 `test_document_metadata_contains_required_fields()`
      - 断言: metadata 包含 source_path, doc_type, page, title, images
    - **Verify RED**: 运行测试确认失败
    - **GREEN**: 添加 metadata 提取逻辑
    - **Verify GREEN**: 运行测试确认通过

  - **验收标准**:
    - [ ] 每个测试都先失败，观察失败原因正确
    - [ ] 输出 Markdown 格式文本
    - [ ] Document 对象包含完整 metadata
    - [ ] 测试输出无警告/错误
  - **devspec 参考**: 第 96 行、第 99 行

- [ ] ⏳ **5.1.3 实现 MarkdownLoader** 🟡 P1
  - **任务描述**: 实现 Markdown 文档解析器
  - **TDD Cycle**: （参照 5.1.2 格式）
  - **验收标准**: 每个测试先失败，测试输出无警告/错误
  - **devspec 参考**: 第 32 行

- [ ] ⏳ **5.1.4 实现 CodeLoader** 🟡 P1
  - **任务描述**: 实现代码文件解析器
  - **TDD Cycle**: （参照 5.1.2 格式）
  - **验收标准**: 每个测试先失败，测试输出无警告/错误
  - **devspec 参考**: 第 32 行

### Milestone 5.2: Splitter 实现

- [ ] ⏳ **5.2.1 实现 RecursiveCharacterSplitter** 🔴 P0
  - **任务描述**: 使用 LangChain 的 RecursiveCharacterTextSplitter 进行切分

  - **TDD Cycle**:
    **Test 1: 继承 Splitter**
    - **RED**:
      - 编写 `test_recursive_splitter_is_splitter()`
      - 断言: RecursiveCharacterSplitter 是 Splitter 的实例
    - **Verify RED**: 运行测试确认失败
    - **GREEN**: 创建 RecursiveCharacterSplitter 类
    - **Verify GREEN**: 运行测试确认通过

    **Test 2: 长文本正确切分**
    - **RED**:
      - 编写 `test_long_text_is_split_into_chunks()`
      - 创建长文本 Document
      - 断言: 返回多个 chunk，每个 chunk 在限制长度内
    - **Verify RED**: 运行测试确认失败
    - **GREEN**: 集成 LangChain RecursiveCharacterTextSplitter
    - **Verify GREEN**: 运行测试确认通过

    **Test 3: chunk 包含定位信息**
    - **RED**:
      - 编写 `test_chunks_contain_position_info()`
      - 断言: 每个 chunk 包含 source, chunk_index, start_offset, end_offset
    - **Verify RED**: 运行测试确认失败
    - **GREEN**: 添加定位信息逻辑
    - **Verify GREEN**: 运行测试确认通过

    **Test 4: 代码块不被切断**
    - **RED**:
      - 编写 `test_code_blocks_not_split()`
      - 创建包含代码块的文本
      - 断言: 代码块在同一个 chunk 中
    - **Verify RED**: 运行测试确认失败
    - **GREEN**: 配置语义断点
    - **Verify GREEN**: 运行测试确认通过

  - **验收标准**:
    - [ ] 每个测试都先失败，观察失败原因正确
    - [ ] 切分结果语义完整
    - [ ] 每个 chunk 包含定位信息
    - [ ] 测试输出无警告/错误
  - **devspec 参考**: 第 105 行

- [ ] ⏳ **5.2.2 实现定长切分策略** 🟢 P2
- [ ] ⏳ **5.2.3 实现语义切分策略** 🟢 P2
  - **任务描述**: 实现其他切分策略（格式同上）
  - **TDD Cycle**: （参照 5.2.1 格式）
  - **验收标准**: 每个测试先失败，测试输出无警告/错误
  - **devspec 参考**: 第 33 行

### Milestone 5.3: Transform 实现

- [ ] ⏳ **5.3.1 实现智能重组 Transform** 🔴 P0
  - **任务描述**: 利用 LLM 对粗切分的片段进行二次加工

  - **TDD Cycle**:
    **Test 1: 继承 Transform**
    - **RED**:
      - 编写 `test_smart_reorganize_is_transform()`
      - 断言: SmartReorganizeTransform 是 Transform 的实例
    - **Verify RED**: 运行测试确认失败
    - **GREEN**: 创建 SmartReorganizeTransform 类
    - **Verify GREEN**: 运行测试确认通过

    **Test 2: 合并被切断的段落**
    - **RED**:
      - 编写 `test_transform_merges_broken_paragraphs()`
      - 创建被切断的 chunk
      - Mock LLM 返回合并后的文本
      - 断言: 返回的 chunk 包含完整的段落
    - **Verify RED**: 运行测试确认失败
    - **GREEN**: 实现 transform() 方法
    - **Verify GREEN**: 运行测试确认通过

    **Test 3: 移除页眉页脚**
    - **RED**:
      - 编写 `test_transform_removes_header_footer()`
      - 创建包含页眉页脚的 chunk
      - 断言: 返回的 chunk 不包含页眉页脚
    - **Verify RED**: 运行测试确认失败
    - **GREEN**: 添加噪音移除逻辑
    - **Verify GREEN**: 运行测试确认通过

  - **验收标准**:
    - [ ] 每个测试都先失败，观察失败原因正确
    - [ ] 每个 chunk 是自包含的语义单元
    - [ ] 页眉页脚和乱码被移除
    - [ ] 测试输出无警告/错误
  - **devspec 参考**: 第 114 行

- [ ] ⏳ **5.3.2 实现语义元数据注入 Transform** 🔴 P0
  - **任务描述**: 利用 LLM 提取语义特征，生成 title、summary、tags

  - **TDD Cycle**:
    **Test 1: 注入 title、summary、tags**
    - **RED**:
      - 编写 `test_transform_injects_semantic_metadata()`
      - 创建测试 chunk
      - Mock LLM 返回元数据
      - 断言: chunk.metadata 包含 title, summary, tags
    - **Verify RED**: 运行测试确认失败
    - **GREEN**: 实现 SemanticMetadataTransform 类
    - **Verify GREEN**: 运行测试确认通过

    **Test 2: title 反映内容**
    - **RED**:
      - 编写 `test_title_reflects_chunk_content()`
      - 断言: 生成的 title 与 chunk 内容相关
    - **Verify RED**: 运行测试确认失败
    - **GREEN**: 确保 LLM prompt 正确
    - **Verify GREEN**: 运行测试确认通过

  - **验收标准**:
    - [ ] 每个测试都先失败，观察失败原因正确
    - [ ] title 准确反映 chunk 内容
    - [ ] summary 简洁准确
    - [ ] tags 相关且有用
    - [ ] 测试输出无警告/错误
  - **devspec 参考**: 第 117 行

- [ ] ⏳ **5.3.3 实现多模态增强 Transform** 🔴 P0
  - **任务描述**: 扫描图像引用，调用 Vision LLM 生成 caption

  - **TDD Cycle**:
    **Test 1: 识别图片引用**
    - **RED**:
      - 编写 `test_transform_detects_image_references()`
      - 创建包含 image_refs 的 chunk
      - 断言: 图片引用被正确识别
    - **Verify RED**: 运行测试确认失败
    - **GREEN**: 实现 MultimodalEnhanceTransform 类
    - **Verify GREEN**: 运行测试确认通过

    **Test 2: 生成并缝合 caption**
    - **RED**:
      - 编写 `test_transform_generates_and_stitches_caption()`
      - Mock Vision LLM 返回 caption
      - 断言: caption 被添加到 chunk.text 或 chunk.metadata
    - **Verify RED**: 运行测试确认失败
    - **GREEN**: 实现 transform() 方法
    - **Verify GREEN**: 运行测试确认通过

  - **验收标准**:
    - [ ] 每个测试都先失败，观察失败原因正确
    - [ ] 图片被正确识别
    - [ ] caption 准确描述图片内容
    - [ ] caption 被正确缝合
    - [ ] 测试输出无警告/错误
  - **devspec 参考**: 第 120 行

- [ ] ⏳ **5.3.4 实现 OCR Transform** 🟡 P1
- [ ] ⏳ **5.3.5 实现 HTML 清理 Transform** 🟡 P1
- [ ] ⏳ **5.3.6 实现原子化与幂等操作** 🟡 P1
  - **任务描述**: 其他 Transform 实现（格式同上）
  - **TDD Cycle**: （参照 5.3.1 格式）
  - **验收标准**: 每个测试先失败，测试输出无警告/错误
  - **devspec 参考**: 第 34 行、第 124 行

### Milestone 5.4: Embedding 实现

- [ ] ⏳ **5.4.1 实现内容哈希计算** 🔴 P0
  - **任务描述**: 计算 chunk 的内容哈希

  - **TDD Cycle**:
    **Test 1: 相同内容相同哈希**
    - **RED**:
      - 编写 `test_same_content_same_hash()`
      - 创建内容相同的两个 chunk
      - 断言: 哈希值相同
    - **Verify RED**: 运行测试确认失败
    - **GREEN**: 实现 calculate_content_hash() 函数
    - **Verify GREEN**: 运行测试确认通过

    **Test 2: 不同内容不同哈希**
    - **RED**:
      - 编写 `test_different_content_different_hash()`
      - 创建内容不同的 chunk
      - 断言: 哈希值不同
    - **Verify RED**: 运行测试确认失败
    - **GREEN**: 确保哈希算法正确
    - **Verify GREEN**: 运行测试确认通过

  - **验收标准**:
    - [ ] 每个测试都先失败，观察失败原因正确
    - [ ] 相同内容产生相同哈希
    - [ ] 不同内容产生不同哈希
    - [ ] 测试输出无警告/错误
  - **devspec 参考**: 第 128 行

- [ ] ⏳ **5.4.2 实现向量复用机制** 🔴 P0
  - **任务描述**: 对内容未变的片段复用已有向量

  - **TDD Cycle**:
    **Test 1: 已存在的向量被复用**
    - **RED**:
      - 编写 `test_existing_vector_is_reused()`
      - Mock 数据库返回已有向量
      - 断言: 不调用 embedding API，直接返回已有向量
    - **Verify RED**: 运行测试确认失败
    - **GREEN**: 实现向量复用逻辑
    - **Verify GREEN**: 运行测试确认通过

    **Test 2: 新内容调用 embedding API**
    - **RED**:
      - 编写 `test_new_content_calls_embedding_api()`
      - Mock 数据库返回空
      - 断言: 调用 embedding API 生成新向量
    - **Verify RED**: 运行测试确认失败
    - **GREEN**: 完善复用逻辑
    - **Verify GREEN**: 运行测试确认通过

  - **验收标准**:
    - [ ] 每个测试都先失败，观察失败原因正确
    - [ ] 已存在的向量被复用
    - [ ] 不重复调用 embedding API
    - [ ] 测试输出无警告/错误
  - **devspec 参考**: 第 128 行

- [ ] ⏳ **5.4.3 实现双路向量化** 🔴 P0
  - **任务描述**: 对每个 chunk 并行执行 dense 和 sparse embedding

  - **TDD Cycle**:
    **Test 1: 生成 dense 和 sparse 向量**
    - **RED**:
      - 编写 `test_dual_embed_generates_both_vectors()`
      - Mock 两个 embedding 客户端
      - 断言: 返回 (dense_vectors, sparse_vectors) 元组
    - **Verify RED**: 运行测试确认失败
    - **GREEN**: 实现 dual_embed() 函数
    - **Verify GREEN**: 运行测试确认通过

    **Test 2: 并行执行**
    - **RED**:
      - 编写 `test_dual_embed_executes_in_parallel()`
      - Mock 计时
      - 断言: 执行时间 < 单独执行时间之和
    - **Verify RED**: 运行测试确认失败
    - **GREEN**: 使用并发执行
    - **Verify GREEN**: 运行测试确认通过

  - **验收标准**:
    - [ ] 每个测试都先失败，观察失败原因正确
    - [ ] dense 和 sparse 向量都正确生成
    - [ ] 并行执行提高效率
    - [ ] 测试输出无警告/错误
  - **devspec 参考**: 第 129 行

- [ ] ⏳ **5.4.4 实现批处理优化** 🟡 P1
  - **任务描述**: 优化 embedding API 调用，支持批量处理
  - **TDD Cycle**: （参照 5.4.3 格式）
  - **验收标准**: 每个测试先失败，批处理提高效率，测试输出无警告/错误
  - **devspec 参考**: 第 132 行

### Milestone 5.5: Upsert & Storage 实现

- [ ] ⏳ **5.5.1 实现 Chunk ID 生成** 🔴 P0
  - **任务描述**: 为每个 chunk 生成全局唯一的 chunk_id

  - **TDD Cycle**:
    **Test 1: chunk_id 全局唯一**
    - **RED**:
      - 编写 `test_chunk_id_is_globally_unique()`
      - 创建不同来源的 chunk
      - 断言: 每个 chunk_id 唯一
    - **Verify RED**: 运行测试确认失败
    - **GREEN**: 实现 generate_chunk_id() 函数
    - **Verify GREEN**: 运行测试确认通过

    **Test 2: 相同内容产生相同 chunk_id**
    - **RED**:
      - 编写 `test_same_content_produces_same_chunk_id()`
      - 断言: 相同 source_path + section_path + content_hash 产生相同 chunk_id
    - **Verify RED**: 运行测试确认失败
    - **GREEN**: 确保生成算法稳定
    - **Verify GREEN**: 运行测试确认通过

  - **验收标准**:
    - [ ] 每个测试都先失败，观察失败原因正确
    - [ ] chunk_id 全局唯一
    - [ ] 相同内容产生相同 chunk_id
    - [ ] 测试输出无警告/错误
  - **devspec 参考**: 第 138 行

- [ ] ⏳ **5.5.2 实现 Batch 事务性写入** 🔴 P0
  - **任务描述**: 以 batch 为单位进行事务性写入

  - **TDD Cycle**:
    **Test 1: 正常写入成功**
    - **RED**:
      - 编写 `test_batch_upsert_succeeds()`
      - Mock VectorStore
      - 断言: batch 中的所有 chunk 被写入
    - **Verify RED**: 运行测试确认失败
    - **GREEN**: 实现 batch_upsert() 函数
    - **Verify GREEN**: 运行测试确认通过

    **Test 2: 部分失败回滚**
    - **RED**:
      - 编写 `test_batch_failure_rolls_back()`
      - Mock 部分写入失败
      - 断言: 失败的 batch 被回滚
    - **Verify RED**: 运行测试确认失败
    - **GREEN**: 添加事务逻辑
    - **Verify GREEN**: 运行测试确认通过

  - **验收标准**:
    - [ ] 每个测试都先失败，观察失败原因正确
    - [ ] batch 写入具有原子性
    - [ ] 失败的 batch 能够回滚
    - [ ] 测试输出无警告/错误
  - **devspec 参考**: 第 140 行

### Milestone 5.6: Dedup & Normalize 实现

- [ ] ⏳ **5.6.1 实现向量去重** 🟡 P1
- [ ] ⏳ **5.6.2 实现文本去重** 🟡 P1
  - **任务描述**: 实现去重功能（格式同上）
  - **TDD Cycle**: （参照 5.5.1 格式）
  - **验收标准**: 每个测试先失败，重复被正确过滤，测试输出无警告/错误
  - **devspec 参考**: 第 87 行

### ✅ Milestone 5.1 验收标准
- [ ] PDFLoader 正常工作
- [ ] RecursiveCharacterSplitter 正常工作
- [ ] 核心 Transform 实现（智能重组、元数据注入、多模态增强）
- [ ] 双路向量化正常工作
- [ ] Milvus upsert 正常工作
- [ ] 端到端：PDF → Chunks → VectorStore 流程打通
- [ ] **TDD 验证**:
  - [ ] 每个方法都有先失败的测试
  - [ ] 所有测试通过
  - [ ] 测试输出无警告/错误
  - [ ] 单元测试覆盖率 > 70%

---

## Phase 6: 检索流水线实现

> **依赖分析**：依赖 Phase 5 的数据摄取（向量已存储），依赖 Phase 4 的 Reranker。

### Milestone 6.1: 查询预处理实现

- [ ] ⏳ **6.1.1 实现关键词提取** 🔴 P0
  - **任务描述**: 利用 NLP 工具提取 query 中的关键词

  - **TDD Cycle**:
    **Test 1: 提取关键词**
    - **RED**:
      - 编写 `test_extract_returns_keywords()`
      - 输入测试查询
      - 断言: 返回关键词列表
    - **Verify RED**: 运行测试确认失败
    - **GREEN**: 实现 KeywordExtractor.extract()
    - **Verify GREEN**: 运行测试确认通过

    **Test 2: 去除停用词**
    - **RED**:
      - 编写 `test_stopwords_are_removed()`
      - 输入包含停用词的查询
      - 断言: 返回结果不包含停用词
    - **Verify RED**: 运行测试确认失败
    - **GREEN**: 添加停用词过滤
    - **Verify GREEN**: 运行测试确认通过

  - **验收标准**:
    - [ ] 每个测试都先失败，观察失败原因正确
    - [ ] 关键词提取准确
    - [ ] 停用词被正确去除
    - [ ] 测试输出无警告/错误
  - **devspec 参考**: 第 147 行

- [ ] ⏳ **6.1.2 实现查询扩展** 🟡 P1
- [ ] ⏳ **6.1.3 实现 Sparse Route 扩展策略** 🟡 P1
- [ ] ⏳ **6.1.4 实现 Dense Route 策略** 🔴 P0
  - **任务描述**: 查询预处理功能（格式同上）
  - **TDD Cycle**: （参照 6.1.1 格式）
  - **验收标准**: 每个测试先失败，测试输出无警告/错误
  - **devspec 参考**: 第 148-151 行

### Milestone 6.2: 混合检索实现

- [ ] ⏳ **6.2.1 实现稀疏检索** 🔴 P0
  - **任务描述**: 实现 BM25 稀疏检索

  - **TDD Cycle**:
    **Test 1: 返回 Top-N 结果**
    - **RED**:
      - 编写 `test_sparse_retriever_returns_top_k()`
      - Mock BM25 算法
      - 断言: 返回 top_k 个结果及 BM25 分数
    - **Verify RED**: 运行测试确认失败
    - **GREEN**: 实现 SparseRetriever.retrieve()
    - **Verify GREEN**: 运行测试确认通过

    **Test 2: 关键词匹配准确**
    - **RED**:
      - 编写 `test_keywords_are_matched_correctly()`
      - 断言: 结果包含匹配关键词的文档
    - **Verify RED**: 运行测试确认失败
    - **GREEN**: 确保 BM25 算法正确
    - **Verify GREEN**: 运行测试确认通过

  - **验收标准**:
    - [ ] 每个测试都先失败，观察失败原因正确
    - [ ] 返回 Top-N 候选及 BM25 分数
    - [ ] 关键词匹配准确
    - [ ] 测试输出无警告/错误
  - **devspec 参考**: 第 154 行

- [ ] ⏳ **6.2.2 实现稠密检索** 🔴 P0
  - **任务描述**: 实现语义向量检索

  - **TDD Cycle**:
    **Test 1: 返回 Top-N 结果**
    - **RED**:
      - 编写 `test_dense_retriever_returns_top_k()`
      - Mock VectorStore
      - 断言: 返回 top_k 个结果及相似度分数
    - **Verify RED**: 运行测试确认失败
    - **GREEN**: 实现 DenseRetriever.retrieve()
    - **Verify GREEN**: 运行测试确认通过

  - **验收标准**:
    - [ ] 每个测试都先失败，观察失败原因正确
    - [ ] 返回 Top-N 候选及相似度分数
    - [ ] 语义匹配准确
    - [ ] 测试输出无警告/错误
  - **devspec 参考**: 第 154 行

- [ ] ⏳ **6.2.3 实现 RRF 融合算法** 🔴 P0
  - **任务描述**: 采用 RRF 算法融合稀疏和稠密检索结果

  - **TDD Cycle**:
    **Test 1: 完全一致的结果**
    - **RED**:
      - 编写 `test_rrf_fusion_identical_results()`
      - 输入两路相同排名的结果
      - 断言: 融合后排名保持一致
    - **Verify RED**: 运行测试确认失败
    - **GREEN**: 实现 RRFFusion.fuse()
    - **Verify GREEN**: 运行测试确认通过

    **Test 2: 完全不一致的结果**
    - **RED**:
      - 编写 `test_rrf_fusion_disjoint_results()`
      - 输入两路完全不同的结果
      - 断言: 融合后按 RRF 分数排序
    - **Verify RED**: 运行测试确认失败
    - **GREEN**: 确保 RRF 公式正确: Score = 1/(k+Rank_Dense) + 1/(k+Rank_Sparse)
    - **Verify GREEN**: 运行测试确认通过

    **Test 3: 部分重叠的结果**
    - **RED**:
      - 编写 `test_rrf_fusion_overlapping_results()`
      - 输入部分重叠的结果
      - 断言: 重叠项分数相加，排名提升
    - **Verify RED**: 运行测试确认失败
    - **GREEN**: 确保融合逻辑正确
    - **Verify GREEN**: 运行测试确认通过

  - **验收标准**:
    - [ ] 每个测试都先失败，观察失败原因正确
    - [ ] 融合算法正确
    - [ ] 平滑单一模态缺陷
    - [ ] 测试输出无警告/错误
  - **devspec 参考**: 第 154 行

- [ ] ⏳ **6.2.4 实现并行召回** 🟡 P1
  - **任务描述**: 稀疏和稠密检索并行执行
  - **TDD Cycle**: （参照 5.4.3 格式）
  - **验收标准**: 每个测试先失败，并行执行提高效率，测试输出无警告/错误
  - **devspec 参考**: 第 154 行

### Milestone 6.3: Filter & Reranking 实现

- [ ] ⏳ **6.3.1 实现 Pre-filter 机制** 🟡 P1
- [ ] ⏳ **6.3.2 实现 Post-filter 兜底机制** 🟡 P1
- [ ] ⏳ **6.3.3 实现软偏好排序信号** 🟢 P2
  - **任务描述**: 过滤和偏好功能（格式同上）
  - **TDD Cycle**: （参照 6.2.1 格式）
  - **验收标准**: 每个测试先失败，测试输出无警告/错误
  - **devspec 参考**: 第 159-161 行

### ✅ Milestone 6.1 验收标准
- [ ] 查询预处理正常工作
- [ ] 混合检索正常工作
- [ ] RRF 融合正确
- [ ] Reranker 正常工作
- [ ] 端到端：Query → Preprocess → Hybrid Retrieve → Rerank 流程打通
- [ ] **TDD 验证**:
  - [ ] 每个方法都有先失败的测试
  - [ ] 所有测试通过
  - [ ] 测试输出无警告/错误
  - [ ] 单元测试覆盖率 > 70%

---

## Phase 7: 可观测性与追踪实现

> **依赖分析**：可贯穿全链路，但核心功能可在 Phase 6 后实现。

### Milestone 7.1: 追踪数据结构

- [ ] ⏳ **7.1.1 实现 TraceContext** 🔴 P0
  - **任务描述**: 实现追踪上下文对象

  - **TDD Cycle**:
    **Test 1: 生成唯一 trace_id**
    - **RED**:
      - 编写 `test_trace_context_generates_unique_id()`
      - 创建多个 TraceContext
      - 断言: 每个 trace_id 唯一
    - **Verify RED**: 运行测试确认失败
    - **GREEN**: 实现 TraceContext.__init__()
    - **Verify GREEN**: 运行测试确认通过

    **Test 2: 记录各阶段数据**
    - **RED**:
      - 编写 `test_record_stage_stores_data()`
      - 调用 record_stage()
      - 断言: 阶段数据被正确存储
    - **Verify RED**: 运行测试确认失败
    - **GREEN**: 实现 record_stage() 方法
    - **Verify GREEN**: 运行测试确认通过

    **Test 3: finish() 序列化并写入**
    - **RED**:
      - 编写 `test_finish_serializes_and_writes_log()`
      - Mock 文件写入
      - 断言: 数据被序列化为 JSON 并写入
    - **Verify RED**: 运行测试确认失败
    - **GREEN**: 实现 finish() 方法
    - **Verify GREEN**: 运行测试确认通过

  - **验收标准**:
    - [ ] 每个测试都先失败，观察失败原因正确
    - [ ] trace_id 唯一
    - [ ] 各阶段数据正确记录
    - [ ] 序列化格式正确
    - [ ] 测试输出无警告/错误
  - **devspec 参考**: 第 369-377 行

### Milestone 7.2: 阶段追踪实现

- [ ] ⏳ **7.2.1 实现 Query Processing 追踪** 🔴 P0
- [ ] ⏳ **7.2.2 实现 Dense Retrieval 追踪** 🔴 P0
- [ ] ⏳ **7.2.3 实现 Sparse Retrieval 追踪** 🔴 P0
- [ ] ⏳ **7.2.4 实现 Fusion 追踪** 🔴 P0
- [ ] ⏳ **7.2.5 实现 Rerank 追踪** 🔴 P0
  - **任务描述**: 各阶段追踪（格式同 7.1.1）
  - **TDD Cycle**: （参照 7.1.1 格式）
  - **验收标准**: 每个测试先失败，记录数据正确，测试输出无警告/错误
  - **devspec 参考**: 第 326-330 行

### Milestone 7.3: 技术方案实现

- [ ] ⏳ **7.3.1 实现 JSON Formatter** 🔴 P0
  - **任务描述**: 基于 Python logging + JSON Formatter 实现结构化日志
  - **TDD Cycle**: （参照 7.1.1 格式）
  - **验收标准**: 每个测试先失败，日志格式为 JSON，字段完整，测试输出无警告/错误
  - **devspec 参考**: 第 366 行

- [ ] ⏳ **7.3.2 实现 JSON Lines 日志写入** 🔴 P0
  - **任务描述**: 将 Trace 数据以 JSON Lines 格式追加写入
  - **TDD Cycle**: （参照 7.1.1 格式）
  - **验收标准**: 每个测试先失败，文件格式正确，追加写入正常，测试输出无警告/错误
  - **devspec 参考**: 第 366 行

- [ ] ⏳ **7.3.3-7.3.8 Streamlit Dashboard 组件** 🔴 P0/🟡 P1
  - **任务描述**: Dashboard 各组件（注意：UI 组件需自动化测试）
  - **TDD Cycle**:
    - **Test**: 编写组件逻辑单元测试（非 UI 渲染）
    - **Verify RED**: 运行测试确认失败
    - **GREEN**: 实现组件逻辑
    - **Verify GREEN**: 运行测试确认通过
  - **验收标准**:
    - [ ] 每个测试都先失败
    - [ ] 组件逻辑正确
    - [ ] **UI 需额外手动验证**
    - [ ] 测试输出无警告/错误
  - **devspec 参考**: 第 367-390 行

### Milestone 7.4: 配置实现

- [ ] ⏳ **7.4.1 实现 observability 配置项** 🔴 P0
  - **任务描述**: 实现可观测性相关配置
  - **TDD Cycle**: （参照 1.7.2 格式）
  - **验收标准**: 每个测试先失败，配置正确解析，测试输出无警告/错误
  - **devspec 参考**: 第 392-408 行

### ✅ Milestone 7.1 验收标准
- [ ] TraceContext 正常工作
- [ ] 所有阶段追踪正常记录
- [ ] JSON Lines 日志正常写入
- [ ] Streamlit Dashboard 正常运行
- [ ] 请求列表和详情页正常展示
- [ ] **TDD 验证**:
  - [ ] 每个方法都有先失败的测试
  - [ ] 所有测试通过
  - [ ] 测试输出无警告/错误

---

## Phase 8: MCP 服务实现

> **依赖分析**：依赖 Phase 6 的检索流水线完成。

### Milestone 8.1: 传输协议实现

- [ ] ⏳ **8.1.1 实现 stdio transport** 🔴 P0
  - **任务描述**: 实现 stdio 作为 MCP 传输协议

  - **TDD Cycle**:
    **Test 1: stdin/stdout 通信**
    - **RED**:
      - 编写 `test_stdio_communication_works()`
      - Mock stdin/stdout
      - 断言: 消息正确传输
    - **Verify RED**: 运行测试确认失败
    - **GREEN**: 配置 stdio transport
    - **Verify GREEN**: 运行测试确认通过

    **Test 2: JSON-RPC 2.0 协议**
    - **RED**:
      - 编写 `test_json_rpc_2_protocol_compliant()`
      - 发送 JSON-RPC 请求
      - 断言: 响应符合 JSON-RPC 2.0 规范
    - **Verify RED**: 运行测试确认失败
    - **GREEN**: 确保 MCP SDK 配置正确
    - **Verify GREEN**: 运行测试确认通过

  - **验收标准**:
    - [ ] 每个测试都先失败，观察失败原因正确
    - [ ] 能够通过 stdin/stdout 与 Client 通信
    - [ ] 正确实现 JSON-RPC 2.0 协议
    - [ ] 测试输出无警告/错误
  - **devspec 参考**: 第 179-187 行

- [ ] ⏳ **8.1.2 实现日志输出隔离** 🔴 P0
  - **任务描述**: 确保 stdout 仅输出 MCP 消息，日志输出到 stderr
  - **TDD Cycle**: （参照 8.1.1 格式）
  - **验收标准**: 每个测试先失败，stdout 无污染，日志正确输出到 stderr，测试输出无警告/错误
  - **devspec 参考**: 第 186 行

### Milestone 8.2: 核心工具实现

- [ ] ⏳ **8.2.1 实现 query_knowledge_hub 工具** 🔴 P0
  - **任务描述**: 实现主检索入口工具

  - **TDD Cycle**:
    **Test 1: 正常查询**
    - **RED**:
      - 编写 `test_query_knowledge_hub_executes_retrieval()`
      - Mock 检索流水线
      - 断言: 返回带引用的结构化结果
    - **Verify RED**: 运行测试确认失败
    - **GREEN**: 实现 query_knowledge_hub() 函数
    - **Verify GREEN**: 运行测试确认通过

    **Test 2: 指定 top_k 和 collection**
    - **RED**:
      - 编写 `test_query_with_top_k_and_collection()`
      - 断言: 参数正确传递给检索流水线
    - **Verify RED**: 运行测试确认失败
    - **GREEN**: 完善参数处理
    - **Verify GREEN**: 运行测试确认通过

  - **验收标准**:
    - [ ] 每个测试都先失败，观察失败原因正确
    - [ ] 执行完整的检索流程
    - [ ] 返回结果符合 MCP 工具规范
    - [ ] 测试输出无警告/错误
  - **devspec 参考**: 第 195-198 行

- [ ] ⏳ **8.2.2 实现 list_collections 工具** 🔴 P0
- [ ] ⏳ **8.2.3 实现 get_document_summary 工具** 🔴 P0
  - **任务描述**: 其他核心工具（格式同上）
  - **TDD Cycle**: （参照 8.2.1 格式）
  - **验收标准**: 每个测试先失败，测试输出无警告/错误
  - **devspec 参考**: 第 199-200 行

### Milestone 8.3: 返回内容与引用透明设计

- [ ] ⏳ **8.3.1 实现 Citation 格式** 🔴 P0
- [ ] ⏳ **8.3.2 实现 Markdown 格式引用** 🔴 P0
- [ ] ⏳ **8.3.3 实现 TextContent 返回** 🔴 P0
- [ ] ⏳ **8.3.4 实现 ImageContent 返回** 🔴 P0
  - **任务描述**: 内容返回和引用（格式同上）
  - **TDD Cycle**: （参照 8.2.1 格式）
  - **验收标准**: 每个测试先失败，格式正确，测试输出无警告/错误
  - **devspec 参考**: 第 210-229 行

### Milestone 8.4: 扩展工具实现

- [ ] ⏳ **8.4.1-8.4.4 扩展工具** 🟢 P2
  - **任务描述**: 扩展工具（格式同上）
  - **TDD Cycle**: （参照 8.2.1 格式）
  - **验收标准**: 每个测试先失败，测试输出无警告/错误
  - **devspec 参考**: 第 203-205 行

### ✅ Milestone 8.1 验收标准
- [ ] stdio transport 正常工作
- [ ] 核心工具正常工作
- [ ] 引用格式正确
- [ ] 多模态内容返回正常
- [ ] 能够与 MCP Client（如 Claude Desktop）通信
- [ ] **TDD 验证**:
  - [ ] 每个方法都有先失败的测试
  - [ ] 所有测试通过
  - [ ] 测试输出无警告/错误

---

## Phase 9: 多模态图片处理实现

> **依赖分析**：依赖 Phase 5 的 Transform 和 Phase 7 的 MCP 服务。

### Milestone 9.1: 图片提取与引用收集

- [ ] ⏳ **9.1.1 在 PDFLoader 中实现图片提取** 🔴 P0
  - **任务描述**: 从 PDF 中提取嵌入图片

  - **TDD Cycle**:
    **Test 1: 提取图片**
    - **RED**:
      - 编写 `test_pdf_loader_extracts_images()`
      - 使用包含图片的测试 PDF
      - 断言: 图片被正确提取
    - **Verify RED**: 运行测试确认失败
    - **GREEN**: 在 PDFLoader 中添加图片提取逻辑
    - **Verify GREEN**: 运行测试确认通过

    **Test 2: 生成唯一 image_id**
    - **RED**:
      - 编写 `test_image_id_is_unique()`
      - 提取多张图片
      - 断言: 每个 image_id 唯一
    - **Verify RED**: 运行测试确认失败
    - **GREEN**: 实现 image_id 生成逻辑
    - **Verify GREEN**: 运行测试确认通过

    **Test 3: 插入图片占位符**
    - **RED**:
      - 编写 `test_image_placeholder_inserted()`
      - 断言: 图片位置被正确标记
    - **Verify RED**: 运行测试确认失败
    - **GREEN**: 实现占位符插入
    - **Verify GREEN**: 运行测试确认通过

  - **验收标准**:
    - [ ] 每个测试都先失败，观察失败原因正确
    - [ ] 图片被正确提取
    - [ ] image_id 唯一
    - [ ] 占位符正确插入
    - [ ] 测试输出无警告/错误
  - **devspec 参考**: 第 425-436 行

### Milestone 9.2-9.5: 图文处理实现

- [ ] ⏳ **9.2.1 在 Splitter 中保留图片引用** 🔴 P0
- [ ] ⏳ **9.3.1 实现 CLIP 风格多模态向量** 🔴 P0
- [ ] ⏳ **9.4.1 在 Milvus 中存储图像向量** 🔴 P0
- [ ] ⏳ **9.4.2 实现文件系统图片存储** 🔴 P0
- [ ] ⏳ **9.5.1 实现混合检索图片支持** 🔴 P0
- [ ] ⏳ **9.5.2 实现多模态内容返回** 🔴 P0
  - **任务描述**: 其他多模态功能（格式同上）
  - **TDD Cycle**: （参照 9.1.1 格式）
  - **验收标准**: 每个测试先失败，测试输出无警告/错误
  - **devspec 参考**: 第 440-468 行

### ✅ Milestone 9.1 验收标准
- [ ] 图片被正确提取和存储
- [ ] 图像向量正确生成和存储
- [ ] 支持图文跨模态检索
- [ ] MCP 工具能返回图片
- [ ] **TDD 验证**:
  - [ ] 每个方法都有先失败的测试
  - [ ] 所有测试通过
  - [ ] 测试输出无警告/错误

---

## Phase 10: 评估框架实现

> **依赖分析**：依赖 Phase 1 的 Evaluator 接口定义。

### Milestone 10.1: Evaluator 实现

- [ ] ⏳ **10.1.1 实现 RagasEvaluator** 🟡 P1
  - **任务描述**: 实现 Ragas 评估框架集成

  - **TDD Cycle**:
    **Test 1: 继承 Evaluator**
    - **RED**:
      - 编写 `test_ragas_evaluator_is_evaluator()`
      - 断言: RagasEvaluator 是 Evaluator 的实例
    - **Verify RED**: 运行测试确认失败
    - **GREEN**: 创建 RagasEvaluator 类
    - **Verify GREEN**: 运行测试确认通过

    **Test 2: 计算 Faithfulness 指标**
    - **RED**:
      - 编写 `test_calculates_faithfulness_metric()`
      - Mock Ragas 框架
      - 断言: 返回 faithfulness 分数
    - **Verify RED**: 运行测试确认失败
    - **GREEN**: 实现 evaluate() 方法
    - **Verify GREEN**: 运行测试确认通过

  - **验收标准**:
    - [ ] 每个测试都先失败，观察失败原因正确
    - [ ] 支持 Faithfulness、Answer Relevancy、Context Precision 等指标
    - [ ] 测试输出无警告/错误
  - **devspec 参考**: 第 280 行

- [ ] ⏳ **10.1.2 实现 DeepEvalEvaluator** 🟡 P1
- [ ] ⏳ **10.1.3 实现 CustomMetricsEvaluator** 🟡 P1
- [ ] ⏳ **10.1.4 实现组合执行** 🟡 P1
- [ ] ⏳ **10.1.5 实现评估指标追踪** 🟢 P2
  - **任务描述**: 其他评估功能（格式同上）
  - **TDD Cycle**: （参照 10.1.1 格式）
  - **验收标准**: 每个测试先失败，测试输出无警告/错误
  - **devspec 参考**: 第 281-286, 337-340 行

### ✅ Milestone 10.1 验收标准
- [ ] 至少实现一个 Evaluator
- [ ] 评估框架可配置切换
- [ ] 评估指标正确记录
- [ ] **TDD 验证**:
  - [ ] 每个方法都有先失败的测试
  - [ ] 所有测试通过
  - [ ] 测试输出无警告/错误

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

## TDD 执行指南

### 核心原则

1. **NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST**
   - 必须先写测试，观察测试失败
   - 然后写最小代码通过测试
   - 最后重构优化

2. **Red-Green-Refactor 循环**
   - **RED**: 编写失败的测试
   - **Verify RED**: 运行测试，确认失败原因正确
   - **GREEN**: 编写最小代码通过测试
   - **Verify GREEN**: 运行测试确认通过
   - **REFACTOR**: 清理代码（保持测试通过）

3. **测试质量要求**
   - 每个测试只测试一个行为
   - 使用真实代码（mock 不可避免时除外）
   - 测试名称清晰描述行为
   - 测试输出无警告/错误

### 验收清单

每个 Milestone 完成时必须确认：
- [ ] 每个方法都有先失败的测试
- [ ] 观察到每个测试的预期失败
- [ ] 所有测试通过
- [ ] 测试输出无警告/错误
- [ ] 代码覆盖率达标

### 常见误区（避免）

- ❌ 写完代码再补测试 → 这是测试后行，不是 TDD
- ❌ 测试立即通过 → 证明测试无效，需重新设计
- ❌ 跳过观察测试失败 → 无法确认测试正确性
- ❌ 过度使用 mock → 应优先测试真实行为

---

**文档生成时间**: 2026-02-24
**依据文档**: devspec.md
**开发模式**: TDD (测试驱动开发)
