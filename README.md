# AI Investigation Engine

RAG სისტემა, რომელიც პასუხობს კითხვებს დოკუმენტებსა და მონაცემთა ბაზაზე დაყრდნობით და ყოველ მტკიცებას წყაროს უთითებს.

## ცოცხალი დეპლოი

- Swagger UI: https://ai-investigation-engine-m22q.onrender.com/docs
- ბაზის URL: https://ai-investigation-engine-m22q.onrender.com

## არქიტექტურა

1. **კითხვის დაშლა (multi-hop):** Gemini (`gemini-3.1-flash-lite`) რთულ კითხვას ყოფს მაქსიმუმ 4 ქვე-კითხვად.
2. **ვექტორული ძიება:** ემბედინგები `BAAI/bge-small-en-v1.5` (FastEmbed, ლოკალურად), ვექტორული ბაზა Qdrant Cloud (კოლექცია `investigation_engine`, 384 განზომილება, Cosine).
3. **რერანკინგი:** `custom_hybrid_reranker` (search.py) აერთიანებს ვექტორულ ქულას (70%) და საკვანძო სიტყვების დამთხვევას (30%), ირჩევს ტოპ-3 ფრაგმენტს.
4. **გენერაცია:** Gemini პასუხობს მხოლოდ მოძიებული წყაროების საფუძველზე და ციტირებს მათ ([1], [2], ...). თუ ინფორმაცია არ არის, უნდა თქვას ეს.

## Endpoint-ები

- `POST /investigate`: სრული ციკლი (დაშლა → ძიება → რერანკინგი → პასუხი).
- `POST /documents`: იღებს ფაილს, ჭრის chunk-ებად (512 ტოკენი, 50 გადაფარვა), ამატებს Qdrant-ში `document_id`-ით.
- `DELETE /documents/{document_id}`: შლის ამ დოკუმენტის ყველა chunk-ს.

## მხარდაჭერილი ფორმატები

- **TXT, MD:** ტესტირებულია, მუშაობს.
- **PDF:** მუშაობს მხოლოდ ტექსტური (არასკანირებული) PDF-ებისთვის. სკანირებული PDF ვერ იკითხება, რადგან OCR არ არის.
- **DOCX:** ატვირთვა მუშაობს, მაგრამ ცხრილებსა და ტექსტურ ყუთებში არსებული ტექსტი არ იკითხება (იკითხება მხოლოდ ჩვეულებრივი პარაგრაფები).
- **JPG და სხვა:** მხარდაუჭერელია, სისტემა აბრუნებს 400-ს.

## გაშვება ლოკალურად

```bash
git clone https://github.com/Incel-ops/ai-investigation-engine.git
cd ai-investigation-engine
python -m venv venv
# Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# macOS / Linux:
source venv/bin/activate
pip install -r requirements.txt
```

შექმენით `.env` ფაილი პროექტის ფოლდერში:

```
GEMINI_API_KEY=your_gemini_key
QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_key
```


გაშვება:

```bash
uvicorn main:app --reload
```

## შედეგები (evaluation, 40 კითხვა)

| მეტრიკა | მნიშვნელობა |
|---|---|
| Answer Correctness | 72.50% |
| Recall@3 | 61.25% |
| Recall@6 | 85.00% |
| MRR | 0.929 |
| Citation Accuracy | 91.25% |

Citation Accuracy გამოთვლილია ხელახლა, ზემოთ აღნიშნული შეცდომის გასწორების შემდეგ. Answer Correctness მხოლოდ სტრიქონის შედარებაა, ამიტომ სწორ, მაგრამ სხვანაირად ფორმულირებულ პასუხებს ვერ ითვლის.

## ცნობილი შეზღუდვები

- Render-ის Free ტარიფზე სერვისი ძილში გადადის. პირველი მოთხოვნა შეიძლება 50 წამს გაგრძელდეს.
- `document_id`-ში ზედმეტი სივრცე (copy-paste-ით) იწვევს არასწორ წაშლას. ID უნდა შეიყვანოთ სუფთად.
- Gemini უფასო ტარიფზე აქვს დღიური და წუთობრივი ლიმიტი (429). ლიმიტის ამოწურვისას `/investigate` ვერ პასუხობს.
- თითო `/investigate` მოთხოვნა ორ Gemini გამოძახებას აკეთებს (დაშლა და პასუხი).
- DOCX-ის ცხრილები და ტექსტური ყუთები არ იკითხება.
- PDF-ისთვის OCR არ არის, სკანირებული ფაილი არ მუშაობს.
- Citation Accuracy გამოთვლილია წყაროების ინდექსების სწორი შედარებით.
- Tool calling (LLM-ის მიერ ინსტრუმენტის გამოძახება) არ არის რეალიზებული.
- კონფლიქტის აღმოჩენა ცალკე მექანიზმად არ არის რეალიზებული, მხოლოდ პრომპტში.
- chunking-ის ორი სტრატეგიის შედარება (მოთხოვნილი) არ არის შესრულებული evaluation-ში.
- Prompt Injection-ის ტესტი არ არის ჩატარებული.
- ფრონტენდი არ არის: ინტერფეისი მხოლოდ Swagger UI-ია.
