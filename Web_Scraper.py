from bs4 import BeautifulSoup
import requests
import pandas  as pd
import warnings
warnings.filterwarnings('ignore')
import time 
import re 
import numpy as np
import os 

#Los que tiene li en la tabla y ahi esta la información 

def Articulos(table,name,informacion):
    i = 1
    for val in table.find_all('blockquote'):
        articulo = val.next_element
        title_re = '".*?\"'
        title = re.findall(title_re, articulo)[0].replace('"','')
        pais_re = r'En: (.*?)\xa0'
        pais = re.findall(pais_re, articulo)[0]
        revista = val.find_all('br')[0].next_sibling.strip()
        ISNN = val.find_all('i')[0].next_sibling.strip()
        ed = val.find_all('i')[1].next_sibling.strip()
        year_aux  = val.find_all('i')[3].next_sibling.strip()
        year_re = ',[0-9]{4},' 
        year = re.findall(year_re, year_aux)[0].replace(',','')
        try:
            doi = val.find_all('i')[4].next_sibling.strip()
        except:
            doi = ''
        paginas = val.find_all('i')[3].next_sibling.strip()
        try:    
            paginas_aux = (paginas.split(',')[0].split('\r\n')[1].strip() +  paginas.split(',')[0].split('\r\n')[2].strip())
        except: 
            paginas:aux = ''
        volumen = val.find_all('i')[2].next_sibling.strip()
        informacion.append([name,f'Artículos_{i}-Pais',pais])
        informacion.append([name,f'Artículos_{i}-Titulo',title])
        informacion.append([name,f'Artículos_{i}-Revista',revista])
        informacion.append([name,f'Artículos_{i}-ISNN',ISNN])
        informacion.append([name,f'Artículos_{i}-Editorial',ed])
        informacion.append([name,f'Artículos_{i}-Año',year])
        informacion.append([name,f'Artículos_{i}-Doi',doi])
        informacion.append([name,f'Artículos_{i}-Paginas',paginas_aux])
        informacion.append([name,f'Artículos_{i}-Volumen',volumen])
        i = i +1 
    return informacion

def Trabajos_Dirigidos(table,name,informacion):
    i = 1
    for val in table.find_all('blockquote'):
        string  = val.text
        string_aux = string.replace('\xa0\r\n',',')
        nivel_aux = table.find_all('li')[i-1].text
        nivel = nivel_aux.split('- ')
        title = string_aux.split(',')
        title_aux = val.next_element.replace('\xa0','**').split('**')[0].replace('\r\n','').strip().split('  ')[-1]
        Institucion_aux = val.next_element.replace('\xa0','**').split('**')[1].strip()
        if 'Estado:' not in Institucion_aux:
            Institucion = Institucion_aux
        else:
            Institucion = ''      
        universidad = string.split('Estado:')[0].split(f'{title[1].lstrip()}')[1].strip()
        Estado = string.split('Estado:')[1].split('\xa0\r\n ')[0]
        year_re = '[1-2][0-9]{3}'
        year = re.search(year_re, string.split('Estado:')[1]).group(0)
        programa = string.split(Estado)[1].split(f'{year}')[0].strip().replace(',','')
        dirigido_re = 'Dirigió como:(.*?),'
        dirigido = re.findall(dirigido_re, string.split('Estado:')[1])[0]
        informacion.append([name,f'Trabajos dirigidos/tutorías_{i}-Nivel',nivel[1]])
        informacion.append([name,f'Trabajos dirigidos/tutorías_{i}-Titulo',title_aux])
        informacion.append([name,f'Trabajos dirigidos/tutorías_{i}-Universidad',universidad])
        informacion.append([name,f'Trabajos dirigidos/tutorías_{i}-Estado',Estado])
        informacion.append([name,f'Trabajos dirigidos/tutorías_{i}-Año',year])
        informacion.append([name,f'Trabajos dirigidos/tutorías_{i}-Programa',programa])
        informacion.append([name,f'Trabajos dirigidos/tutorías_{i}-Institucion',Institucion])
        informacion.append([name,f'Trabajos dirigidos/tutorías_{i}-Dirigido',dirigido])
        i = i+ 1

    return informacion

def Asesorias(table,name,informacion):
    i = 1
    for val in table.find_all('blockquote'):
        string1 = val.text
        institucion_re = 'Institución: (.*?),' 
        institucion = re.findall(institucion_re, string1)[0]
        ciudad = string1.split('Ciudad: ')[1]
        informacion.append([name,f'Asesorías_{i}-Institución',institucion])
        informacion.append([name,f'Asesorías_{i}-Ciudad',ciudad])
        informacion.append([name,f'Asesorías_{i}-Proyecto',table.find_all('b')[i-1].text])
        i = i+1
    
    return informacion 

def CursoCortaDuración(table,name,informacion):
    i = 1
    for val in table.find_all('blockquote'):
        curso = val.text
        nivel_aux = table.find_all('b')[i-1].text
        try:
            nivel = nivel_aux.split('- ')[2]
        except:
            nivel  = 'Otro'
        nombre = val.next_element.split(',')[-2].strip()
        pais_re = 'En: (.*?)\n'
        pais = re.findall(pais_re, curso)
        year = curso.split(pais[0])[1].split(',')[1]
        try:
            participacion = curso.split('participación: ')[1].split(',')[0].rstrip()
        except:
            participacion = 'Otro'
        try:
            duracion = int(curso.split(' semanas')[0].split(f'{participacion}')[1].split(',')[-1])
        except:
            duracion = 'N/A'
        informacion.append([name,f'Cursos de corta duración_{i}-Nivel',nivel])
        informacion.append([name,f'Cursos de corta duración_{i}-Nombre',nombre])
        informacion.append([name,f'Cursos de corta duración_{i}-Pais',pais[0].replace(',','')])
        informacion.append([name,f'Cursos de corta duración_{i}-Año',year])
        informacion.append([name,f'Cursos de corta duración_{i}-Participacion',participacion])
        informacion.append([name,f'Cursos de corta duración_{i}-Semanas',duracion])

        i = i +1 
    return informacion

def JuradoComiteEvaluacion(table,name,informacion):
    i = 1
    for val in table.find_all('blockquote'):
        nivel_aux = table.find_all('li')[i-1].text
        nivel = nivel_aux.split('- ')[2]
        informacion.append([name,f'Jurado en comités de evaluación_{i}-Nivel',nivel])
        campos = [f'Jurado en comités de evaluación_{i}-Titulo',f'Jurado en comités de evaluación_{i}-Tipo'
                  ,f'Jurado en comités de evaluación_{i}-Institucion',f'Jurado en comités de evaluación_{i}-Programa']
        j = 0 
        for x in val.find_all('i'):
            try:
                val1  = str(x.next_sibling).strip()
                informacion.append([name,campos[j],val1])
            except:
                pass
            j = j +1 
        i = i+1
    return informacion

def ParEvaluador(table,name,informacion):
    i = 1 
    for val in table.find_all('blockquote'):
        ambito = str(val.find_all('i')[0].next_sibling).strip()
        evaluadorde = str(val.find_all('i')[1].next_sibling).strip()
        string_aux = str(val.find_all('i')[2].next_sibling).replace('\xa0','**')
        
        revista = string_aux.split('**')[0].replace(',','')
        Tipo = val.find_all('i')[2].text.replace(':','')
        year_re = '[0-9]{4}'
        year = re.findall(year_re, string_aux)
        try:
            year = year[0]
        except:
            year = 'N/A'
        informacion.append([name,f'Par evaluador_{i}-Ambito',ambito])
        informacion.append([name,f'Par evaluador_{i}-EvaluadorDe',evaluadorde])
        informacion.append([name,f'Par evaluador_{i}-Revista',revista])
        informacion.append([name,f'Par evaluador_{i}-Año',year])
        informacion.append([name,f'Par evaluador_{i}-Tipo',Tipo])
        i = i +1 
    return informacion

def ComitesEvaluacion(table,name,informacion):
    i = 1
    for val in table.find_all('blockquote'):
        nivel_aux = table.find_all('li')[i-1].text
        tipo =nivel_aux.split('- ')[2]
        institucion = str(val.find_all('i')[0].next_sibling.strip())
        titulo = str(val.next_element).split(',')[1].strip()
        informacion.append([name,f'Participación en comités de evaluación_{i}-Tipo',tipo])
        informacion.append([name,f'Participación en comités de evaluación_{i}-Institucion',institucion])
        informacion.append([name,f'Participación en comités de evaluación_{i}-Titulo',titulo])
        i = i +1 
    return informacion

def PublicacionesNoEspecializadas(table,name,informacion):
    i = 1
    for val in table.find_all('blockquote'):
        Nombre_Producto = val.find_all('i')[0].next_sibling.strip().replace(',','')
        Fecha =  val.find_all('i')[1].next_sibling.strip().replace(',','').split(' -')[0]
        MedioVerificacion =  val.find_all('i')[3].next_sibling.strip().replace(',','')
        RutaVerificacion = val.find_all('i')[4].next_sibling.strip().replace(',','')
        informacion.append([name,f'Publicaciones editoriales no especializadas_{i}-Nombre',Nombre_Producto])
        informacion.append([name,f'Publicaciones editoriales no especializadas_{i}-Fecha',Fecha])
        informacion.append([name,f'Publicaciones editoriales no especializadas_{i}-Medio Verificación',MedioVerificacion])
        informacion.append([name,f'Publicaciones editoriales no especializadas_{i}-Ruta Circulación',RutaVerificacion])
        i =  i +1 
    return informacion
        
def DigitalAudiovisual(table,name,informacion):
    i = 1
    for val in table.find_all('blockquote'):
        nivel_aux = table.find_all('b')[i-1].text
        tipo =nivel_aux.split('- ')[3]
        Titulo = val.find_all('i')[0].next_sibling.strip().replace(',','')
        Fecha_aux = val.find_all('i')[1].next_sibling.strip()
        Fecha_re = '[0-9]{4}'
        Fecha = re.search(Fecha_re, Fecha_aux).group(0)
        MedioVerificacion  = val.find_all('i')[3].next_sibling.strip().replace(',','')
        RutaCiruculacion = val.find_all('i')[4].next_sibling.strip().replace(',','')
        informacion.append([name,f'Producciones de contenido digital Audiovisual_{i}-Tipo',tipo])
        informacion.append([name,f'Producciones de contenido digital Audiovisual_{i}-Titulo',Titulo])
        informacion.append([name,f'Producciones de contenido digital Audiovisual_{i}-Fecha',Fecha])
        informacion.append([name,f'Producciones de contenido digital Audiovisual_{i}-Medio Verificación',MedioVerificacion])
        informacion.append([name,f'Producciones de contenido digital Audiovisual_{i}-Ruta Circulación',RutaCiruculacion])
        i =  i +1 
    return informacion

def DigitalSonoro(table,name,informacion):
    i = 1
    for val in table.find_all('blockquote'):
        nivel_aux = table.find_all('b')[i-1].text
        tipo =nivel_aux.split('- ')[3]
        Titulo = val.find_all('i')[0].next_sibling.strip().replace(',','')
        Fecha_aux = val.find_all('i')[1].next_sibling.strip()
        Fecha_re = '[0-9]{4}'
        Fecha = re.search(Fecha_re, Fecha_aux).group(0)
        MedioVerificacion  = val.find_all('i')[3].next_sibling.strip().replace(',','')
        RutaCiruculacion = val.find_all('i')[4].next_sibling.strip().replace(',','')
        informacion.append([name,f'Producciones de contenido digital Sonoro_{i}-Tipo',tipo])
        informacion.append([name,f'Producciones de contenido digital Sonoro_{i}-Titulo',Titulo])
        informacion.append([name,f'Producciones de contenido digital Sonoro_{i}-Fecha',Fecha])
        informacion.append([name,f'Producciones de contenido digital Sonoro_{i}-Medio Verificación',MedioVerificacion])
        informacion.append([name,f'Producciones de contenido digital Sonoro_{i}-Ruta Circulación',RutaCiruculacion])
        i =  i +1 
    return informacion

def RecursosGraficos(table,name,informacion):
    i = 1
    for val in table.find_all('blockquote'):
        nivel_aux = table.find_all('b')[i-1].text
        tipo =nivel_aux.split('- ')[3]
        Titulo = val.find_all('i')[0].next_sibling.strip().replace(',','')
        Fecha_aux = val.find_all('i')[1].next_sibling.strip()
        Fecha_re = '[0-9]{4}'
        Fecha = re.search(Fecha_re, Fecha_aux).group(0)
        MedioVerificacion  = val.find_all('i')[3].next_sibling.strip().replace(',','')
        RutaCiruculacion = val.find_all('i')[4].next_sibling.strip().replace(',','')
        informacion.append([name,f'Producciones de contenido digital Recursos gráficos_{i}-Tipo',tipo])
        informacion.append([name,f'Producciones de contenido digital Recursos gráficos_{i}-Titulo',Titulo])
        informacion.append([name,f'Producciones de contenido digital Recursos gráficos_{i}-Fecha',Fecha])
        informacion.append([name,f'Producciones de contenido digital Recursos gráficos_{i}-Medio Verificación',MedioVerificacion])
        informacion.append([name,f'Producciones de contenido digital Recursos gráficos_{i}-Ruta Circulación',RutaCiruculacion])
        i =  i +1 
    return informacion
     
def ContenidoTransmedia(table,name,informacion):
    i = 1
    for val in table.find_all('blockquote'):
        Titulo = val.find_all('i')[0].next_sibling.strip().replace(',','')
        Fecha_aux = val.find_all('i')[1].next_sibling.strip()
        Fecha_re = '[0-9]{4}'
        Fecha = re.search(Fecha_re, Fecha_aux).group(0)
        MedioVerificacion  = val.find_all('i')[3].next_sibling.strip().replace(',','')
        RutaCiruculacion = val.find_all('i')[4].next_sibling.strip().replace(',','')
        informacion.append([name,f'Producción de estrategias y contenidos transmedia_{i}-Titulo',Titulo])
        informacion.append([name,f'Producción de estrategias y contenidos transmedia_{i}-Fecha',Fecha])
        informacion.append([name,f'Producción de estrategias y contenidos transmedia_{i}-Medio Verificación',MedioVerificacion])
        informacion.append([name,f'Producción de estrategias y contenidos transmedia_{i}-Ruta Circulación',RutaCiruculacion])
        i =  i +1 
    return informacion

def DesarrolloWeb(table,name,informacion):
    i = 1
    for val in table.find_all('blockquote'):
        Titulo = val.find_all('i')[0].next_sibling.strip().replace(',','')
        Fecha_aux = val.find_all('i')[1].next_sibling.strip()
        Fecha_re = '[0-9]{4}'
        Fecha = re.search(Fecha_re, Fecha_aux).group(0)
        MedioVerificacion  = val.find_all('i')[3].next_sibling.strip().replace(',','')
        RutaCiruculacion = val.find_all('i')[4].next_sibling.strip().replace(',','')
        informacion.append([name,f'Desarrollos web_{i}-Titulo',Titulo])
        informacion.append([name,f'Desarrollos web_{i}-Fecha',Fecha])
        informacion.append([name,f'Desarrollos web_{i}-Medio Verificación',MedioVerificacion])
        informacion.append([name,f'Desarrollos web_{i}-Ruta Circulación',RutaCiruculacion])
        i =  i +1 
    return informacion

def InteresSocial(table,name,informacion):
    i = 1
    for val in table.find_all('blockquote'):
        Titulo = val.find_all('i')[0].next_sibling.strip().replace(',','')
        Fecha_aux = val.find_all('i')[1].next_sibling.strip()
        Fecha_re = '[0-9]{4}'
        Fecha = re.search(Fecha_re, Fecha_aux).group(0)
        MedioVerificacion  = val.find_all('i')[2].next_sibling.strip().replace(',','')
        Licencia = val.find_all('i')[3].next_sibling.strip().replace(',','')
        Formato = val.find_all('i')[4].next_sibling.strip().replace(',','')
        informacion.append([name,f'Fortalecimiento o solución de asuntos de interés social_{i}-Titulo',Titulo])
        informacion.append([name,f'Fortalecimiento o solución de asuntos de interés social_{i}-Fecha',Fecha])
        informacion.append([name,f'Fortalecimiento o solución de asuntos de interés social_{i}-Medio Verificación',MedioVerificacion])
        informacion.append([name,f'Fortalecimiento o solución de asuntos de interés social_{i}-Licencia Verficación',Licencia])
        informacion.append([name,f'Fortalecimiento o solución de asuntos de interés social_{i}-Formato',Formato])
        i =  i +1 
    return informacion
        
def CadenasProductivas(table,name,informacion):
    i = 1
    for val in table.find_all('blockquote'):
        Titulo = val.find_all('i')[0].next_sibling.strip().replace(',','')
        Fecha_aux = val.find_all('i')[1].next_sibling.strip()
        Fecha_re = '[0-9]{4}'
        Fecha = re.search(Fecha_re, Fecha_aux).group(0)
        MedioVerificacion  = val.find_all('i')[2].next_sibling.strip().replace(',','')
        Licencia = val.find_all('i')[3].next_sibling.strip().replace(',','')
        Formato = val.find_all('i')[4].next_sibling.strip().replace(',','')
        informacion.append([name,f'Fortalecimiento de cadenas productivas_{i}-Titulo',Titulo])
        informacion.append([name,f'Fortalecimiento de cadenas productivas_{i}-Fecha',Fecha])
        informacion.append([name,f'Fortalecimiento de cadenas productivas_{i}-Medio Verificación',MedioVerificacion])
        informacion.append([name,f'Fortalecimiento de cadenas productivas_{i}-Licencia Verficación',Licencia])
        informacion.append([name,f'Fortalecimiento de cadenas productivas_{i}-Formato',Formato])
        i =  i +1 
    return informacion

def Consultorias(table,name,informacion):
    i = 1
    for val in table.find_all('blockquote'):
        nivel_aux = table.find_all('b')[i-1].text
        try:
            tipo =nivel_aux.split('- ')[2]
        except:
            tipo = 'Otra'
        #print(tipo)
        
        titulo = str(val.next_element).strip().replace('\r\n','').split('  ')[-1]
        registro = val.find_all('i')[1].next_sibling.strip().replace(',','')
        registro_re = 'contrato/registro:(.*?),'
        registro = re.findall(registro_re, val.text)[0].strip()
        pais_re = 'En:(.*?),'
        pais = re.findall(pais_re, val.text)[0].strip()
        year_re = ',([0-9]{4}),'
        year = re.findall(year_re, val.text)[0].strip()
        try:
            meses = float(val.text.split(f'{year},')[1].split('meses')[0].strip())
        except:
            meses = 0
        informacion.append([name,f'Consultorías_{i}-Tipo',tipo])
        informacion.append([name,f'Consultorías_{i}-Titulo',titulo])
        informacion.append([name,f'Consultorías_{i}-Registro',registro])
        informacion.append([name,f'Consultorías_{i}-Pais',pais])
        informacion.append([name,f'Consultorías_{i}-Año',year])
        informacion.append([name,f'Consultorías_{i}-Meses',meses])
        i =  i +1 
    return informacion

def DocumentosTrabajo(table,name,informacion):
    i = 1
    for val in table.find_all('blockquote'):
        string_aux = str(val.next_element)
        titulo_re = '".*?\"'
        titulo = re.findall(titulo_re, string_aux)[0]
        string_aux2 = string_aux.split('En: ')[1]
        year_re = '([0-9]{4}).'
        year = re.findall(year_re, string_aux2)[0]
        informacion.append([name,f'Documentos de trabajo_{i}-Titulo',titulo])
        informacion.append([name,f'Documentos de trabajo_{i}-Año',year])      
        i =  i +1 
    return informacion

def EdicionesRevisiones(table,name,informacion):
    i = 1
    for val in table.find_all('blockquote'):
        #string_aux = str(val.next_element)
        try:
            nivel_aux = table.find_all('b')[i-1].text
            nivel = nivel_aux.split('- ')[2]
        except:
            nivel = 'Otro'
        
        registro = val.find_all('i')[1].next_sibling.strip()
        Fecha_Re = ',([0-9]{4}),'
        Fecha = re.findall(Fecha_Re, registro)[0]
        pais_re = 'En:(.*?),'
        pais = re.findall(pais_re, registro)[0].strip()
        paginas = registro.split('p.')[-1]
        editorial = registro.split(f',{Fecha},')[-1].split('p.')[0].strip()
        #print(registro.split(f',{Fecha},')[-1].split('p.')[0].strip())
        #print(Fecha)
        informacion.append([name,f'Ediciones/revisiones_{i}-Nivel',nivel])
        informacion.append([name,f'Ediciones/revisiones_{i}-Año',Fecha])  
        informacion.append([name,f'Ediciones/revisiones_{i}-Pais',pais])  
        informacion.append([name,f'Ediciones/revisiones_{i}-Paginas',paginas]) 
        informacion.append([name,f'Ediciones/revisiones_{i}-Editorial',editorial]) 
        
        i =  i +1 
    return informacion

def EventosCientificos(table,name,informacion):
    i = 1
    for val in table.find_all('table'):
        aux_1 = val.find_all('td')
        aux_2 = aux_1[0].find_all('i')
        Nombre = aux_2[0].next_sibling.strip()
        tipo = aux_2[1].next_sibling.strip()
        Ambito = aux_2[2].next_sibling.strip()
        Ambito_aux = aux_2[2].next_sibling.next_element.text
        Fechas = '[0-9]{4}-[0-9]{2}-[0-9]{2}'
        Fecha = re.findall(Fechas, Ambito_aux)
        try:
            Fecha_inicio = Fecha[0]
        except:
            Fecha_inicio = ''
        try:
            Fecha_final = Fecha[1]
        except:
            Fecha_final  = ''
        Ciudad_re = 'en(.*?)-'
        Ciudad  = re.findall(Ciudad_re, Ambito_aux)[0].strip()
        Lugar = Ambito_aux.replace('\xa0','**').split('**')[-2].strip()
        j = 1
        for producto in val.find_all('tr')[1].find_all('ul'):
            nombre_producto = str(producto.find_all('i')[0].next_sibling).strip()
            tipo_producto = str(producto.find_all('i')[1].next_sibling).strip()
            informacion.append([name,f'Eventos científicos_{i},{j}-Nombre Producto',nombre_producto])
            informacion.append([name,f'Eventos científicos_{i},{j}-Tipo Producto',tipo_producto])
            j = j +1 
            
        j =  1    
        for institucion in val.find_all('tr')[2].find_all('ul'):
            nombre_institucion = str(institucion.find_all('i')[0].next_sibling).strip()
            tipo_institucion = str(institucion.find_all('i')[1].next_sibling).strip()
            informacion.append([name,f'Eventos científicos_{i},{j}-Nombre Institución',nombre_institucion])
            informacion.append([name,f'Eventos científicos_{i},{j}-Tipo Institución',tipo_institucion])
            j = j +1
        Rol = str(val.find_all('tr')[3].find_all('i')[1].next_sibling).strip()  
        informacion.append([name,f'Eventos científicos_{i}-Rol',Rol])
        #print(val.find_all('tr')[1].find_all('ul'))

        informacion.append([name,f'Eventos científicos_{i}-Nombre',Nombre])
        informacion.append([name,f'Eventos científicos_{i}-Tipo',tipo])
        informacion.append([name,f'Eventos científicos_{i}-Ambito',Ambito])
        informacion.append([name,f'Eventos científicos_{i}-Fecha Inicio',Fecha_inicio])  
        informacion.append([name,f'Eventos científicos_{i}-Fecha Final',Fecha_final])  
        informacion.append([name,f'Eventos científicos_{i}-Ciudad',Ciudad]) 
        informacion.append([name,f'Eventos científicos_{i}-Lugar',Lugar])
        i =  i +1 
    return informacion
    
def InformeInvestigacion(table,name,informacion):
    i = 1
    for val in table.find_all('blockquote'):
        string_aux = str(val.next_element)
        Titulo = string_aux.split('. En:')[0].strip().replace('\r\n','').split('  ')[-1]
        Fecha_aux =  string_aux.split('. En:')[1]
        Fecha_re = '[0-9]{4}'
        Fecha = re.findall(Fecha_re, Fecha_aux)[0]        
        informacion.append([name,f'Informes de investigación_{i}-Titulo',Titulo])
        informacion.append([name,f'Informes de investigación_{i}-Año',Fecha])         
        i =  i +1 
    return informacion

def InformesTecnicos(table,name,informacion):
    i = 1
    for val in table.find_all('blockquote'):
        string_aux = str(val.next_element)
        Titulo = string_aux.replace('\r\n','').replace('  ','')      
        Contrato = val.find_all('i')[1].next_sibling.split(',')[0].strip()
        string_aux2 = val.find_all('i')[1].next_sibling
        pais_re = 'En:(.*?),'
        pais = re.findall(pais_re, string_aux2)[0].strip()
        Fecha_re = ',[0-9]{4},'
        try:
            Fecha = re.findall(Fecha_re, string_aux2)[0].strip().replace(',','')
        except:
            Fecha = ''
        Meses_re = '(.*?)meses'
        Mes = re.findall(Meses_re, string_aux2)[0].strip()
        Paginas = string_aux2.split('p.')[-1].strip()
        informacion.append([name,f'Informes técnicos_{i}-Titulo',Titulo])
        informacion.append([name,f'Informes técnicos_{i}-Contrato',Contrato])       
        informacion.append([name,f'Informes técnicos_{i}-Pais',pais])
        informacion.append([name,f'Informes técnicos_{i}-Fecha',Fecha])
        informacion.append([name,f'Informes técnicos_{i}-Meses',Mes])
        informacion.append([name,f'Informes técnicos_{i}-Paginas',Paginas])
        
        i =  i +1 
    return informacion

def RedesConocimiento(table,name,informacion):
    i = 1
    for val in table.find_all('blockquote'):
        #string_aux = str(val.next_element)
        Nombre = val.find_all('i')[0].next_sibling
        Tipo = val.find_all('i')[1].next_sibling.replace(',','')
        Fecha_aux = val.find_all('i')[1].next_sibling.next_element.text
        Fecha_re = '[0-9]{4}-[0-9]{2}-[0-9]{2}'
        
        try:
            Fecha = re.findall(Fecha_re, Fecha_aux)[0]
        except:
            Fecha = ''
        informacion.append([name,f'Redes de conocimiento especializado_{i}-Nombre',str(Nombre)])
        informacion.append([name,f'Redes de conocimiento especializado_{i}-Tipo',Tipo])
        informacion.append([name,f'Redes de conocimiento especializado_{i}-Fecha Creacion',Fecha])  
        i =  i +1 
    return informacion

def ObrasProductos(table,name,informacion):
    i = 1
    for val in table.find_all('blockquote'):
        #string_aux = str(val.next_element)
        Nombre = val.find_all('i')[0].next_sibling.strip().replace(',','')
        Disiplina = val.find_all('i')[1].next_sibling.strip().split('--')[-1].replace(',','')
        Creacion = val.find_all('i')[2].next_sibling.strip()
       
        informacion.append([name,f'Obras o productos_{i}-Nombre',Nombre])
        informacion.append([name,f'Obras o productos_{i}-Disciplina',Disiplina])
        informacion.append([name,f'Obras o productos_{i}-Fecha Creacion',Creacion])
        j = 1 
        for x in val.find_all('li'):
            val = x.text
            Fecha_re = '[0-9]{4}-[0-9]{2}-[0-9]{2}'
            try:
                Fecha = re.findall(Fecha_re, val)[0]
            except: 
                Fecha = ''
            Entidad_convocante = val.split(':')[-1].strip()
            informacion.append([name,f'Obras o productos_{i}-Fecha Presentacion {j}',Fecha])
            informacion.append([name,f'Obras o productos_{i}-Entidad Convocante {j}',Entidad_convocante])
            j = j + 1
        
        i =  i +1 
    return informacion


def IndustriasCreativas(table,name,informacion):
    i = 1
    for val in table.find_all('blockquote'):
        Nombre = val.find_all('i')[0].next_sibling.strip()
        Nit = val.find_all('i')[1].next_sibling.strip()
        Fecha_aux = val.find_all('i')[2].next_sibling.strip()
        Fecha_re = '[0-9]{4}-[0-9]{2}-[0-9]{2}'
        Fecha = re.findall(Fecha_re, Fecha_aux)[0]
        informacion.append([name,f'Industrias Creativas y culturales_{i}-Nombre Empresa Creativa',Nombre])
        informacion.append([name,f'Industrias Creativas y culturales_{i}-Nit/Registro',Nit])
        informacion.append([name,f'Industrias Creativas y culturales_{i}-Fecha',Fecha])      
        i =  i +1 
    return informacion


def EventosArtisticos(table,name,informacion):
    i = 1
    for val in table.find_all('blockquote'):
        Nombre = val.find_all('i')[0].next_sibling.strip()
        Fecha_aux = val.find_all('i')[1].next_sibling.strip()
        Fecha_re = '[0-9]{4}-[0-9]{2}-[0-9]{2}'
        Fecha = re.findall(Fecha_re, Fecha_aux)[0]
        Tipo_Evento = val.find_all('i')[2].next_sibling.strip()
        
        informacion.append([name,f'Eventos artísticos_{i}-Nombre Evento',Nombre])
        informacion.append([name,f'Eventos artísticos_{i}-Fecha',Fecha])
        informacion.append([name,f'Eventos artísticos_{i}-Tipo Evento',Tipo_Evento])
        i =  i +1 
    return informacion


def TalleresCreativos(table,name,informacion):
    i = 1
    for val in table.find_all('blockquote'):
        string = val.next_element
        #print(val.next_element)
        Nombre_re = 'Nombre del taller:(.*?)Tipo'
        try:
            Nombre = re.findall(Nombre_re, val.text)[0].strip()
        except:
            Nombre  = 'N/A'
        Tipo_re = 'Tipo de taller:(.*?),'
        try:
            Tipo = re.findall(Tipo_re, string)[0].strip()
        except:
            Tipo = 'N/A'
        Fecha_aux = val.find_all('br')[0].next_sibling.strip()
        Fecha_inicio_re = '[0-9]{4}-[0-9]{2}-[0-9]{2}'
        Fecha  = re.findall(Fecha_inicio_re, Fecha_aux)
        try:
            Fecha_inicio = Fecha[0]
        except:
            Fecha_inicio = ''
        try:
            Fecha_Fin = Fecha[1]
        except:
            Fecha_Fin = ''
        
        Lugar_aux = val.find_all('br')[1].next_sibling.strip()
        Lugar = Lugar_aux.split(':')[-1].strip()
        Participacion_re = 'Participación:(.*?)'
        try:
            Participacion = re.findall(Participacion_re, string)[0]
        except: 
            Participacion  = 'N/A'
            
        Ambito_aux = val.find_all('br')[2].next_sibling.strip()
        ambio_re = 'Ámbito:(.*?),'
        try:
            ambito = re.findall(ambio_re, Ambito_aux)[0].strip()
        except: 
            ambito ='N/A'
        distincion_re = 'Distinción obtenida:(.*?),'
        try:
            distincion = re.findall(distincion_re, Ambito_aux)[0].strip()
        except: 
            distincion = 'N/A'
        try:
            Mecanimos = Ambito_aux.split('Mecanismo de selección:')[-1].strip()    
        except: 
            Mecanimos  = 'N/A'
        informacion.append([name,f'Talleres Creativos_{i}-Nombre',Nombre])
        informacion.append([name,f'Talleres Creativos_{i}-Tipo',Tipo])
        informacion.append([name,f'Talleres Creativos_{i}-Fecha Inicio',Fecha_inicio])
        informacion.append([name,f'Talleres Creativos_{i}-Fecha Fin',Fecha_Fin])
        informacion.append([name,f'Talleres Creativos_{i}-Lugar',Lugar])
        informacion.append([name,f'Talleres Creativos_{i}-Participacion',Participacion])
        informacion.append([name,f'Talleres Creativos_{i}-Ambito',ambito])
        informacion.append([name,f'Talleres Creativos_{i}-Distinción Obtenida',distincion])
        informacion.append([name,f'Talleres Creativos_{i}-Mecanismos Selección',Mecanimos])

        i =  i +1 
    return informacion

def CapituloLibro(table,name,informacion):
    i = 1
    for val in table.find_all('blockquote'):
        Tipo_aux = val.next_element
        Tipo = Tipo_aux.split(':')[-1].strip()
        Titulo_aux = val.text
        Titulo_re = '"(.*?)"'
        Titulo = re.findall(Titulo_re, Titulo_aux)[0]
        if Titulo == "":
            Titulo_re = '""(.*?)""'
            Titulo = re.findall(Titulo_re, Titulo_aux)[0]
        isbn = val.find_all('i')[0].next_sibling.strip()
        ed = val.find_all('i')[1].next_sibling.strip()
        paginas_aux =val.find_all('i')[2].next_sibling.strip() 
        paginas = paginas_aux.split(',')[1].replace('\r\n ','').replace(' ','').split('\xa0')[0]
        year = paginas_aux.split(',')[-1]
        Pais = Titulo_aux.split('En:')[-1].split('ISBN')[0].strip()
        informacion.append([name,f'Capitulos de libro_{i}-Tipo',Tipo])
        informacion.append([name,f'Capitulos de libro_{i}-Titulo',Titulo])
        informacion.append([name,f'Capitulos de libro_{i}-ISBN',isbn])
        informacion.append([name,f'Capitulos de libro_{i}-ed',ed])
        informacion.append([name,f'Capitulos de libro_{i}-Paginas',paginas])
        informacion.append([name,f'Capitulos de libro_{i}-Año',year])
        informacion.append([name,f'Capitulos de libro_{i}-Pais',Pais])
        i = i +1 
    return informacion

def Libros(table,name,informacion):
    i = 1
    for val in table.find_all('blockquote'):
        Tipo = table.find_all('li')[i-1].text.split('-')[-1]
        Titulo_aux = val.text
        Titulo_re = '"(.*?)"'
        Titulo = re.findall(Titulo_re, Titulo_aux)[0].strip()
        Pais_aux = Titulo_aux.split('En:')[-1].split('ed')[0].strip()
        Pais = ''.join([i for i in Pais_aux if not i.isdigit()]).lstrip().replace('\r\n','').replace('.','')
        year = ''.join([i for i in Pais_aux if i.isdigit()]).lstrip().replace('\r\n','').replace('.','')
        Editorial_aux = val.next_element
        Edditorial = Editorial_aux.split('ed:')[-1]
        isbn = val.find_all('i')[0].next_sibling.strip().replace('ISBN:','')
        paginas = val.find_all('i')[2].next_sibling.strip()
        informacion.append([name,f'Libros_{i}-Titulo',Titulo])
        informacion.append([name,f'Libros_{i}-Tipo',Tipo])
        informacion.append([name,f'Libros_{i}-Pais',Pais])
        informacion.append([name,f'Libros_{i}-Año',year])
        informacion.append([name,f'Libros_{i}-Editorial',Edditorial])
        informacion.append([name,f'Libros_{i}-ISBN',isbn])
        informacion.append([name,f'Libros_{i}-Paginas',paginas])
        i = i+1
    return informacion

def TraduccionesFiliologicas(table,name,informacion):
    i = 1
    for val in table.find_all('blockquote'):
        Nombre = val.find_all('i')[0].next_sibling.replace(',','').strip()
        Fecha = val.find_all('i')[1].next_sibling.replace(',','').strip()
        Fecha_aux = val.find_all('i')[1].next_sibling.replace(',','').strip()
        Fecha_re = '[0-9]{4}'  
        try:
            Fecha = re.findall(Fecha_re, Fecha_aux)[0]
        except:
            Fecha = ''
        ISBN = val.find_all('i')[2].next_sibling.replace(',','').strip()
        MedioDivulgacion = val.find_all('i')[3].next_sibling.replace(',','').strip()
        Lugar = val.find_all('i')[4].next_sibling.replace(',','').strip()
        Editorial = val.find_all('i')[5].next_sibling.replace(',','').strip()
        
        informacion.append([name,f'Traducciones Filológicas y Edición de Fuentes_{i}-Nombre',Nombre])
        informacion.append([name,f'Traducciones Filológicas y Edición de Fuentes_{i}-Fecha',Fecha])
        informacion.append([name,f'Traducciones Filológicas y Edición de Fuentes_{i}-ISBN',ISBN])
        informacion.append([name,f'Traducciones Filológicas y Edición de Fuentes_{i}-Medio Divulgacion',MedioDivulgacion])
        informacion.append([name,f'Traducciones Filológicas y Edición de Fuentes_{i}-Lugar',Lugar])
        informacion.append([name,f'Traducciones Filológicas y Edición de Fuentes_{i}-Editorial',Editorial])
        i = i +1
    return informacion


def LibrosFormacion(table,name,informacion):
    i = 1
    for val in table.find_all('blockquote'):
        Nombre = val.find_all('i')[0].next_sibling.replace(',','').strip()
        Fecha = val.find_all('i')[1].next_sibling.replace(',','').strip()
        Fecha_aux = val.find_all('i')[1].next_sibling.replace(',','').strip()
        Fecha_re = '[0-9]{4}'  
        try:
            Fecha = re.findall(Fecha_re, Fecha_aux)[0]
        except:
            Fecha = ''
        ISBN = val.find_all('i')[2].next_sibling.replace(',','').strip()
        MedioDivulgacion = val.find_all('i')[3].next_sibling.replace(',','').strip()
        Lugar = val.find_all('i')[4].next_sibling.replace(',','').strip()
        Editorial = val.find_all('i')[5].next_sibling.replace(',','').strip()
        informacion.append([name,f'Libro de Formación_{i}-Nombre',Nombre])
        informacion.append([name,f'Libro de Formación_{i}-Fecha',Fecha])
        informacion.append([name,f'Libro de Formación_{i}-ISBN',ISBN])
        informacion.append([name,f'Libro de Formación_{i}-Medio Divulgacion',MedioDivulgacion])
        informacion.append([name,f'Libro de Formación_{i}-Lugar',Lugar])
        informacion.append([name,f'Libro de Formación_{i}-Editorial',Editorial])
        i = i +1
    return informacion


def LibrosDivulgacion(table,name,informacion):
    i = 1
    for val in table.find_all('blockquote'):
        Nombre = val.find_all('i')[0].next_sibling.replace(',','').strip()
        Fecha = val.find_all('i')[1].next_sibling.replace(',','').strip()
        Fecha_aux = val.find_all('i')[1].next_sibling.replace(',','').strip()
        Fecha_re = '[0-9]{4}'  
        try:
            Fecha = re.findall(Fecha_re, Fecha_aux)[0]
        except:
            Fecha = ''
        ISBN = val.find_all('i')[2].next_sibling.replace(',','').strip()
        MedioDivulgacion = val.find_all('i')[3].next_sibling.replace(',','').strip()
        Lugar = val.find_all('i')[4].next_sibling.replace(',','').strip()
        Editorial = val.find_all('i')[5].next_sibling.replace(',','').strip()
       
        informacion.append([name,f'Libros de divulgación y/o Compilación de divulgación_{i}-Nombre',Nombre])
        informacion.append([name,f'Libros de divulgación y/o Compilación de divulgación_{i}-Fecha',Fecha])
        informacion.append([name,f'Libros de divulgación y/o Compilación de divulgación_{i}-ISBN',ISBN])
        informacion.append([name,f'Libros de divulgación y/o Compilación de divulgación_{i}-Medio Divulgacion',MedioDivulgacion])
        informacion.append([name,f'Libros de divulgación y/o Compilación de divulgación_{i}-Lugar',Lugar])
        informacion.append([name,f'Libros de divulgación y/o Compilación de divulgación_{i}-Editorial',Editorial])
        i = i +1 
    return informacion


def OtraProduccionBibliografica(table,name,informacion):
    i = 1
    for val in table.find_all('blockquote'):
       Tipo =  table.find_all('li')[i-1].text.split('-')[-1].strip()
       Titulo_re = '"(.*?)"'
       Titulo = re.findall(Titulo_re, val.text)[0].strip()
       Pais = val.text.split('En:')[-1].split('.')[0]
       fecha_re = '[0-9]{4}'
       try:
           Fecha = re.findall(fecha_re, val.text)[-1]
       except: 
           Fecha = ''
      
       informacion.append([name,f'Otra producción blibliográfica_{i}-Tipo',Tipo])
       informacion.append([name,f'Otra producción blibliográfica_{i}-Titulo',Titulo])
       informacion.append([name,f'Otra producción blibliográfica_{i}-Pais',Pais])
       informacion.append([name,f'Otra producción blibliográfica_{i}-Fecha',Fecha])
       i = i +1 
    return informacion

def NotasCientificas(table,name,informacion):
    i = 1
    for val in table.find_all('blockquote'):
       Titulo_re = '"(.*?)"'
       Titulo = re.findall(Titulo_re, val.text)[0].strip()
       
       MedioDivulgacion = val.find_all('i')[0].next_sibling.replace(',','').strip().replace('.','')
       Idioma = val.find_all('i')[1].next_sibling.replace('.','').strip()
       ed = val.find_all('i')[3].next_sibling.replace('.','').strip()
       paginas_aux = val.find_all('i')[5].next_sibling.replace('.','').strip()
       Fecha_re = ',([0-9]{4}),'
       try:
           Fecha = re.findall(Fecha_re, paginas_aux)[0]
       except:
            Fecha = ''
       url = val.find_all('i')[6].next_sibling.replace('.','').strip()
     
       informacion.append([name,f'Notas científicas_{i}-Nombre',Titulo])
       informacion.append([name,f'Notas científicas_{i}-Medio Devulgación',MedioDivulgacion])
       informacion.append([name,f'Notas científicas_{i}-Idioma',Idioma])
       informacion.append([name,f'Notas científicas_{i}-Editorial',ed])
       informacion.append([name,f'Notas científicas_{i}-Fecha',Fecha])
       informacion.append([name,f'Notas científicas_{i}-URL',url])
       i = i +1 
    return informacion


def Traducciones(table,name,informacion):
    i = 1
    for val in table.find_all('blockquote'):
        Tipo =  table.find_all('li')[i-1].text.split('-')[-1].strip()
        Titulo_re = '"(.*?)"'
        Titulo = re.findall(Titulo_re, val.text)[0]
        Pais  = val.text.split('En:')[-1].split('.')[0].strip()
        year  = val.text.split('En:')[-1].split('.')[1].strip()
        Lengua_Orignal  = val.find_all('i')[0].next_sibling.replace('.','').strip()
        Lengua_Traducido = val.find_all('i')[1].next_sibling.replace('.','').strip()
        informacion.append([name,f'Traducciones_{i}-Tipo',Tipo])
        informacion.append([name,f'Traducciones_{i}-Titulo',Titulo])
        informacion.append([name,f'Traducciones_{i}-Pais',Pais])
        informacion.append([name,f'Traducciones_{i}-Año',year])
        informacion.append([name,f'Traducciones_{i}-Lenguaje Original',Lengua_Orignal])
        informacion.append([name,f'Traducciones_{i}-Lenguaje Traducido',Lengua_Traducido])
        i = i +1 
    return informacion


def InnovacioneDeProceso(table,name,informacion):
    i = 1
    for val in table.find_all('blockquote'):
        Titulo = val.next_element.split(',')[-2].strip()
        Registro =  val.find_all('i')[1].next_sibling.replace('.','').strip()
        Fecha_re = ',([0-9]{4}),'
        try:
            Fecha = re.findall(Fecha_re, Registro)[0]
        except:
             Fecha = ''
        Pais_re = 'En: (.*?),'     
        try:
            Pais = re.findall(Pais_re, Registro)[0]
        except:
            Pais = ''
        informacion.append([name,f'Innovación de proceso o procedimiento_{i}-Titulo',Titulo])
        informacion.append([name,f'Innovación de proceso o procedimiento_{i}-Fecha',Fecha])
        informacion.append([name,f'Innovación de proceso o procedimiento_{i}-Pais',Pais])
        #print([Titulo,Fecha,Pais])
        i = i +1 
    return informacion

def InnovacioneEmpresal(table,name,informacion):
    i = 1
    for val in table.find_all('blockquote'):
        Tipo = table.find_all('b')[i-1].text.split('-')[-1].strip()
        Titulo = val.next_element.split(',')[-2].strip()
        Registro =  val.find_all('i')[1].next_sibling.replace('.','').strip()
        Fecha_re = ',([0-9]{4}),'
        try:
            Fecha = re.findall(Fecha_re, Registro)[0]
        except:
             Fecha = ''
        Pais_re = 'En: (.*?),'     
        try:
            Pais = re.findall(Pais_re, Registro)[0]
        except:
            Pais = ''
        informacion.append([name,f'Innovación generada en la gestión empresarial_{i}-Titulo',Titulo])
        informacion.append([name,f'Innovación generada en la gestión empresarial_{i}-Fecha',Fecha])
        informacion.append([name,f'Innovación generada en la gestión empresarial_{i}-Pais',Pais])
        informacion.append([name,f'Innovación generada en la gestión empresarial_{i}-Tipo',Tipo])
    return informacion

def LibrosCreacionPiloto(table,name,informacion):
    i = 1
    for val in table.find_all('blockquote'):    
        NombreLibro = val.find_all('i')[0].next_sibling.replace(',','').strip()
        FechaPresentacion = val.find_all('i')[1].next_sibling.replace(',','').split('-')[0].strip()
        ISBN = val.find_all('i')[2].next_sibling.replace(',','').strip()
        MedioDivulgacion = val.find_all('i')[4].next_sibling.replace(',','').strip()
        LugarPublicacion = val.find_all('i')[5].next_sibling.replace(',','').strip()
        Editorial = val.find_all('i')[6].next_sibling.replace(',','').strip()
        informacion.append([name,f'Libro de creación (Piloto)_{i}-Nombre',NombreLibro])
        informacion.append([name,f'Libro de creación (Piloto)_{i}-Fecha Presentacion',FechaPresentacion])
        informacion.append([name,f'Libro de creación (Piloto)_{i}-ISBN',ISBN])
        informacion.append([name,f'Libro de creación (Piloto)_{i}-Medio Divulgacion',MedioDivulgacion])
        informacion.append([name,f'Libro de creación (Piloto)_{i}-Lugar Publicación',LugarPublicacion])
        informacion.append([name,f'Libro de creación (Piloto)_{i}-Editorial',Editorial])
        i = i + 1
        
    return informacion

def ManualesGuiasEspecializadas(table,name,informacion):
    i = 1
    for val in table.find_all('blockquote'):    
        NombreLibro = val.find_all('i')[0].next_sibling.replace(',','').strip()
        FechaPresentacion = val.find_all('i')[1].next_sibling.replace(',','').split('-')[0].strip()
        ISBN = val.find_all('i')[2].next_sibling.replace(',','').strip()
        MedioDivulgacion = val.find_all('i')[3].next_sibling.replace(',','').strip()
        LugarPublicacion = val.find_all('i')[4].next_sibling.replace(',','').strip()
        Editorial = val.find_all('i')[5].next_sibling.replace(',','').strip()
        informacion.append([name,f'Manuales y Guías Especializadas_{i}-Nombre',NombreLibro])
        informacion.append([name,f'Manuales y Guías Especializadas_{i}-Fecha Presentacion',FechaPresentacion])
        informacion.append([name,f'Manuales y Guías Especializadas_{i}-ISBN',ISBN])
        informacion.append([name,f'Manuales y Guías Especializadas_{i}-Medio Divulgacion',MedioDivulgacion])
        informacion.append([name,f'Manuales y Guías Especializadas_{i}-Lugar Publicación',LugarPublicacion])
        informacion.append([name,f'Manuales y Guías Especializadas_{i}-Editorial',Editorial])
        i = i + 1
        
    return informacion

def CartasMapasSimilares(table,name,informacion):
    i = 1
    
    for val in table.find_all('blockquote'):    
        Tipo =  table.find_all('li')[i-1].text.split('-')[-1].strip()
        Titulo = val.text.split(',')[1].strip()
        En = val.text.split('En:')[1].strip().split(',')[0].strip()
        year = val.text.split('En:')[1].strip().split(',')[2].strip()
        informacion.append([name,f'Cartas, mapas y similares_{i}-Tipo',Tipo])
        informacion.append([name,f'Cartas, mapas y similares_{i}-Titulo',Titulo])
        informacion.append([name,f'Cartas, mapas y similares_{i}-En',En])
        informacion.append([name,f'Cartas, mapas y similares_{i}-Año',year])
        i = i + 1
        
    return informacion

def ConceptoTecnico(table,name,informacion):
    i = 1
    
    for val in table.find_all('blockquote'):    
        Titulo =  val.text.split(',')[1].strip().split('.')[0]
        Institucion = val.find_all('i')[0].next_sibling.strip().split('.')[0].strip()
        En =  val.find_all('i')[0].next_sibling.strip().split('En:')[1].strip().replace('.','')
        year_solicitud = val.find_all('i')[2].next_sibling.strip().split('.')[0].strip().split(' ')[0]
        year_envio = val.find_all('i')[4].next_sibling.strip().split('.')[0].strip().split(' ')[0]
        NumConsecutivo = val.find_all('i')[5].next_sibling.strip().split('.')[0].strip().split(' ')[0]
        
        informacion.append([name,f'Concepto técnico_{i}-Titulo',Titulo])
        informacion.append([name,f'Concepto técnico_{i}-Institucion Solicitante',Institucion])
        informacion.append([name,f'Concepto técnico_{i}-En',En])
        informacion.append([name,f'Concepto técnico_{i}-Año Solicitud',year_solicitud])
        informacion.append([name,f'Concepto técnico_{i}-Año Envio',year_envio])
        informacion.append([name,f'Concepto técnico_{i}-Numero Consecutivo',NumConsecutivo])
        
        i = i + 1
        
    return informacion

def DisIndustrial(table,name,informacion):
    i = 1
    
    for val in table.find_all('blockquote'):    
        Nombre =  val.next_element.split(',')[-2].strip()
        contrato = val.find_all('i')[1].next_sibling.split(',')[0].strip()
        En = val.find_all('i')[1].next_sibling.split('En:')[1].strip().split(',')[0]
        year_aux = val.find_all('i')[1].next_sibling.split('En:')[1].strip()
        Year_re = '[0-9]{4}'
        year = re.findall(Year_re, year_aux)[0].strip()       
        informacion.append([name,f'Diseño industrial_{i}-Nombre Diseño',Nombre])
        informacion.append([name,f'Diseño industrial_{i}-Contrato',contrato])
        informacion.append([name,f'Diseño industrial_{i}-En',En])
        informacion.append([name,f'Diseño industrial_{i}-Año',year])
        i = i + 1
        
    return informacion

def EmpresasBaseTecno(table,name,informacion):
    i = 1
    
    for val in table.find_all('blockquote'):    
        TipoEmpresa  =  table.find_all('li')[i-1].text.split('Empresa de base tecnológica')[-1].strip().replace('-','').strip()
        Nombre = val.text.split('Nit')[0].split(',')[-2].strip()
        NIT = val.text.split('Nit')[1].split(',')[0]
        FechaRegistro_aux = val.find_all('i')[1].next_sibling.replace(',','').strip()
        Fecha_re = '[0-9]{4}'
        FechaRegistro = re.findall(Fecha_re, FechaRegistro_aux)[0]
        informacion.append([name,f'Empresas de base tecnológica_{i}-Tipo Empresa',TipoEmpresa])
        informacion.append([name,f'Empresas de base tecnológica_{i}-Nombre',Nombre])
        informacion.append([name,f'Empresas de base tecnológica_{i}-NIT',NIT])
        informacion.append([name,f'Empresas de base tecnológica_{i}-Fecha Registro',FechaRegistro])
        i = i + 1
        
    return informacion

def PlantaPiloto(table,name,informacion):
    i = 1
    
    for val in table.find_all('blockquote'):    
        NombrePlanta  =  val.text.split('Nombre comercial')[0].split(',')[-2].strip()
        En = val.find_all('i')[1].next_sibling.split('En:')[-1].split(',')[0].strip()
        year_aux = val.find_all('i')[1].next_sibling.split('En:')[-1]
        Year_re = '[0-9]{4}'
        year = re.findall(Year_re, year_aux)[0].strip()
        
        informacion.append([name,f'Planta piloto_{i}-Nombre Planta Piloto',NombrePlanta])
        informacion.append([name,f'Planta piloto_{i}-En',En])
        informacion.append([name,f'Planta piloto_{i}-Año',year])
        
        i = i + 1
        
    return informacion

def NuevosRegistrosCientificos(table,name,informacion):
    i = 1
    
    for val in table.find_all('blockquote'): 
        year_re = ',([0-9]{4}),'
        try:
            year = re.findall(year_re, val.text)[0]
        except:
            year = ''
        BaseDatos = val.find_all('i')[0].next_sibling.split('En:')[-1].split(',')[0].strip()
        Disponible = val.find_all('i')[1].next_sibling.split('En:')[-1].split(',')[0].strip()
        InstitucionRegistro = val.find_all('i')[2].next_sibling.split('En:')[-1].split(',')[0].strip()
        InstitucionCertificadora= val.find_all('i')[3].next_sibling.split('En:')[-1].split(',')[0].strip()
        informacion.append([name,f'Nuevos registros científicos_{i}-Año',year])
        informacion.append([name,f'Nuevos registros científicos_{i}-Base de Datos',BaseDatos])
        informacion.append([name,f'Nuevos registros científicos_{i}-Disponible',Disponible])
        informacion.append([name,f'Nuevos registros científicos_{i}-Registro',InstitucionRegistro])
        informacion.append([name,f'Nuevos registros científicos_{i}-Certificadora',InstitucionCertificadora])
        i = i + 1
    return informacion


def ProductosTecnologicos(table,name,informacion):
    i = 1
    
    for val in table.find_all('blockquote'): 
        Tipo = table.find_all('li')[i-1].text.split('-')[-1].strip()
        Nombre = val.next_element.replace('\r\n','**').split('**')[-2].strip()
        Contrato_aux = val.find_all('i')[1].next_sibling
        Fecha_re = ',([0-9]{4}),'
        try:    
            Fecha = re.findall(Fecha_re, Contrato_aux)[0]
        except:
            Fecha = ''
        Pais_re = 'En: (.*?),'     
        Pais = re.findall(Pais_re,Contrato_aux )[0]
        informacion.append([name,f'Productos tecnológicos_{i}-Tipo',Tipo])
        informacion.append([name,f'Productos tecnológicos_{i}-Nombre',Nombre])
        informacion.append([name,f'Productos tecnológicos_{i}-Año',Fecha])
        informacion.append([name,f'Productos tecnológicos_{i}-Pais',Pais])
        i = i + 1
    return informacion

def Prototipos(table,name,informacion):
    i = 1
    
    for val in table.find_all('blockquote'): 
        Tipo = table.find_all('img')[i-1].findNext('b').text.split('-')[-1]
        Nombre = val.next_element.split(',')[-2].strip()
        Contrato_aux = val.find_all('i')[1].next_sibling
        Fecha_re = ',([0-9]{4}),'
        try:    
            Fecha = re.findall(Fecha_re, Contrato_aux)[0]
        except:
            Fecha = ''
        Pais_re = 'En: (.*?),'     
        Pais = re.findall(Pais_re,Contrato_aux )[0]
        informacion.append([name,f'Prototipos_{i}-Tipo',Tipo])
        informacion.append([name,f'Prototipos_{i}-Nombre',Nombre])
        informacion.append([name,f'Prototipos_{i}-Año',Fecha])
        informacion.append([name,f'Prototipos_{i}-Pais',Pais])
        i = i + 1
    return informacion

def NormasyRegulaciones(table,name,informacion):
    i = 1
    for val in table.find_all('blockquote'): 
       Tipo = table.find_all('li')[i-1].text.split('-')[-1].strip()
       Nombre = val.next_element.split('\r\n')[-2].strip()
       Contrato_aux = val.find_all('i')[1].next_sibling
       Fecha_re = ',([0-9]{4}),'
       try:    
           Fecha = re.findall(Fecha_re, Contrato_aux)[0]
       except:
           Fecha = ''
       Pais_re = 'En: (.*?),'     
       Pais = re.findall(Pais_re,Contrato_aux )[0]
       informacion.append([name,f'Normas y Regulaciones_{i}-Tipo',Tipo])
       informacion.append([name,f'Normas y Regulaciones_{i}-Nombre',Nombre])
       informacion.append([name,f'Normas y Regulaciones_{i}-Año',Fecha])
       informacion.append([name,f'Normas y Regulaciones_{i}-Pais',Pais])
       i = i + 1
    return informacion

def SignosDistintivos(table,name,informacion):
    i = 1
    for val in table.find_all('blockquote'): 
        Nombre = val.find_all('img')[0].next_element.strip().replace(',','')
        Pais = val.find_all('i')[0].next_sibling.strip().replace(',','')
        year = val.find_all('i')[1].text
        aux = val.find_all('i')[1].next_sibling
        registro_re = 'Registro:(.*?),'
        registro = re.findall(registro_re,aux)[0]
        Titular = aux.split('Titular:')[-1].strip()
        informacion.append([name,f'Signos distintivos_{i}-Nombre',Nombre])
        informacion.append([name,f'Signos distintivos_{i}-Pais',Pais])
        informacion.append([name,f'Signos distintivos_{i}-Año',year])
        informacion.append([name,f'Signos distintivos_{i}-Registro',registro])
        informacion.append([name,f'Signos distintivos_{i}-Titular',Titular])
        i = i + 1
    return informacion

def Softwares(table,name,informacion):
    i = 1
    for val in table.find_all('blockquote'): 
        Tipo = val.find_previous('b').text.split('-')[-1].strip()
        Titulo  = val.next_element.replace('\r\n','**').split('**')[-2].strip().replace(',','')
        Contrato =  val.find_all('i')[1].next_sibling
        Fecha_re = ',([0-9]{4}),'
        try:    
            Fecha = re.findall(Fecha_re, Contrato)[-1]
        except:
            Fecha = ''
        Pais_re = 'En: (.*?),'     
        Pais = re.findall(Pais_re,Contrato )[0]
        plataforma_aux = val.find_all('i')[2].text
        plataforma_re = 'plataforma: (.*?),'  
        try:
            plataforma = re.findall(plataforma_re,plataforma_aux)[0]
        except:
            plataforma = ''
        ambiente_aux = val.find_all('i')[3].text
        ambiente_re = 'ambiente: (.*?),'  
        try:
            ambiente = re.findall(ambiente_re,ambiente_aux)[0]
        except:
            ambiente = ''
        informacion.append([name,f'Softwares_{i}-Tipo',Tipo])
        informacion.append([name,f'Softwares_{i}-Titulo',Titulo])
        informacion.append([name,f'Softwares_{i}-Año',Fecha])
        informacion.append([name,f'Softwares_{i}-Pais',Pais])
        informacion.append([name,f'Softwares_{i}-Plataforma',plataforma])
        informacion.append([name,f'Softwares_{i}-Ambiente',ambiente])
        i = i + 1
    return informacion

def DemasTrabajos(table,name,informacion):
    i = 1
    
    for val in table.find_all('blockquote'): 
        Titulo = val.next_element.replace('\r\n','**').split('En:')[0].split('**')[-2].strip()
        Titulo_aux = val.next_element.split('En:')[1]
        Pais = Titulo_aux.split(',')[0].strip() 
        Fecha_re = ',([0-9]{4}),'
        try:    
            Fecha = re.findall(Fecha_re, Titulo_aux)[-1]
        except:
            Fecha = ''
        informacion.append([name,f'Demás trabajos_{i}-Titulo',Titulo])
        informacion.append([name,f'Demás trabajos_{i}-Pais',Pais])
        informacion.append([name,f'Demás trabajos_{i}-Año',Fecha])
        i = i + 1
    return informacion

def ContenidoImpreso(table,name,informacion):
    i = 1
    
    for val in table.find_all('blockquote'): 
        Titulo = val.find_all('i')[0].next_sibling.strip()
        Tipo = val.find_all('i')[1].next_sibling.split('-')[-1].replace(',','').strip()
        Medio = val.find_all('i')[2].next_sibling.replace(',','').strip()
        Ambito_aux = val.find_all('i')[3].next_sibling.strip()
        disponible = val.find_all('i')[4].next_sibling.strip()
        Fecha_re = '[0-9]{4}-[0-9]{2}-[0-9]{2}'
        try:
            Fecha = re.findall(Fecha_re, Ambito_aux)[0]
        except:
            Fecha = ''
        Ambito = Ambito_aux.split('en la fecha')[0].strip() 
        informacion.append([name,f'Generación de contenido impresa_{i}-Titulo',Titulo])
        informacion.append([name,f'Generación de contenido impresa_{i}-Tipo',Tipo])
        informacion.append([name,f'Generación de contenido impresa_{i}-Medio',Medio])
        informacion.append([name,f'Generación de contenido impresa_{i}-Ambito',Ambito])
        informacion.append([name,f'Generación de contenido impresa_{i}-Disponible en ',disponible])
        informacion.append([name,f'Generación de contenido impresa_{i}-Año',Fecha])   
        i = i + 1
    return informacion


def ContenidoMultimedia(table,name,informacion):
    i = 1
    for val in table.find_all('blockquote'): 
        Tipo = table.find_all('li')[i-1].text.split('-')[-1].strip()
        Titulo = val.next_element.split('En:')[0].strip().replace('\r\n','').replace('  ','')
        Fecha = val.next_element.split(',')[-2]
        Pais = val.next_element.split('En:')[1].split(',')[0].strip()
        Emisora_aux = val.find_all('i')[0].next_sibling.strip()
        Emisora = Emisora_aux.split(',')[0].strip() 
        Minutos = Emisora_aux.split(',')[-1].split('minutos')[0] 
        informacion.append([name,f'Generación de contenido multimedia_{i}-Tipo',Tipo])   
        informacion.append([name,f'Generación de contenido multimedia_{i}-Año',Fecha])   
        informacion.append([name,f'Generación de contenido multimedia_{i}-Titulo',Titulo])   
        informacion.append([name,f'Generación de contenido multimedia_{i}-Pais',Pais])   
        informacion.append([name,f'Generación de contenido multimedia_{i}-Emisora',Emisora])   
        informacion.append([name,f'Generación de contenido multimedia_{i}-Minutos',Minutos])   
        i = i + 1
    return informacion

def ContenidoAudio(table,name,informacion):
    i = 1
    for val in table.find_all('blockquote'): 
        Titulo = val.next_element.replace('\r\n','').strip().split('  ')[-1]
        Fecha_re = '[0-9]{4}'
        try:
            Fecha = re.findall(Fecha_re,val.text)[0]
        except: 
            Fecha = ''
        Ciudad  = val.find_all('i')[1].next_sibling.split('En: ')[-1].replace('.','')
        Formato = str(val.find_all('i')[2].next_sibling)
        informacion.append([name,f'Generación de contenido de audio_{i}-Titulo',Titulo])   
        informacion.append([name,f'Generación de contenido de audio_{i}-Fecha',Fecha])   
        informacion.append([name,f'Generación de contenido de audio_{i}-Ciudad',Ciudad])   
        informacion.append([name,f'Generación de contenido de audio_{i}-Formato',Formato])   
        i = i + 1
    return informacion

def ContenidoVirtual(table,name,informacion):
    i = 1
    for val in table.find_all('blockquote'): 
        Titulo = val.find_all('i')[0].next_sibling.strip()
        Tipo_aux = val.find_all('i')[1].next_sibling
        Tipo_re = '-(.*?),'
        Tipo = re.findall(Tipo_re,Tipo_aux)[0].split('-')[-1].strip()
        Fecha_re = '[0-9]{4}-[0-9]{2}-[0-9]{2}'
        try:
            Fecha = re.findall(Fecha_re,Tipo_aux)[0]
        except:
            Fecha = ''
        Disponible = val.find_all('i')[2].next_sibling.strip()
        informacion.append([name,f'Generación de contenido virtual_{i}-Titulo',Titulo])
        informacion.append([name,f'Generación de contenido virtual_{i}-Tipo',Tipo]) 
        informacion.append([name,f'Generación de contenido virtual_{i}-Fecha',Fecha])   
        informacion.append([name,f'Generación de contenido virtual_{i}-Disponible',Disponible])   
        i = i + 1
    return informacion

def ContenidoCTI(table,name,informacion):
    i = 1
    for val in table.find_all('blockquote'): 
        Titulo = val.find_all('i')[0].next_sibling.strip()
        Fecha_inicio = val.find_all('i')[1].next_sibling.strip().replace(',','')
        Fecha_Final_aux = val.find_all('i')[2].text
        Fecha_final_re = 'Finalizó en :(.*?),'
        FechaFinal  = re.findall(Fecha_final_re,Fecha_Final_aux)[0] 
        informacion.append([name,f'Estrategias pedagógicas para el fomento a la CTI_{i}-Titulo',Titulo])
        informacion.append([name,f'Estrategias pedagógicas para el fomento a la CTI_{i}-Fecha inicio',Fecha_inicio])
        informacion.append([name,f'Estrategias pedagógicas para el fomento a la CTI_{i}-Fecha Final',FechaFinal])
        i = i + 1
    return informacion

def ComunicacionConocimiento(table,name,informacion):
    i = 1
    for val in table.find_all('blockquote'): 
        Titulo = val.find_all('i')[0].next_sibling.strip()
        Fecha_inicio = val.find_all('i')[1].next_sibling.strip().replace(',','')
        Fecha_Final_aux = val.find_all('i')[2].text
        Fecha_final_re = 'Finalizó en :(.*?),'
        FechaFinal  = re.findall(Fecha_final_re,Fecha_Final_aux)[0] 
        informacion.append([name,f'Estrategias de comunicación del conocimiento_{i}-Titulo',Titulo])
        informacion.append([name,f'Estrategias de comunicación del conocimiento_{i}-Fecha inicio',Fecha_inicio])
        informacion.append([name,f'Estrategias de comunicación del conocimiento_{i}-Fecha Final',FechaFinal])
        i = i + 1
    return informacion


def EspacioParticipacionCiudadana(table,name,informacion):
    i = 1
    for val in table.find_all('tr'):
        if i != 1:
            
            Titulo = val.find_all('i')[0].next_sibling.strip()
            Fecha_aux = val.find_all('i')[1].text
            Fecha_re = '[0-9]{4}-[0-9]{2}-[0-9]{2}'
            try:
                Fecha = re.findall(Fecha_re,Fecha_aux)[0]
            except:
                Fecha = ''
            Pais = val.find_all('i')[1].text.split('en ')[-1].split('-')[0].strip()
            Participantes = val.find_all('i')[1].findNext('i').next_sibling.split('participantes')[0]
            informacion.append([name,f'Espacios de participación ciudadana_{i}-Titulo',Titulo])
            informacion.append([name,f'Espacios de participación ciudadana_{i}-Fecha',Fecha])
            informacion.append([name,f'Espacios de participación ciudadana_{i}-Pais',Pais])
            informacion.append([name,f'Espacios de participación ciudadana_{i}-Participantes',Participantes])
        i = i + 1
    return informacion

def EspacioParticipacionCiudadanaCTI(table,name,informacion):
    i = 1
    for val in table.find_all('blockquote'):
        Titulo = val.find_all('i')[0].next_sibling.strip()
        Inicio = val.find_all('i')[1].next_sibling.strip().replace(',','')
        Final = val.find_all('i')[2].next_sibling.strip().replace(',','')
        informacion.append([name,f'Participación ciudadana en proyectos de CTI_{i}-Titulo',Titulo])
        informacion.append([name,f'Participación ciudadana en proyectos de CTI_{i}-Fecha Inicio',Inicio])
        informacion.append([name,f'Participación ciudadana en proyectos de CTI_{i}-Fecha Fin',Final])
        i = i + 1
    return informacion

def PublicacionesNoCientificas(table,name,informacion):
    i = 1
    for val in table.find_all('blockquote'):
        Tipo = table.find_all('li')[i-1].text.split('-')[-1].strip()
        Nombre = val.next_element
        Titulo_re = '"(.*?)"'
        Titulo = re.findall(Titulo_re,Nombre)[0]
        Pais = Nombre.split('En:')[-1].split('.')[0].strip()
        Fecha_re = '[0-9]{4}\.'
        Fecha = re.findall(Fecha_re,Nombre)[-1].replace('.','')        
        Revista = Nombre.split(f'{Fecha}.')[-1].strip()
        ISNN = val.find_all('i')[0].next_sibling.strip()
        Paginas = val.find_all('i')[1].next_sibling.strip().replace('\r\n ','').split('v.')[0]
        informacion.append([name,f'Textos en publicaciones no científicas_{i}-Tipo',Tipo])
        informacion.append([name,f'Textos en publicaciones no científicas_{i}-Titulo',Titulo])
        informacion.append([name,f'Textos en publicaciones no científicas_{i}-Pais',Pais])
        informacion.append([name,f'Textos en publicaciones no científicas_{i}-Año',Fecha])
        informacion.append([name,f'Textos en publicaciones no científicas_{i}-Revista',Revista])
        informacion.append([name,f'Textos en publicaciones no científicas_{i}-ISSN',ISNN])
        informacion.append([name,f'Textos en publicaciones no científicas_{i}-Paginas',Paginas])
        i = i + 1
    return informacion

profesoresPlanta = os.environ['Profesores de Planta']
docentes = pd.read_excel(profesoresPlanta)
#155002
informacion = []
aux = []
# j = 1
# n  =10

# docentes = docentes[docentes.index >= j]
listas_campos = []
for cvlac,name in zip(docentes['CvLAC'].values,docentes['NOMBRES Y APELLIDOS']):
   if  type(cvlac) != float:
       print(name) 
       lista_campos = []
       # if j == n:
       #     break 
       # else: 
       #     pass
       # j =  j +1 
       while True:
           try:
               r = requests.get(cvlac,verify=False)
               break
           except:
               print('*'*100)
               time.sleep(120)
               print(name)
       soup = BeautifulSoup(r.content, "html.parser")
       table = soup.find_all('table')
       if len(table) == 1:
           pass
           #print(table)
       for row in table:
            try:
                variable = row.find_all('h3')
                variable_aux =  variable[0].text
            except: 
                pass
            lista_campos.append(variable_aux)
            if variable_aux == 'Artículos':
                informacion = Articulos(row,name,informacion)
            elif variable_aux == 'Asesorías':
                informacion = Asesorias(row,name,informacion)
            elif variable_aux == 'Cursos de corta duración':
                informacion = CursoCortaDuración(row,name,informacion)
            elif variable_aux == 'Trabajos dirigidos/tutorías':
                informacion = Trabajos_Dirigidos(row,name,informacion)
            elif variable_aux == 'Jurado en comités de evaluación':
                informacion = JuradoComiteEvaluacion(row,name,informacion)
            elif variable_aux == 'Par evaluador':
                informacion = ParEvaluador(row,name,informacion)
            elif variable_aux == 'Participación en comités de evaluación':
                informacion = ComitesEvaluacion(row,name,informacion)
            elif variable_aux == 'Publicaciones editoriales no especializadas':
                informacion = PublicacionesNoEspecializadas(row,name,informacion)
            elif variable_aux == 'Producciones de contenido digital Audiovisual':
                informacion = DigitalAudiovisual(row,name,informacion)
            elif variable_aux == 'Producciones de contenido digital Sonoro':
                informacion = DigitalSonoro(row,name,informacion)
            elif variable_aux == 'Producciones de contenido digital Recursos gráficos':
                informacion = RecursosGraficos(row,name,informacion)
            elif variable_aux == 'Producción de estrategias y contenidos transmedia':
                informacion = ContenidoTransmedia(row,name,informacion)
            elif variable_aux == 'Desarrollos web':
                informacion = DesarrolloWeb(row,name,informacion)
            elif variable_aux == 'Fortalecimiento o solución de asuntos de interés social':
                informacion = InteresSocial(row,name,informacion)
            elif variable_aux == 'Fortalecimiento de cadenas productivas':
                informacion = CadenasProductivas(row,name,informacion) 
            elif variable_aux == 'Consultorías':
                informacion = Consultorias(row,name,informacion) 
            elif variable_aux == 'Documentos de trabajo':
                informacion = DocumentosTrabajo(row,name,informacion) 
            elif variable_aux == 'Ediciones/revisiones':
                informacion = EdicionesRevisiones(row,name,informacion) 
            elif variable_aux == 'Eventos científicos':
                informacion = EventosCientificos(row,name,informacion) 
            elif variable_aux == 'Informes de investigaci&oacuten':
                informacion = InformeInvestigacion(row,name,informacion) 
            elif variable_aux == 'Informes técnicos':
                informacion = InformesTecnicos(row,name,informacion) 
            elif variable_aux == 'Redes de conocimiento especializado':
                informacion = RedesConocimiento(row,name,informacion) 
            elif variable_aux == 'Obras o productos':
                informacion = ObrasProductos(row,name,informacion) 
            elif variable_aux == 'Industrias Creativas y culturales':
                informacion = IndustriasCreativas(row,name,informacion) 
            elif variable_aux == 'Eventos artísticos':
                informacion = EventosArtisticos(row,name,informacion) 
            elif variable_aux == 'Talleres Creativos':
                informacion = TalleresCreativos(row,name,informacion) 
            elif variable_aux == 'Capitulos de libro':
                informacion = CapituloLibro(row,name,informacion) 
            elif variable_aux == 'Libros':
                informacion = Libros(row,name,informacion) 
            elif variable_aux == 'Traducciones Filológicas y Edición de Fuentes':
                informacion = TraduccionesFiliologicas(row,name,informacion) 
            elif variable_aux == 'Libro de Formación':
                informacion = LibrosFormacion(row,name,informacion) 
            elif variable_aux == 'Libros de divulgación y/o Compilación de divulgación':
                informacion = LibrosDivulgacion(row,name,informacion) 
            elif variable_aux == 'Otra producción blibliográfica':
                informacion = OtraProduccionBibliografica(row,name,informacion) 
            elif variable_aux == 'Notas científicas':
                informacion = NotasCientificas(row,name,informacion)
            elif variable_aux == 'Traducciones':
                informacion = Traducciones(row,name,informacion)
            elif variable_aux == 'Innovación de proceso o procedimiento':
                informacion = InnovacioneDeProceso(row,name,informacion)
            elif variable_aux == 'Innovación generada en la gestión empresarial':
                informacion = InnovacioneEmpresal(row,name,informacion)
            elif variable_aux == 'Libro de creación (Piloto)':
                informacion = LibrosCreacionPiloto(row,name,informacion) 
            elif variable_aux == 'Manuales y Guías Especializadas':
                informacion = ManualesGuiasEspecializadas(row,name,informacion) 
            elif variable_aux == 'Cartas, mapas y similares':
                informacion = CartasMapasSimilares(row,name,informacion) 
            elif variable_aux == 'Concepto técnico':
                informacion = ConceptoTecnico(row,name,informacion) 
            elif variable_aux == 'Diseño industrial':
                informacion = DisIndustrial(row,name,informacion)    
            elif variable_aux == 'Empresas de base tecnológica':
                informacion = EmpresasBaseTecno(row,name,informacion) 
            elif variable_aux == 'Planta piloto':
                informacion = PlantaPiloto(row,name,informacion)   
            elif variable_aux == 'Nuevos registros científicos':
                informacion = NuevosRegistrosCientificos(row,name,informacion)  
            elif variable_aux == 'Productos tecnológicos':
                informacion = ProductosTecnologicos(row,name,informacion)  
            elif variable_aux == 'Prototipos':
                informacion = Prototipos(row,name,informacion)  
            elif variable_aux == 'Normas y Regulaciones':
                informacion = NormasyRegulaciones(row,name,informacion)  
            elif variable_aux == 'Signos distintivos':
                informacion = SignosDistintivos(row,name,informacion)
            elif variable_aux == 'Softwares':
                informacion = Softwares(row,name,informacion)
            elif variable_aux == 'Demás trabajos':
                informacion = DemasTrabajos(row,name,informacion)
            elif variable_aux == 'Generación de contenido impresa':
                informacion = ContenidoImpreso(row,name,informacion)
            elif variable_aux == 'Generación de contenido multimedia':
                informacion = ContenidoMultimedia(row,name,informacion)
            elif variable_aux == 'Generación de contenido de audio':
                informacion = ContenidoAudio(row,name,informacion)
            elif variable_aux == 'Generación de contenido virtual':
                informacion = ContenidoVirtual(row,name,informacion)
            elif variable_aux == 'Estrategias pedagógicas para el fomento a la CTI':
                informacion = ContenidoCTI(row,name,informacion)
            elif variable_aux == 'Estrategias de comunicación del conocimiento':
                informacion = ComunicacionConocimiento(row,name,informacion)
            elif variable_aux == 'Espacios de participación ciudadana':
                informacion = EspacioParticipacionCiudadana(row,name,informacion)
            elif variable_aux == 'Participación ciudadana en proyectos de CTI':
                informacion = EspacioParticipacionCiudadanaCTI(row,name,informacion)
            elif variable_aux == 'Textos en publicaciones no científicas':
                informacion = PublicacionesNoCientificas(row,name,informacion)
            else:
                pass
       listas_campos.append(lista_campos)
       
       if len(set(lista_campos)) == 1:
           if 'Hoja de vida' in set(lista_campos):
               print('-'*20)
               print(name)
               informacion.append([name,'Hoja de vida_1-Hoja de vida',''])
         
        
df_final = pd.DataFrame(informacion, columns = ['Nombre','Variable','Valor'])
#%%
df_final['Variable_aux'] = df_final['Variable'].apply(lambda x: x[:x.find('_')])
df_final['Tipo_aux'] = df_final['Variable'].apply(lambda x: x[x.find('-')+1:])
                

df_final_aux = pd.DataFrame()
df_final_aux['Nombre'] = df_final['Nombre']
df_final_aux['Variable'] = df_final['Variable']
df_final_aux['Variable_aux'] = df_final['Variable_aux']
df_final_aux['Tipo_aux'] = df_final['Tipo_aux']
df_final_aux['Valor'] = df_final['Valor']


#%%
#Nueva Columna 

NuevaColumnaDic = {'Actividades Formación':['Asesorías','Cursos de corta duración','Trabajos dirigidos/tutorías'],
                   'Actividades Evaluador': ['Jurado en comités de evaluación','Par evaluador','Participación en comités de evaluación'],
                   'Apropiación Social': ['Publicaciones editoriales no especializadas','Producciones de contenido digital Audiovisual','Producciones de contenido digital Sonoro',
                       'Producciones de contenido digital Recursos gráficos','Producción de estrategias y contenidos transmedia','Desarrollos web',
                       'Fortalecimiento o solución de asuntos de interés social','Fortalecimiento de cadenas productivas','Consultorías','Documentos de trabajo',
                       'Ediciones/revisiones','Eventos científicos','Informes de investigación','Informes técnicos','Redes de conocimiento especializado',
                       'Generación de contenido impresa','Generación de contenido multimedia','Generación de contenido de audio','Generación de contenido virtual',
                       'Estrategias pedagógicas para el fomento a la CTI','Estrategias de comunicación del conocimiento',
                       'Espacios de participación ciudadana','Participación ciudadana en proyectos de CTI'],
                   'Obras de Arte': ['Obras o productos','Industrias Creativas y culturales','Eventos artísticos','Talleres Creativos'],
                   'Producción Bibliográfica':['Artículos','Capitulos de libro','Libros','Traducciones Filológicas y Edición de Fuentes',
                       'Libro de creación (Piloto)','Libro de Formación','Libros de divulgación y/o Compilación de divulgación',
                       'Manuales y Guías Especializadas','Otra producción blibliográfica','Traducciones','Notas científicas','Textos en publicaciones no científicas'],
                   'Producción Técnica':['Cartas, mapas y similares','Concepto técnico','Diseño industrial','Empresas de base tecnológica',
                       'Innovación de proceso o procedimiento','Innovación generada en la gestión empresarial','Nuevos registros científicos',
                       'Planta piloto','Productos tecnológicos','Prototipos','Normas y Regulaciones','Signos distintivos','Softwares'],
                   'Más Información': ['Demás trabajos'],
                   'Hoja de vida':['Hoja de vida']}

NuevaColumnalista = []
for x in df_final_aux['Variable_aux']:
    for y in NuevaColumnaDic:
        if x in NuevaColumnaDic[y]:
            NuevaColumnalista.append(y)
            break
        
df_final_aux['Categoria'] = NuevaColumnalista
#df_final_aux.to_excel('VersionFinal.xlsx')
