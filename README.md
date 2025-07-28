# Round 1B: Persona-Driven Document Intelligence

**Theme: "Connect What Matters — For the User Who Matters"**

## Challenge Overview

This system acts as an intelligent document analyst, extracting and prioritizing the most relevant sections from a collection of documents based on a specific persona and their job-to-be-done.

### Challenge Brief

You will build a system that processes diverse document collections and extracts the most relevant content based on:

- **Document Collection**: 3-10 related PDFs
- **Persona Definition**: Role description with specific expertise and focus areas
- **Job-to-be-Done**: Concrete task the persona needs to accomplish

The solution must be generic to handle diverse scenarios:

- **Documents**: Research papers, textbooks, financial reports, news articles, etc.
- **Personas**: Researcher, Student, Salesperson, Journalist, Entrepreneur, etc.
- **Jobs-to-be-Done**: Literature reviews, exam preparation, financial analysis, etc.

## Sample Test Cases

### Test Case 1: Academic Research

- **Documents**: 4 research papers on "Graph Neural Networks for Drug Discovery"
- **Persona**: PhD Researcher in Computational Biology
- **Job**: "Prepare a comprehensive literature review focusing on methodologies, datasets, and performance benchmarks"

### Test Case 2: Business Analysis

- **Documents**: 3 annual reports from competing tech companies (2022-2024)
- **Persona**: Investment Analyst
- **Job**: "Analyze revenue trends, R&D investments, and market positioning strategies"

### Test Case 3: Educational Content

- **Documents**: 5 chapters from organic chemistry textbooks
- **Persona**: Undergraduate Chemistry Student
- **Job**: "Identify key concepts and mechanisms for exam preparation on reaction kinetics"

## Technical Requirements

### Constraints

- **CPU Only**: No GPU acceleration allowed
- **Model Size**: ≤ 1GB
- **Processing Time**: ≤ 60 seconds for document collection (3-5 documents)
- **No Internet Access**: All processing must be offline

### Required Output Format

The system must produce a JSON output with the following structure:

```json
{
  "metadata": {
    "input_documents": ["list of document filenames"],
    "persona": "User Persona",
    "job_to_be_done": "Task description",
    "timestamp": "ISO format timestamp"
  },
  "extracted_sections": [
    {
      "document": "source.pdf",
      "page_number": 1,
      "section_title": "Section Title",
      "importance_rank": 1
    }
  ],
  "subsection_analysis": [
    {
      "document": "source.pdf",
      "refined_text": "Extracted and refined content",
      "page_number": 1
    }
  ]
}
```

## Implementation

### Architecture

The system consists of three main modules:

1. **Parser** (`modules/parser.py`): Extracts sections from PDF documents
2. **Ranker** (`modules/ranker.py`): Uses semantic similarity to rank sections by relevance
3. **Formatter** (`modules/formatter.py`): Formats the final JSON output

### Core Technologies

- **Semantic Ranking**: Sentence Transformers (all-MiniLM-L6-v2)
- **PDF Processing**: PyMuPDF
- **ML Framework**: PyTorch
- **Text Processing**: NLTK, scikit-learn

### Key Features

- **Persona-Driven Analysis**: Custom query building based on persona and task
- **Semantic Relevance**: Cosine similarity scoring for content ranking
- **Diversity Optimization**: Penalizes duplicate document selections
- **Content Filtering**: Removes generic or low-quality sections
- **Structured Output**: Comprehensive JSON with metadata and analysis

## Project Structure

```
├── main.py                          # Main execution script
├── requirements.txt                 # Python dependencies
├── Dockerfile                      # Container configuration
├── modules/                        # Core implementation modules
│   ├── __init__.py
│   ├── parser.py                   # PDF section extraction
│   ├── ranker.py                   # Semantic ranking engine
│   └── formatter.py                # Output formatting
├── Challenge_1b/                   # Test collections
│   ├── Collection 1/               # Travel Planning
│   ├── Collection 2/               # Adobe Acrobat Learning
│   └── Collection 3/               # Recipe Collection
└── Expected Outputs/               # Expected results for validation
```

## Usage

### Local Development

1. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

2. **Run Analysis**:
   ```bash
   python main.py
   ```

### Docker Deployment

1. **Build Container**:

   ```bash
   docker build -t persona-document-intelligence .
   ```

2. **Run Analysis**:

   ```bash
   docker run --rm -v $(pwd)/Challenge_1b:/app/Challenge_1b --network none persona-document-intelligence
   ```

   The output will be generated in `Challenge_1b/Collection_x/challenge1b_output.json` where x is collection number (1-3)

## Test Collections

### Collection 1: Travel Planning

- **Persona**: Travel Planner
- **Task**: Plan a 4-day trip for 10 college friends to South of France
- **Documents**: 7 travel guides covering cities, cuisine, history, restaurants, activities, tips, and culture

### Collection 2: Adobe Acrobat Learning

- **Persona**: HR Professional
- **Task**: Create and manage fillable forms for onboarding and compliance
- **Documents**: 15 Acrobat guides covering creation, editing, exporting, AI features, e-signatures, and sharing

### Collection 3: Recipe Collection

- **Persona**: Food Contractor
- **Task**: Prepare vegetarian buffet-style dinner menu for corporate gathering
- **Documents**: 9 cooking guides covering breakfast, lunch, dinner mains, and sides

## Performance Metrics

The system is evaluated on:

- **Relevance**: How well extracted sections match the persona's needs
- **Completeness**: Coverage of important information across documents
- **Efficiency**: Processing time within 60-second constraint
- **Accuracy**: Semantic understanding of persona and task requirements

## Approach Explanation

The system uses a three-stage pipeline:

1. **Document Parsing**: Extracts structured sections from PDFs with page numbers and titles
2. **Semantic Ranking**: Uses sentence transformers to compute relevance scores based on persona and task
3. **Output Generation**: Formats ranked sections into the required JSON structure with metadata

The ranking algorithm employs:

- **Query Building**: Creates context-aware queries from persona and task
- **Similarity Scoring**: Cosine similarity between query and content embeddings
- **Diversity Optimization**: Penalizes duplicate document selections
- **Quality Filtering**: Removes short or generic content sections

This approach ensures the system can handle diverse document types, personas, and tasks while maintaining high relevance and performance within the specified constraints.

---

**Note**: This implementation meets all technical requirements including CPU-only processing, model size constraints, and offline operation while providing robust semantic analysis capabilities.
