const { defineConfig } = require("cypress");

module.exports = defineConfig({
  projectId: '6cyytc',
  e2e: {
    baseUrl: "http://127.0.0.1:5000", // URL base do servidor backend
    supportFile: "cypress/support/e2e.js", // Caminho para o arquivo de suporte

    setupNodeEvents(on, config) {
      // Registra a tarefa 'log' que vai exibir as mensagens no console
      on('task', {
        log(message) {
          console.log(message);
          return null;
        },
      });
    },
  },
});
