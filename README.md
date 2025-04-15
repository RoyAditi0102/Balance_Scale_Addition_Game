# ⚖️ Balance Scale Addition Game

An interactive and educational web-based game designed to help young learners practice basic addition using a balance scale analogy.

## 🌐 Live Demo

🚀 [Click here to try it out!](https://balance-scale-addition-game-1.onrender.com)  
🔧 Backend API(Make sure to launch this first) : [https://balance-scale-addition-game.onrender.com](https://balance-scale-addition-game.onrender.com)


## 📦 Tech Stack

- **Frontend:** Vue.js (Vite)
- **Backend:** FastAPI (Python)
- **Auth & Database:** Firebase (Authentication + Firestore)
- **Deployment:** Render (Frontend & Backend)

---

## ✨ Features

- 🔢 Drag-and-drop number blocks onto a scale to balance the equation.
- 🔒 User authentication with Firebase (Login / Signup).
- 📊 Stores game history and scores per user using Firestore.
- 📱 Responsive and intuitive UI for desktop and mobile.
- 🎯 Real-time feedback to improve learning and engagement.

---

## 🛠️ Setup & Installation

### Prerequisites:
- Node.js & npm
- Python 3.9+
- Firebase project setup

### Clone the repository:
```bash
git clone https://github.com/yourusername/Balance-Scale-Addition-Game.git
cd Balance-Scale-Addition-Game
```

### Frontend Setup:
```bash
cd frontend
npm install
npm run dev
```

### Backend Setup:
```bash
cd backend
pip install -r requirements.txt
uvicorn fapi:app --reload
```

---


## 🧠 How to Play

1. Login or sign up.
2. Observe the scale and available number blocks.
3. Choose numbers onto the scale to make both sides equal.

---

## 🤝 Contributors

- **Aditi Roy** – Developer & Designer  
  [GitHub](https://github.com/RoyAditi0102)

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
