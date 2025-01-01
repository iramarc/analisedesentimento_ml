// cypress/support/e2e.js

// Este arquivo é processado e carregado automaticamente antes dos arquivos de teste.
// Use este arquivo para configurar comportamentos globais e modificar o Cypress.

// Remova ou comente a linha abaixo se não houver um arquivo commands.js
// import './commands';

// Você pode adicionar mais configurações ou comandos personalizados aqui

// Exemplo de sobrescrita de comando personalizado
Cypress.Commands.overwrite('log', (originalFn, message) => {
    console.log(message);
    return originalFn(message);
  });
  
  
