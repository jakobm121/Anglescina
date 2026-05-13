# English Coach

Preprosta spletna aplikacija za učenje angleščine za slovensko govoreče uporabnike.

## Funkcije

- vadba besedišča,
- vadba slovnice,
- kratke pisne naloge,
- osnovno spremljanje napredka v seji brskalnika.

## Namestitev

```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
# venv\Scripts\activate   # Windows
pip install -r requirements.txt
python app.py
```

Nato odpri:

```text
http://127.0.0.1:5000
```

## Struktura projekta

```text
english-learning-web/
├── app.py
├── requirements.txt
├── data/
│   ├── vocabulary.json
│   ├── grammar.json
│   └── writing_prompts.json
├── static/
│   └── style.css
└── templates/
    ├── base.html
    ├── index.html
    ├── vocabulary.html
    ├── grammar.html
    ├── writing.html
    └── progress.html
```

## Ideje za nadgradnjo

- prijava uporabnikov,
- SQLite baza,
- dnevni streak,
- težavnostne stopnje,
- AI popravljanje pisanja,
- več vaj in kategorij.
