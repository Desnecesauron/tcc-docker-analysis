import subprocess
import json

golpe_messages = [
    "Parabéns! Você ganhou um iPhone 15. Clique: link.com/premio",
    'Sua conta foi sorteada com R$50.000! Responda "SIM" para resgatar.',
    'Você é o ganhador do nosso concurso! Acesse e retire seu prêmio: site.com/ganhador',
    'Última chance de resgatar seu prêmio exclusivo. Não perca!',
    'Seu CPF foi selecionado para um bônus de R$1.000. Saiba mais: bit.ly/bonus',
    'Vaga de emprego urgente! Salário alto, sem experiência. Detalhes: link.com/vaga',
    'Procuro pessoas para trabalhar em casa, ganhos diários. Interessados? Chame no WhatsApp.',
    'Oportunidade única! Torne-se um milionário em 30 dias. Clique aqui!',
    'Empresa busca talentos para cargo de liderança. Envie seu currículo para: email@spam.com',
    'Ganhe dinheiro fácil sem sair de casa. Saiba como: bit.ly/dinheiro',
    'Empréstimo aprovado na hora, sem consulta! Liberação imediata. Acesse: emprestimo.com/agora',
    'Precisa de dinheiro? Temos as menores taxas. Fale conosco: (XX) XXXXX-XXXX',
    'Seu crédito pré-aprovado espera por você. Não perca essa chance!',
    'Libere seu FGTS agora! Dinheiro na conta em 24h. Clique: fgts.com/libere',
    'Empréstimo consignado para negativados. Simule já!',
    'Sua conta bancária foi bloqueada por segurança. Atualize seus dados: banco.com/seguranca',
    'Detectamos atividade suspeita em seu cartão. Confirme sua identidade: cartao.com/seguro',
    'Sua fatura está atrasada. Evite juros, pague agora: fatura.com/pagar',
    'Alerta de segurança: Seu dispositivo foi invadido. Instale nosso antivírus: virus.com/proteja',
    'Receita Federal: Você tem pendências. Regularize sua situação: receita.com/pendencia'
]

nao_golpe_messages = [
    'Oi! Tudo bem?',
    'Chego em 10 minutos.',
    'Pode me ligar agora?',
    'Não esqueça do pão!',
    'Vamos almoçar juntos?',
    'A reunião foi adiada.',
    'Me encontra na praça.',
    'Vi seu recado, obrigado.',
    'Como foi seu dia?',
    'Preciso de ajuda com isso.',
    'Te vejo mais tarde.',
    'Onde você está?',
    'Feliz aniversário!',
    'Já estou saindo de casa.',
    'Conseguiu resolver?',
    'Manda um abraço pra ele.',
    'Que horas é o jogo?',
    'Peguei o ônibus errado.',
    'Me avisa quando chegar.',
    'Boa noite! Durma bem.'
]

misto_messages = [
    'Seu pacote está aguardando retirada. Confirme o endereço em: link.com/rastreio',
    'Atualize seus dados cadastrais para evitar bloqueio. Acesse: link.com/atualizar',
    'Parabéns! Você foi selecionado para uma oferta exclusiva. Saiba mais: link.com/oferta',
    'Sua fatura vence hoje. Evite juros, pague agora: link.com/pagar',
    'Notamos uma atividade incomum em sua conta. Verifique: link.com/seguranca',
    'Olá! Temos uma novidade importante para você. Confira: link.com/noticia',
    'Seu agendamento foi confirmado para amanhã. Detalhes: link.com/agenda',
    'Recebemos seu pedido. Acompanhe a entrega aqui: link.com/entrega',
    'Última chance! Desconto de 50% válido só hoje. Aproveite: link.com/desconto',
    'Seu saldo está baixo. Recarregue para continuar usando: link.com/recarga',
    'Precisamos da sua confirmação para prosseguir. Responda "SIM" ou acesse: link.com/confirmar',
    'Alerta: Seu limite de dados está quase esgotado. Gerencie: link.com/dados',
    'Sua senha expirou. Crie uma nova agora: link.com/nova-senha',
    'A pesquisa que você participou tem resultados! Veja: link.com/resultados',
    'Seu benefício foi liberado. Consulte o valor em: link.com/beneficio',
    'Urgente: Sua assinatura será cancelada se não for renovada. Renove: link.com/renovar',
    'Um amigo te enviou um presente! Resgate em: link.com/presente',
    'Sua conta está em análise. Para mais informações, acesse: link.com/analise',
    'Não perca! Evento exclusivo com vagas limitadas. Inscreva-se: link.com/evento',
    'Seu comprovante está disponível. Baixe aqui: link.com/comprovante'
]

def run_test(message):
    command = f'curl -X POST http://localhost:5000/classificar -H "Content-Type: application/json" -d "{{\\"mensagem\\": \\"{message}\\"}}"'
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    print("")
    print("command=" + command)
    print(result.stdout)
    print("")
    if result.stdout:
        try:
            return json.loads(result.stdout)
        except json.JSONDecodeError:
            return {"classificacao": "Erro de JSON", "confianca": 0.0}
    else:
        return {"classificacao": "Erro", "confianca": 0.0}

results = {
    "Golpe": [],
    "Não Golpe": [],
    "Misto": []
}

for msg in golpe_messages:
    res = run_test(msg)
    results["Golpe"].append({
        "Mensagem": msg,
        "Resultado Esperado": "Golpe",
        "Resultado Obtido": res['classificacao'],
        "Confiança": res['confianca'],
        "Status": "Correto" if res['classificacao'] == "Golpe" else "Incorreto"
    })

for msg in nao_golpe_messages:
    res = run_test(msg)
    results["Não Golpe"].append({
        "Mensagem": msg,
        "Resultado Esperado": "N Golpe (mensagem normal)",
        "Resultado Obtido": res['classificacao'],
        "Confiança": res['confianca'],
        "Status": "Correto" if res['classificacao'] == "N Golpe (mensagem normal)" else "Incorreto"
    })

for msg in misto_messages:
    res = run_test(msg)
    results["Misto"].append({
        "Mensagem": msg,
        "Resultado Esperado": "Ambíguo",
        "Resultado Obtido": res['classificacao'],
        "Confiança": res['confianca'],
        "Status": "N/A"
    })

with open("resultados_testes.md", "w") as f:
    f.write("# Resultados dos Testes Manuais\n\n")
    for category, category_results in results.items():
        f.write(f"## {category}\n\n")
        f.write("| Mensagem | Resultado Esperado | Resultado Obtido | Confiança | Status |\n")
        f.write("|---|---|---|---|---|")
        for result in category_results:
            f.write(f"| {result['Mensagem']} | {result['Resultado Esperado']} | {result['Resultado Obtido']} | {result['Confiança']} | {result['Status']} |\n")
        f.write("\n")

print("Testes concluídos e resultados salvos em resultados_testes.md")