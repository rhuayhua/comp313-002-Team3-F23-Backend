# Jpas Backend

Backend for **Jpas**, a service that pulls technical skills and keywords out of job descriptions.

The repo has three parts:

| Part | What it does |
| --- | --- |
| `Capabilities/` | Flask API that returns keywords for a job description, using either a fixed keyword list or an LSTM model |
| `WebScrapping/` | Java + Selenium scraper that collects job postings |
| Root scripts | Data prep and model training used to build the files the API loads |

## Project structure

```
.
├── Capabilities/
│   ├── app.py                      # Flask app (port 8910)
│   ├── requirements.txt
│   ├── serviceslib/
│   │   ├── heuristic_service.py    # Regex match against a fixed keyword list
│   │   └── ml_service.py           # spaCy noun phrases + LSTM classifier
│   ├── lstm_weights.h5             # Trained LSTM weights
│   ├── CNN_model.keras             # Trained CNN model (not used by the API)
│   ├── embedding_matrix_w2v.pickle # Word2Vec embedding matrix
│   ├── tokenizer.pickle            # Keras tokenizer fitted on training data
│   └── model_dummy.pkl             # Baseline dummy classifier
├── WebScrapping/                   # Maven project: Selenium + TestNG scraper
├── job_postings.csv                # Scraped postings (position, description)
├── process_job_postings_script.py  # Extracts noun phrases from postings for labelling
├── CNN_LSTM_script.py              # Trains the CNN and LSTM models
└── Dockerfile
```

## How the ML endpoint works

1. Finds bullet-point lines in the job description (`•`, `·`, `-`, `1.`, `1)`).
2. Pulls noun phrases out of those lines with spaCy (`en_core_web_sm`).
3. Tokenizes and pads each phrase (max length 50), then embeds it with a 300-dimension Word2Vec matrix.
4. An LSTM classifier scores each phrase. Phrases scoring above **0.9** are returned as keywords.

## Running the API

### With Docker (recommended)

The ML service loads its files from `/app/Capabilities/...`, which matches the Docker image layout.

```bash
docker build -t jpas-backend .
docker run -p 8910:8910 jpas-backend
```

### Locally

```bash
cd Capabilities
pip install -r requirements.txt
python -m spacy download en_core_web_sm
python app.py
```

The server listens on `http://0.0.0.0:8910`.

> **Note:** `/ml` uses hardcoded paths under `/app/Capabilities/` in `serviceslib/ml_service.py`. Outside Docker, either change those paths or only use `/heuristics`.

## API

Both endpoints accept `GET` or `POST` with a JSON body and return:

```json
{ "keywords": ["..."] }
```

### `POST /heuristics`

Matches the description against a fixed list of terms (Java, Python, AWS, Kubernetes, CI/CD, and others).

```bash
curl -X POST http://localhost:8910/heuristics \
  -H "Content-Type: application/json" \
  -d '{"jobDescription": "Experience with Java, Jenkins and AWS."}'
```

### `POST /ml`

Uses the LSTM model. The body is a list of rows with `position` and `jobDescription`; only the first row is processed.

```bash
curl -X POST http://localhost:8910/ml \
  -H "Content-Type: application/json" \
  -d '[{"position": "Backend Developer", "jobDescription": "Requirements:\n- Build REST APIs in Python\n- Write unit tests"}]'
```

## Training pipeline

1. **Scrape postings** with the `WebScrapping` project (or use the included `job_postings.csv`).
2. **Extract noun phrases:** `python process_job_postings_script.py` writes `job_posting_noun_phrases.csv` and a de-duplicated `list_noun_phrases.xlsx` for manual labelling.
3. **Train models:** `CNN_LSTM_script.py` trains a CNN and an LSTM on the labelled phrases using pretrained Google News Word2Vec vectors (`GoogleNews-vectors-negative300.bin`).
4. Copy the resulting weights, tokenizer and embedding matrix into `Capabilities/`.

> `CNN_LSTM_script.py` reads `Data.csv` and `GoogleNews-vectors-negative300.bin` from the current folder. Change `root` and `word2vec_path` if your files live elsewhere.

## Web scraper

`WebScrapping/` is a Maven project built with Selenium 4, TestNG and Allure. It searches for a role and location and saves the job listings.

```bash
cd WebScrapping
mvn test -DsuiteXmlFile=TestNG/testng_Scrapping.xml
```

Requires Java, Maven and a Chrome/ChromeDriver setup that Selenium can use.

## License

MIT. See [LICENSE](LICENSE).
