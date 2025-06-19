# TimeTables 📅

Comprehensive academic schedule management system developed in Python, designed to facilitate the creation, administration and visualization of class schedules in an efficient and intuitive manner.

This project was initially designed for schedule management at the **Mathematics Academic Unit** of the **Autonomous University of Zacatecas (UAZ)**, later adapted for general use in educational institutions.

---

## 🔧 Prerequisites

Before getting started, make sure you have the following installed on your system:

| Requirement | Minimum Version | Description |
|-------------|-----------------|-------------|
| **Python** | 3.8+ | Main programming language |
| **pip** | Latest version | Python package manager |
| **git** | Any | Version control |
| **LaTeX** | Any | Required for PDF export functionality |

> **📝 Important note:** It is highly recommended to create a virtual environment to isolate project dependencies. On Linux systems, this is **mandatory**.

---

## ⚙️ Installation

### 1. Install LaTeX Distribution

LaTeX is required for PDF export functionality. Choose the appropriate distribution for your operating system:

**Windows:**
1. Download and install [MiKTeX](https://miktex.org/download) or [TeX Live](https://www.tug.org/texlive/windows.html)
2. Run the installer and follow the setup wizard
3. Verify installation by opening Command Prompt and typing:
   ```cmd
   pdflatex --version
   ```

**macOS:**
1. Install [MacTeX](https://www.tug.org/mactex/):
   ```bash
   # Using Homebrew (recommended)
   brew install --cask mactex
   
   # Or download the installer from the website
   ```
2. Verify installation:
   ```bash
   pdflatex --version
   ```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install texlive-full
```

**Linux (CentOS/RHEL/Fedora):**
```bash
# Fedora
sudo dnf install texlive-scheme-full

# CentOS/RHEL
sudo yum install texlive-collection-*
```

**Verify Linux installation:**
```bash
pdflatex --version
```

> **💡 Tip:** If you want a minimal LaTeX installation, you can install `texlive-latex-base` instead of the full version, but you may need to install additional packages as needed.

### 2. Clone Repository

```bash
git clone --depth 1 https://github.com/juan15377/TimeTables.git
cd TimeTables
```

### 3. Configure Virtual Environment (Recommended)

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On Linux/macOS:**
```bash
python -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Run Application

```bash
python -m src
```

---

## 🗄️ Database Architecture

TimeTables uses a relational database model implemented in **SQLite**, ensuring maximum compatibility and portability across different platforms and devices.

### Entity-Relationship Diagram
![ERD Diagram](./assets/ERD_TIMETABLE.png)

### Database Structure
- **17 interconnected tables** that model relationships between:
  - 👨‍🏫 **Teachers**
  - 🏫 **Classrooms**
  - 📚 **Subjects**
  - 👥 **Groups**
  - ⏰ **Schedules**

![Database View](./assets/view_database.png)

---

## 🖥️ User Interface

The application features a modern graphical interface developed with **DearPyGui**, offering an intuitive and efficient user experience.

### Main Window
Centralized interface with **6 main views** for complete system management:

![Main Window - Classroom Management](./assets/main_window_classrooms_manager_view.png)

### Subject Management
Complete visualization and administration of subjects assigned to teachers, classrooms and groups:

![Subject Manager](./assets/subjects_manager_window.png)

### Creating New Subjects
Dedicated window for efficient registration of new subjects in the system:

![New Subject](./assets/window_new_subject.png)

---

## 📊 Schedule System

### Constraint Visualization
The software provides advanced tools to visualize and manage schedule constraints, facilitating the creation of optimized academic calendars:

![Schedule Grid View](./assets/main_window_schedule_grid_view.png)

### PDF Export
Once the schedule is completed, the system allows **professional PDF export** using LaTeX to ensure high-quality documents:

![Exported Schedule](./assets/schedule_grid.png)

---

## ✨ Key Features

- 🔄 **Comprehensive Management**: Complete administration of teachers, classrooms, subjects and groups
- 📱 **Cross-platform**: Compatible with Windows, Linux and macOS
- 📈 **Advanced Visualization**: Tools to identify conflicts and optimize schedules
- 📄 **Professional Export**: High-quality PDF document generation
- 💾 **Robust Database**: Efficient and reliable storage system

---

## 🤝 Contributions

Contributions are welcome. For major changes, please open an issue first to discuss what you would like to change.

---

## Future Improvements

- Documentation
- Testing
- Bug fixes
- Interface responsiveness
- New export methods like Excel, Epub, etc.

---

## 📄 License

This project is under the GNU License. See the `LICENSE` file for more details.

---