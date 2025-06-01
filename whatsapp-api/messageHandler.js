const path = require('path');
require('dotenv').config({ path: path.resolve(__dirname, '../.env') }); // 🔐 Carrega variáveis do .env

const axios = require('axios');

const GRUPO_AUTORIZADO = process.env.GRUPO_AUTORIZADO;

if (!GRUPO_AUTORIZADO) {
  console.error('❌ Variável GRUPO_AUTORIZADO não está definida no .env');
  process.exit(1);
} else {
  console.log(`🔐 Grupo autorizado carregado: ${GRUPO_AUTORIZADO}`);
}

function setupMessageListener(client) {
  client.on('message_create', async msg => {
    console.log('📨 Mensagem recebida de:', msg.id.remote);

    // ✅ Verifica se é do grupo autorizado
    if (msg.id.remote !== GRUPO_AUTORIZADO) {
      console.log('⛔ Mensagem ignorada (grupo não autorizado)');
      return;
    }

    console.log('💬 Conteúdo da mensagem:', msg.body);

    const payload = {
      from_: msg.from,
      name: msg.to,
      message: msg.body,
      from_me: msg.id.fromMe
    };

    try {
      console.log('📤 Enviando para API Python:', payload);

      const response = await axios.post('http://localhost:8000/webhook', payload);
      const reply = response.data.reply;

      if (reply) {
        await client.sendMessage(msg.id.remote, reply);
        console.log('📤 Resposta enviada ao grupo:', reply);
      }
    } catch (error) {
      console.error('❌ Erro ao enviar/receber da API Python:', error.message);
      if (error.response) {
        console.error('❌ Resposta da API:', error.response.status, error.response.data);
      }
    }
  });
}

module.exports = { setupMessageListener };
