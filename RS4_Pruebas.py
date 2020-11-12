def GetAllFacultades(info: dict)-> list:
    facultades = set()
    
    for estudiante in info:
        
        listaMaterias = info.get(estudiante).get("materias")
        
        for materia in listaMaterias :
            
            try:
                creditos = int(materia.get('creditos'))
            except:
                return "Error numérico."
            
            retirada = materia.get('retirada')
            
            if int(creditos) > 0 and retirada == "No":
                #[{key:value},{key:value},{key:value}]
                
                facultad = materia.get('facultad')
                facultades.add(facultad)
    
    return sorted(list(facultades))

def specialCharChange(sentence:list):   
    
    letrasAcento = ["á","é","í","ó","ú","ñ"]
    letrasSinAcento = ["a","e","i","o","u","n"] 
    
    for letra in sentence:
        for key in letrasAcento:
            if letra == key:
                index = sentence.index(letra)
                sentence[index] = letrasSinAcento[index]
                     
    return sentence
      
def GetEmail(names:str, surnames:str, numero:int)->str:
    
    names = names.lower().split()
    surnames = surnames.lower().split(", ")
    
    firstName = specialCharChange([letra for letra in names[0]])
        
    firstSurnameWord = specialCharChange([letra for letra in surnames[1]])
    firstSurname = ''.join(firstSurnameWord)
    secondSurnameWord = specialCharChange([letra for letra in surnames[0]])
    secondSurname = ''.join(secondSurnameWord)
        
    Id = [str(i) for i in str(numero)]
    
    if len(names) == 2:
        
        secondNameWord = specialCharChange([letra for letra in names[1]])
        email = firstName[0] + secondNameWord[0] + "." + firstSurname + Id[-2] + Id[-1]
        
    else:
        email = firstName[0] + firstSurnameWord[0] + "." + secondSurname + Id[-2] + Id[-1]
           
    return email

def promedio_facultades(info: dict, contando_externos : bool = True ) -> tuple:
    
    allFacultades = GetAllFacultades(info)
    facultadesByNotes = {item:0 for item in allFacultades}
    emails = set()

    for key, value in facultadesByNotes.items():
        numerador = 0
        denominador = 0
    
        for estudiante in info:

            listaMaterias = info.get(estudiante).get("materias")
            nombres = info.get(estudiante).get("nombres")
            apellidos = info.get(estudiante).get("apellidos")
            documento = info.get(estudiante).get("documento")
            programa = info.get(estudiante).get("programa")
            
            for materia in listaMaterias :
                
                try:
                    creditos = int(materia.get('creditos'))
                except:
                    return "Error numérico."
                
                retirada = materia.get('retirada')
                facultad = materia.get('facultad')
                nota = materia.get('nota')
                
                if creditos > 0 and retirada == "No" and key == facultad:
                    
                    if contando_externos:
                        emails.add(GetEmail(nombres,apellidos,documento))
                                                
                        try:
                            numerador += nota * creditos
                            denominador += creditos
                        except:
                            return "Error numérico."
   
                    else:
                        
                        codigo = materia.get('codigo').split("-")[0]
                        codigosEstudiantes =  [i for i in str(estudiante)]
                        codigoVerano = codigosEstudiantes[4] + codigosEstudiantes[5]
                        
                        if programa == codigo and codigoVerano != '05' :
                            
                            emails.add(GetEmail(nombres,apellidos,documento))
                            
                            try:
                                numerador += nota * creditos
                                denominador += creditos
                            except:
                                return "Error numérico."
                            
        try:
            facultadesByNotes[key] = round(numerador / denominador, 2 )
        except:
            return "Error numérico."
            
    return(facultadesByNotes, sorted(list(emails)))
    