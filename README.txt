
INSTRUÇÕES BÁSICAS:

1. Instale as dependências:
   pip install -r requirements.txt

2. Crie um projeto no Google Cloud e baixe o JSON da conta de serviço (Google Sheets API).
   Renomeie o arquivo para: gsheets-credentials.json

3. Crie uma planilha no Google Sheets com nome "Atendimentos WhatsApp".

4. Substitua os valores:
   - SUA_CHAVE_ZAPI
   - SEU_ID_INSTANCIA
   - SUA_CHAVE_OPENAI
   pelo que você tem.

5. Rode o servidor:
   python app.py

6. Cadastre o webhook da Z-API com a URL:
   http://SEU_IP_PUBLICO:5000/webhook

   (ou use ngrok: ngrok http 5000)

Agora você tem:
- Recebimento automático de texto e áudio
- Resposta com ChatGPT
- Registro no Google Sheets
