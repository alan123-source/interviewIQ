# InterviewIQ Resume Service

## 1. Resume Service Architecture

The Resume Service is responsible for handling resume uploads, extracting resume content, analyzing the content using AI, and storing the processed resume information.

The resume processing architecture follows a layered design:

```text
Frontend
    |
    v
Resume Router
    |
    v
Resume Service
    |
    +------------------+
    |                  |
    v                  v
PDF Service       Storage Service
    |
    v
Text Service
    |
    v
Resume AI Service
    |
    v
PostgreSQL
```

### Components

#### 1. Resume Router

The Resume Router provides the HTTP API for resume operations.

Its responsibilities include:

* Receiving resume uploads.
* Authenticating the current user.
* Validating uploaded files.
* Handling resume-related API requests.
* Returning responses and HTTP errors.

The router uses the `/resumes` prefix.

#### 2. Resume Service

The Resume Service coordinates the complete resume-processing workflow.

It connects the different services involved in processing a resume:

```text
Upload
  ↓
Storage
  ↓
PDF Extraction
  ↓
Text Cleaning
  ↓
AI Analysis
  ↓
Database Storage
```

This keeps the main business workflow separate from the HTTP router.

#### 3. PDF Service

The PDF Service extracts text from uploaded PDF files.

It receives the PDF as bytes and uses PyMuPDF to read the document and extract text from each page.

If the PDF cannot be processed, the service raises an extraction error.

#### 4. Text Service

The Text Service cleans and normalizes the text extracted from the PDF.

Its purpose is to make the resume text more suitable for further processing and AI analysis.

#### 5. Storage Service

The Storage Service manages the uploaded resume files.

Each uploaded resume is stored using a unique filename rather than the original filename.

The stored file path is associated with the corresponding resume record in the database.

The service also provides functionality to delete stored resume files.

#### 6. Resume AI Service

The Resume AI Service analyzes the cleaned resume text using Gemini.

The AI response is converted into the application's structured `ResumeAIData` schema.

The structured information includes:

* Personal information
* Summary
* Technical skills
* Tools
* Concepts
* Education
* Experience
* Projects
* Certifications
* Achievements

Pydantic validation ensures that the AI response follows the expected structure.

#### 7. PostgreSQL Database

PostgreSQL stores the processed resume information.

The `resumes` table stores:

* User ID
* Original filename
* File path
* Extracted text
* AI analysis
* Processing status
* Creation timestamp
* Update timestamp

The AI analysis is stored as structured JSON data.

## 2. Resume API Documentation

The Resume Service exposes REST API endpoints under the `/resumes` route prefix.

All resume endpoints require an authenticated user unless otherwise specified.

---

### 2.1 Upload Resume

**Endpoint**

```text
POST /resumes/upload
```

**Purpose**

Uploads a resume PDF and processes it through the Resume Service.

**Request Format**

The request uses `multipart/form-data`.

The uploaded file is sent using the field name:

```text
file
```

**Validation**

The following validations are performed:

* Only PDF files are accepted.
* Empty files are rejected.
* Files larger than 5 MB are rejected.
* The uploaded file must contain a valid PDF signature.

**Processing**

After validation, the resume is:

1. Saved to local storage.
2. Processed by the PDF Service.
3. Cleaned by the Text Service.
4. Analyzed by the Resume AI Service.
5. Validated against the `ResumeAIData` schema.
6. Stored in PostgreSQL.

**Response**

The endpoint returns information including:

* Resume ID
* Original filename
* Stored file path
* Content type
* File size
* Extracted text
* AI analysis
* Processing status
* User ID
* Creation timestamp
* Update timestamp

---

### 2.2 Get User Resumes

**Endpoint**

```text
GET /resumes/
```

**Purpose**

Returns all resumes belonging to the currently authenticated user.

The query filters resumes using the authenticated user's ID.

This prevents users from retrieving resumes belonging to other users through this endpoint.

---

### 2.3 Get Resume by ID

**Endpoint**

```text
GET /resumes/{resume_id}
```

**Purpose**

Returns a specific resume using its ID.

The endpoint verifies both:

```text
resume_id
+
authenticated user ID
```

Therefore, a user can only access a resume that belongs to their account.

If the resume does not exist or does not belong to the authenticated user, the API returns:

```text
404 Resume not found
```

---

### 2.4 Get Resume Skills

**Endpoint**

```text
GET /resumes/{resume_id}/skills
```

**Purpose**

Returns the skills and related technical information extracted from a resume.

The response contains:

```text
technical_skills
tools
concepts
```

The endpoint first verifies that the requested resume belongs to the authenticated user.

If AI analysis is unavailable, the endpoint returns:

```text
404 AI analysis not available
```

---

### 2.5 Delete Resume

**Endpoint**

```text
DELETE /resumes/{resume_id}
```

**Purpose**

Deletes a resume belonging to the authenticated user.

The operation performs two actions:

1. Deletes the resume record from PostgreSQL.
2. Deletes the corresponding resume file from local storage.

If the resume does not exist or does not belong to the authenticated user, the API returns:

```text
404 Resume not found
```

---

### Authentication

Resume endpoints use the application's existing authentication system.

The authenticated user's identity is obtained through:

```text
get_current_user
```

The user's ID is used to enforce ownership of resume records.

The ownership check follows this pattern:

```text
Authenticated User
        |
        v
     user_id
        |
        v
Find Resume
        |
        v
Resume.user_id == current_user.id
        |
   +----+----+
   |         |
  Yes       No
   |         |
Access     404
```

This ensures that users cannot access or delete resumes belonging to another account.

## 3. Resume Processing Data Flow

The resume processing workflow begins when an authenticated user uploads a PDF resume and ends when the processed resume information is stored in PostgreSQL.

### 3.1 Complete Processing Flow

```text
User
  |
  | Upload PDF
  v
Frontend
  |
  | multipart/form-data
  v
POST /resumes/upload
  |
  v
Authentication
  |
  v
File Validation
  |
  +---- Invalid ──> HTTP 400
  |
  v
Resume Service
  |
  v
Save PDF File
  |
  v
PDF Text Extraction
  |
  v
Text Cleaning
  |
  v
Extracted Text Validation
  |
  v
Gemini AI Analysis
  |
  v
Pydantic Schema Validation
  |
  v
Create Resume Record
  |
  v
PostgreSQL
  |
  v
API Response
```

### 3.2 Step-by-Step Processing

#### Step 1 — Resume Upload

The user selects a resume PDF through the frontend.

The frontend sends the file to:

```text
POST /resumes/upload
```

The request uses `multipart/form-data` because a PDF is binary data and cannot be sent as normal JSON.

---

#### Step 2 — Authentication

The request passes through the application's authentication system.

The `get_current_user` dependency identifies the currently authenticated user.

The user's ID is later stored with the resume record.

---

#### Step 3 — File Validation

The Resume Router validates the uploaded file before processing it.

The following checks are performed:

```text
Content Type
     ↓
File Empty?
     ↓
File Size
     ↓
PDF Signature
```

Invalid files are rejected before they reach the processing pipeline.

---

#### Step 4 — File Storage

The Resume Service saves the uploaded PDF using the Storage Service.

A unique UUID-based filename is generated.

For example:

```text
uploads/resumes/
└── 7c4f...a91.pdf
```

The original filename is still stored separately in the database.

This allows the system to avoid filename collisions.

---

#### Step 5 — PDF Text Extraction

The PDF Service receives the uploaded PDF bytes.

PyMuPDF reads the PDF and extracts text from each page.

For a multi-page resume:

```text
Page 1 → Text
Page 2 → Text
Page 3 → Text
   ↓
Combined Resume Text
```

If the PDF cannot be processed, the processing workflow stops and the stored file is removed.

---

#### Step 6 — Text Cleaning

The extracted text is passed to the Text Service.

The service cleans and normalizes the text so that it is more suitable for AI processing.

The cleaned text becomes the input for resume analysis.

---

#### Step 7 — Extracted Text Validation

The system checks whether enough text was successfully extracted.

If the extracted content is too short, the resume is rejected because meaningful resume information could not be obtained.

The uploaded file is removed when processing is stopped at this stage.

---

#### Step 8 — AI Resume Analysis

The cleaned resume text is sent to the Resume AI Service.

Gemini analyzes the resume and extracts structured information such as:

```text
Personal Information
Summary
Technical Skills
Tools
Concepts
Education
Experience
Projects
Certifications
Achievements
```

The AI service is instructed to extract only information explicitly present in the resume.

---

#### Step 9 — Schema Validation

The AI response is validated against the `ResumeAIData` Pydantic schema.

The schema ensures that the returned information has the expected structure and data types.

For example:

```text
technical_skills → List[str]
tools            → List[str]
concepts         → List[str]
education        → List[Education]
experience       → List[Experience]
projects         → List[Project]
```

If the AI response does not match the expected schema, processing fails rather than storing incorrectly structured data.

---

#### Step 10 — Database Storage

After successful processing, a `Resume` database object is created.

The database record contains:

```text
user_id
original_filename
file_path
extracted_text
ai_analysis
status
created_at
updated_at
```

The AI analysis is stored in PostgreSQL using a JSONB column.

---

#### Step 11 — API Response

After the database transaction succeeds, the API returns the processed resume information to the frontend.

The frontend can then use the returned information to display the resume details and extracted intelligence.

## 4. Error Handling and Failure Recovery

The Resume Service uses structured error handling to prevent failed resume processing from leaving incomplete data or unused files in the system.

### 4.1 File Validation Errors

File validation is performed before the resume enters the processing pipeline.

The following conditions result in an HTTP `400` response:

| Condition             | Response                           |
| --------------------- | ---------------------------------- |
| Non-PDF file          | `Only PDF files are allowed`       |
| Empty file            | `File is empty`                    |
| File larger than 5 MB | `File size must be less than 5 MB` |
| Invalid PDF content   | `Invalid PDF file`                 |

These checks prevent invalid files from reaching the PDF extraction and AI processing stages.

---

### 4.2 PDF Extraction Failure

If the PDF Service cannot process the uploaded document, a `ResumeExtractionError` is raised.

The Resume Service then:

1. Stops further processing.
2. Deletes the previously stored PDF file.
3. Returns an appropriate error to the API layer.

This prevents a failed resume from leaving an unnecessary file in storage.

---

### 4.3 AI Processing Failure

If Gemini analysis fails, the Resume AI Service raises an error.

The Resume Service handles the failure by:

1. Stopping the processing workflow.
2. Deleting the uploaded resume file.
3. Raising a `ResumeAIError`.
4. Returning an error response through the API.

The system also uses retry logic for temporary Gemini server failures.

The retry mechanism uses exponential backoff:

```text id="a1n5re"
Attempt 1
   ↓
Wait 1 × 2 seconds
   ↓
Attempt 2
   ↓
Wait 2 × 2 seconds
   ↓
Attempt 3
```

If the service remains unavailable after the maximum number of attempts, the processing operation fails.

---

### 4.4 Database Failure

The database operation is performed inside a transaction.

If storing the resume fails:

1. The database transaction is rolled back.
2. The uploaded file is deleted.
3. The database error is logged.
4. A `ResumeProcessingError` is raised.

This prevents the system from keeping a file when its corresponding database record was not successfully created.

---

### 4.5 Processing Failure Principle

The Resume Service follows a cleanup principle:

```text id="9wh3dx"
Processing starts
      |
      v
File stored
      |
      +---- Processing succeeds ----> Database record created
      |
      +---- Processing fails -------> Delete stored file
                                      |
                                      v
                                   Return error
```

This keeps file storage and database state consistent and prevents orphaned resume files.

## 5. Resume Storage Architecture

InterviewIQ currently uses local file storage for uploaded resume PDFs and PostgreSQL for resume metadata and processed information.

The physical PDF file and its database record are connected through the stored file path.

### 5.1 Storage Structure

Uploaded resumes are stored under:

```text
uploads/
└── resumes/
    ├── <unique-file-id>.pdf
    ├── <unique-file-id>.pdf
    └── ...
```

Each uploaded resume receives a unique UUID-based filename.

For example:

```text
uploads/resumes/550e8400-e29b-41d4-a716-446655440000.pdf
```

This prevents filename collisions when multiple users upload files with the same original filename.

---

### 5.2 Original Filename vs Stored Filename

The system maintains two different pieces of information.

**Original filename**

The filename provided by the user is stored in the database:

```text
original_filename
```

**Stored filename**

The actual PDF file is saved using a generated UUID:

```text
<uuid>.pdf
```

The database stores the relative location of this file using:

```text
file_path
```

For example:

```text
original_filename:
Alan_Resume.pdf

file_path:
uploads/resumes/550e8400-e29b-41d4-a716-446655440000.pdf
```

This separation provides predictable and collision-free file storage while preserving the filename shown to the user.

---

### 5.3 Relationship Between Storage and Database

The storage architecture can be represented as:

```text
                  Resume Upload
                       |
             ┌─────────┴─────────┐
             |                   |
             v                   v
       File Storage          PostgreSQL
             |                   |
             |              Resume Record
             |                   |
             └──── file_path ────┘
```

The PDF itself is stored in the file system, while PostgreSQL stores information about that file and the results of processing it.

The `Resume` database model contains:

```text
id
user_id
original_filename
file_path
extracted_text
ai_analysis
status
created_at
updated_at
```

---

### 5.4 File Deletion

When a resume is deleted, the system performs two operations:

```text
Delete Resume
      |
      ├── Delete database record
      |
      └── Delete physical PDF file
```

The stored `file_path` is used to locate and remove the corresponding PDF.

This prevents unnecessary files from remaining in storage after a resume has been deleted.

---

### 5.5 Current Storage Design

The current implementation uses local storage because InterviewIQ is being developed and tested in a local environment.

The storage service is isolated from the rest of the resume-processing logic.

This means the Resume Service does not need to directly manage file-system operations. Instead, it calls the Storage Service to save and delete files.

The architecture can later be extended to use cloud object storage without changing the overall resume-processing workflow.

## 6. Resume Intelligence and AI Extraction

The Resume Intelligence component converts unstructured resume text into structured information that can be used by other parts of InterviewIQ.

### 6.1 AI Extraction Flow

The AI extraction process follows:

```text
Resume PDF
    |
    v
PDF Text Extraction
    |
    v
Text Cleaning
    |
    v
Clean Resume Text
    |
    v
Gemini AI
    |
    v
Structured JSON
    |
    v
Pydantic Validation
    |
    v
ResumeAIData
    |
    v
PostgreSQL JSONB
```

The AI service receives only the cleaned resume text and extracts information that is explicitly present in the resume.

The system instructs the AI not to invent or assume information.

---

### 6.2 Structured Resume Data

The extracted information follows the `ResumeAIData` schema.

The schema contains:

```text
personal_info
summary
technical_skills
tools
concepts
education
experience
projects
certifications
achievements
```

This provides a consistent structure for resumes with different layouts and formats.

---

### 6.3 Skill Extraction

Skills are divided into three categories:

#### Technical Skills

Programming languages, frameworks, libraries, databases and other technical technologies.

Examples include:

```text
Python
JavaScript
React
FastAPI
PostgreSQL
```

#### Tools

Development tools, platforms and software used by the candidate.

Examples include:

```text
Git
GitHub
Docker
Swagger
Vercel
```

#### Concepts

Technical concepts or areas of knowledge mentioned in the resume.

Examples include:

```text
Data Structures and Algorithms
REST API
Authentication
```

This separation allows the application to use different categories of resume intelligence independently.

---

### 6.4 Skill Normalization

Extracted skills can appear in different forms.

For example:

```text
JS       → JavaScript
Postgres → PostgreSQL
```

The Skill Service normalizes recognized skill names into consistent representations.

For example:

```text
Input:
Python, JS, React, Postgres

Output:
Python, JavaScript, React, PostgreSQL
```

This improves consistency when skills are later used for searching, matching or comparison.

---

### 6.5 Schema Validation

The AI response is validated using Pydantic before it is stored.

For example:

```text
technical_skills → List[str]
tools            → List[str]
concepts         → List[str]
education        → List[Education]
experience       → List[Experience]
projects         → List[Project]
```

If the AI returns an incorrect data type, validation fails.

For example:

```text
Invalid:

technical_skills: "Python, React"

Expected:

technical_skills: ["Python", "React"]
```

This prevents malformed AI output from being stored as valid resume intelligence.

---

### 6.6 Storage of AI Analysis

After successful validation, the structured AI result is converted into a dictionary and stored in the `ai_analysis` JSONB column of the `resumes` table.

This allows the database to store the complete structured analysis while keeping the resume model flexible for future additions.

The data can later be used by InterviewIQ features such as:

* Resume dashboards
* Skill analysis
* Interview question generation
* Candidate profiling
* Job matching
* Interview preparation

---

### 6.7 Role of Resume Intelligence

The Resume Intelligence layer provides the foundation for future AI-powered interview features.

Instead of repeatedly analyzing the original PDF, InterviewIQ can use the structured resume information stored in the database.

```text
Resume
  |
  v
Structured Resume Intelligence
  |
  +── Skills
  +── Experience
  +── Projects
  +── Education
  +── Certifications
  |
  v
Future Interview Features
```

This makes the resume a reusable source of structured candidate information throughout the InterviewIQ system.
