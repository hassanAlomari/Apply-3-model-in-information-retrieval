# 🔍 Multi-Model Information Retrieval Engine

An advanced, offline desktop application built with Python and Tkinter for extracting, processing, and retrieving information from PDF documents. This system implements multiple foundational Information Retrieval (IR) algorithms to rank and fetch the most relevant documents based on user queries.

---

## ✨ Key Features

* **PDF Parsing Engine:** Dynamically load, read, and extract text from multiple `.pdf` files locally using `PyPDF2`.
* **Multi-Model Search:** Choose between four distinct retrieval algorithms based on your precision requirements:
    1.  **Boolean Retrieval Model:** Evaluates exact logical queries using Postfix notation (`AND`, `OR`, `NOT`).
    2.  **Vector Space Model (VSM):** Ranks documents using TF-IDF and Cosine Similarity.
    3.  **Updated Vector Space Model:** An optimized or variant implementation of the standard VSM.
    4.  **Okapi BM25 Model:** A state-of-the-art probabilistic retrieval model with adjustable tuning parameters ($k_1$ and $b$).
* **Interactive GUI:** A clean, responsive desktop interface built with `tkinter` and `ttk` themes.
* **Dynamic Parameter Tuning:** Adjust the $k_1$ parameter directly from the GUI when using the BM25 model.

---

## 🏗️ System Architecture & Workflow

The following flowchart illustrates the internal pipeline of the system, from document ingestion to the final ranked output.

```mermaid
graph TD
    A[User Uploads PDF Files] --> B(PyPDF2 Text Extraction)
    B --> C{Document Corpus Dictionary}
    
    U[User Enters Query] --> D[Text Preprocessing]
    D --> E(Tokenization, Lowercasing, Stop-words Removal)
    
    C --> F[Select Retrieval Model]
    E --> F
    
    F -->|Boolean Model| G[Inverted Index & Postfix Evaluation]
    F -->|VSM / Updated VSM| H[TF-IDF Matrix & Vectorization]
    F -->|Okapi BM25| I[Probabilistic Term Weighting]
    
    G --> J[Exact Matching Doc IDs]
    H --> K[Cosine Similarity Ranking]
    I --> L[BM25 Score Ranking]
    
    J --> M((Ranked Results GUI Display))
    K --> M
    L --> M

    🧮 Mathematical BackgroundThe engine is powered by robust mathematical models implemented entirely from scratch using numpy and nltk.1. Vector Space Model (VSM)Documents and queries are represented as vectors in a multi-dimensional space. The similarity is calculated using the Cosine Similarity formula:$$ \text{Cosine}(Q, D) = \frac{Q \cdot D}{|Q| |D|} $$Where the weights are calculated using Term Frequency-Inverse Document Frequency (TF-IDF):$$ IDF(t) = \log\left(\frac{N}{df_t}\right) $$2. Okapi BM25The BM25 algorithm improves upon TF-IDF by penalizing excessively long documents and saturating term frequency. The ranking score is computed as:$$ \text{Score}(D, Q) = \sum_{i=1}^{n} IDF(q_i) \cdot \frac{f(q_i, D) \cdot (k_1 + 1)}{f(q_i, D) + k_1 \cdot \left(1 - b + b \cdot \frac{|D|}{avgdl}\right)} $$Where:$f(q_i, D)$ is the term frequency in the document.$|D|$ is the length of the document.$avgdl$ is the average document length in the corpus.$k_1$ (Term frequency saturation) and $b$ (Length normalization) are tunable parameters (Default: $k_1 = 1.5$, $b = 0.75$).🚀 Installation & SetupClone the repository:Bashgit clone [https://github.com/YourUsername/Your-Repo-Name.git](https://github.com/YourUsername/Your-Repo-Name.git)
cd Your-Repo-Name
Install dependencies:It is recommended to use a virtual environment. Install the required libraries using:Bashpip install pandas numpy nltk PyPDF2
Download NLTK Data:The application requires the English stopwords corpus. Open a Python terminal and run:Pythonimport nltk
nltk.download('stopwords')
Run the Application:Bashpython gui/app.py
🕹️ How to UseClick 📌 Attach PDF files and select one or multiple PDF documents from your machine.Verify the loaded documents in the left content pane.Enter your search terms in the Search Query field.Select your preferred Recovery Model from the dropdown menu.Note: If BM25 is selected, an additional input field will appear allowing you to tune the $k_1$ parameter (between 1.2 and 2.0).Click 🔍 Search to view the ranked results and their corresponding scores in the bottom pane.
