# 🏗️ NagarNirman

**NagarNirman** is a modern, "Boss UI" (Premier User Interface) city management system designed to streamline infrastructure reporting and administration. Built with **Streamlit**, it provides a platform for citizens to report issues like potholes, waste, and more, while giving authorities a powerful dashboard to manage them.

## 🌟 Features

-   **Glassmorphism Design**: A premium, dark-themed UI with translucent cards and vibrant accents.
-   **Interactive Map**: A visual representation of reports across the city.
-   **Role-Based Views**:
    -   **Citizen**: Submit reports with titles, types, descriptions, and location data.
    -   **Admin**: View all reports, filter by status, and update resolution status (Pending → Resolved).
-   **Modular Architecture**: Clean, industry-standard "Boss Code" structure (MVC pattern).

## 📂 Project Structure

This project follows a clean, modular architecture:

```text
NagarNirman/
├── app.py                  # 🚀 Main entry point of the application
├── assets/
│   └── style.css           # 🎨 Custom CSS for the "Boss UI" look
├── utils/
│   ├── data_manager.py     # 💾 Handles data operations (Mock DB simulation)
│   └── ui_manager.py       # 🖌️ Reusable UI components & styling helpers
├── views/
│   ├── dashboard.py        # 📊 Home & Map view logic
│   ├── report.py           # 📝 Report submission form logic
│   └── admin.py            # 👮 Admin dashboard & management logic
├── requirements.txt        # 📦 Project dependencies
└── README.md               # 📖 Project documentation
```

## 🚀 Getting Started

Follow these steps to run the project locally.

### Prerequisites

-   Python 3.8 or higher installed.

### Installation

1.  **Clone the repository** (if applicable) or download the source.
2.  **Navigate to the project directory**:
    ```bash
    cd "d:/Python-program/Python projects/NagarNirman"
    ```
3.  **Install Dependencies**:
    *You can create a virtual environment first if you prefer.*
    ```bash
    pip install streamlit pandas
    ```

### Running the App

Run the application using the Streamlit CLI:

```bash
streamlit run app.py
```

*Note: Do not run `main.py` if it exists (it is legacy). use `app.py`.*

## 🛠️ Tech Stack

-   **Frontend/Backend**: [Streamlit](https://streamlit.io/) (Python)
-   **Data Processing**: Pandas
-   **Styling**: Custom CSS (Glassmorphism & Neomorphism elements)
-   **Icons**: [Icons8](https://icons8.com/) (Embedded)

## 🤝 Contributing

1.  Fork the repository.
2.  Create a feature branch (`git checkout -b feature/AmazingFeature`).
3.  Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4.  Push to the branch (`git push origin feature/AmazingFeature`).
5.  Open a Pull Request.

---

**© 2025 NagarNirman** | Built with Python 🐍 & Passion ❤️
