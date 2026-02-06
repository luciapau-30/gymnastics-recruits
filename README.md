# 🤸 NCAA Gymnastics Recruit Database (2024–2027)

![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)

**Live Dashboard:** 🚀 [https://gymnastics-recruits-ohrtqszxjbcf5voognscce.streamlit.app/](https://gymnastics-recruits-ohrtqszxjbcf5voognscce.streamlit.app/)

A Python + Streamlit data application that tracks and analyzes **500+ NCAA gymnastics recruits** (2024-2027 classes), featuring data pipelines, custom ranking algorithms, and an interactive dashboard.

**If we have recruiting databases for football, why not for gymnastics?!** ⚡

Built to showcase **software engineering + data science skills** through real-world athlete data, compiled with the gymnastics community.

---

## ✨ Features

### 📊 Data Engineering Pipeline
- **Automated data cleaning** - Converts raw recruit spreadsheets into structured CSV format
- **Data validation** - Handles missing scores, inconsistent naming, and duplicate entries
- **Multi-year aggregation** - Combines 2024, 2025, 2026, and 2027 recruiting classes
- **Jupyter notebooks** for reproducible data processing (`/ntbks`)

### 🏅 Athlete Tracking System
- Tracks **Level 10** and **Elite** gymnasts across USA
- Coverage of all NCAA regions (1-6)
- School commitments and verbals
- Individual event scores when available:
  - **VT** - Vault
  - **UB** - Uneven Bars
  - **BB** - Balance Beam
  - **FX** - Floor Exercise
  - **AA** - All-Around average

### 🧮 Custom Ranking Algorithm
- Proprietary athlete rating system based on:
  - Event high scores (normalized by event)
  - All-Around averages
  - Perfect 10.0 achievement count
  - Elite status weighting
- Enables fair comparison across different competitions and scoring systems

### 🌐 Interactive Streamlit Dashboard
- **Real-time filtering** by region, level, and school
- **Top 10 recruits** leaderboard by All-Around score
- **Regional distribution** visualizations
- **Responsive design** - Works on desktop and mobile
- **Deployed live** on Streamlit Community Cloud

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| **Python 3.13** | Core language |
| **Pandas** | Data manipulation and analysis |
| **Streamlit** | Interactive web dashboard |
| **Plotly** | Interactive visualizations |
| **Matplotlib** | Static charts |
| **Jupyter Notebooks** | Data exploration and cleaning |
| **GitHub Actions** | CI/CD and app keepalive |

---

## 📊 Data Schema

The cleaned dataset (`cleaned_data.csv`) contains **20 fields**:

```python
{
  'athlete': str,           # Athlete name
  'dob': date,              # Date of birth
  'region': int,            # NCAA region (1-6)
  'school': str,            # Committed/verbal school
  'level': int,             # Competition level (10 or Elite)
  'vt_high': float,         # Vault high score
  'ub_high': float,         # Uneven bars high score
  'bb_high': float,         # Balance beam high score
  'fx_high': float,         # Floor exercise high score
  'aa_high': float,         # All-around high score
  'gym_insta': str,         # Gymnastics Instagram
  'personal_insta': str,    # Personal Instagram
  'club_gym': str,          # Club/training gym
  'state': str,             # Home state
  'year': int,              # Recruiting class year
  'grad_year': int,         # High school graduation year
  'country': str,           # Country (mostly USA)
  'is_elite': bool,         # Elite level flag
  'rating': float,          # Custom recruit rating
  'has_perfect10': bool     # Has scored 10.0 flag
}
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher
- pip or conda package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/luciapau-30/gymnastics-recruits.git
   cd gymnastics-recruits
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Streamlit app locally**
   ```bash
   streamlit run app.py
   ```

4. **Open in browser**
   - The app will automatically open at `http://localhost:8501`
   - Or visit the [live deployment](https://gymnastics-recruits-ohrtqszxjbcf5voognscce.streamlit.app/)

---

## 📁 Project Structure

```
gymnastics-recruits/
├── app.py                  # Main Streamlit dashboard
├── cleaned_data.csv        # Processed recruit dataset (500+ rows)
├── requirements.txt        # Python dependencies
├── README.md              # Project documentation
├── .github/
│   └── workflows/
│       └── keepalive.yml  # GitHub Actions for deployment
├── data/                   # Raw data files
│   ├── 2024s.csv
│   ├── 2025s.csv
│   ├── 2026s.csv
│   └── 2027s.csv
└── ntbks/                  # Jupyter notebooks
    ├── clean-data.ipynb   # Data cleaning pipeline
    ├── setup.ipynb        # Initial data exploration
    └── cleaned_data.csv   # Notebook output
```

---

## 💡 Usage Examples

### Filter by Region
Use the sidebar to select NCAA Region(s):
- **Region 1**: Northeast
- **Region 2**: Southeast
- **Region 3**: Mid-Atlantic
- **Region 4**: Midwest
- **Region 5**: South Central
- **Region 6**: West

### Find Top Recruits
The dashboard automatically displays the **Top 10 recruits by All-Around score** based on your filters.

### View Distribution
See how recruits are distributed across regions with the interactive bar chart.

### Export Data
Click the download button on any dataframe to export filtered results as CSV.

---

## 🎯 Key Learning Highlights

This project demonstrates proficiency in:

- **Data Engineering** - Building ETL pipelines with Pandas
- **Algorithm Design** - Creating custom ranking/scoring systems
- **Web Development** - Building interactive dashboards with Streamlit
- **Data Visualization** - Creating charts with Plotly and Matplotlib
- **Version Control** - Git workflow and GitHub collaboration
- **Cloud Deployment** - Deploying apps to Streamlit Community Cloud
- **CI/CD** - Automated workflows with GitHub Actions

---

## 🚀 Future Enhancements

- [ ] **Advanced analytics** - Trend analysis by region, school pipeline tracking
- [ ] **Recruiting timelines** - Visualize commitment dates and trends
- [ ] **School comparison** - Side-by-side roster strength analysis
- [ ] **Prediction model** - ML model to predict recruiting rankings
- [ ] **Social integration** - Pull Instagram stats for athlete engagement
- [ ] **Search functionality** - Find athletes by name or club gym
- [ ] **Historical data** - Include previous recruiting classes (2020-2023)
- [ ] **Mobile app** - React Native version for iOS/Android

---

## 📊 Data Insights

Based on the current dataset of 500+ recruits:

- **Most competitive region**: Region 6 (West Coast) - includes UCLA, Utah, Cal
- **Average All-Around score**: ~37.5 for Level 10 recruits
- **Elite representation**: ~5-8% of total recruits
- **Top programs**: SEC and Pac-12 schools dominate top 50 recruits

---

## 🤝 Contributing

This project was built collaboratively with the gymnastics community! Data was compiled from:
- Public recruiting announcements
- College Gym News
- Social media commitments
- Club gym Instagram pages

**Want to contribute?**
- Report data errors via GitHub Issues
- Submit updated recruit info via Pull Requests
- Suggest new features or analytics

---

## 📄 License

This project is open source and available for educational purposes.

**Data Attribution**: Recruit data compiled from publicly available sources and social media announcements. All data is used for educational and analytical purposes only.

---

## 🙏 Acknowledgments

- **College Gym News** - Recruiting updates and news
- **ChalkBucket Forums** - Community discussions
- **NCAA Gymnastics** - Official statistics and rosters
- **Streamlit** - Amazing framework for data apps
- **The gymnastics community** - For supporting women's NCAA gymnastics! 🤸‍♀️

---

## 📧 Contact

Questions or feedback? Open an issue on GitHub or connect via the repository!

---

**Built with 💜 for gymnastics fans and data enthusiasts**

*Go Gym!* 🤸‍♀️✨
