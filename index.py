# botao de iniciar chat
# popup para entrar no chat
# quando entrar no chat: (aparece para todos os usuarios)
#     a mensagem que voce entrou no chat
#     o campo de botao de enviar a mensagem
# a cada mensagem que voce envia : (aparece para todos os usuarios)
#     Nome: Texto da mensagem

import flet as ft
import random

# Defina uma lista de cores que você deseja atribuir aos usuários
CORES_USUARIOS = [
    ft.colors.RED_ACCENT_700,
    ft.colors.BLUE_ACCENT_700,
    ft.colors.GREEN_ACCENT_700,
    ft.colors.PURPLE_ACCENT_700,
    ft.colors.ORANGE_ACCENT_700,
    # Adicione outras cores aqui
]

def main(pagina):

    def gerar_cor_usuario(nome):
        # Use a função de hash do nome de usuário para selecionar uma cor da lista
        hash_usuario = hash(nome)
        indice_cor = hash_usuario % len(CORES_USUARIOS)
        return CORES_USUARIOS[indice_cor]
    
    msg_entrada = ft.Text("Seja bem vindo ao chat!")
    chat = ft.Column()
    nome_usuario = ft.TextField(label="Digite seu nome")

    def enviar_mensagem_tunel(mensagem):
        tipo = mensagem["tipo"]
        if tipo == "mensagem":
            conteudo = mensagem["texto"]
            usuario = mensagem["usuario"]
            cor_usuario = mensagem["cor"] 
            
            mensagem_formatada = ft.Text(f"{usuario}: {conteudo}", color=cor_usuario)
            chat.controls.append(mensagem_formatada)
        else:
            usuario = mensagem["usuario"]
            chat.controls.append(ft.Text(f"HashBot: {usuario} entrou no chat",
                                          size=12,
                                          italic=True,
                                          color=ft.colors.DEEP_ORANGE_ACCENT_700
                                         ))
        pagina.update()

    # PUBSUB
    pagina.pubsub.subscribe(enviar_mensagem_tunel)

    def enviar_mensagem(evento):
        usuario = nome_usuario.value
        mensagem_texto = campo_mensagem.value

        # Gere uma cor única para o usuário
        cor_usuario = gerar_cor_usuario(usuario)

        # Envie a mensagem para todos
        pagina.pubsub.send_all({"texto": mensagem_texto, "usuario": usuario, "cor": cor_usuario, "tipo": "mensagem"})

        # Limpe o campo de mensagem
        campo_mensagem.value = ""
        pagina.update()

    campo_mensagem = ft.TextField(label="Digite sua mensagem", on_submit=enviar_mensagem)
    botao_enviar = ft.ElevatedButton("Enviar", on_click=enviar_mensagem)


    def entrar_popup(evento):
        
        pagina.pubsub.send_all({"usuario": nome_usuario.value, "tipo": "entrada"})

        #adicionar chat
        pagina.add(chat)

        #fechar popup
        popup.open = False

        #remover botao de iniciar chat
        pagina.remove(botao_iniciar)

        #criar campo de mensagem do usuario
        pagina.add(ft.Row([
            campo_mensagem,
            botao_enviar
            ]))

        pagina.update()

    popup = ft.AlertDialog(
        open=False,
        modal=True,
        title=ft.Text("Bem vindo ao Hashzap!"),
        content=nome_usuario,
        actions=[ft.ElevatedButton("Entrar", on_click=entrar_popup)]
    )

    def entrar_chat(evento):
        pagina.dialog = popup
        popup.open = True
        pagina.update()

    botao_iniciar = ft.ElevatedButton("Iniciar Chat", on_click=entrar_chat)

    pagina.add(msg_entrada)
    pagina.add(botao_iniciar)

ft.app(target=main, view=ft.WEB_BROWSER)
