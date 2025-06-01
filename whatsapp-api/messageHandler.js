const axios = require('axios');
const GRUPO_AUTORIZADO = '120363402444501478@g.us'; // Grupo correto

function setupMessageListener(client) {
  client.on('message_create', async msg => {
    console.log('📨 Mensagem recebida de:', msg.id.remote);

    // Verifica se é do grupo autorizado
    if (msg.id.remote !== GRUPO_AUTORIZADO) {
      return;
    }

    console.log('📨 Conteúdo:', msg.body);
    console.log('📨 Conteúdo:', msg);

    const payload = {
      from_: msg.from,
      name: msg.to,
      message: msg.body,
      from_me:msg.id.fromMe
    };

    try {
      const response = await axios.post('http://localhost:8000/webhook', payload);
      const reply = response.data.reply;

      if (reply) {
        await client.sendMessage(msg.id.remote, reply);  // ← envia para o grupo certo
        console.log('📤 Resposta enviada:', reply);
      }
    } catch (error) {
      console.error('❌ Erro ao enviar/receber da API Python:', error.message);
    }
  });
}

module.exports = { setupMessageListener };
