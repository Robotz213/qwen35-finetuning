from __future__ import annotations

import os
import queue
import shutil
import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk
from typing import Any

from src.context_builder import (
    SUPPORTED_EXTENSIONS,
    build_context_chunks,
    write_jsonl,
    write_manifest,
    write_markdown_pack,
)
from src.context_search import build_prompt, load_chunks, score_chunks


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE_DIR = PROJECT_ROOT / "context" / "sources"
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "outputs" / "context"

BRAND_REFERENCES = [
    "Vercel",
    "GitHub",
    "Linear",
    "Stripe",
    "Raycast",
    "Notion",
    "Figma",
    "Framer",
    "Clerk",
    "Supabase",
    "OpenAI",
    "Anthropic",
    "Cursor",
    "Railway",
    "Cloudflare",
]


class ContextGeneratorApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Qwen3.5 Context Studio")
        self.geometry("1180x760")
        self.minsize(1040, 680)

        self.message_queue: queue.Queue[tuple[str, Any]] = queue.Queue()
        self.is_running = False

        self.source_dir = tk.StringVar(value=str(DEFAULT_SOURCE_DIR))
        self.output_dir = tk.StringVar(value=str(DEFAULT_OUTPUT_DIR))
        self.chunk_size = tk.IntVar(value=1800)
        self.chunk_overlap = tk.IntVar(value=250)
        self.max_rows = tk.IntVar(value=5000)
        self.context_title = tk.StringVar(value="Base de conhecimento")
        self.copy_to_sources = tk.BooleanVar(value=True)
        self.top_k = tk.IntVar(value=5)

        self._configure_style()
        self._build_layout()
        self._refresh_sources()
        self.after(150, self._drain_messages)

    def _configure_style(self) -> None:
        self.configure(bg="#f7f8fb")
        style = ttk.Style(self)
        style.theme_use("clam")

        style.configure(".", font=("Segoe UI", 10))
        style.configure("TFrame", background="#f7f8fb")
        style.configure("Surface.TFrame", background="#ffffff", relief="flat")
        style.configure("Sidebar.TFrame", background="#111827")
        style.configure("Muted.TLabel", foreground="#64748b", background="#ffffff")
        style.configure("Heading.TLabel", font=("Segoe UI Semibold", 18), foreground="#0f172a", background="#ffffff")
        style.configure("Title.TLabel", font=("Segoe UI Semibold", 11), foreground="#0f172a", background="#ffffff")
        style.configure("SidebarTitle.TLabel", font=("Segoe UI Semibold", 16), foreground="#ffffff", background="#111827")
        style.configure("SidebarMuted.TLabel", foreground="#9ca3af", background="#111827", wraplength=220)
        style.configure("Accent.TButton", font=("Segoe UI Semibold", 10), foreground="#ffffff", background="#2563eb")
        style.map("Accent.TButton", background=[("active", "#1d4ed8")])
        style.configure("TButton", padding=(12, 7), background="#eef2ff")
        style.configure("TEntry", padding=6)
        style.configure("Treeview", rowheight=28, background="#ffffff", fieldbackground="#ffffff", borderwidth=0)
        style.configure("Treeview.Heading", font=("Segoe UI Semibold", 10), background="#f1f5f9", foreground="#334155")
        style.configure("Horizontal.TProgressbar", troughcolor="#e5e7eb", background="#10b981")

    def _build_layout(self) -> None:
        root = ttk.Frame(self)
        root.pack(fill="both", expand=True)

        sidebar = ttk.Frame(root, style="Sidebar.TFrame", width=270)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        ttk.Label(sidebar, text="Context Studio", style="SidebarTitle.TLabel").pack(anchor="w", padx=24, pady=(28, 8))
        ttk.Label(
            sidebar,
            text="Gerador visual de contexto para PDFs, planilhas, documentos e bases textuais.",
            style="SidebarMuted.TLabel",
        ).pack(anchor="w", padx=24, pady=(0, 18))

        ref_frame = ttk.Frame(sidebar, style="Sidebar.TFrame")
        ref_frame.pack(fill="x", padx=24, pady=(8, 18))
        ttk.Label(ref_frame, text="Base visual", style="SidebarMuted.TLabel").pack(anchor="w")
        ttk.Label(
            ref_frame,
            text=", ".join(BRAND_REFERENCES),
            style="SidebarMuted.TLabel",
        ).pack(anchor="w", pady=(6, 0))

        self.status_label = ttk.Label(sidebar, text="Pronto", style="SidebarMuted.TLabel")
        self.status_label.pack(side="bottom", anchor="w", padx=24, pady=(0, 24))

        main = ttk.Frame(root, padding=22)
        main.pack(side="left", fill="both", expand=True)

        header = ttk.Frame(main, style="Surface.TFrame", padding=18)
        header.pack(fill="x", pady=(0, 14))
        ttk.Label(header, text="Gerador de contexto", style="Heading.TLabel").pack(anchor="w")
        ttk.Label(
            header,
            text="Insira arquivos, ajuste o processamento e gere contexto pronto para prompts, RAG ou datasets.",
            style="Muted.TLabel",
        ).pack(anchor="w", pady=(6, 0))

        body = ttk.Frame(main)
        body.pack(fill="both", expand=True)

        left = ttk.Frame(body, style="Surface.TFrame", padding=16)
        left.pack(side="left", fill="both", expand=True, padx=(0, 14))

        right = ttk.Frame(body, style="Surface.TFrame", padding=16, width=350)
        right.pack(side="right", fill="y")
        right.pack_propagate(False)

        self._build_source_panel(left)
        self._build_settings_panel(right)
        self._build_log_panel(main)

    def _build_source_panel(self, parent: ttk.Frame) -> None:
        top = ttk.Frame(parent, style="Surface.TFrame")
        top.pack(fill="x")
        ttk.Label(top, text="Arquivos de entrada", style="Title.TLabel").pack(side="left")
        ttk.Button(top, text="Atualizar", command=self._refresh_sources).pack(side="right")
        ttk.Button(top, text="Adicionar pasta", command=self._add_folder).pack(side="right", padx=(0, 8))
        ttk.Button(top, text="Adicionar arquivos", command=self._add_files, style="Accent.TButton").pack(side="right", padx=(0, 8))

        path_row = ttk.Frame(parent, style="Surface.TFrame")
        path_row.pack(fill="x", pady=(14, 10))
        ttk.Entry(path_row, textvariable=self.source_dir).pack(side="left", fill="x", expand=True)
        ttk.Button(path_row, text="Escolher", command=self._choose_source_dir).pack(side="left", padx=(8, 0))

        columns = ("name", "type", "size")
        self.source_tree = ttk.Treeview(parent, columns=columns, show="headings", height=12)
        self.source_tree.heading("name", text="Arquivo")
        self.source_tree.heading("type", text="Tipo")
        self.source_tree.heading("size", text="Tamanho")
        self.source_tree.column("name", width=420)
        self.source_tree.column("type", width=80, anchor="center")
        self.source_tree.column("size", width=100, anchor="e")
        self.source_tree.pack(fill="both", expand=True, pady=(4, 10))

        actions = ttk.Frame(parent, style="Surface.TFrame")
        actions.pack(fill="x")
        ttk.Checkbutton(actions, text="Copiar arquivos adicionados para context/sources", variable=self.copy_to_sources).pack(side="left")
        ttk.Button(actions, text="Remover selecionado", command=self._remove_selected).pack(side="right")

    def _build_settings_panel(self, parent: ttk.Frame) -> None:
        ttk.Label(parent, text="Configuracao", style="Title.TLabel").pack(anchor="w")
        ttk.Label(parent, text="Ajustes inspirados em produtos SaaS: poucos controles, saida clara.", style="Muted.TLabel").pack(anchor="w", pady=(4, 14))

        self._field(parent, "Pasta de saida", self.output_dir, browse=self._choose_output_dir)
        self._field(parent, "Titulo do contexto", self.context_title)
        self._number_field(parent, "Tamanho do chunk", self.chunk_size)
        self._number_field(parent, "Sobreposicao", self.chunk_overlap)
        self._number_field(parent, "Linhas max. por planilha", self.max_rows)

        ttk.Label(parent, text="Instrucao padrao", style="Title.TLabel").pack(anchor="w", pady=(12, 6))
        self.instruction_text = tk.Text(parent, height=5, wrap="word", bd=0, bg="#f8fafc", fg="#0f172a", insertbackground="#2563eb")
        self.instruction_text.pack(fill="x")
        self.instruction_text.insert(
            "1.0",
            "Use este contexto como fonte de referencia. Quando a resposta depender dele, preserve nomes, numeros, datas e termos exatamente como aparecem.",
        )

        ttk.Button(parent, text="Gerar contexto", command=self._start_build_context, style="Accent.TButton").pack(fill="x", pady=(18, 8))
        ttk.Button(parent, text="Abrir pasta de saida", command=self._open_output_dir).pack(fill="x")

        ttk.Separator(parent).pack(fill="x", pady=18)
        ttk.Label(parent, text="Prompt com contexto", style="Title.TLabel").pack(anchor="w")
        ttk.Label(parent, text="Busca trechos relevantes no contexto gerado.", style="Muted.TLabel").pack(anchor="w", pady=(4, 8))
        self.question_text = tk.Text(parent, height=4, wrap="word", bd=0, bg="#f8fafc", fg="#0f172a", insertbackground="#2563eb")
        self.question_text.pack(fill="x")
        self.question_text.insert("1.0", "Qual e o resumo dos documentos?")
        self._number_field(parent, "Trechos", self.top_k)
        ttk.Button(parent, text="Criar prompt", command=self._start_make_prompt).pack(fill="x", pady=(8, 0))

    def _build_log_panel(self, parent: ttk.Frame) -> None:
        panel = ttk.Frame(parent, style="Surface.TFrame", padding=14)
        panel.pack(fill="x", pady=(14, 0))
        top = ttk.Frame(panel, style="Surface.TFrame")
        top.pack(fill="x")
        ttk.Label(top, text="Atividade", style="Title.TLabel").pack(side="left")
        self.progress = ttk.Progressbar(top, mode="indeterminate")
        self.progress.pack(side="right", fill="x", expand=True, padx=(14, 0))
        self.log_text = tk.Text(panel, height=7, wrap="word", bd=0, bg="#0f172a", fg="#dbeafe", insertbackground="#ffffff")
        self.log_text.pack(fill="x", pady=(10, 0))
        self._log("Pronto. Adicione arquivos ou escolha uma pasta de fontes.")

    def _field(self, parent: ttk.Frame, label: str, variable: tk.StringVar, browse: Any | None = None) -> None:
        ttk.Label(parent, text=label, style="Title.TLabel").pack(anchor="w", pady=(8, 4))
        row = ttk.Frame(parent, style="Surface.TFrame")
        row.pack(fill="x")
        ttk.Entry(row, textvariable=variable).pack(side="left", fill="x", expand=True)
        if browse:
            ttk.Button(row, text="...", width=3, command=browse).pack(side="left", padx=(6, 0))

    def _number_field(self, parent: ttk.Frame, label: str, variable: tk.IntVar) -> None:
        ttk.Label(parent, text=label, style="Title.TLabel").pack(anchor="w", pady=(8, 4))
        ttk.Spinbox(parent, textvariable=variable, from_=1, to=100000, increment=50).pack(fill="x")

    def _choose_source_dir(self) -> None:
        selected = filedialog.askdirectory(initialdir=self.source_dir.get() or str(PROJECT_ROOT))
        if selected:
            self.source_dir.set(selected)
            self._refresh_sources()

    def _choose_output_dir(self) -> None:
        selected = filedialog.askdirectory(initialdir=self.output_dir.get() or str(PROJECT_ROOT))
        if selected:
            self.output_dir.set(selected)

    def _add_files(self) -> None:
        filetypes = [("Arquivos suportados", " ".join(f"*{ext}" for ext in sorted(SUPPORTED_EXTENSIONS))), ("Todos", "*.*")]
        selected = filedialog.askopenfilenames(title="Adicionar arquivos", filetypes=filetypes)
        if not selected:
            return
        self._import_paths([Path(path) for path in selected])

    def _add_folder(self) -> None:
        selected = filedialog.askdirectory(title="Adicionar pasta")
        if not selected:
            return
        paths = [path for path in Path(selected).rglob("*") if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS]
        self._import_paths(paths)

    def _import_paths(self, paths: list[Path]) -> None:
        target_dir = Path(self.source_dir.get())
        target_dir.mkdir(parents=True, exist_ok=True)

        if not self.copy_to_sources.get():
            common_parent = self._common_parent(paths)
            if common_parent:
                self.source_dir.set(str(common_parent))
                self._refresh_sources()
                self._log(f"Pasta de fontes alterada para {common_parent}")
            return

        imported = 0
        for path in paths:
            if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
                continue
            if self.copy_to_sources.get():
                destination = self._unique_destination(target_dir / path.name)
                shutil.copy2(path, destination)
            imported += 1

        self._refresh_sources()
        self._log(f"{imported} arquivo(s) adicionados.")

    def _common_parent(self, paths: list[Path]) -> Path | None:
        if not paths:
            return None
        common = os.path.commonpath([str(path.parent if path.is_file() else path) for path in paths])
        return Path(common)

    def _unique_destination(self, destination: Path) -> Path:
        if not destination.exists():
            return destination
        stem = destination.stem
        suffix = destination.suffix
        for index in range(2, 10000):
            candidate = destination.with_name(f"{stem}-{index}{suffix}")
            if not candidate.exists():
                return candidate
        raise RuntimeError(f"Nao foi possivel criar nome unico para {destination.name}")

    def _refresh_sources(self) -> None:
        for item in self.source_tree.get_children():
            self.source_tree.delete(item)

        source = Path(self.source_dir.get())
        source.mkdir(parents=True, exist_ok=True)
        files = [path for path in sorted(source.rglob("*")) if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS]
        for path in files:
            relative = path.relative_to(source).as_posix()
            self.source_tree.insert("", "end", values=(relative, path.suffix.lower(), self._format_size(path.stat().st_size)))
        self.status_label.configure(text=f"{len(files)} arquivo(s) na base")

    def _remove_selected(self) -> None:
        selected = self.source_tree.selection()
        if not selected:
            return
        source = Path(self.source_dir.get()).resolve()
        safe_source = DEFAULT_SOURCE_DIR.resolve()
        if source != safe_source:
            messagebox.showinfo(
                "Remocao bloqueada",
                "Por seguranca, a GUI so remove arquivos da pasta context/sources do projeto.",
            )
            return
        if not messagebox.askyesno("Remover", "Remover os arquivos selecionados da pasta de fontes?"):
            return
        for item in selected:
            values = self.source_tree.item(item, "values")
            if values:
                target = (source / values[0]).resolve()
                if target.exists() and source.resolve() in target.parents:
                    target.unlink()
        self._refresh_sources()

    def _start_build_context(self) -> None:
        if self.is_running:
            return
        self._set_running(True, "Gerando contexto...")
        thread = threading.Thread(target=self._build_context_worker, daemon=True)
        thread.start()

    def _build_context_worker(self) -> None:
        try:
            source_dir = Path(self.source_dir.get())
            output_dir = Path(self.output_dir.get())
            instruction = self.instruction_text.get("1.0", "end").strip()
            chunks = build_context_chunks(
                source_dir=source_dir,
                include_extensions=SUPPORTED_EXTENSIONS,
                chunk_size=int(self.chunk_size.get()),
                chunk_overlap=int(self.chunk_overlap.get()),
                max_rows_per_sheet=int(self.max_rows.get()),
            )
            if not chunks:
                self.message_queue.put(("error", "Nenhum arquivo suportado encontrado."))
                return
            write_jsonl(chunks, output_dir / "context_chunks.jsonl")
            write_markdown_pack(chunks, output_dir / "context_pack.md", self.context_title.get(), instruction)
            write_manifest(chunks, output_dir / "manifest.json")
            sources = len({chunk.source_path for chunk in chunks})
            self.message_queue.put(("done", f"Contexto gerado: {sources} fonte(s), {len(chunks)} chunk(s)."))
        except Exception as exc:
            self.message_queue.put(("error", str(exc)))

    def _start_make_prompt(self) -> None:
        if self.is_running:
            return
        self._set_running(True, "Criando prompt...")
        thread = threading.Thread(target=self._make_prompt_worker, daemon=True)
        thread.start()

    def _make_prompt_worker(self) -> None:
        try:
            output_dir = Path(self.output_dir.get())
            chunks_path = output_dir / "context_chunks.jsonl"
            prompt_path = output_dir / "prompt.md"
            question = self.question_text.get("1.0", "end").strip()
            chunks = load_chunks(chunks_path)
            ranked = score_chunks(question, chunks)
            selected = [chunk for _, chunk in ranked[: int(self.top_k.get())]]
            if not selected:
                self.message_queue.put(("error", "Nenhum trecho relevante encontrado. Gere o contexto ou refine a pergunta."))
                return
            prompt_path.write_text(build_prompt(question, selected), encoding="utf-8")
            self.message_queue.put(("done", f"Prompt criado em {prompt_path}"))
        except Exception as exc:
            self.message_queue.put(("error", str(exc)))

    def _drain_messages(self) -> None:
        try:
            while True:
                kind, payload = self.message_queue.get_nowait()
                if kind == "done":
                    self._log(payload)
                    self._set_running(False, "Pronto")
                    self._refresh_sources()
                elif kind == "error":
                    self._log(f"Erro: {payload}")
                    self._set_running(False, "Erro")
                    messagebox.showerror("Erro", payload)
        except queue.Empty:
            pass
        self.after(150, self._drain_messages)

    def _set_running(self, running: bool, status: str) -> None:
        self.is_running = running
        self.status_label.configure(text=status)
        if running:
            self.progress.start(10)
            self._log(status)
        else:
            self.progress.stop()

    def _open_output_dir(self) -> None:
        output_dir = Path(self.output_dir.get())
        output_dir.mkdir(parents=True, exist_ok=True)
        os.startfile(output_dir)

    def _log(self, message: str) -> None:
        self.log_text.insert("end", f"{message}\n")
        self.log_text.see("end")

    @staticmethod
    def _format_size(size: int) -> str:
        value = float(size)
        for unit in ("B", "KB", "MB", "GB"):
            if value < 1024 or unit == "GB":
                return f"{value:.1f} {unit}" if unit != "B" else f"{int(value)} B"
            value /= 1024
        return f"{size} B"


def main() -> None:
    app = ContextGeneratorApp()
    app.mainloop()
