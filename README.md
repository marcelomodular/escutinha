# Whisper-CLI: Instalação e Guia de Uso (Ubuntu + Virtual Environment)

> Transcrição de áudio offline usando Whisper (OpenAI) + FFmpeg + Python — linha de comando, **dentro de um ambiente virtual isolado**.

---

## Pré-requisitos (sistema)

| Ferramenta | Versão mínima | Para que serve |
|---|---|---|
| **Python 3** | 3.8+ | Ambiente do projeto |
| **pip + venv** | (incluído) | Criar e gerenciar ambientes virtuais |
| **FFmpeg** | qualquer recente | Extrair áudio de vídeos |
| **Git** | qualquer recente | Clonar o repositório do Whisper |
| **GPU NVIDIA (opcional)** | CUDA 11.8+ | Aceleração por GPU |

> **Sem GPU?** Funciona em CPU, mas é mais lento. Ainda assim, o ambiente virtual funciona perfeitamente.

---

## 1 — Instalar dependências do sistema (Ubuntu)

```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv ffmpeg git
```

Verifique:
```bash
python3 --version   # >= 3.8
pip3 --version
ffmpeg -version
git --version
```

---

## 2 — Criar e ativar o ambiente virtual

Escolha um diretório para o projeto (ex: `~/whisper-project`):

```bash
mkdir ~/whisper-project
cd ~/whisper-project

# Criar o ambiente virtual
python3 -m venv venv

# Ativar o ambiente
source venv/bin/activate
```

Após a ativação, seu prompt deve mostrar `(venv)`.  
**Todos os comandos seguintes devem ser executados com o ambiente ativado.**

---

## 3 — Instalar o Whisper dentro do ambiente

Com o `(venv)` ativado, instale o Whisper diretamente (sem clonar o repositório, a menos que queira):

```bash
# Dentro do venv, use 'pip' (não pip3)
pip install --upgrade pip
pip install openai-whisper
```

> **Alternativa (clone do repositório):**  
> ```bash
> git clone https://github.com/openai/whisper.git
> cd whisper
> pip install -e .
> cd ..
> ```

Instale também o `yt-dlp` para baixar vídeos:
```bash
pip install yt-dlp
```

---

## 4 — Baixar os modelos do Whisper

Os modelos serão baixados automaticamente na primeira execução, ou você pode forçar o download:

```bash
    whisper --model small --download
```

Modelos recomendados: `tiny`, `base`, `small`, `medium`, `large`.  
O `small` é um bom ponto de partida.

---

## 5 — Verificar GPU (se tiver NVIDIA)

```bash
nvidia-smi
```

Se detectar GPU, o PyTorch (instalado automaticamente pelo whisper) já tentará usar CUDA.  
Caso queira garantir a versão com CUDA dentro do venv:
```bash
pip uninstall torch
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

---

## 6 — Uso básico (com o venv ativado)

### Baixar áudio de um vídeo
```bash
yt-dlp -x --audio-format mp3 --audio-quality 0 -o "audio.mp3" "URL_DO_VIDEO"
```

### Transcrever
```bash
whisper audio.mp3 --model small --language Portuguese
```

### Outros formatos de saída
```bash
whisper audio.mp3 --model small --language Portuguese --output-format json --output-dir ./transcripts
```

---

## 7 — Script automatizado (usando o venv)

Crie o arquivo `transcribe.sh` dentro da pasta do projeto (`~/whisper-project`):

```bash
#!/bin/bash
# transcribe.sh - usa o ambiente virtual automaticamente

# Ativa o venv
source "$(dirname "$0")/venv/bin/activate"

URL="$1"
MODEL="${2:-small}"
OUTPUT_PREFIX="audio_$(date +'%Y%m%d_%H%M%S')"

echo -e "\e[36mBaixando áudio...\e[0m"
yt-dlp -x --audio-format mp3 --audio-quality 0 -o "$OUTPUT_PREFIX.%(ext)s" "$URL"

AUDIO_FILE=$(ls "$OUTPUT_PREFIX".* 2>/dev/null | head -n1)

echo -e "\e[36mTranscrevendo com modelo: $MODEL...\e[0m"
whisper "$AUDIO_FILE" --model "$MODEL" --language Portuguese --output-format txt --output-dir "./transcripts"

echo -e "\e[32mPronto! Verifique a pasta ./transcripts\e[0m"
```

Torne executável:
```bash
chmod +x transcribe.sh
```

**Como usar:**  
```bash
./transcribe.sh "https://youtu.be/..." small
```

O script já ativa o `venv` automaticamente.

---

## 8 — Resumo de comandos (com venv)

```bash
# 1. Preparar o ambiente
mkdir ~/whisper-project && cd ~/whisper-project
python3 -m venv venv
source venv/bin/activate

# 2. Instalar pacotes
pip install openai-whisper yt-dlp

# 3. Testar transcrição
yt-dlp -x --audio-format mp3 -o "teste.mp3" "https://www.youtube.com/watch?v=...  "
whisper teste.mp3 --model base --language Portuguese

# 4. Sair do ambiente
deactivate
```

---

## 9 — Dicas importantes

- **Sempre ative o venv** antes de usar `whisper` ou `yt-dlp`, ou use o script que ativa automaticamente.
- Para sair do ambiente virtual: `deactivate`.
- Se quiser apagar o ambiente e recomeçar: `rm -rf venv` e recrie.
- O `pip` instalado dentro do venv não interfere nos pacotes globais do sistema.
- Para atualizar o Whisper: ative o venv e execute `pip install --upgrade openai-whisper`.

---

## 10 — Solução de erros comuns

| Erro | Solução |
|------|---------|
| `whisper: command not found` | O venv não está ativado. Execute `source venv/bin/activate`. |
| `pip install` permission denied | Você está tentando instalar fora do venv. Use o venv. |
| `FFmpeg not found` | Instale no sistema: `sudo apt install ffmpeg`. |
| `CUDA not available` | Instale o PyTorch com CUDA dentro do venv (veja passo 5). |

---

**Agora você tem um ambiente Python totalmente isolado, portável e reproduzível para rodar o Whisper no Ubuntu.** 🐍🎙️
