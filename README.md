````  
```

That causes Markdown to break — the **folder structure won't render correctly** on GitHub.

---

```markdown
# CropFertilizer_prediction 🌱

A Flask-based web app that recommends the best crop and fertilizer based on:
- 🌾 Soil nutrients (N, P, K)
- 🌿 Crop type
- 💧 Soil moisture
- 🌦️ Real-time weather (temperature and humidity from user location)

## 🔧 Tech Stack
- Python, Flask
- Scikit-learn (ML models)
- HTML, CSS
- OpenWeatherMap API (for weather)

## 🧪 How to Run
1. Clone the repo  
2. Install dependencies: `pip install -r requirements.txt`  
3. Run: `python app.py`  
4. Open `http://localhost:5000`

---

## 📁 Project Structure

```
CropFertilizer_prediction/
│
├── app.py                         # Main Flask application
├── models.py                      # Helper/model code
├── crop_model.pkl                 # Trained ML model for crop prediction
├── fertilizer_model.pkl           # Trained ML model for fertilizer
├── crop_encoder.pkl               # Encoder for crop
├── soil_encoder.pkl               # Encoder for soil type
├── train_crop_model.py           # Script to train crop model
├── train_fertilizer_model.py     # Script to train fertilizer model
├── users.json                     # JSON file for user data
│
├── templates/                    # HTML templates for frontend
│   ├── index.html
│   ├── login.html
│   ├── home.html
│   ├── crop_result.html
│   └── ...
│
├── static/                       # Static files (CSS, images)
│   ├── css/
│   │   └── style.css
│   └── images/
│       ├── bg.png
│       └── background.png
│
├── requirements.txt              # List of required Python packages
├── .gitignore                    # Files/folders to ignore in Git
└── README.md                     # Project documentation
```

---

### ✅ Now What?

- Go to GitHub `README.md`
- Click ✏️ Edit → **Replace your current structure with this**
- Click ✅ **“Commit changes”**

Let me know if you want to add:
- 🔗 Live demo or deployment
- 📸 Screenshots
- 🪪 License section (MIT, etc.)  
You’re literally at the finishing touch!

```
