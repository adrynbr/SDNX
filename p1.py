import os
import sys
import shutil
import subprocess
import threading
import zipfile
import requests
import psutil
import customtkinter as ctk
from tkinter import filedialog, messagebox

# Configurações de Aparência do CustomTkinter
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# Repositório GitHub Oficial do CNX Pack
GITHUB_API_LATEST = "https://api.github.com/repos/CostelaCNX/CNX/releases/latest"

class SwitchSDPreparer(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Preparador de MicroSD para Nintendo Switch")
        self.geometry("620x520")
        self.resizable(False, False)

        # Variáveis de Controle
        self.selected_drive = ctk.StringVar()
        self.drives_map = {}
        self.backup_nintendo_path = ""
        self.backup_emummc_path = ""

        self._build_main_ui()
        self.refresh_drives()

    def _build_main_ui(self):
        """Constrói a interface principal."""
        self.title_label = ctk.CTkLabel(
            self, 
            text="Preparador de MicroSD - Nintendo Switch", 
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.title_label.pack(pady=(25, 10))

        self.subtitle_label = ctk.CTkLabel(
            self, 
            text="Selecione o cartão de memória para iniciar a formatação e instalação do pacote.",
            font=ctk.CTkFont(size=12)
        )
        self.subtitle_label.pack(pady=(0, 20))

        self.main_frame = ctk.CTkFrame(self, corner_radius=10)
        self.main_frame.pack(padx=30, pady=10, fill="both", expand=True)

        self.drive_label = ctk.CTkLabel(self.main_frame, text="Selecione o Cartão SD / Drive USB:", font=ctk.CTkFont(weight="bold"))
        self.drive_label.pack(pady=(20, 5))

        self.drive_menu_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.drive_menu_frame.pack(pady=5)

        self.drive_dropdown = ctk.CTkOptionMenu(self.drive_menu_frame, variable=self.selected_drive, width=320)
        self.drive_dropdown.pack(side="left", padx=5)

        self.refresh_btn = ctk.CTkButton(self.drive_menu_frame, text="🔄", width=40, command=self.refresh_drives)
        self.refresh_btn.pack(side="left", padx=5)

        self.install_btn = ctk.CTkButton(
            self.main_frame, 
            text="Instalar Desbloqueio", 
            font=ctk.CTkFont(size=16, weight="bold"),
            height=45,
            fg_color="#1f538d",
            hover_color="#14375e",
            command=self.start_process_thread
        )
        self.install_btn.pack(pady=(30, 20), padx=40, fill="x")

        self.status_label = ctk.CTkLabel(self.main_frame, text="Aguardando início...", font=ctk.CTkFont(size=13))
        self.status_label.pack(pady=(10, 5))

        self.progress_bar = ctk.CTkProgressBar(self.main_frame, width=420)
        self.progress_bar.pack(pady=(0, 20))
        self.progress_bar.set(0)

    def refresh_drives(self):
        """Lista os drives de armazenamento evitando crashes em drives não formatados (RAW)."""
        self.drives_map.clear()
        options = []
        
        for partition in psutil.disk_partitions(all=False):
            if 'removable' in partition.opts or '/media' in partition.mountpoint or '/Volumes' in partition.mountpoint or 'cdrom' not in partition.opts:
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    gb_free = round(usage.free / (1024**3), 2)
                    label = f"{partition.device} ({gb_free} GB livre) - {partition.mountpoint}"
                except Exception:
                    label = f"{partition.device} (Acesso Restrito / RAW) - {partition.mountpoint}"

                self.drives_map[label] = partition.mountpoint
                options.append(label)

        if options:
            self.drive_dropdown.configure(values=options)
            self.selected_drive.set(options[0])
            self.install_btn.configure(state="normal")
        else:
            self.drive_dropdown.configure(values=["Nenhum cartão detectado"])
            self.selected_drive.set("Nenhum cartão detectado")
            self.install_btn.configure(state="disabled")

    def fetch_latest_cnx_download_url(self):
        """Obtém o link de download direto do ZIP da release mais recente no GitHub."""
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(GITHUB_API_LATEST, headers=headers)
        if response.status_code != 200:
            raise Exception(f"Não foi possível consultar a API do GitHub (Status: {response.status_code}).")

        data = response.json()
        assets = data.get("assets", [])

        for asset in assets:
            name = asset.get("name", "")
            download_url = asset.get("browser_download_url", "")
            if name.endswith(".zip") and not name.startswith("Source_code"):
                return download_url, name

        raise Exception("Nenhum arquivo de pacote ZIP válido foi encontrado na release mais recente do CNX Pack.")

    def start_process_thread(self):
        """Inicia o processo em uma thread separada."""
        drive_key = self.selected_drive.get()
        if drive_key not in self.drives_map:
            messagebox.showerror("Erro", "Selecione um cartão de memória válido.")
            return

        target_drive = self.drives_map[drive_key]

        confirm = messagebox.askyesno(
            "Atenção!", 
            f"TODOS OS DADOS em {target_drive} serão APAGADOS permanentemente durante a formatação.\n\nDeseja continuar?"
        )
        if not confirm:
            return

        self.install_btn.configure(state="disabled")
        self.refresh_btn.configure(state="disabled")
        self.drive_dropdown.configure(state="disabled")

        threading.Thread(target=self.run_installation, args=(target_drive,), daemon=True).start()

    def run_installation(self, drive_path):
        """Executa a formatação, busca a versão recente, baixa e extrai."""
        try:
            # Passo 1: Formatação
            self.update_status("Formatando cartão SD...", 0.1)
            self.format_to_fat32(drive_path)

            # Passo 2: Obter a versão mais recente do GitHub
            self.update_status("Buscando versão mais recente do CNX Pack no GitHub...", 0.2)
            download_url, filename = self.fetch_latest_cnx_download_url()

            # Passo 3: Download
            self.update_status(f"Baixando {filename}...", 0.3)
            zip_path = os.path.join(os.getcwd(), "cnx_pack_temp.zip")
            self.download_file(download_url, zip_path)

            # Passo 4: Extração
            self.update_status("Extraindo arquivos para a raiz do SD...", 0.75)
            self.extract_zip(zip_path, drive_path)

            if os.path.exists(zip_path):
                os.remove(zip_path)

            self.update_status("Instalação do pacote concluída!", 1.0)
            self.after(500, lambda: self.prompt_backup_restoration(drive_path))

        except Exception as e:
            self.update_status("Erro no processo!", 0)
            messagebox.showerror("Erro Crítico", f"Ocorreu um erro durante a execução:\n{str(e)}")
            self.reset_ui()

    def format_to_fat32(self, drive_path):
        """Formata o cartão selecionado em FAT32."""
        drive_letter = drive_path.rstrip("\\").rstrip("/")
        
        if os.name == 'nt':
            cmd = f"format {drive_letter} /FS:FAT32 /A:32K /Q /Y"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode != 0:
                raise Exception(f"Falha ao formatar. Execute o VS Code como Administrador.\n{result.stderr}")
        else:
            cmd = f"mkfs.vfat -F 32 -s 64 {drive_letter}"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode != 0:
                raise Exception(f"Falha ao formatar no sistema Unix.\n{result.stderr}")

    def download_file(self, url, dest_path):
        """Baixa o pacote exibindo a porcentagem na interface."""
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        downloaded = 0

        with open(dest_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
                    downloaded += len(chunk)
                    if total_size > 0:
                        prog = 0.3 + (downloaded / total_size) * 0.45
                        self.update_status(f"Baixando pacote... ({int((downloaded/total_size)*100)}%)", prog)

    def extract_zip(self, zip_path, extract_to):
        """Extrai todo o conteúdo do zip na raiz do cartão SD."""
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)

    def update_status(self, message, progress_val):
        self.status_label.configure(text=message)
        self.progress_bar.set(progress_val)
        self.update_idletasks()

    def prompt_backup_restoration(self, drive_path):
        question = messagebox.askyesno(
            "Restauração de Backup",
            "Você possui um backup das pastas emuMMC e/ou Nintendo para restaurar?"
        )
        if question:
            self.show_backup_modal(drive_path)
        else:
            self.finish_process()

    def show_backup_modal(self, drive_path):
        backup_win = ctk.CTkToplevel(self)
        backup_win.title("Restaurar Pastas de Backup")
        backup_win.geometry("500x380")
        backup_win.grab_set()

        label_info = ctk.CTkLabel(
            backup_win, 
            text="Selecione os diretórios do seu backup anterior:", 
            font=ctk.CTkFont(size=14, weight="bold")
        )
        label_info.pack(pady=15)

        frame_nintendo = ctk.CTkFrame(backup_win)
        frame_nintendo.pack(fill="x", padx=20, pady=10)

        lbl_nin = ctk.CTkLabel(frame_nintendo, text="Pasta 'Nintendo': Não selecionada", anchor="w")
        lbl_nin.pack(side="left", padx=10, expand=True, fill="x")

        def select_nintendo():
            path = filedialog.askdirectory(title="Selecione a pasta 'Nintendo'")
            if path:
                self.backup_nintendo_path = path
                lbl_nin.configure(text=f"Nintendo: ...{path[-25:]}")

        btn_nin = ctk.CTkButton(frame_nintendo, text="Buscar", width=80, command=select_nintendo)
        btn_nin.pack(side="right", padx=10, pady=8)

        frame_emummc = ctk.CTkFrame(backup_win)
        frame_emummc.pack(fill="x", padx=20, pady=10)

        lbl_emu = ctk.CTkLabel(frame_emummc, text="Pasta 'emuMMC': Não selecionada", anchor="w")
        lbl_emu.pack(side="left", padx=10, expand=True, fill="x")

        def select_emummc():
            path = filedialog.askdirectory(title="Selecione a pasta 'emuMMC'")
            if path:
                self.backup_emummc_path = path
                lbl_emu.configure(text=f"emuMMC: ...{path[-25:]}")

        btn_emu = ctk.CTkButton(frame_emummc, text="Buscar", width=80, command=select_emummc)
        btn_emu.pack(side="right", padx=10, pady=8)

        modal_status = ctk.CTkLabel(backup_win, text="", font=ctk.CTkFont(size=12))
        modal_status.pack(pady=10)

        def process_copy():
            if not self.backup_nintendo_path and not self.backup_emummc_path:
                messagebox.showwarning("Aviso", "Selecione ao menos uma das pastas para restaurar.", parent=backup_win)
                return

            def copy_task():
                try:
                    if self.backup_nintendo_path:
                        modal_status.configure(text="Copiando pasta Nintendo...")
                        dest = os.path.join(drive_path, "Nintendo")
                        if os.path.exists(dest):
                            shutil.rmtree(dest)
                        shutil.copytree(self.backup_nintendo_path, dest)

                    if self.backup_emummc_path:
                        modal_status.configure(text="Copiando pasta emuMMC...")
                        dest = os.path.join(drive_path, "emuMMC")
                        if os.path.exists(dest):
                            shutil.rmtree(dest)
                        shutil.copytree(self.backup_emummc_path, dest)

                    backup_win.destroy()
                    self.finish_process()
                except Exception as ex:
                    messagebox.showerror("Erro ao Copiar", f"Não foi possível restaurar os arquivos:\n{str(ex)}", parent=backup_win)

            threading.Thread(target=copy_task, daemon=True).start()

        btn_confirm = ctk.CTkButton(
            backup_win, 
            text="Copiar Pastas para o SD", 
            fg_color="green", 
            hover_color="darkgreen",
            command=process_copy
        )
        btn_confirm.pack(pady=15)

    def finish_process(self):
        self.reset_ui()
        messagebox.showinfo(
            "Concluído!", 
            "Processo concluído com sucesso! O cartão SD está pronto para o Nintendo Switch."
        )

    def reset_ui(self):
        self.install_btn.configure(state="normal")
        self.refresh_btn.configure(state="normal")
        self.drive_dropdown.configure(state="normal")
        self.progress_bar.set(0)
        self.status_label.configure(text="Aguardando início...")
        self.refresh_drives()


if __name__ == "__main__":
    app = SwitchSDPreparer()
    app.mainloop()