import whisper
import ffmpeg
import os
import sys

# ==================================================
# CONFIGURAÇÕES QUE VOCÊ PODE ALTERAR (FIQUE À VONTADE!)
# ==================================================
CAMINHO_VIDEO = "./2026-06-24 10-53-17.mp4"    # Nome do seu arquivo de vídeo
MODELO_WHISPER = "medium"           # Modelo: tiny, base, small, medium, large
LINGUA = "Portuguese"              # Ou "English", "Spanish", "French", etc.
CAMINHO_MP3_SAIDA = "2026-06-24 10-53-17.mp3" # Arquivo de áudio temporário
# ==================================================

def converter_mp4_para_mp3(entrada_video, saida_audio):
    """Converte um arquivo MP4 para MP3 usando ffmpeg-python."""
    print(f"🎬 Convertendo '{entrada_video}' para MP3...")
    try:
        # Carrega o arquivo de vídeo, extrai apenas o áudio e salva em MP3
        ffmpeg.input(entrada_video).output(saida_audio, acodec='libmp3lame', audio_bitrate='192k').run(overwrite_output=True)
        print(f"✅ Conversão concluída! Áudio salvo em: {saida_audio}")
        return True
    except ffmpeg.Error as e:
        print(f"❌ Erro na conversão: {e.stderr.decode() if e.stderr else 'Erro desconhecido'}")
        return False

def transcrever_audio(arquivo_audio, modelo_whisper, lingua):
    """Carrega o modelo Whisper e transcreve o áudio."""
    print(f"\n🎙️ Carregando o modelo Whisper ('{modelo_whisper}')...")
    modelo = whisper.load_model(modelo_whisper)
    print("🔄 Transcrevendo o áudio...")
    resultado = modelo.transcribe(arquivo_audio, language=lingua)
    print("✅ Transcrição concluída!")
    return resultado["text"]

# --- Início da execução ---
if __name__ == "__main__":
    # Verifica se o arquivo de vídeo existe
    if not os.path.exists(CAMINHO_VIDEO):
        print(f"❌ Erro: Arquivo de vídeo '{CAMINHO_VIDEO}' não encontrado.")
        sys.exit(1)

    # Passo 1: Converter MP4 para MP3
    if not converter_mp4_para_mp3(CAMINHO_VIDEO, CAMINHO_MP3_SAIDA):
        sys.exit(1)

    # Passo 2: Transcrever o áudio
    texto_transcrito = transcrever_audio(CAMINHO_MP3_SAIDA, MODELO_WHISPER, LINGUA)

    # Exibe o resultado
    print("\n" + "="*40)
    print("📝 RESULTADO DA TRANSCRIÇÃO:")
    print("="*40)
    print(texto_transcrito)
    print("="*40)

    # (Opcional) Limpar o arquivo MP3 temporário após o uso
    if os.path.exists(CAMINHO_MP3_SAIDA):
        os.remove(CAMINHO_MP3_SAIDA)
        print(f"\n🧹 Arquivo temporário '{CAMINHO_MP3_SAIDA}' removido.")
