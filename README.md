# Magic Point 🕒✨

![GitHub](https://img.shields.io/github/license/seu-usuario/ponto-magico)
![GitHub last commit](https://img.shields.io/github/last-commit/seu-usuario/ponto-magico)

Magic Point is a tool that simplifies the treatment of employee time clock markings, transforming raw records into valuable data for analysis.

## Features 🚀

- Automatic separation of Date and Day of the Week 📆
- Intelligent division of clock-ins ⏰
- Cleaning of justifications 🔍
- Generation of spreadsheet ready for analysis 📊

## How to Use 📝

1. **Download the Project:**
   Clone this repository or download the ZIP code.

2. **Installation:**
   Run the `install.bat` file to set up the virtual environment and install the dependencies, or manually install the dependencies using pip.
```bash
$ pip install -r requirements.txt
```

3. **Execution:**
   Open the terminal and navigate to the project folder. Run the command:
```bash
$ python3 PontoMagico.py
```

4. **Input:**
You will be asked for the path of the input spreadsheet (.xlsx). Enter the full path or drag the file to the terminal.

5. **Results:**
The program will perform the necessary treatments and create a new spreadsheet in the `treatments` folder.

## Example of Use 👁️‍🗨️

Suppose you have a spreadsheet `time_report.xlsx` with time clock markings. Run Magic Point and provide the path of the spreadsheet. After processing, you will find the treated spreadsheet in the `treatments` folder, ready for analysis.

## License 📜

---

This project is licensed under the MIT License - see the [LICENSE](LICENSE) ile for more details.


Made with 💪 by [Anderson Monteiro](https://github.com/Draken573) 💻
