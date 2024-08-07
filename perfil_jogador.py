import os
import json

class PerfilJogador:
    def __init__(self, save_file='perfil_jogador.json'):
        self.save_file = save_file
        self.niveis_completados = self.carregar_progresso()

    def carregar_progresso(self):
        if os.path.exists(self.save_file):
            with open(self.save_file, 'r') as file:
                return json.load(file)
        return {'nivel1': False, 'nivel2': False, 'nivel3': False}

    def salvar_progresso(self):
        with open(self.save_file, 'w') as file:
            json.dump(self.niveis_completados, file)

    def completar_nivel(self, nivel):
        if nivel in self.niveis_completados:
            self.niveis_completados[nivel] = True
            self.salvar_progresso()

    def apagar_perfil(self):
        self.niveis_completados = {'nivel1': False, 'nivel2': False, 'nivel3': False}
        self.salvar_progresso()
