import tkinter as tk


class DesenhoMixin:
    """Utilitários de desenho reaproveitados por botões, campos e modais."""

    def desenhar_fundo_arredondado(self, pai, largura, altura, raio, cor_fundo, cor_forma):
        """Cria um canvas apenas para desenhar as bordas arredondadas de um elemento."""
        canvas = tk.Canvas(pai, width=largura, height=altura, bg=cor_fundo, highlightthickness=0)

        # Desenha os 4 cantos arredondados (arcos)
        canvas.create_arc(0, 0, raio * 2, raio * 2, start=90, extent=90, fill=cor_forma, outline=cor_forma)
        canvas.create_arc(largura - raio * 2, 0, largura, raio * 2, start=0, extent=90, fill=cor_forma, outline=cor_forma)
        canvas.create_arc(0, altura - raio * 2, raio * 2, altura, start=180, extent=90, fill=cor_forma, outline=cor_forma)
        canvas.create_arc(largura - raio * 2, altura - raio * 2, largura, altura, start=270, extent=90, fill=cor_forma, outline=cor_forma)

        # Preenche o miolo interno com retângulos
        canvas.create_rectangle(raio, 0, largura - raio, altura, fill=cor_forma, outline=cor_forma)
        canvas.create_rectangle(0, raio, largura, altura - raio, fill=cor_forma, outline=cor_forma)

        return canvas
