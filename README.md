# TalentScreen (dummy test app)

A deliberately incomplete AI recruiting assistant used to test **Holistic AI Envelope**. It is not a real product, has no users and holds no secrets. The candidate data in `data/candidates.csv` is synthetic.

- `app/chatbot.py` – "Ava", a candidate-facing chatbot built on the Anthropic Messages API. It can shortlist or reject candidates through tools.
- `app/screening.py` – a scikit-learn model that scores applications.

Known gaps (on purpose): Ava never says it is an AI, model calls are not logged, and shortlist/reject actions run without a person approving them.

Run the tests with `pip install -r requirements.txt && python -m pytest`.
