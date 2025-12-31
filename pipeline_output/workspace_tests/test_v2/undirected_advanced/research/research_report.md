# Comprehensive Analysis of Retrieval-Augmented Generation (RAG) Architectures: Evolution, Implementation, and Frameworks

## Executive Summary

Retrieval-Augmented Generation (RAG) has evolved from a static technique for grounding Large Language Models (LLMs) into a dynamic, agentic paradigm capable of complex reasoning and self-correction. Originally proposed to mitigate hallucinations and knowledge cutoffs in parametric models, RAG has matured through three distinct phases: Naive RAG, Advanced RAG, and Modular RAG. Recent innovations in 2024 and 2025 have introduced sophisticated architectures such as **Self-RAG**, which utilizes reflection tokens for self-critique; **Corrective RAG (CRAG)**, which employs lightweight evaluators to trigger web search fallbacks; and **GraphRAG**, which leverages hierarchical community summarization for global dataset understanding.

Parallel to these architectural advancements, the implementation landscape is dominated by two primary frameworks: **LangChain** and **LlamaIndex**. While LangChain excels in orchestrating complex, stateful workflows and agentic behaviors (particularly through LangGraph), LlamaIndex provides superior abstractions for data ingestion, indexing, and efficient retrieval strategies. This report provides an exhaustive technical analysis of these architectures, their theoretical underpinnings, and their practical implementations, synthesizing data from over 100 authoritative sources.

### Key Findings
*   **Architectural Shift:** The field is moving away from linear "Retrieve-then-Generate" pipelines toward non-linear, iterative workflows (Modular RAG) where the model actively decides *when* and *what* to retrieve.
*   **Self-Correction:** Architectures like Self-RAG and CRAG demonstrate that adding a "critic" loop significantly improves factual accuracy and robustness against irrelevant context compared to Naive RAG.
*   **Global Reasoning:** Microsoft's GraphRAG addresses the "global query" limitation of vector-based RAG (e.g., "What are the main themes?") by summarizing graph communities, enabling holistic dataset comprehension.
*   **Framework Specialization:** LlamaIndex is the preferred choice for "Data-Centric" RAG (optimizing the index), while LangChain is the standard for "Agentic" RAG (optimizing the workflow).

---

## 1. Introduction to Retrieval-Augmented Generation

Retrieval-Augmented Generation (RAG) represents a hybrid architecture that combines the parametric memory of pre-trained Large Language Models (LLMs) with the non-parametric memory of external knowledge bases. First formalized by Lewis et al. in 2020, RAG was designed to address two fundamental limitations of LLMs: **hallucinations** (generating plausible but incorrect information) and **knowledge obsolescence** (inability to access information post-training) [1].

### 1.1 The Core Problem: Parametric vs. Non-Parametric Memory
LLMs, such as GPT-4 or Llama 3, store knowledge implicitly within their dense neural weights (parametric memory). This storage mechanism is lossy, static, and computationally expensive to update. In contrast, RAG systems maintain an external index (non-parametric memory)—typically a vector database—that can be updated in real-time without retraining the model.

The fundamental RAG equation can be expressed as:
\[ P(y|x) = \sum_{z \in TopK(x)} P_{\eta}(z|x) P_{\theta}(y|x, z) \]
Where:
*   \(x\) is the input query.
*   \(z\) represents the retrieved documents.
*   \(P_{\eta}\) is the retriever model (e.g., a dense bi-encoder).
*   \(P_{\theta}\) is the generator model (the LLM).

### 1.2 The Evolution Timeline
The evolution of RAG can be categorized into three distinct paradigms, as defined in recent surveys [2, 3, 4]:
1.  **Naive RAG (2020-2022):** A linear pipeline of Indexing, Retrieval, and Generation.
2.  **Advanced RAG (2023):** Introduction of pre-retrieval (query rewriting) and post-retrieval (reranking) optimizations.
3.  **Modular RAG (2024-Present):** A componentized approach allowing for iterative loops, branching, and agentic decision-making.

---

## 2. Naive RAG: The Baseline Architecture

Naive RAG represents the earliest and simplest implementation of the paradigm. It follows a strict "Retrieve-Read" process.

### 2.1 Architecture Components
1.  **Indexing:** Documents are split into chunks (e.g., 512 tokens) and encoded into vectors using an embedding model (e.g., OpenAI `text-embedding-3`, BGE-M3). These vectors are stored in a Vector Database (e.g., Pinecone, Milvus, Weaviate) [3, 5].
2.  **Retrieval:** The user's query is embedded into the same vector space. A similarity search (typically Cosine Similarity or Euclidean Distance) identifies the top-\(k\) most similar chunks.
3.  **Generation:** The retrieved chunks are concatenated with the original query into a prompt, which is fed to the LLM to generate a response [6, 7].

### 2.2 Limitations of Naive RAG
Despite its utility, Naive RAG suffers from significant drawbacks, often referred to as "retrieval failures" and "generation failures" [3, 8]:
*   **Low Precision (Hallucination):** If the retriever fetches irrelevant documents (noise), the LLM may hallucinate or produce incoherent answers ("Garbage In, Garbage Out").
*   **Low Recall (Missed Information):** The system may fail to retrieve the correct document if the query wording does not semantically match the document embedding, even if the answer exists.
*   **"Lost in the Middle" Phenomenon:** LLMs often struggle to utilize information located in the middle of a long context window, prioritizing information at the beginning or end [9].
*   **Lack of Global Understanding:** Naive RAG relies on local similarity. It cannot answer global questions like "Summarize the trends in this dataset" because the top-\(k\) chunks only represent a tiny fraction of the corpus [10, 11].

---

## 3. Advanced RAG: Optimizing the Pipeline

Advanced RAG introduces interventions before and after the retrieval step to improve the quality of the context fed to the LLM.

### 3.1 Pre-Retrieval Optimizations
These techniques modify the user's query to improve the likelihood of finding relevant documents.
*   **Query Rewriting:** Using an LLM to rewrite the query to be more precise or to align better with the document style [12].
*   **Query Expansion (Multi-Query):** Breaking a complex query into multiple sub-queries or generating variations of the query to broaden the search scope [12].
*   **HyDE (Hypothetical Document Embeddings):** Instead of embedding the query, the LLM generates a *hypothetical answer*. This hypothetical answer is embedded and used for retrieval. The intuition is that a hypothetical answer is semantically closer to the real answer document than the question is [13, 14, 15].
    *   *Mechanism:* Query \(\rightarrow\) LLM \(\rightarrow\) Hypothetical Document \(\rightarrow\) Embedding \(\rightarrow\) Retrieval.

### 3.2 Post-Retrieval Optimizations
These techniques refine the retrieved documents before generation.
*   **Reranking:** A specialized Cross-Encoder model (e.g., Cohere Rerank, BGE-Reranker) scores the relevance of the retrieved documents against the query. Unlike bi-encoders (used for fast retrieval), cross-encoders process the query and document together, providing higher accuracy but higher latency. The top documents are reordered, and the less relevant ones are discarded [16, 17].
*   **Context Compression:** Removing irrelevant sentences or tokens from the retrieved chunks to maximize the information density within the LLM's context window [16].

---

## 4. Modular RAG: The "LEGO" Framework

Modular RAG, formalized by Gao et al. (2024), represents a paradigm shift from linear pipelines to reconfigurable, graph-like flows. It treats RAG components (Retriever, Generator, Rewriter, Router) as independent modules that can be orchestrated in various patterns [2, 18, 19, 20, 21].

### 4.1 Core Modules
*   **Search Module:** Can search vector stores, knowledge graphs, or the web (e.g., Tavily, Serper) [5].
*   **Memory Module:** Maintains conversation history or long-term user preferences [5].
*   **Fusion Module:** Combines results from multiple retrieval strategies (e.g., Hybrid Search combining Keyword BM25 + Semantic Vector Search) using algorithms like Reciprocal Rank Fusion (RRF) [5].
*   **Routing Module:** Decides which path to take (e.g., "Is this a math question? Send to code interpreter. Is this a history question? Send to Vector DB") [5].

### 4.2 Patterns
Modular RAG enables complex patterns such as:
*   **Iterative RAG:** Repeatedly retrieving and generating to refine an answer.
*   **Recursive RAG:** Breaking a query down, solving sub-parts, and aggregating the results.
*   **Adaptive RAG:** Dynamically choosing the retrieval strategy based on query complexity.

---

## 5. Deep Dive: Self-RAG (Self-Reflective RAG)

**Self-RAG** (Asai et al., 2023) is a seminal architecture that introduces "self-reflection" into the generation process. Unlike standard RAG, which retrieves indiscriminately, Self-RAG trains the LLM to critique its own retrieval and generation quality using special tokens [22, 23, 24].

### 5.1 Mechanism: Reflection Tokens
Self-RAG fine-tunes an LLM (e.g., Llama 2) to generate specific "reflection tokens" during inference. These tokens act as internal control signals:
1.  **Retrieve Token (`[Retrieve]`):** Decides *if* retrieval is necessary. (Options: `Yes`, `No`, `Continue`).
2.  **Relevance Token (`[IsRel]`):** Evaluates if a retrieved document is relevant to the query. (Options: `Relevant`, `Irrelevant`).
3.  **Support Token (`[IsSup]`):** Checks if the generated response is supported by the retrieved document (hallucination check). (Options: `FullySupported`, `PartiallySupported`, `NoSupport`).
4.  **Utility Token (`[IsUse]`):** Assesses if the response is useful to the user. (Options: `Useful`, `NotUseful`) [23, 25, 26].

### 5.2 The Self-RAG Workflow
1.  **Assessment:** Given a query, the model predicts `[Retrieve]`. If `No`, it answers from parametric memory.
2.  **Retrieval:** If `Yes`, it retrieves \(D\) documents.
3.  **Parallel Generation:** For each document \(d \in D\), the model generates a candidate response segment and predicts `[IsRel]` and `[IsSup]`.
4.  **Critique & Selection:** The model scores the candidate segments based on the reflection tokens. It selects the best segment (e.g., one that is both Relevant and Supported) to append to the final response [25].

### 5.3 Implementation & Performance
Self-RAG significantly outperforms standard RAG and ChatGPT on benchmarks like PubHealth and PopQA, particularly in reducing hallucinations [27]. While the original paper relies on fine-tuning, "Self-RAG" workflows are often implemented in frameworks like LangGraph using prompt engineering with powerful models (GPT-4) to simulate the critic behavior without explicit training [28, 29].

---

## 6. Deep Dive: Corrective RAG (CRAG)

**Corrective RAG (CRAG)** (Yan et al., 2024) focuses specifically on the robustness of the retrieval step. It operates on the premise that retrieval is often imperfect and that the system should detect and correct low-quality retrieval results before generation [30, 31, 32].

### 6.1 The Lightweight Retrieval Evaluator
CRAG introduces a specialized "evaluator" model (often a smaller, faster LLM or a fine-tuned BERT) that assesses the relevance of retrieved documents and assigns a confidence score. Based on this score, it triggers one of three actions:
1.  **Correct:** The retrieved documents are relevant. Proceed to generation.
2.  **Incorrect:** The documents are irrelevant. Discard them and fall back to **Web Search** to find fresh information.
3.  **Ambiguous:** The documents are partially relevant. Combine the internal knowledge with Web Search results [33, 34, 35].

### 6.2 Decompose-then-Recompose
For documents deemed "Correct" or "Ambiguous," CRAG applies a "decompose-then-recompose" algorithm. It breaks documents into fine-grained strips, evaluates each strip, filters out irrelevant noise, and recomposes the high-value information. This minimizes the noise fed into the generator [34, 36].

### 6.3 Implementation
CRAG is highly effective for "high-stakes" environments where accuracy is paramount. It is often implemented using **LlamaIndex** (via the Corrective RAG Pack) or **LangGraph**, utilizing tools like Tavily AI for the web search fallback [37, 38, 39].

---

## 7. Deep Dive: Adaptive RAG

**Adaptive RAG** (Jeong et al., 2024) introduces a routing mechanism that adjusts the retrieval strategy based on the *complexity* of the user's query. It optimizes for both efficiency (latency/cost) and accuracy [40, 41, 42].

### 7.1 The Complexity Classifier
A classifier (often a smaller LLM) analyzes the query and categorizes it into one of three levels:
1.  **Simple (No Retrieval):** Queries the model can answer from parametric memory (e.g., "What is the capital of France?").
2.  **Moderate (Single-Step RAG):** Queries requiring specific factual lookups (e.g., "What are the features of the 2024 Toyota Camry?").
3.  **Complex (Multi-Step/Iterative RAG):** Queries requiring reasoning across multiple documents or steps (e.g., "Compare the revenue growth of Apple and Microsoft over the last 5 years and explain the primary drivers") [17, 42].

### 7.2 Dynamic Routing
Based on the classification, the system routes the query to the appropriate pipeline. This prevents "overkill" (using expensive multi-hop retrieval for simple questions) and "underperformance" (using simple retrieval for complex reasoning) [43, 44].

---

## 8. Deep Dive: GraphRAG (Microsoft)

**GraphRAG**, introduced by Microsoft Research in 2024, addresses a critical failure mode of vector-based RAG: **Global Sensemaking**. Standard RAG excels at "needle-in-a-haystack" queries (local retrieval) but fails at "haystack summarization" (global queries like "What are the main themes in these 10,000 emails?") because vector search only retrieves a few disparate chunks [10, 11, 45].

### 8.1 Architecture: From Local to Global
GraphRAG builds a structured Knowledge Graph (KG) from the raw text corpus using an LLM.
1.  **Indexing (Graph Construction):** The LLM extracts entities (People, Places, Orgs) and Relationships from the text.
2.  **Community Detection:** It uses algorithms like **Leiden** to cluster entities into hierarchical communities (e.g., a "Legal" community, a "Product" community).
3.  **Community Summarization:** The LLM generates a summary for *each* community. These summaries represent a high-level understanding of the dataset [46, 47, 48].

### 8.2 Query Processing
*   **Global Search:** For broad questions, GraphRAG uses the *community summaries* (not the raw text) to synthesize an answer. This allows it to "read" the entire dataset structure.
*   **Local Search:** For specific entity questions, it traverses the graph to find related concepts, offering better context than simple vector proximity [49, 50].

### 8.3 Performance
Microsoft reports that GraphRAG significantly outperforms Naive RAG on comprehensiveness and diversity metrics for global queries, though it incurs a higher upfront indexing cost [45, 51].

---

## 9. Deep Dive: Agentic RAG

**Agentic RAG** represents the convergence of RAG and Autonomous Agents. Instead of a fixed pipeline, an LLM acts as an "agent" with access to tools (Retrievers, Calculators, APIs) [52, 53].

### 9.1 Characteristics
*   **Autonomy:** The agent plans a sequence of actions. It might decide to search the vector DB, then search the web, then use a calculator, and finally synthesize the answer.
*   **Multi-Step Reasoning:** It can handle complex queries by breaking them down (e.g., "Find the CEO of Company X, then find their age, then calculate...").
*   **Tool Use:** The retriever is just one tool in the agent's toolkit [54, 55].

### 9.2 Multi-Agent RAG
This involves multiple specialized agents (e.g., a "Research Agent," a "Reviewer Agent," a "Writer Agent") collaborating to answer a query. Frameworks like **LangGraph** and **AutoGen** are key enablers here [33, 52].

---

## 10. Framework Analysis: LangChain vs. LlamaIndex

The implementation of these architectures relies heavily on two dominant open-source frameworks: **LangChain** and **LlamaIndex**. While they have overlapping capabilities, their design philosophies differ significantly [56, 57, 58, 59].

### 10.1 LlamaIndex: The Data Framework
**Philosophy:** "Data-Centric." LlamaIndex (formerly GPT Index) focuses on unlocking data for LLMs. It excels at ingestion, parsing, indexing, and retrieval [57, 59].

**Key Strengths:**
*   **Indexing:** Offers advanced index structures (Vector Store, Tree Index, Keyword Table, Knowledge Graph Index).
*   **Retrieval Efficiency:** Highly optimized for retrieval tasks. Features "Router Query Engines" and "Recursive Retrieval" out of the box.
*   **Structured Data:** Better handling of structured data (SQL) and hierarchical documents.
*   **Ease of Use:** Generally faster to set up a high-performance RAG pipeline (e.g., `VectorStoreIndex.from_documents()`) [56, 58, 60].

**Best For:** Building robust, production-grade RAG systems where data quality and retrieval accuracy are the primary bottlenecks.

### 10.2 LangChain: The Orchestration Framework
**Philosophy:** "Flow-Centric." LangChain is a general-purpose toolkit for building LLM applications. It focuses on chaining steps, managing memory, and orchestrating agents [57, 59].

**Key Strengths:**
*   **Flexibility:** The "Swiss Army Knife" of LLM apps. Can build anything from chatbots to autonomous agents.
*   **LangGraph:** A powerful extension for building stateful, cyclic, multi-agent workflows. This is the *de facto* standard for implementing complex architectures like Self-RAG and Adaptive RAG [28, 29, 39].
*   **Integrations:** Massive ecosystem of integrations (over 300+) [61].

**Best For:** Complex applications requiring multi-step reasoning, agentic behaviors, cyclic logic, or integration with many non-RAG tools.

### 10.3 Comparison Summary

| Feature | LlamaIndex | LangChain |
| :--- | :--- | :--- |
| **Primary Focus** | Data Indexing & Retrieval | Workflow Orchestration & Agents |
| **RAG Implementation** | Optimized, "out-of-the-box" advanced RAG | Flexible, requires manual assembly |
| **Agentic Capabilities** | Growing (LlamaAgents), but secondary | Core strength (LangGraph) |
| **Learning Curve** | Lower for RAG, Higher for Agents | Steeper (due to vast surface area) |
| **Best Use Case** | Enterprise Search, Knowledge Bases | Autonomous Agents, Complex Apps |

*Table synthesized from [56, 57, 58, 59, 60].*

---

## 11. Conclusion and Future Directions

The evolution of RAG from 2020 to 2025 has been characterized by a shift from **passive retrieval** to **active, agentic reasoning**.
*   **Naive RAG** is now considered a baseline, suitable only for simple prototypes.
*   **Modular RAG** provides the necessary flexibility for modern applications.
*   **Self-RAG** and **CRAG** have set new standards for accuracy by introducing self-correction loops.
*   **GraphRAG** has solved the problem of global dataset understanding.

**Future Trends:**
1.  **Hybrid Architectures:** Combining GraphRAG (for structure) with Vector RAG (for specificity) and Self-RAG (for reliability) [25].
2.  **Long-Context vs. RAG:** While LLMs with 1M+ token windows (e.g., Gemini 1.5) are emerging, RAG remains essential for latency, cost, and handling datasets larger than any context window (e.g., terabytes of enterprise data) [62].
3.  **Standardization:** Frameworks like LlamaIndex and LangChain are converging, with LlamaIndex adding workflow capabilities and LangChain improving data abstractions.

For researchers and engineers, the choice of architecture depends on the specific constraints of the use case: **CRAG** for high accuracy, **Adaptive RAG** for efficiency, and **GraphRAG** for complex sensemaking.

---

## References

### Publications
[56] "LangChain vs LlamaIndex: A Comprehensive Comparison for Retrieval-Augmented Generation (RAG)" (Tamanna). Medium, 2024. https://medium.com/@tam.tamanna18/langchain-vs-llamaindex-a-comprehensive-comparison-for-retrieval-augmented-generation-rag-0adc119363fe
[57] "LangChain vs LlamaIndex 2025: Complete RAG Framework Comparison" (Latenode). Latenode Blog, 2025. https://latenode.com/blog/platform-comparisons-alternatives/automation-platform-comparisons/langchain-vs-llamaindex-2025-complete-rag-framework-comparison
[60] "LlamaIndex vs LangChain: Which RAG tool is right for you?" (Mihai Farcas). n8n Blog, 2025. https://blog.n8n.io/llamaindex-vs-langchain/
[63] "LlamaIndex vs. LangChain: A comparison" (IBM). IBM Topics, 2024. https://www.ibm.com/think/topics/llamaindex-vs-langchain
[64] "LangChain vs LlamaIndex" (Reddit Discussion). Reddit r/LangChain, 2024. https://www.reddit.com/r/LangChain/comments/1bbog83/langchain_vs_llamaindex/
[18] "Modular RAG: Transforming RAG Systems into LEGO-like Reconfigurable Frameworks" (Gao et al.). arXiv:2407.21059, 2024. https://arxiv.org/abs/2407.21059
[19] "Modular RAG" (Deepchecks). Deepchecks Glossary. https://www.deepchecks.com/glossary/modular-rag/
[20] "A Comprehensive Guide to Implementing Modular RAG for Scalable AI Systems" (AI Engineer). Medium, 2024. https://medium.com/aingineer/a-comprehensive-guide-to-implementing-modular-rag-for-scalable-ai-systems-3fb47c46dc8e
[65] "Modular RAG using LLMs: What is it and how does it work?" (Samia Sahin). Medium, 2024. https://medium.com/@sahin.samia/modular-rag-using-llms-what-is-it-and-how-does-it-work-d482ebb3d372
[66] "Modular RAG: Transforming RAG Systems into LEGO-like Reconfigurable Frameworks" (Gao et al.). arXiv HTML, 2024. https://arxiv.org/html/2407.21059v1
[67] "Evolution of RAG Architecture in Large Language Models: A Comprehensive Review" (Perera et al.). IUP Journal of Information Technology, 2025. https://iupindia.in/ViewArticleDetails.asp?ArticleID=7913
[68] "Evolution of RAG in Generative AI" (Coralogix). Coralogix Blog, 2024. https://coralogix.com/ai-blog/evolution-of-rag-in-generative-ai/
[6] "The Evolution of Retrieval-Augmented Generation (RAG) in Large Language Models: From Naive to Agentic Systems" (Vamsi). Medium, 2025. https://medium.com/@vamsikd219/the-evolution-of-retrieval-augmented-generation-rag-in-large-language-models-from-naive-to-776956336c90
[69] "Evolution of a RAG Architecture" (ResearchGate). ResearchGate, 2025. https://www.researchgate.net/figure/Evolution-of-a-RAG-Architecture_fig2_394049293
[70] "Evolution of Retrieval-Augmented Generation (RAG) Architectures" (Saltmarch). YouTube, 2025. https://www.youtube.com/watch?v=BTn2x5WKJu4
[25] "Advanced RAG: Comparing GraphRAG, Corrective RAG, and Self-RAG" (JavaScript Plain English). Medium, 2025. https://javascript.plainenglish.io/advanced-rag-comparing-graphrag-corrective-rag-and-self-rag-e633cbaf5bf7
[33] "Beyond Vanilla RAG: The 7 Modern RAG Architectures Every AI Engineer Must Know" (Naresh). Dev.to, 2025. https://dev.to/naresh_007/beyond-vanilla-rag-the-7-modern-rag-architectures-every-ai-engineer-must-know-4l0c
[13] "A Comprehensive Guide to RAG Implementations" (Armand). Newsletter, 2024. https://newsletter.armand.so/p/comprehensive-guide-rag-implementations
[62] "Advanced RAG Variants: LongRAG, Self-RAG, and GraphRAG" (DasRoot). DasRoot Blog, 2025. https://dasroot.net/posts/2025/11/longrag-vs-self-rag-vs-graphrag/
[44] "RAG Architectures Every AI Developer Must Know: A Complete Guide" (Towards AI). Medium, 2025. https://pub.towardsai.net/rag-architectures-every-ai-developer-must-know-a-complete-guide-f3524ee68b9c
[71] "Types of RAG" (Exemplar). Exemplar Handbook. https://handbook.exemplar.dev/ai_engineer/rag/types_of_rag
[43] "Building an Effective RAG Pipeline: A Guide to Integrating Self-RAG, Corrective RAG, and Adaptive RAG" (GoOpenAI). Medium, 2024. https://blog.gopenai.com/building-an-effective-rag-pipeline-a-guide-to-integrating-self-rag-corrective-rag-and-adaptive-ab7767f8ead1
[72] "RAG Types" (Meilisearch). Meilisearch Blog, 2025. https://www.meilisearch.com/blog/rag-types
[30] "Corrective Retrieval Augmented Generation" (Yan et al.). OpenReview, 2024. https://openreview.net/forum?id=JnWJbrnaUE
[36] "Scaling Knowledge: RAG" (Substack). Scaling Knowledge, 2024. https://scalingknowledge.substack.com/p/rag
[31] "Corrective Retrieval Augmented Generation" (Yan et al.). arXiv:2401.15884, 2024. https://arxiv.org/abs/2401.15884?
[73] "An Overview of Methods to Effectively Improve RAG Performance" (Alibaba Cloud). Alibaba Cloud Blog, 2024. https://www.alibabacloud.com/blog/an-overview-of-methods-to-effectively-improve-rag-performance_601725
[9] "LongRAG: A Dual-Perspective RAG System" (ACL Anthology). EMNLP, 2024. https://aclanthology.org/2024.emnlp-main.1259.pdf
[74] "Retrieval-Augmented Generation (RAG) and LLM Integration" (Tural et al.). Semantic Scholar, 2024. https://www.semanticscholar.org/paper/Retrieval-Augmented-Generation-%28RAG%29-and-LLM-Tural-%C3%96rpek/8201d0c97667eb11711b1eb580d0a76e179b4268
[1] "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks" (Lewis et al.). NeurIPS, 2020. https://arxiv.org/abs/2005.11401
[2] "Modular RAG: Transforming RAG Systems into LEGO-like Reconfigurable Frameworks" (Gao et al.). Semantic Scholar, 2024. https://www.semanticscholar.org/paper/Modular-RAG%3A-Transforming-RAG-Systems-into-Gao-Xiong/21620a67bbef3a4c607bf17be07d42514163dfaf
[21] "Modular RAG: Transforming RAG Systems into LEGO-like Reconfigurable Frameworks" (Gao et al.). arXiv:2407.21059, 2024. https://arxiv.org/abs/2407.21059
[75] "Implementing Modular RAG with Haystack and Hypster" (Towards Data Science). Medium, 2024. https://towardsdatascience.com/implementing-modular-rag-with-haystack-and-hypster-d2f0ecc88b8f/
[66] "Modular RAG: Transforming RAG Systems into LEGO-like Reconfigurable Frameworks" (Gao et al.). arXiv HTML, 2024. https://arxiv.org/html/2407.21059v1
[22] "Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection" (Asai et al.). arXiv:2310.11511, 2023. https://arxiv.org/abs/2310.11511
[23] "Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection" (Asai et al.). NSF PAR, 2023. https://par.nsf.gov/servlets/purl/10539591
[45] "GraphRAG: Unlocking LLM discovery on narrative private data" (Larson & Truitt). Microsoft Research Blog, 2024. https://www.microsoft.com/en-us/research/blog/graphrag-unlocking-llm-discovery-on-narrative-private-data/
[32] "Corrective Retrieval Augmented Generation" (Yan et al.). arXiv HTML, 2024. https://arxiv.org/html/2401.15884v3
[34] "Corrective Retrieval Augmented Generation (CRAG) Paper Review" (Sulbha Jindal). Medium, 2025. https://medium.com/@sulbha.jindal/corrective-retrieval-augmented-generation-crag-paper-review-2bf9fe0f3b31
[28] "Self-RAG: A Guide With LangGraph Implementation" (DataCamp). DataCamp Tutorial, 2025. https://www.datacamp.com/tutorial/self-rag
[39] "Building a Self-Correcting RAG Pipeline with LangGraph" (Vishnu). Medium, 2025. https://medium.com/@vishnudhat/building-a-self-correcting-rag-pipeline-with-langgraph-a-practical-guide-b4add131d877
[26] "Self-RAG: Learning to Retrieve, Generate, and Critique" (Analytics Vidhya). Analytics Vidhya Blog, 2025. https://www.analyticsvidhya.com/blog/2025/01/self-rag/
[27] "Self-RAG: Self-Reflective Retrieval-Augmented Generation" (Samia Sahin). Medium, 2024. https://medium.com/@sahin.samia/self-rag-self-reflective-retrieval-augmented-generation-the-game-changer-in-factual-ai-dd32e59e3ff9
[10] "From Local to Global: A Graph RAG Approach to Query-Focused Summarization" (Edge et al.). arXiv:2404.16130, 2024. https://arxiv.org/abs/2404.16130
[40] "Adaptive-RAG: Learning to Adapt Retrieval-Augmented Large Language Models through Question Complexity" (Jeong et al.). NAACL, 2024. https://aclanthology.org/2024.naacl-long.389/
[41] "Adaptive-RAG: Learning to Adapt Retrieval-Augmented Large Language Models through Question Complexity" (Jeong et al.). arXiv:2403.14403, 2024. https://arxiv.org/abs/2403.14403
[42] "Adaptive RAG: Ultimate Guide to Dynamic Retrieval Augmented Generation" (MachineLearningPlus). MachineLearningPlus, 2025. https://www.machinelearningplus.com/gen-ai/adaptive-rag-ultimate-guide-to-dynamic-retrieval-augmented-generation/
[16] "Naive RAG, Advanced RAG and Modular RAG Architectures" (DevStark). DevStark Blog, 2025. https://www.devstark.com/blog/naive-rag-advanced-rag-and-modular-rag-architectures/
[3] "Evolution of RAGs: Naive RAG, Advanced RAG, and Modular RAG Architectures" (MarkTechPost). MarkTechPost, 2024. https://www.marktechpost.com/2024/04/01/evolution-of-rags-naive-rag-advanced-rag-and-modular-rag-architectures/
[5] "What are Naive RAG, Advanced RAG, Modular RAG Paradigms?" (Dr. Julija). Medium, 2024. https://medium.com/@drjulija/what-are-naive-rag-advanced-rag-modular-rag-paradigms-edff410c202e
[7] "RAG Techniques" (IBM). IBM Topics. https://www.ibm.com/think/topics/rag-techniques
[8] "Naive RAG, Advanced RAG, Modular RAG" (Plain English). Medium, 2025. https://ai.plainenglish.io/naive-rag-advanced-rag-modular-rag-b18b8669193e
[25] "Advanced RAG: Comparing GraphRAG, Corrective RAG, and Self-RAG" (JavaScript Plain English). Medium, 2025. https://javascript.plainenglish.io/advanced-rag-comparing-graphrag-corrective-rag-and-self-rag-e633cbaf5bf7
[46] "Microsoft GraphRAG: Redefining AI-Based Content Interpretation" (JingleMind). Medium, 2024. https://medium.com/@jinglemind.dev/microsoft-graphrag-redefining-ai-based-content-interpretation-and-search-part-1-6491dab0e2b3
[47] "Global Community Summary Retriever" (GraphRAG Docs). Microsoft GraphRAG Documentation, 2025. https://graphrag.com/reference/graphrag/global-community-summary-retriever/
[4] "Retrieval-Augmented Generation Systems: A Comprehensive Survey" (ResearchGate). ResearchGate, 2025. https://www.researchgate.net/publication/394999616_Retrieval-Augmented_Generation_Systems_A_Comprehensive_Survey_of_Architectures_Applications_and_Future_Directions
[12] "Advancements in RAG: A Comprehensive Survey" (Samia Sahin). Medium, 2025. https://medium.com/@sahin.samia/advancements-in-rag-a-comprehensive-survey-of-techniques-and-applications-b6160b035199
[14] "Chain of Thought, HyDE, Step-Back Techniques" (Mayank Pratap Singh). Blog, 2025. https://blogs.mayankpratapsingh.in/blog/chain-of-thought-hyde-step-back-techniques
[52] "Agentic RAG" (DataCamp). DataCamp Blog, 2025. https://www.datacamp.com/blog/agentic-rag
[53] "Agentic RAG" (IBM). IBM Think, 2025. https://www.ibm.com/think/topics/agentic-rag

### Code & Tools
[37] llama_index - Data framework for LLM applications. https://developers.llamaindex.ai/python/examples/workflow/corrective_rag_pack/
[61] llama-index-core - Core library for LlamaIndex. https://medium.com/the-ai-forum/implementing-advanced-rag-using-llamaindex-workflow-and-groq-bd6047299fa5
[76] langgraph - Library for building stateful, multi-actor applications with LLMs. https://github.com/langchain-ai/langgraph
[51] GraphRAG-Implementations - Repository for GraphRAG implementations. https://github.com/Artsplendr/GraphRAG-Implementations