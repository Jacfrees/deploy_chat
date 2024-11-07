from flask import Blueprint, request

from app.IA.openIA import get_chatgpt_response
from app.IA.geminiIA import get_gemini_response
from app.routes.metadata_routes import get_metadata_by_code
from app.routes.project_routes import get_projects
from app.services.twilio_services import sendMessageTwilio, sendMessageTwilioWithTemplate, update_list_projects

msg_bp = Blueprint('msg', __name__)


def display_projects(projects):
    messages = []
    for i, project in enumerate(projects, 1):
        name = project.get('name', 'N/A')
        code = project.get('code', 'N/A')
        project_message = f'{i}. Nombre: {name}\n   Código: {code}\n\n'
        messages.append(project_message)
    return ''.join(messages)


# Diccionario para almacenar el estado del usuario
user_states = {}


@msg_bp.route("/Chatbot", methods=['POST'])
def menu_whatsapp():
    message = ''
    user_message = request.values.get('Body', '').strip()
    user_phone = request.values.get('From', '')
    user_phone_clean = user_phone.replace("whatsapp:", "")
    print("user_phone ====> ", user_phone)
    print('user_message ===> ' + user_message)

    show_menu = False
    sid_list_projects = ''
    template_to_show = ''
    sid_projects = 'HXe2886cbdc159859d120124bc7a49d605'

    if user_phone_clean not in user_states:
        projects = get_projects()
        user_states[user_phone_clean] = {'step': 'inicio', 'projects': projects}
        message = f'Hola, aquí tienes una lista de los proyectos que tengo disponibles'

        #sid_list_projects = update_list_projects(projects, sid_list_projects)
        template_to_show = sid_projects
        show_menu = True
    elif user_message.lower() == 'change_project':
        projects = get_projects()
        user_states[user_phone_clean] = {'step': 'inicio', 'projects': projects}
        template_to_show = sid_projects
        show_menu = True
    else:
        user_state = user_states[user_phone_clean]
        current_step = user_state['step']

        if current_step == 'inicio':
            try:
                selection = int(user_message)
                projects = user_state['projects']
                if 1 <= selection <= len(projects):
                    selected_project = projects[selection - 1]
                    user_state['selected_project'] = selected_project
                    user_state['step'] = 'selected'
                    message = f"Has seleccionado el proyecto: *{selected_project.get('name')}* con el código: *{selected_project.get('code')}*\nAhora puedes hacer preguntas sobre este proyecto."
                else:
                    message = "Selección inválida. Por favor, ingresa un número válido."
            except ValueError:
                message = "Entrada inválida. Por favor selecciona un proyecto de la lista."
        elif current_step == 'selected':
            if user_message.lower() == 'continue_in_project':
                message = f"Sigues en el proyecto *{user_state['selected_project'].get('name')}* con el código: *{user_state['selected_project'].get('code')}*. ¿Qué otra pregunta tienes?"
            else:
                selected_project = user_state.get('selected_project')
                if selected_project:
                    metadata_project = get_metadata_by_code(selected_project.get('code'))
                    question = f"basado en '{metadata_project.get('metadata')}' {user_message} , todo en menos de 1000 caracteres"
                    message = get_gemini_response(question)

                    show_menu = True
                    template_to_show = 'HX96c186379e6e1995f3de1b15b482bee6'
                else:
                    message = "Hubo un problema al recuperar el proyecto seleccionado."

    if message != '':
        sendMessageTwilio(user_phone, message)
    if show_menu:
        sendMessageTwilioWithTemplate(user_phone, template_to_show)
        show_menu = False
        template_to_show = ''

    return "Success", 200
