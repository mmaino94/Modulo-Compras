# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 13:55:00 2023

@author: mmaino
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pandas as pd
import time
import os

#data = pd.read_excel("ejemplo materiales.xlsx")

# Cargar la tabla de ejemplo de materiales desde el archivo
nombre_archivo = input("Ingrese el nombre del archivo del listado de materiales: ")
data= pd.read_excel(nombre_archivo +".xlsx")

proveedores = pd.read_excel("Tabla de datos Proveedores.xlsx")

grupos = data.groupby("Grupo")

# Crear una lista vacía para almacenar los grupos seleccionados
grupos_seleccionados = []
grupos_sin_proveedor = []

# Recorrer la tabla de ejemplo de materiales y agregar cada grupo de materiales único a la lista de grupos seleccionados
for grupo in data['Grupo'].unique():
    grupos_seleccionados.append(grupo)
    
# Imprimir los grupos disponibles
print('Grupos disponibles:')
grupos_disponibles = data['Grupo'].unique()
print(grupos_disponibles)

# Creamos un diccionario que asocia cada grupo de materiales con sus proveedores
proveedores_grupos = dict(zip(proveedores["Material"], proveedores["Mail"]))

# Creamos una lista vacía para los grupos de materiales que no tienen proveedores asociados
grupos_sin_proveedor = []

# Preguntar si el usuario desea eliminar algún grupo
eliminar = input('¿Desea eliminar algún grupo? (S/N): ')

if eliminar.lower() == 's':
    # Mostrar los grupos disponibles para enviar correo
    print('Grupos disponibles para enviar correo:')
    print(grupos.groups.keys())

    # Solicitar al usuario que ingrese los grupos a eliminar
    eliminar_grupos = input('Ingrese los grupos que desea eliminar (separados por comas): ').split(',')

    # Eliminar los espacios en blanco de los nombres de grupo
    eliminar_grupos = [grupo.strip() for grupo in eliminar_grupos]
    
    #Prueba de ver si actualiza grupos
    grupos = [grupo for grupo in grupos]

    # Eliminar los grupos seleccionados de la lista de grupos a enviar correo
    for grupo in eliminar_grupos:
        if grupo in grupos_seleccionados:
            grupos_seleccionados.remove(grupo)
            print(f'Se ha eliminado el grupo {grupo} de la lista de grupos seleccionados.')
        else:
            print(f'El grupo {grupo} no se encontraba en la lista de grupos seleccionados.')
else:
    print('No se eliminará ningún grupo.')
    
for grupo in grupos_seleccionados:
    # Verificamos si el grupo tiene proveedor asociado
    if grupo not in proveedores_grupos:
        grupos_sin_proveedor.append(grupo)
        continue



# Obtner la dirección de correo electrónico y la contraseña del usuario
while True:
    direccion_correo = input('Ingrese su dirección de correo electrónico: ')
    contraseña = input('Ingrese su contraseña: ')
    
    # Crear un objeto SMTP para verificar las credenciales
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    
    try:
        # Intentar iniciar sesión en el servidor SMTP
        server.login(direccion_correo, contraseña)
        break
    except smtplib.SMTPAuthenticationError:
        # Si se produce un error al intentar iniciar sesión, solicitar al usuario que ingrese las credenciales nuevamente
        print('Las credenciales ingresadas son incorrectas. Por favor, inténtelo nuevamente.')
    
    # Cerrar la conexión SMTP
    server.quit()


titulo = input("Ingrese asunto del correo: ")
"""
for grupo, datos in grupos:
    
    # Seleccionar los correos electrónicos de los proveedores para este grupo
    correos = proveedores.loc[proveedores["Material"] == grupo,"Mail"].tolist()
    if correos:        
        # Crear un dataframe con los datos del grupo
        df_grupo = pd.DataFrame(datos)
        df_grupo = df_grupo.drop(["Grupo"],axis=1)
        
        # Crear el cuerpo del correo electrónico
        cuerpo_correo = 'Estimado,envio solicitud de materiales para cotizar:\n\n'+ df_grupo.to_string(index=False)+ "\n\n Desde ya muchas gracias." 
        
        
        ##HASTA ACA FUNCIONA BIEN LA GENERACION DEL MAIL
        
        # CODIGO QUE ANDA PARA ENVIAR MAILS A VARIOS
        # Configuración del servidor SMTP y credenciales
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        smtp_username = direccion_correo
        smtp_password = contraseña
        
        message = MIMEMultipart()
        message['From'] = smtp_username
        message['Subject'] = titulo
        body = cuerpo_correo
        message.attach(MIMEText(body, 'plain'))
        
        # Lista de destinatarios
        to_list = correos[0:2]
        bcc_list = correos[2:]
        
        
        # Envío del correo electrónico con copia oculta
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            for to_address in to_list:
                recipients = [to_address] + bcc_list
                server.sendmail(smtp_username, recipients, message.as_string())
        
    else:
        # Si no hay proveedores para este grupo, imprimir un mensaje de aviso
        print(f"No hay proveedores asociados para el grupo {grupo}. No se enviará correo electrónico.")

"""
print("No encontro proveedor para pedir materiales de: " + ", ".join(grupos_sin_proveedor))