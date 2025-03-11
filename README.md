# Project "QRLogic" | Проєкт "QRLogic"

## __Purpose of the Project__ | __Мета створення проєкту__

This project was created as a practice over a Django module. Its purpose was to learn the key features of the module and improve our coding skills<br> <br> Цей проєкт створений для практики з модулем Django. Його метою було вивчити ключові можливості модуля, вдосконалити наші скіли в кодингу

## __Plan-navigation for README__ | __План-навігація по README__
[Purpose of the Project | Мета створення проєкту](#purpose-of-the-project--мета-створення-проєкту)<br>
[Team members | Склад команди](#team-members--склад-команди)<br>
[Project installation guide | Інструкція до встановлення проєкту](#project-installation-guide--інструкція-до-встановлення-проєкту)<br>
[Useful project-related links | Корисні посилання стосовно проекту](#useful-project-related-links--корисні-посилання-стосовно-проекту)<br>

## __Team members__ | __Склад команди__

* [Дмитро Печенюк](https://github.com/DmitriyPechenyuk0) Teamlead
* [Нікіта Емріх](https://github.com/NikitaEmrih)

## __Project installation guide__ | __Інструкція до встановлення проєкту__
<details>
  <summary><strong>For Linux</strong></summary>

  ### This guide is intended for Ubuntu. For other Linux distributions, the installation may differ

  ### In English

  * **Step 1**: Open terminal

  * **Step 2**: Update the packages 
  ```sh
  sudo apt update
  ```

  * **Step 3**: Install Python 
  ```sh
  sudo apt install python3
  ```  

  * **Step 4**: Install pip (package manager for Python)
  ```sh
  sudo apt install python3-pip
  ```

  * **Step 5**: Install Git
   ```sh
   sudo apt install git
   ```

  * **Step 6**: Install VSCode:
  ```sh
  sudo apt install software-properties-common && sudo add-apt-repository "deb [arch=amd64] https://packages.microsoft.com/repos/vscode stable main" && curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > /usr/share/keyrings/microsoft-archive-keyring.gpg && sudo apt update && sudo apt install code
  ```

  ### Українською мовою

  * **Крок 1**: Відкрити термінал
  * **Крок 2**: Оновити пакети
  ```sh
  sudo apt update
  ```
  * **Крок 3**: Встановити Python
  ```sh
  sudo apt install python3
  ```  
  * **Крок 4**: Встановити pip (пакетний менеджер у Python)
  ```sh
  sudo apt install python3-pip
  ```
  * **Крок 5**: Встановити Git
   ```sh
   sudo apt install git
   ```
  * **Крок 6**: Встановити VSCode
  ```sh
  sudo apt install software-properties-common && sudo add-apt-repository "deb [arch=amd64] https://packages.microsoft.com/repos/vscode stable main" && curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > /usr/share/keyrings/microsoft-archive-keyring.gpg && sudo apt update && sudo apt install code
  ```



</details>
<details>
  <summary><strong>For Windows</strong></summary>

  ### In English

  * **Step 1**: Download and install Python: Go to the official website [python.org](https://www.python.org/) and download the latest version of Python for your operating system. Make sure to check the 'Add Python to PATH' option during the installation.

  * **Step 2**: Download and install Git: Go to the official website [git-scm.com](https://git-scm.com/) and download the latest version of Git for your operating system.

  * **Step 3**: Install Visual Studio Code from the official website: [https://code.visualstudio.com/](https://code.visualstudio.com/)

  * **Step 4**: Open Visual Studio Code, select the folder where you want to run the project through the navigation menu `File -> Open Folder`.

  * **Step 5**: Use the shortcut <kbd>Ctrl</kbd> + <kbd>~</kbd> to open the terminal menu and select 'Git Bash'.

  * **Step 6**: Copy the command below into the Git terminal:
    ```sh
    git clone https://github.com/DmitriyPechenyuk0/QRLogic.git
    ```

  * **Step 7**: Create a new Command Prompt terminal, then copy and run:
    ```sh
    python -m venv QRLogic/venv && cd QRLogic/venv/Scripts && activate.bat && cd ../.. && pip install -r requirements.txt && python QRLogic/manage.py runserver
    ```

  ---

  ### Українською мовою

  * **Крок 1**: Завантажте та встановіть Python: Перейдіть на офіційний сайт [python.org](https://www.python.org/) і завантажте останню версію Python для вашої операційної системи. Під час встановлення обов’язково відзначте опцію "Add Python to PATH".

  * **Крок 2**: Завантажте та встановіть Git: Перейдіть на офіційний сайт [git-scm.com](https://git-scm.com/) і завантажте останню версію Git для вашої операційної системи.

  * **Крок 3**: Встановіть Visual Studio Code з офіційного сайту: [https://code.visualstudio.com/](https://code.visualstudio.com/)

  * **Крок 4**: Відкрийте Visual Studio Code, виберіть папку, в якій хочете запустити проєкт, через навігаційне меню `File -> Open Folder`.

  * **Крок 5**: Скористайтеся комбінацією клавіш <kbd>Ctrl</kbd> + <kbd>~</kbd>, щоб відкрити меню терміналів, і виберіть "Git Bash".

  * **Крок 6**: Скопіюйте команду у Git-термінал:
    ```sh
    git clone https://github.com/DmitriyPechenyuk0/QRLogic.git
    ```

  * **Крок 7**: Створіть новий термінал Command Prompt і виконайте:
    ```sh
    python -m venv QRLogic/venv && cd QRLogic/venv/Scripts && activate.bat && cd ../.. && pip install -r requirements.txt && python QRLogic/manage.py runserver
    ```
</details>




## __Useful project-related links__ | __Корисні посилання стосовно проекту__

* [Figma Design](https://www.figma.com/design/zuJFbfVMv3Gj0Nj5enrInM/QRLogic-Design?node-id=5-3&p=f&t=m3kC5uEKsHLNVoZs-0)
* [FigJam](https://www.figma.com/board/6FgTky1OFCN0xwHK6livO5/QRLogic-FigJam?node-id=0-1&p=f&t=55d6m70bPoKnphCC-0)
