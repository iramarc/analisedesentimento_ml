describe('Sentiment Analysis Tests', () => {
    beforeEach(() => { cy.visit('http://127.0.0.1:5000'); });
        
    // Teste 1: Verifica predição para texto válido em inglês
    it('Should return a prediction for valid text', () => {
        const text = "I am feeling great!";

        cy.request({
            method: 'POST',
            url: 'http://127.0.0.1:5000/predict',  // Endpoint da API
            body: { text },
        }).then((response) => {
            // Verifica se a predição está dentro dos valores esperados
            expect(response.body.prediction).to.be.oneOf(['POSITIVE', 'NEGATIVE', 'NEUTRAL']);
            // Verifica se a confiança é um número maior que 0
            expect(response.body.confidence).to.be.a('number');
            expect(response.body.confidence).to.be.greaterThan(0);
        });
    });

    // Teste 2: Verifica predição para texto válido em português
    it('Should return a prediction for valid text in Portuguese', () => {
        const text = "Hoje foi um dia incrível!";

        cy.request({
            method: 'POST',
            url: 'http://127.0.0.1:5000/predict',
            body: { text },
        }).then((response) => {
            // Validação similar ao teste em inglês
            expect(response.body.prediction).to.be.oneOf(['POSITIVE', 'NEGATIVE', 'NEUTRAL']);
            expect(response.body.confidence).to.be.a('number');
            expect(response.body.confidence).to.be.greaterThan(0);
        });
    });

    // Teste 3: Valida comportamento para texto vazio
    it('Should handle empty text', () => {
        const text = "";
    
        cy.request({
            method: 'POST',
            url: '/predict',
            body: { text },
            failOnStatusCode: false  // Permite validar respostas de erro
        }).then((response) => {
            // Verifica se a mensagem de erro está correta
            expect(response.body.error).to.equal('Texto inválido ou vazio.');
        });
    });
    
    // Teste 4: Valida comportamento para entrada numérica
    it('Should handle numeric-only input', () => {
        const text = "123456";
    
        cy.request({
            method: 'POST',
            url: '/predict',
            body: { text },
            failOnStatusCode: false
        }).then((response) => {
            // Verifica mensagem de erro específica para entradas numéricas
            expect(response.body.error).to.equal('Texto inválido: insira um texto com palavras.');
        });
    });

    // Teste 5: Verifica processamento de texto com caracteres especiais
    it('Should handle text with special characters', () => {
        const text = "Olá! Como você está? #feliz :)";

        cy.request({
            method: 'POST',
            url: 'http://127.0.0.1:5000/predict',
            body: { text },
        }).then((response) => {
            // Verifica predição e confiança para entrada válida
            expect(response.body.prediction).to.be.oneOf(['POSITIVE', 'NEGATIVE', 'NEUTRAL']);
            expect(response.body.confidence).to.be.a('number');
            expect(response.body.confidence).to.be.greaterThan(0);
        });
    });

    // Teste 6: Valida funcionalidade de limpeza de campos na interface
    it('Should clear the text input and result when the clear button is clicked', () => {
        cy.visit('http://127.0.0.1:5000'); // Porta correta
        cy.get('#text-input').type('Teste de limpeza');
        cy.get('button').contains('Limpar').click();
        // Verifica se os campos foram limpos corretamente
        cy.get('#text-input').should('have.value', '');
        cy.get('#result').should('have.text', '');
    });

    // Teste 7: Valida comportamento para texto contendo apenas caracteres especiais
    it('Should handle input with only special characters', () => {
        const text = "@#$%^&*!";

        cy.request({
            method: 'POST',
            url: 'http://127.0.0.1:5000/predict',
            body: { text },
            failOnStatusCode: false,
        }).then((response) => {
            // Verifica se a mensagem de erro está correta
            expect(response.status).to.eq(400);
            expect(response.body.error).to.equal('Texto inválido: insira um texto válido.');
        });
    });
});

describe('Performance Benchmark', () => {
    const MAX_RESPONSE_TIME = 200; // Tempo limite em milissegundos

    // Teste 8: Mede o tempo de resposta para entrada válida
    it('Should respond within acceptable time', () => {
        const text = "I am feeling great!";

        const start = Date.now(); // Inicia o cronômetro
        cy.request({
            method: 'POST',
            url: '/predict',
            body: { text },
        }).then((response) => {
            const end = Date.now(); // Finaliza o cronômetro
            const responseTime = end - start;

            // Valida se o tempo de resposta está dentro do limite aceitável
            expect(responseTime).to.be.lessThan(MAX_RESPONSE_TIME);
            cy.log(`Tempo de resposta: ${responseTime} ms`);
        });
    });
});
