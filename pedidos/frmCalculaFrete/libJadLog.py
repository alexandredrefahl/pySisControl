import requests
import json
import xlrd

def calcula_frete(Cep,peso,valor):
   url = 'http://www.jadlog.com.br/embarcador/api/cte/xml'
   url1 = 'http://www.jadlog.com.br/embarcador/api/frete/valor'
   cabecalho = {'content-type' : 'application/json', 'Authorization' : 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOjc3MDQ1LCJkdCI6IjIwMTkxMDExIn0.8yYFYJqGSQ9mpWXXs-WD5xRdvBc_FRazWnnzYHv5hag'}

   # para consulta de DACTE, mas esta seria uma outra função
   dados = { 'dacte' : '42190904884082000305570000067081591067081590' }

   # Modalidades
   # 0  - Expresso   - Aereo
   # 3  - .Package   - Rodoviário
   # 4  - Rodoviario - Rodoviario
   # 5  - Economico  - Rodoviario
   # 6  - DOC        - Rodoviario
   # 7  - Corporate  - Aereo
   # 9  - .COM       - Aereo
   # 12 - Cargo      - Aereo

   # Dados de entrada para consulta de Valor
   dados1 = {
   "frete": [
            {'cepori':'89203001', 'cepdes' : Cep, 'frap' : 'N', 'peso' : peso, 'cnpj' : '07727715000190' , 'conta' : '77045', 'contrato' : '', 'modalidade' : 9 , 'tpentrega' : 'D' , 'tpseguro' : 'N' , 'vldeclarado' : valor }
            ]
   }
   # Formata os dados JSON para envio
   data_json = json.dumps(dados1)
   # Faz a requisição para o servidor
   r = requests.post(url1, data=data_json, headers=cabecalho)
   # Converte o retorno em uma variável JSON que pode ser lida
   retorno = json.loads(r.content)

   # Calcula as correções para informar o valor do fretes
   valor_base = retorno['frete'][0]['vltotal']
   #print(valor_base)
   valor_corrigido = (valor_base + 4.5)*1.02
   #print(valor_corrigido)
   prazo = retorno['frete'][0]['prazo']

   return valor_corrigido, prazo

def calcula_peso_real(largura, altura, profundidade, modalidade, peso):
    """
    Função que retorna o peso de cubagem para calculo de frete via Jadlog
    * Modalidades de Frete
    * Modalidade 0 = Expresso
    * Modalidade 4 = Rodoviário
    :Largura: Largura em centímetros
    :Altura: Altura em centímetros
    :Profundidade: Profundidade em centímetros
    :Modalidade: Modalidade (0 - Expresso / 4 - Rodoviário)
    :Peso: Em Kg (Ex.: 27)
    :return: Peso real de cubagem para Jadlog
    """
    peso_cubagem = 0
    if modalidade == '0':
        peso_cubagem = largura * altura * profundidade / 6000
    if modalidade == '4':
        peso_cubagem = largura * altura * profundidade / 3333

    # Se o peso de cubagem for maior do que o real, ele deve ser usado
    if peso_cubagem > peso:
        peso_real = peso_cubagem
    else:
        peso_real = peso

    return peso_real

def aliquota_seguro(Cep):
   # Para consulta do Seguro na tabela de preços
   cepConsulta = int(Cep)

   # Faixas de taxação de seguro
   taxa_0 = 0.66
   taxa_1 = 1.00
   taxa_2 = 2.00

   #Localização das informações na planilha
   col_CEP = 2
   col_Seg = 9
   file_XLSX = "./pedidos/frmCalculaFrete/jadlog_cidaten_20.02.03.xls"

   # Abre o arquivo no na variável
   wb = xlrd.open_workbook(file_XLSX) 
   sheet = wb.sheet_by_index(0)
  
   #Percorre a tabela de CEP procurando o valor
   for i in range(sheet.nrows-17):
      # Procura a faixa de CEP
      faixa_CEP = sheet.cell_value(i + 17, col_CEP)
      # Se for valor único
      if len(faixa_CEP) == 8: 
         if int(faixa_CEP) == cepConsulta:
            # Pega na planilha a faixa de seguro
            faixa_seg = int(sheet.cell_value(i+17,col_Seg))
            print("Encontrado na linha ",(i+17))
            break
      if len(faixa_CEP) > 8:
         CEP_ini = int(faixa_CEP[:8])
         CEP_fim = int(faixa_CEP[11:])
         if cepConsulta >= CEP_ini and cepConsulta <= CEP_fim:
            # Pega na planilha a faixa de seguro
            faixa_seg = int(sheet.cell_value(i+17,col_Seg))
            print(CEP_ini, " - ", CEP_fim)
            print("Encontrado na linha ",(i+17))
            break
   
   # Calcula o valor do seguro
   aliq_seg = 0
   if faixa_seg == 0:
      aliq_seg = taxa_0
   if faixa_seg == 1:
      aliq_seg = taxa_1
   if faixa_seg == 2:
      aliq_seg = taxa_2

   return aliq_seg

def retorna_orcamento(CEP,Larg,Altu,Prof,Peso,Valor):
   # Função que retorna o orçamento no formato de string
   varValor = float(Valor)
   # Extrai as dimensões com base no texto de entrada
   varLarg = int(Larg)
   varProf = int(Prof)
   varAltu = int(Altu)
   varPeso = float(Peso)
   # Verifica se vai ser usado o peso calculado ou peso cubado
   peso_considerado = calcula_peso_real(varLarg, varAltu, varProf, 0, varPeso)
   Preco, Prazo = calcula_frete(CEP, peso_considerado, varValor)
   Preco += 4.5
   # Calcula Taxa Reguro
   seguro = aliquota_seguro(CEP)
   val_seguro = varValor * (seguro / 100)
   valor_final = Preco + val_seguro
   valor_orcado = valor_final / 0.955

def main():
   # Função principal da aplicação.
   varCEP = input("Digite o CEP:")
   varDIM = input("Digite as dimensões:")
   varPeso = input("Digite o Peso:")
   varValor = input("Digite o valor:")
   
   # Converte para número
   varValor = float(varValor)
   # Extrai as dimensões com base no texto de entrada
   varLarg = int(varDIM[:2])
   varProf = int(varDIM[3:5])
   varAltu = int(varDIM[6:])
   
   # Verifica se vai ser usado o peso calculado ou peso cubado
   peso_considerado = calcula_peso_real(varLarg,varAltu,varProf,0,float(varPeso))

   print("Peso considerado: ", peso_considerado)

   Preco,Prazo = calcula_frete(varCEP,peso_considerado,varValor)
   # Acréscimo de taxa Administrativa
   Preco += 4.5
   print("Preço Base: ", Preco)
   # Calcula Taxa Reguro
   seguro = aliquota_seguro(varCEP)
   val_seguro = varValor * (seguro/100)
   print("Valor Seguro: ",val_seguro)
   valor_final = Preco + val_seguro
   print("------------------------------")
   print("Preço Total: ", valor_final)
   print("Preço com Simples:", (valor_final/0.955))
   print("Prazo: ", Prazo, " dias úteis")
   print("------------------------------")

if __name__ == '__main__':
    main()