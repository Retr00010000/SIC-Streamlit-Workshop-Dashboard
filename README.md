# Training Center Workshop Dashboard

An interactive Streamlit web application designed for a training center to monitor workshop performance, track learner participation, inspect ratings, and analyze operational costs.

Developed as part of the **Samsung Innovation Campus** Chapter 8 Streamlit task.

---

## Features

- **Multi-Page Navigation (Sidebar):**
  - **Overview:** Executive KPIs (Total Learners, Average Rating, Total Cost) with live deltas comparing filtered results to overall numbers, formula documentation (`st.latex`, `st.code`), and dataset health summary.
  - **Dataset Explorer:** Search courses by keyword, inspect the filtered dataset (`st.dataframe`), view track-level averages (`st.table`), and edit workshop details directly in-browser (`st.data_editor`).
  - **Insights:** Answers key operational questions, displays category distribution via grouped bar charts (`st.bar_chart`), and visualizes attendance trends over time with line charts (`st.line_chart`).
  - **Feedback:** Add notes that persist across page switches and reruns using Streamlit's `st.session_state`.

- **Interactive Filters:**
  - Track dropdown (`st.selectbox`)
  - Status multiselect (`st.multiselect`)
  - Minimum rating slider (`st.slider`)
  - Date range selector (`st.date_input`)
  - Minimum learners number input (`st.number_input`)
  - Raw dataset toggle (`st.checkbox`)

- **Performance & State:**
  - `@st.cache_data`: Caches dataset loading and date parsing to avoid re-reading disk files during user interactions.
  - `st.session_state`: Retains user notes across script reruns.
  - Safe error handling for empty filter results.

---

## Dataset (`workshops.csv`)

The dataset contains 28 workshop records with the following fields:
- `course`: Title of the training workshop
- `track`: Field of study (AI & Data Science, Web Development, Cloud & DevOps, Cybersecurity)
- `trainer`: Instructor leading the workshop
- `city`: Location (Riyadh, Jeddah, Dammam, Khobar)
- `date`: Workshop scheduled date (`YYYY-MM-DD`)
- `learners`: Number of enrolled learners
- `rating`: Workshop feedback rating (1.0 - 5.0)
- `cost`: Total workshop delivery cost in USD
- `status`: Delivery status (Completed, In Progress, Scheduled)

---

## Installation & Running Locally

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Retr00010000/SIC-Streamlit-Workshop-Dashboard.git
   cd SIC-Streamlit-Workshop-Dashboard
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Launch the Streamlit app:**
   ```bash
   streamlit run app.py
   ```

4. Open `http://localhost:8501` in your browser.

---

## Project Structure

```text
├── app.py              # Main Streamlit application
├── workshops.csv       # Training workshop dataset
├── banner.png          # Dashboard header banner
├── requirements.txt    # Python package dependencies
├── .gitignore          # Git ignore rules
└── README.md           # Project documentation
```
