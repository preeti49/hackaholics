# Mama Care — Connected Healthcare Platform

Role-based healthcare coordination for patients, reception staff and doctors.

## Included workflows

- Secure account registration and sign-in with email-format and 8-character password validation.
- Patient portal for reports, appointments/tokens, insurance, prescriptions, visit history and multilingual AI assistance.
- Reception desk patient lookup, insurance updates, document extraction/review, missing-information follow-up and appointment/token creation.
- Doctor queue with live appointment status and prescriptions that immediately appear in the patient portal.

## Run locally

Open two terminals from this project folder.

```powershell
cd backend
pip install -r requirements.txt
python app.py
```

```powershell
cd frontend
npm install
npm run dev
```

Open `http://localhost:3000`. The API runs at `http://localhost:5000`.

Demo login password: `password123`

- Patient: `patient@mamacare.org`
- Doctor: `doctor@mamacare.org`
- Receptionist: `reception@mamacare.org`

## Production frontend build

```powershell
cd frontend
npm run build
```

Deploy the generated `frontend/dist` folder to a static host and serve the Flask API separately. Configure the frontend API base URL for the deployed backend before production release.
