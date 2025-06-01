// app.js
const express = require('express');
const client = require('./whatsappClient');
const { setupMessageListener } = require('./messageHandler');

const app = express();
const port = 3000;

app.use(express.json());

// Endpoint para enviar mensagem
app.post('/send', async (req, res) => {
  const { number, message } = req.body;

  if (!number || !message) {
    return res.status(400).send({ error: 'Número e mensagem são obrigatórios.' });
  }

  const chatId = number.includes('@c.us') ? number : `${number}@c.us`;

  try {
    await client.sendMessage(chatId, message);
    res.send({ status: 'Mensagem enviada com sucesso!' });
  } catch (error) {
    console.error('Erro ao enviar mensagem:', error);
    res.status(500).send({ error: 'Erro ao enviar mensagem.' });
  }
});

// Inicializa o cliente e o servidor
// Inicializa o cliente e o servidor
setupMessageListener(client);

client.initialize()
  .then(() => {
    console.log('🔄 Inicializando cliente...');
  })
  .catch(err => {
    console.error('Erro ao inicializar cliente:', err);
  });


app.listen(port, () => {
  console.log(`🚀 API rodando em http://localhost:${port}`);
});
