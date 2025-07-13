# 🐍 30 Days Python Challenge – Indian Data Club

Welcome to my journey through the **#30DaysOfPython Challenge** by [Indian Data Club](https://indiandataclub.com)!  
This repository is where I'll be tracking and sharing my daily Python practice, projects, and learnings all in one place.

📌 **Roadmap:** [Click Here](https://indiandataclub.notion.site/30DaysOfPython-1f9a16c0422f8074bf29eee315a6802a)

---

## ✅ About the Challenge

The goal of this 30-day challenge is to build a solid foundation in Python from the basics to some advanced concepts while sharing progress publicly to stay consistent and learn together.

---

## 📓 Notebook

- All challenge questions and code are updated daily in a single Jupyter Notebook file: 📘 [Click here to view/download the Jupyter Notebook File](30DaysChallenge.ipynb).
  
- For the **Day 30 Challenge (Capstone Project)**, the code and dataset can be accessed from [here](pmpml_ridership). You can also access it through the below instructions.

---

## 🚍 Capstone Project: PMPML Ridership Dashboard

As a culmination of this challenge, I built a **PMPML Ridership Dashboard** using **Streamlit**, **Pandas**, **Matplotlib**, and **Lottie animations**.

This dashboard analyzes dummy PMPML bus ridership data to uncover passenger trends, peak routes, boarding stations, fare collection, and more. It's designed to show how data-driven insights can help enhance public transportation in Pune.

### ✨ Features
- Interactive filters for Year, Route, and Boarding Station.
- Tabs for Overview, Routes, Stations, Trends, Fare Collection, and full Documentation.
- Beautiful bus animation using Lottie.
- Custom CSS styling.
- Upload your own CSV file and explore!

### 📂 How to Run Locally

1. **Clone the Repository**
   ```bash
   git clone https://github.com/MohdAkif919/30-Days-Python-Challenge-IDC.git
   cd 30-Days-Python-Challenge-IDC/pmpml_ridership
   ```
2. **Create Virtual Environment (Recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate   # macOS/Linux
   venv\Scripts\activate      # Windows
   ```
4. **Install Requirements**
   ```bash
   pip install -r requirements.txt
   ```
5. **Run the Streamlit App**
   ```bash
   streamlit run app.py
   ```
6. **Upload Your CSV File**
   ```bash
   - Upload your PMPML ridership CSV file (data/pmpml_ridership_data.csv) when prompted.
   - Use the filters and tabs to explore the data and insights!
   ```

## 📁 Files in This Repository

- **`30DaysChallenge.ipynb`** - Daily Python practice notebook.

- **`pmpml_ridership/`**
  - **`app.py`** - Streamlit dashboard for the PMPML Ridership Capstone Project.
  - **`requirements.txt`** - All dependencies for easy setup.
  - **`style.css`** - Custom styles for the dashboard.
  - **`bus.json`** - Lottie animation file for the bus icon.
  - **`eda.py`** - Exploratory Data Analysis scripts.
  - **`plots.py`** - Python file for creating plots and charts.
  - **`utils.py`** - Utility functions used across the project.
  - **`data/`**
    - **`pmpml_ridership_data.csv`** — PMPML ridership dataset used for analysis and visualizations.

- **`.streamlit/`** - Streamlit configuration files.
- **`__pycache__/`** - Compiled Python files (auto-generated).

---

## 🔗 Connect with Me
Feel free to connect or follow my progress:
- **LinkedIn:** [mohdakif919](https://www.linkedin.com/in/mohdakif919/)
- **X (Twitter):** [@mohdakif919](https://x.com/mohdakif919)
- **Portfolio:** [View Portfolio](https://codebasics.io/portfolio/Mohd-Akif)

---

## ✨ Hashtags to Follow

Stay in the loop and see others’ progress too!  
Use and follow:  
**`#30DaysOfPython`** | **`#IDC30DaysChallenge`**
