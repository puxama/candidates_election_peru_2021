import requests
import json
import pandas as pd

dict_tp_eleccion = {'Presidencial':'1', 'Congresal':'2', 'Parlamento': '3'}


def get_postulantes(tp_eleccion):
    
    lt_postulantes = []
    id_tp_eleccion = dict_tp_eleccion[tp_eleccion]
    url = \
    "https://plataformaelectoral.jne.gob.pe/Candidato/GetExpedientesLista/110-{0}-null------0-".format(id_tp_eleccion)
    expediente_response = requests.request("GET", url)
    expediente_response = json.loads(expediente_response.text)
    
    for expediente in expediente_response['data']:
        url_get_candidatos = \
        "https://plataformaelectoral.jne.gob.pe/Candidato/GetCandidatos/{0}-110-{1}-{2}"\
        .format(id_tp_eleccion, 
                expediente['idSolicitudLista'],
                expediente['idExpediente'])
        
        candidatos_response = requests.request("GET", url_get_candidatos)
        candidatos_response = json.loads(candidatos_response.text)
        
        
        for candidato in candidatos_response['data']:
            url_hv_candidato = \
            "https://plataformaelectoral.jne.gob.pe/HojaVida/GetHVConsolidado?param={0}-0-{1}-110"\
            .format(candidato['idHojaVida'],
                    expediente['idOrganizacionPolitica'])
            print(url_hv_candidato)
            
            hv_response = requests.request("GET", url_hv_candidato)
            hv_response = json.loads(hv_response.text)['data']
            dict_atributos = {}
            dict_atributos['APELLIDO PATERNO'] = hv_response['oDatosPersonales']['strApellidoPaterno']
            dict_atributos['APELLIDO MATERNO'] = hv_response['oDatosPersonales']['strApellidoMaterno']
            dict_atributos['NOMBRE'] = hv_response['oDatosPersonales']['strNombres']
            dict_atributos['NUMERO'] = candidato['intPosicion']
            dict_atributos['DESIGNADO'] = candidato['strFGDesignado']
            dict_atributos['NATIVO'] = candidato['strFGNativo']
            dict_atributos['ESTADO'] = candidato['strEstadoExp']
            dict_atributos['DNI'] = candidato['strDocumentoIdentidad']
            #M = 1; F = 2
            dict_atributos['SEXO'] = candidato['strSexo']
            dict_atributos['FEC. NACIMIENTO'] = candidato['strFechaNacimiento']
            dict_atributos['PAIS NACIMIENTO'] = hv_response['oDatosPersonales']['strPaisNacimiento']
            dict_atributos['DEPARTAMENTO NACIMIENTO'] = hv_response['oDatosPersonales']['strNaciDepartamento']
            dict_atributos['PROVINCIA NACIMIENTO'] = hv_response['oDatosPersonales']['strNaciProvincia']
            dict_atributos['DISTRITO NACIMIENTO'] = hv_response['oDatosPersonales']['strNaciDistrito']
            
            dict_atributos['DEPARTAMENTO DOMICILIO'] = hv_response['oDatosPersonales']['strDomiDepartamento']
            dict_atributos['PROVINCIA DOMICILIO'] = hv_response['oDatosPersonales']['strDomiProvincia']
            dict_atributos['DISTRITO DOMICILIO'] = hv_response['oDatosPersonales']['strDomiDistrito']
            dict_atributos['DIRECCION'] = hv_response['oDatosPersonales']['strDomicilioDirecc']
            dict_atributos['ORGANIZACION POLITICA'] = expediente['strOrganizacionPolitica']
            dict_atributos['CARGO POSTULACION'] = candidato['strCargoEleccion']
            dict_atributos['CARGO CIRCUNSCRIPCION'] = hv_response['oDatosPersonales']['strPostulaDistrito']
            
            #EDUCACION BASICA
            dict_atributos['EDU BASICA'] = hv_response['oEduBasica']['strTengoEduBasica']
            dict_atributos['EDU PRIMARIA'] = hv_response['oEduBasica']['strEduPrimaria']
            dict_atributos['CONCLUIDO EDU PRIM'] = hv_response['oEduBasica']['strConcluidoEduPrimaria']
            dict_atributos['EDU SECUNDARIA'] = hv_response['oEduBasica']['strEduSecundaria']
            dict_atributos['CONCLUIDO EDU SEC'] = hv_response['oEduBasica']['strConcluidoEduSecundaria']
            
            #EDUCACION NO UNIVERSITARIA
            #dict_atributos['EDUCACION NO UNIVERSITARIA'] = hv_response['oEduNoUniversitaria']
            dict_atributos['TENGO NO UNIVERSITARIO'] = hv_response['oEduNoUniversitaria']['strTengoNoUniversitaria']
            dict_atributos['EDU NO UNIVERSITARIO'] = hv_response['oEduNoUniversitaria']['strEduNoUniversitaria']
            dict_atributos['CENTRO ESTUDIO NO UNIV.'] = hv_response['oEduNoUniversitaria']['strCentroEstudioNoUni']
            dict_atributos['CARRERA NO UNIV.'] = hv_response['oEduNoUniversitaria']['strCarreraNoUni']
            dict_atributos['CONCLUIDO NO UNI'] = hv_response['oEduNoUniversitaria']['strConcluidoNoUni']
            
            #POSGRADO
            #dict_atributos['POSGRADO'] = hv_response['oEduPosgrago']
            dict_atributos['TENGO POSGRADO'] = hv_response['oEduPosgrago']['strTengoPosgrado']
            dict_atributos['CENTRO ESTUDIO POSGRADO'] = hv_response['oEduPosgrago']['strCenEstudioPosgrado']
            dict_atributos['ESPEC. POSGRADO'] = hv_response['oEduPosgrago']['strEspecialidadPosgrado']
            dict_atributos['CONCLUIDO POSGRADO'] = hv_response['oEduPosgrago']['strConcluidoPosgrado']
            dict_atributos['EGRESADO POSGRADO'] = hv_response['oEduPosgrago']['strEgresadoPosgrado']
            dict_atributos['ES MAESTRO'] = hv_response['oEduPosgrago']['strEsMaestro']
            dict_atributos['ES DOCTOR'] = hv_response['oEduPosgrago']['strEsDoctor']
            dict_atributos['ANIO POSGRADO'] = hv_response['oEduPosgrago']['strAnioPosgrado']
            dict_atributos['POSGRADO COMENTARIO'] = hv_response['oEduPosgrago']['strComentario']
            
            #DECLARACION JURADA DE BIENES Y RENTAS
            #dict_atributos['DECL. JURADA DE BIENES y RENTAS'] = hv_response['oIngresos']
            dict_atributos['TENGO INGRESOS'] = hv_response['oIngresos']['strTengoIngresos']
            dict_atributos['ANIO INGRESOS'] = hv_response['oIngresos']['strAnioIngresos']
            dict_atributos['REMU BRUTA PUBLICA'] = hv_response['oIngresos']['decRemuBrutaPublico']
            dict_atributos['REMU BRUTA PRIVADO'] = hv_response['oIngresos']['decRemuBrutaPrivado']
            dict_atributos['RENTA IND. PUBLICO'] = hv_response['oIngresos']['decRentaIndividualPublico']
            dict_atributos['RENTA IND. PRIVADO'] = hv_response['oIngresos']['decRentaIndividualPrivado']
            dict_atributos['OTRO INGRESO PUBLICO'] = hv_response['oIngresos']['decOtroIngresoPublico']
            dict_atributos['OTRO INGRESO PRIVADO'] = hv_response['oIngresos']['decOtroIngresoPrivado']
            
            #INFORMACION ADICIONAL
            #dict_atributos['INFORMACION ADICIONAL'] = hv_response['oInfoAdicional']
            dict_atributos['TENGO INF. ADICIONAL'] = hv_response['oInfoAdicional']['strTengoInfoAdicional']
            dict_atributos['INFORMACION ADICIONAL'] = hv_response['oInfoAdicional']['strInfoAdicional']
            
            dict_atributos['FECHA LLENADO DATOS'] = hv_response['oDatosPersonales']['strFeTerminoRegistro']
            
            dict_atributos['EXPERIENCIA LABORAL'] = hv_response['lExperienciaLaboral']
            dict_atributos['EDUCACION UNIVERSITARIA'] = hv_response['lEduUniversitaria']
            
            dict_atributos['TRAYECTORIA PARTIDARIA'] = hv_response['lCargoPartidario']
            dict_atributos['CARGO ELECCION POPULAR'] = hv_response['lCargoEleccion']
            dict_atributos['RENUNCIA ORG. POLITICAS'] = hv_response['lRenunciaOP']
            
            dict_atributos['SENTENCIAS PENALES'] = hv_response['lSentenciaPenal']
            dict_atributos['SENTENCIAS POR OBLIGACION'] = hv_response['lSentenciaObliga']
            
            
            dict_atributos['BIENES INMUEBLES'] = hv_response['lBienInmueble']
            dict_atributos['BIENES MUEBLES'] = hv_response['lBienMueble']
            
            lt_postulantes.append(dict_atributos)
        
    return lt_postulantes



def format_atributos(df, path):

    #ltAtributos = ['EXPERIENCIA LABORAL']
    dfatributo_EL = pd.DataFrame()
    dfatributo_EU = pd.DataFrame()
    dfatributo_TP = pd.DataFrame()
    dfatributo_EP = pd.DataFrame()
    dfatributo_RP = pd.DataFrame()
    dfatributo_SP = pd.DataFrame()
    dfatributo_SO = pd.DataFrame()
    dfatributo_BI = pd.DataFrame()
    dfatributo_BM = pd.DataFrame()


    for index, row in df.iterrows():

        dfatributo_EL_tmp = pd.DataFrame(row['EXPERIENCIA LABORAL'])
        dfatributo_EU_tmp = pd.DataFrame(row['EDUCACION UNIVERSITARIA'])
        dfatributo_TP_tmp = pd.DataFrame(row['TRAYECTORIA PARTIDARIA'])
        dfatributo_EP_tmp = pd.DataFrame(row['CARGO ELECCION POPULAR'])
        dfatributo_RP_tmp = pd.DataFrame(row['RENUNCIA ORG. POLITICAS'])
        dfatributo_SP_tmp = pd.DataFrame(row['SENTENCIAS PENALES'])
        dfatributo_SO_tmp = pd.DataFrame(row['SENTENCIAS POR OBLIGACION'])
        dfatributo_BI_tmp = pd.DataFrame(row['BIENES INMUEBLES'])
        dfatributo_BM_tmp = pd.DataFrame(row['BIENES MUEBLES'])

        dfatributo_EL_tmp['strUsuario'] = row['DNI'].zfill(8)
        dfatributo_EU_tmp['strUsuario'] = row['DNI'].zfill(8)
        dfatributo_TP_tmp['strUsuario'] = row['DNI'].zfill(8)
        dfatributo_EP_tmp['strUsuario'] = row['DNI'].zfill(8)
        dfatributo_RP_tmp['strUsuario'] = row['DNI'].zfill(8)
        dfatributo_SP_tmp['strUsuario'] = row['DNI'].zfill(8)
        dfatributo_SO_tmp['strUsuario'] = row['DNI'].zfill(8)
        dfatributo_BI_tmp['strUsuario'] = row['DNI'].zfill(8)
        dfatributo_BM_tmp['strUsuario'] = row['DNI'].zfill(8)

        dfatributo_EL = pd.concat([dfatributo_EL,dfatributo_EL_tmp], axis=0)
        dfatributo_EU = pd.concat([dfatributo_EU,dfatributo_EU_tmp], axis=0)
        dfatributo_TP = pd.concat([dfatributo_TP,dfatributo_TP_tmp], axis=0)
        dfatributo_EP = pd.concat([dfatributo_EP,dfatributo_EP_tmp], axis=0)
        dfatributo_RP = pd.concat([dfatributo_RP,dfatributo_RP_tmp], axis=0)
        dfatributo_SP = pd.concat([dfatributo_SP,dfatributo_SP_tmp], axis=0)
        dfatributo_SO = pd.concat([dfatributo_SO,dfatributo_SO_tmp], axis=0)
        dfatributo_BI = pd.concat([dfatributo_BI,dfatributo_BI_tmp], axis=0)
        dfatributo_BM = pd.concat([dfatributo_BM,dfatributo_BM_tmp], axis=0)

    dfatributo_EL.to_csv(path+'/EXPERIENCIA LABORAL.csv', index=False, encoding='utf-8')
    dfatributo_EU.to_csv(path+'/EDUCACION UNIVERSITARIA.csv', index=False, encoding='utf-8') 
    dfatributo_TP.to_csv(path+'/TRAYECTORIA PARTIDARIA.csv', index=False, encoding='utf-8') 
    dfatributo_EP.to_csv(path+'/CARGO ELECCION POPULAR.csv', index=False, encoding='utf-8') 
    dfatributo_RP.to_csv(path+'/RENUNCIA ORG. POLITICAS.csv', index=False, encoding='utf-8') 
    dfatributo_SP.to_csv(path+'/SENTENCIAS PENALES.csv', index=False, encoding='utf-8') 
    dfatributo_SO.to_csv(path+'/SENTENCIAS POR OBLIGACION.csv', index=False, encoding='utf-8') 
    dfatributo_BI.to_csv(path+'/BIENES INMUEBLES.csv', index=False, encoding='utf-8') 
    dfatributo_BM.to_csv(path+'/BIENES MUEBLES.csv', index=False, encoding='utf-8', )



if __name__ == '__main__':

	#dict_tp_eleccion = {'Presidencial':'1', 'Congresal':'2', 'Parlamento': '3'}

	ltCongreso = get_postulantes('Congresal')
	dfCongreso = pd.DataFrame(ltCongreso)

	dfCongreso.to_csv('Congresal/CANDIDATOS CONGRESALES.CSV', index=False, encoding='utf-8')

	format_atributos(dfCongreso, 'Congresal')