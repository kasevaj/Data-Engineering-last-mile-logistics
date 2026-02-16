## **This is a simulation project for learning how to stream data into a database and then showcase it on a dashboard.**

The dataset is a simulated delivery dataset from Kaggle.
Data streaming is simulated with a Python script that inserts rows into an SQLite database.
Data is processed and analyzed with Pandas.

The dashboard is built with Streamlit. It includes:
    KPI cards (average and p90 delivery times, total orders)
    Distribution of delivery times
    Filters by area, vehicle type and weather
    An interactive map of drop-off locations.

---

## 🛠️ Tech Stack

- **Node.js**
- **Express.js**
- **React**
- **JavaScript (ES6+)**
- Environment configuration using `.env`

---

## 🚀 Getting Started

### 1️⃣ Clone the repository

```bash
git clone https://github.com/kasevaj/Data-Engineering-last-mile-logistics.git
cd Data-Engineering-last-mile-logistics
```

---

### 2️⃣ Install dependencies

Install dependencies separately for backend and frontend.

#### Backend

```bash
cd backend
npm install
```

#### Frontend

```bash
cd ../frontend
npm install
```

---

### 3️⃣ Configure Environment Variables

Create a `.env` file inside the backend directory.

Example:

```env
PORT=5000
```

Add any required database or API credentials if applicable.

---

### 4️⃣ Run the Application

#### Start Backend

```bash
cd backend
npm run dev
```

Backend runs at:

```
http://localhost:5000
```

#### Start Frontend

```bash
cd frontend
npm start
```

Frontend runs at:

```
http://localhost:3000
```

---

## 🧪 How to Test

1. Start both backend and frontend.
2. Open browser at:

```
http://localhost:3000
```

3. Interact with the UI.
4. Monitor API calls in browser DevTools (Network tab).
5. Check backend logs in terminal.

---

<img width="545" height="369" alt="image" src="https://github.com/user-attachments/assets/0709d9ab-145d-47a5-9679-88aced7b2370" />

<img width="538" height="415" alt="image" src="https://github.com/user-attachments/assets/e5d9a67e-6dfc-4c84-829a-de75680e335e" />

