🔍 AI Investigation Engine
მრავალნაბიჯიანი RAG არქიტექტურაზე აგებული ინტელექტუალური საძიებო და საგამოძიებო ძრავა. სისტემა ამუშავებს რთულ კითხვებს, ატარებს ვექტორულ ძიებას, ჰიბრიდულ რერანკინგს და Google Gemini-ს მეშვეობით აგენერებს ფაქტებზე დაფუძნებულ პასუხებს წყაროების მკაცრი ციტირებით.

🌐 ცოცხალი დეპლოი (Live Deployment)
API დოკუმენტაცია (Swagger UI): https://ai-investigation-engine-m22q.onrender.com/docs

ბაზის URL: [https://ai-investigation-engine-m22q.onrender.com](https://ai-investigation-engine-m22q.onrender.com)

⚙️ არქიტექტურა და ფუნქციონალი
მრავალნაბიჯიანი დეკომოზიცია (Multi-Hop Reasoning): რთული კითხვები Google Gemini-ს (gemini-3.1-flash-lite) დახმარებით ავტომატურად იყოფა ატომურ ქვე-კითხვებად (მაქსიმუმ 4-მდე) მეტი სიზუსტისთვის.

მკვრივი ძიება და ჰიბრიდული რერანკინგი:

ემბედინგები: BAAI/bge-small-en-v1.5 (FastEmbed).

ვექტორული ბაზა: Qdrant Cloud (investigation_engine).

ჰიბრიდული რერანკერი: აერთიანებს ვექტორულ მსგავსებასა და ლექსიკურ/სათაურების დამთხვევებს (custom_hybrid_reranker), არჩევს ტოპ-3 ფრაგმენტს და წმენდს დუბლიკატებისგან.

დაფუძნებული გენერაცია (Grounded Generation): პასუხები გენერირდება მხოლოდ მოძიებული კონტექსტიდან, წყაროების სავალდებულო ინდექსაციით ([1], [2]), ჰალუცინაციების გარეშე.

დოკუმენტების მართვის სრული ციკლი: მხარდაჭერილია ფორმატები (.txt, .md, .pdf, .docx) სენტენცებზე დაფუძნებული ჭრით (chunk_size=512, chunk_overlap=50) და მყისიერი წაშლით იდენტიფიკატორის (document_id) მიხედვით.

📡 API ენდპოინტები
POST /investigate – ატარებს სრულ საგამოძიებო ციკლს (დეკომოზიცია -> ძიება -> რერანკინგი -> გენერაცია).

POST /documents – ტვირთავს, ჭრის და ინდექსირებს ახალ დოკუმენტს Qdrant ბაზაში.

DELETE /documents/{document_id} – შლის დოკუმენტთან დაკავშირებულ ყველა ვექტორულ ფრაგმენტს ბაზიდან.

🛠️ ადგილობრივი გაშვება (Local Setup)

დააკლონეთ რეპოზიტორია:
(Bash)
git clone https://github.com/Incel-ops/ai-investigation-engine.git
cd ai-investigation-engine

შექმენით და გააქტიურეთ ვირტუალური გარემო:
(Bash)
python -m venv venv
source venv/bin/activate  # Windows-ზე: venv\Scripts\activate

დააინსტალირეთ საჭირო ბიბლიოთეკები:
(Bash)
pip install -r requirements.txt

შეიყვანეთ გარემოს ცვლადები (.env ფაილი):
შექმენით .env ფაილი პროექტის მთავარ ფოლდერში და ჩაწერეთ:
(Code snippet)
GEMINI_API_KEY=თქვენი_გემინის_ქიი
QDRANT_URL=თქვენი_ქუადრანთის_ურლი
QDRANT_API_KEY=თქვენი_ქუადრანთის_ქიი

გაუშვით სერვერი:
(Bash)
uvicorn main:app --reload
👨‍💻 ავტორი
სანდო დიხამინჯია (Sandro Dikhaminjia)
