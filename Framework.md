# RAG System Framework: Data Ingestion and Injection

This document provides a detailed, step-by-step explanation of the data processing pipeline, from raw documents to an intelligent, queryable knowledge base.

---

## Part 1: Data Ingestion — From Raw File to Processed Chunks

"Ingestion" is the process of taking raw, unstructured documents and preparing them for the AI. In our system, this is handled by the **"Document Ingestion"** tab, which automates the extraction and chunking of text.

### Step 1: File Discovery
*   **Action:** The user specifies an **Input Folder Path** containing the raw documents (`.pdf`, `.docx`, `.txt`).
*   **Process:** The system scans this directory to identify all supported files. This is the starting point of the automated pipeline.

### Step 2: Text Extraction
*   **Action:** The system reads each discovered file one by one.
*   **Process:** The `DocumentProcessor` service is used to extract clean text from each file format.
    *   For **PDFs**, the `PyMuPDF` (fitz) library is used to read the document page by page and extract its text content. This library is highly effective even with complex layouts.
    *   For **Word Documents** (`.docx`), the `python-docx` library is used to parse the file and extract text from its paragraphs.
    *   For **Plain Text** (`.txt`), the file is read directly.
*   **Model Used:** No Large Language Model (LLM) is used at this stage. This is a deterministic process handled by specialized Python libraries.

### Step 3: Header Standardization
*   **Action:** Before chunking, a metadata header is prepared.
*   **Process:** The system generates a header line in the format: `Source: [Original_Filename]`. This is crucial for maintaining context and traceability.

### Step 4: Text Chunking
*   **Action:** The extracted text is split into smaller, uniform pieces.
*   **Process:** The system takes the full text and divides it into chunks of a maximum of **2,000 characters**. This size is a deliberate choice to balance context preservation with the token limits of most LLMs.

### Step 5: Final Assembly and Local Output
*   **Action:** Each chunk is saved as a new, separate Word document.
*   **Process:** For each chunk, the system:
    1.  Creates a new `.docx` file.
    2.  Writes the `Source:` header as the first line.
    3.  Writes the 2,000-character text chunk, with 80-character overlap.
    4.  Saves the file to the user-specified **Output Folder Path** with the naming convention: `[Original_Filename][Increment_Number].docx`.
*   **Result:** The output folder now contains a collection of standardized, chunked Word documents, ready for the next stage.

---

## Part 2: Data Injection — From Chunks to a Queryable Knowledge Base

"Injection" is the process of taking the prepared chunks and making them "understandable" to the AI by converting them into vector embeddings and storing them in a database. This is handled by the **"Documents"** tab.

### Step 1: File Upload and Pre-processing
*   **Action:** The user uploads one or more documents (`.pdf`, `.docx`, `.txt`) and optionally assigns a **Category**.
*   **Process:** The system uses the same `DocumentProcessor` service as in the ingestion phase to extract the text and split it into chunks. This time, however, the chunks are kept in memory for the next step.

### Step 2: Vector Embedding Generation
*   **Action:** Each text chunk is converted into a numerical representation (a vector embedding).
*   **Process:**
    1.  The system sends each text chunk to an external LLM API.
    2.  The LLM processes the text and returns a **vector embedding**—a list of numbers (in our case, 768) that represents the semantic meaning of the text.
*   **Model Used:** **Google Gemini's Embedding Model** (`models/text-embedding-004`). This model is specifically designed to convert text into high-quality vector embeddings for retrieval tasks.

### Step 3: Database Storage
*   **Action:** The document metadata and the vectorized chunks are stored in the local PostgreSQL database.
*   **Process:**
    1.  A new entry is created in the `documents` table, storing the filename, file type, and category.
    2.  For each chunk, a new entry is created in the `chunks` table, storing the original text of the chunk and its corresponding vector embedding.
*   **Model Used:** No LLM is used here. This is a standard database transaction handled by `psycopg`.

### Step 4: Querying the Knowledge Base
*   **Action:** The user asks a natural language question in the **"Ask Questions"** tab.
*   **Process:**
    1.  **Query Vectorization:** The user's question is sent to the **Google Gemini Embedding Model** to be converted into a vector embedding, just like the document chunks were.
    2.  **Similarity Search:** The system uses the `pgvector` extension in PostgreSQL to perform a similarity search. It compares the question's vector to the vectors of all the chunks in the database and retrieves the **Top-K** (e.g., the top 5) most semantically similar chunks.
    3.  **Context-Aware Synthesis:** The system then sends the user's original question along with the retrieved text chunks to the **Google Gemini Generation Model**.
    4.  The LLM reads the question and the provided context and generates a comprehensive, human-readable answer based *only* on the information in those chunks.
*   **Models Used:**
    *   **Google Gemini Embedding Model:** Used to vectorize the user's query.
    *   **Google Gemini Generation Model:** Used to synthesize the final answer from the retrieved context. This is where the "reasoning" happens.
