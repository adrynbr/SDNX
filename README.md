# ⚡ SDNX — Nintendo Switch MicroSD Prep Tool

[Português](#português) | [English](#english)

---

<a name="português"></a>
## 🇧🇷 Português

<p align="center">
  <img src="icon.ico" width="128" height="128" alt="SDNX Icon">
</p>

**SDNX** é uma ferramenta standalone moderna e simplificada para Windows, projetada para automatizar o processo de preparação de cartões MicroSD para Nintendo Switch, incluindo formatação em **FAT32** e instalação dinâmica do **CNX Pack**.

---

### 🚀 Funcionalidades

- 📁 **Formatação Inteligente em FAT32:** Suporte completo para cartões de grande capacidade (64GB, 128GB, 256GB, 512GB+) usando tamanho de cluster de 32KB.
- 🔄 **Suporte a Discos RAW:** Reconhece e recupera cartões não formatados ou corrompidos diretamente no ecossistema Windows.
- 📦 **Download Dinâmico do CNX Pack:** Conecta-se diretamente à API do GitHub para baixar e extrair sempre a última versão lançada, sem baixar código-fonte desnecessário.
- 🎨 **Interface Moderna:** Criada com CustomTkinter, oferecendo uma experiência fluida no modo escuro.
- ⚡ **Standalone:** Executável leve e sem necessidade de instalação prévia do Python.

---

### 🛠️ Como Executar o Programa (.exe)

1. Vá até a aba **[Releases](../../releases/latest)** e baixe o arquivo `SDNX.zip`.
2. Extraia o arquivo `.zip` no seu computador.
3. Clique com o botão direito sobre o arquivo `SDNX.exe` e escolha **"Executar como Administrador"** (necessário para gerenciar e formatar partições de disco).

> ⚠️ **Aviso sobre o Windows SmartScreen:** Como o executável não possui assinatura digital paga, o Windows pode exibir um aviso na primeira execução. Basta clicar em **"Mais informações"** e depois em **"Executar assim mesmo"**.

---

### 💻 Como Rodar a Partir do Código-Fonte

Caso queira executar ou modificar o código Python diretamente:

```bash
# 1. baixe a source do projeto e abra no VS Code ou um editor de sua preferência.

# 2. Instale as dependências necessárias
pip install customtkinter psutil requests

# 3. Execute o aplicativo
python p1.py
```

#### Como Compilar seu próprio `.exe`:
```powershell
pyinstaller --noconsole --onefile --clean --collect-all customtkinter --icon="icon.ico" -n "SDNX" p1.py
```

---

### ☕ Apoie o Projeto / Doações

Se o **SDNX** te ajudou e economizou seu tempo, considere apoiar o desenvolvimento contínuo!

- 💸 **Pix:** `adryanescobar29@gmail.com`

---

### 📬 Contato e Suporte

Fique à vontade para abrir uma **Issue** aqui no GitHub para relatar problemas, sugerir melhorias ou enviar *Pull Requests*!

- 📱 **WhatsApp / Contato:** +55 51 99448-7569

---

<a name="english"></a>
## 🇺🇸 English

<p align="center">
  <img src="icon.ico" width="128" height="128" alt="SDNX Icon">
</p>

**SDNX** is a modern and lightweight standalone Windows tool designed to automate the preparation of MicroSD cards for the Nintendo Switch, including **FAT32** formatting and dynamic installation of the **CNX Pack**.

---

### 🚀 Features

- 📁 **Smart FAT32 Formatting:** Full support for high-capacity cards (64GB, 128GB, 256GB, 512GB+) using a 32KB cluster size.
- 🔄 **RAW Disk Support:** Detects and recovers unformatted or corrupted cards directly within Windows.
- 📦 **Dynamic CNX Pack Download:** Connects directly to the GitHub API to fetch and extract the latest release, ignoring unnecessary source code files.
- 🎨 **Modern Interface:** Built with CustomTkinter, featuring a smooth dark theme.
- ⚡ **Standalone Executable:** Lightweight `.exe` with no Python installation required.

---

### 🛠️ How to Run (.exe)

1. Go to the **[Releases](../../releases/latest)** tab and download `SDNX.zip`.
2. Extract the `.zip` file on your computer.
3. Right-click `SDNX.exe` and select **"Run as Administrator"** (required for disk partition management and formatting).

> ⚠️ **Windows SmartScreen Notice:** Since the application is not signed with a paid digital certificate, Windows may display a warning on the first run. Click **"More info"** and then **"Run anyway"**.

---

### 💻 Running from Source Code

If you prefer to run or modify the Python script directly:

```bash
# 1. Download the source code of this project and open it in VS Code or your preferred editor.

# 2. Install dependencies
pip install customtkinter psutil requests

# 3. Run the application
python p1.py
```

#### How to Compile your own `.exe`:
```powershell
pyinstaller --noconsole --onefile --clean --collect-all customtkinter --icon="icon.ico" -n "SDNX" p1.py
```

---

### ☕ Support & Donations

If **SDNX** helped you and saved your time, consider supporting the project!

- 💸 **Pix:** `adryanescobar29@gmail.com`

---

### 📬 Contact & Support

Feel free to open an **Issue** to report bugs, suggest new features, or submit a Pull Request!

- 📱 **WhatsApp / Contact:** +55 51 99448-7569
