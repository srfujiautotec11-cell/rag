# Project Journey & Changelog

This document logs the key architectural decisions and code changes made throughout the development of the RAG system, presented in sequential order.

---

### **Change Log Entry 1: Correcting Vector Store Persistence**

*   **File Modified:** `services/vector_store.py`
*   **Reason:** An issue was identified where re-uploading an existing document did not update its content in the knowledge base. The logic was modified to ensure that when a document is processed, its old text chunks are first deleted from the database, guaranteeing a clean and complete re-ingestion.

---

### **Change Log Entry 2: Implementing the Document Ingestion Tab**

*   **File Modified:** `app.py`
*   **Reason:** To provide a dedicated space for pre-processing documents, the "Document Ingestion" tab was created. This feature allowed users to upload files, have them chunked into 2,000-character segments, and download them as individual `.docx` files.

---

### **Change Log Entry 3: Automating the Ingestion Workflow**

*   **File Modified:** `app.py`
*   **Reason:** The manual upload-and-download process was inefficient for larger document sets. The "Document Ingestion" tab was enhanced to use input and output folder paths, enabling fully automated, batch processing of entire directories.

---

### **Change Log Entry 4: Adding File Management to Ingestion Tab**

*   **File Modified:** `app.py`
*   **Reason:** To give users control over the generated files, a file management system was added. This feature scans the output directory and displays a list of processed files, allowing users to select and delete them individually or in bulk.

---

### **Change Log Entry 5: Implementing Multi-Document Deletion**

*   **File Modified:** `app.py`
*   **Reason:** The "Documents" tab initially only allowed for deleting one document at a time. This was upgraded to a more efficient form-based system with checkboxes, enabling users to select and delete multiple documents from the knowledge base in a single action.

---

### **Change Log Entry 6: Fixing "Select All" Functionality**

*   **File Modified:** `app.py`
*   **Reason:** A bug was discovered where the "Select All" checkbox did not correctly update the state of individual item checkboxes. The UI logic was refactored to use an `on_change` callback, ensuring the selection state is reliably synchronized across the interface.

---

### **Change Log Entry 7: Resolving the Category State Bug**

*   **File Modified:** `app.py`
*   **Reason:** It was noted that the "Category" field was not being saved correctly during document upload. This was caused by the widget losing its state during app reruns. The issue was resolved by assigning a unique key to the category input field, preserving its value in the session state.

---

### **Change Log Entry 8: Upgrading PDF Processing Library**

*   **File Modified:** `services/document_processor.py`
*   **Reason:** The initial PDF processing library (`PyPDF2`) was found to be unreliable. It was replaced with the more robust and accurate `PyMuPDF` (fitz) library, which significantly improved the success rate of text extraction from PDF files.
