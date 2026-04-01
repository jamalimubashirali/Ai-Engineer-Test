# Q5: System Architecture Diagram for AI-Powered Ad Personalization Engine

```mermaid
graph TD
    %% Define Client Layer
    subgraph Client [Client-Side (E-Commerce Storefront)]
        UI[Web/Mobile Interface]
        Tracker[User Behavior Tracker]
    end

    %% Define API Gateway
    API[API Gateway / Load Balancer]

    %% Define Microservices
    subgraph Services [Backend Microservices]
        AdEngine[Ad Decision Engine]
        ProfileAgg[User Profile & Context Aggregator]
        ContentGen[AI Content Generation Service]
    end

    %% Define Data & AI Layer
    subgraph DataAI [Data & AI Infrastructure]
        Cache[(Low-Latency Cache - Redis)]
        DB[(User & Product DB - PostgreSQL)]
        VectorDB[(Vector DB - Chroma/Pinecone)]
        LLM[LLM API - OpenRouter/OpenAI]
        Assets[Asset Storage - S3]
    end

    %% Define Workflows / Pipelines
    subgraph Offline [Offline / Async Pipelines]
        DataPipeline[Data Ingestion Streaming - Kafka/Kinesis]
        Embedder[Embedding & Indexing Worker]
    end

    %% Connections
    UI -- "1. Request Ad Component" --> API
    Tracker -- "Clickstream / Events" --> DataPipeline

    API -- "2. Fetch Ad context" --> AdEngine
    AdEngine -- "3. Get User Segment" --> ProfileAgg

    ProfileAgg -- "Read user history" --> DB
    ProfileAgg -- "Read session state" --> Cache
    ProfileAgg -.-> AdEngine

    AdEngine -- "4. Request creative variants" --> ContentGen

    ContentGen -- "5. Semantic Search context" --> VectorDB
    ContentGen -- "6. Generate Copy/Image params" --> LLM
    LLM -.-> ContentGen

    ContentGen -- "Fetch static assets" --> Assets
    ContentGen -.-> AdEngine

    AdEngine -- "7. Return personalized JSON Ad" --> API
    API -.-> UI

    %% Offline sync
    DataPipeline --> DB
    DataPipeline --> Embedder
    Embedder --> VectorDB

    classDef standard fill:#f9f9f9,stroke:#333,stroke-width:2px;
    classDef ai fill:#cce5ff,stroke:#0066cc,stroke-width:2px;
    classDef db fill:#e2efda,stroke:#548235,stroke-width:2px;

    class LLM,ContentGen,VectorDB,Embedder ai;
    class Cache,DB,Assets db;
```

## Architecture Explanation:

1. **Real-time Engine:** When a user hits the storefront (UI), a request routes through the API Gateway to the Ad Decision Engine.
2. **Context Aggregation:** The Profile Aggregator fetches the user's historical data (from PostgreSQL) and current real-time session intent (from Redis).
3. **AI Generation:** The Content Generation Service uses this context to query a Vector DB for relevant past top-performing campaigns, then prompts the LLM (via OpenRouter/OpenAI) to generate hyper-personalized ad copy and select relevant imagery.
4. **Latency Buffering:** Due to LLM latency, the system likely pre-generates & caches ad variants for known user segments asynchronously. For real-time generation, it relies on fast, smaller models (like Claude-3-Haiku) to construct the ad JSON within hundreds of milliseconds.
5. **Continuous Learning:** The Data Ingestion pipeline captures clicks/conversions via Kafka, feeding back into the Database and updating Vector Embeddings to constantly improve the RAG context for future ad generation.
