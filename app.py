import streamlit as st
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from streamlit_option_menu import option_menu
import re
import uuid

uri = "mongodb+srv://admin:Ny5g0LLbxlC2Ehcb@cluster0.qt8yb.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client.topicos
estudiantes = db.Estudiantes
maestros = db.Maestros
horarios = db.Horarios
materias = db.Materias
profesores = db.Profesores
usuarios = db.Usuarios

##FRONTEND
page_title = "SUDOKU"
page_icon = "📚" 
layout = "centered"

horas = ["16:00","17:00","18:00","19:00"]
materias_agenda = ["Matematicas","Español","Ingles","Fisica","Quimica","CENEVAL","Otro... (Especificar en notas)",]


def validar_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    if re.match(pattern, email):
        return True
    else:
        return False

def generate_uuid():
    return str(uuid.uuid4())


st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)


st.title("SUDOKU 📚")



selected = option_menu(menu_title=None, options=["Reservar", "agendas","Materias","Detalles"], 
                        icons=["calendar-date","", "clipboard-minus","journals"],

                        orientation="horizontal") 

if selected == "agendas":
    hora_buscada = st.selectbox("Hora", horas)
    resultado = estudiantes.find(
        {"hora": hora_buscada},
        {"nombre": 1, "materia": 1, "_id": 0})
    resultado = list(resultado)
    if resultado:
        st.header(f"Estudiantes en el horario {hora_buscada}:")
        for estudiante in resultado:
            st.write(f"- Nombre: {estudiante['nombre']}")
            st.write(f"-  Materia: {estudiante['materia']}")        
    else:
        st.header(f"No hay estudiantes registrados en el horario: {hora_buscada}")

if selected == "Detalles":
    st.subheader("Dirección 📍")
    st.text("Fuente de Cantos #418 - Fracc. Las Funtes")
    st.markdown("""<iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3643.5564154373074!2d-104.6155591!3d24.0467028!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x869bb7a97dbb4657%3A0x80facab57446a07!2sFuente%20de%20Cantos%20418%2C%20Las%20Fuentes%2C%2034220%20Durango%2C%20Dgo.!5e0!3m2!1ses-419!2smx!4v1717991662364!5m2!1ses-419!2smx" width="600" height="450" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>""", unsafe_allow_html=True)
    st.markdown("""<iframe src="https://www.google.com/maps/embed?pb=!4v1717992194441!6m8!1m7!1suOP9KH4IF-EwkotSvfzV8A!2m2!1d24.04678423868657!2d-104.6156675734958!3f112.41069411220789!4f-6.5140040354368125!5f0.7820865974627469" width="600" height="450" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>""", unsafe_allow_html=True) 
    st.subheader("Horarios 🕓")
    dia, hora, = st.columns(2)
    dia.text("Lunes a viernes excepto días festivos")
    hora.text("16:00 - 20:00")
    st.subheader("Contacto")
    wp, inst, fb, = st.columns(3)
    wp.markdown("[WhatsApp](https://w.app/SUDOKU)")
    inst.markdown("[Facebook](https://www.facebook.com/escueladereforzamiento?mibextid=ZbWKwL)")
    fb.markdown("[Instagram](https://www.instagram.com/sudoku_dgo?igsh=MW52YWx5ZjA3OTV3ag==)")

if selected == "Materias":
    materia_seleccionada = option_menu(menu_title="Materias", options=["Matematicas","Quimica","Ingles", "Lectoescritura", "Fisica"], orientation="vertical")
    if materia_seleccionada == "Matematicas":
        materia = materias.find_one({"nombre": materia_seleccionada})
        st.subheader(f"Materia: {materia['nombre']}")
        st.write(f"Descripcion: {materia['descripcion']}")

    if materia_seleccionada == "Quimica":
        materia = materias.find_one({"nombre": materia_seleccionada})
        st.subheader(f"Materia: {materia['nombre']}")
        st.write(f"Descripcion: {materia['descripcion']}")

    if materia_seleccionada == "Ingles":
        materia = materias.find_one({"nombre": materia_seleccionada})
        st.subheader(f"Materia: {materia['nombre']}")
        st.write(f"Descripcion: {materia['descripcion']}")

    if materia_seleccionada == "Lectoescritura":
        materia = materias.find_one({"nombre": materia_seleccionada})
        st.subheader(f"Materia: {materia['nombre']}")
        st.write(f"Descripcion: {materia['descripcion']}")

    if materia_seleccionada == "Fisica":    
        materia = materias.find_one({"nombre": materia_seleccionada})
        st.subheader(f"Materia: {materia['nombre']}")
        st.write(f"Descripcion: {materia['descripcion']}")

if selected == "Reservar":
    st.subheader("Reservar")
    c1, c2 = st.columns(2)
    nombre = c1.text_input("Nombre del alumn@*", placeholder=("Nombre"))
    email = c2.text_input("Tu email*", placeholder=("Email"))
    fecha = c1.date_input("Fecha")   
    hora = c2.selectbox("Hora", horas)
    materia = c1.selectbox("Materia",materias_agenda)
    notas = c2.text_area("Notas", placeholder=("Notas adicionales, especificaciones, etc..."))
    boton_enviar = st.button("Reservar")
    

##BACKEND
    if boton_enviar:
        try:
            with st.spinner("Reservando..."):
                if nombre =="":
                    st.warning("El nombre es obligatorio")
                elif email=="":
                    st.warning("El email es obligatorio")
                elif not validar_email(email):
                    st.warning("El email no es valido")    
                else:
                    uid = generate_uuid()
                    nuevo_estudiante={
                        "_id": uid,  
                        "materia": str(materia),
                        "email": str(email),
                        "fecha": str(fecha),
                        "hora": str(hora),
                        "nombre": str(nombre),
                        "notas": str(notas)
                        }   
                    resultado = estudiantes.insert_one(nuevo_estudiante)
                    nuevo_usuario={
                        "_id": uid,
                        "nombre": str(nombre),
                        "rol": "estudiante",
                        "fecha_creacion": str(fecha),
                    }
                    st.success("Su pasantia ha sido reservada de forma exitosa.")
        except Exception as e:
            st.error("Ha ocurrido un error, intente de nuevo")
            print(e)
            st.stop()