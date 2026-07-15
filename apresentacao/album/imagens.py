from pathlib import Path
from PIL import Image, ImageTk


class ImagensMixin:
    """Responsável por localizar e carregar os ícones usados na tela de álbuns."""

    def carregar_imagem(self):
        icon_dirs = [
            Path.cwd() / "icones",
            Path(__file__).resolve().parent / "icones",
            Path(__file__).resolve().parent.parent / "icones",
        ]

        def carregar(nome, tamanho):
            if Image is None or ImageTk is None:
                return None
            for diretorio in icon_dirs:
                caminho = diretorio / nome
                if caminho.exists():
                    try:
                        imagem = Image.open(caminho)
                        imagem_redimensionada = imagem.resize(tamanho, Image.Resampling.LANCZOS)
                        return ImageTk.PhotoImage(imagem_redimensionada)
                    except Exception:
                        pass
            return None

        self.img_logo = carregar("logo.png", (50, 50))
        self.img_usuario = carregar("usuario.png", (40, 40))
