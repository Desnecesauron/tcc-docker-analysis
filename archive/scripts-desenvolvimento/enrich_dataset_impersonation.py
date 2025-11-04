"""
Script para enriquecer o dataset com golpes de impersonation (se passando por instituições)
e golpes sem URLs
"""
import pandas as pd

# Golpes de impersonation (bancos, lojas, órgãos públicos)
impersonation_scams = [
    # Bancos - pedindo dados
    "Olá, aqui é do Banco Bradesco. Identificamos uma atividade suspeita em sua conta. Por favor, nos envie seu CPF e senha para verificação.",
    "Banco Itaú informa: sua conta será bloqueada em 24h. Atualize seus dados enviando CPF, senha e código do cartão.",
    "Santander: detectamos tentativa de fraude. Confirme sua identidade enviando dados do cartão de crédito.",
    "Nubank: sua conta apresenta irregularidades. Envie CVV e senha para regularização imediata.",
    "Caixa Econômica: você tem um saque do FGTS pendente. Informe seus dados bancários para liberação.",
    "Inter Bank: bloqueio preventivo ativado. Digite sua senha e token para desbloquear.",
    "Banco do Brasil alerta: acesso não autorizado detectado. Confirme seus dados agora.",
    "C6 Bank: atualize seu cadastro com CPF, RG e comprovante de residência para evitar bloqueio.",

    # Bancos - promessas de dinheiro
    "Parabéns! O Bradesco sorteou seu CPF. Você ganhou R$ 50.000. Envie seus dados para receber.",
    "Banco Santander: você foi contemplado com R$ 100 mil em crédito pré-aprovado. Confirme seus dados.",
    "Itaú Unibanco: promoção exclusiva! Ganhe R$ 10.000 agora. Cadastre seus dados do cartão.",
    "Nubank: você tem 1 milhão de reais disponível para saque. Informe sua senha para liberar.",

    # E-commerce - compras não reconhecidas
    "Mercado Livre informa: sua compra de R$ 2.500 foi aprovada. Se não reconhece, entre em contato urgente.",
    "Amazon: compra de iPhone 15 Pro no valor de R$ 8.999 confirmada. Caso não tenha comprado, clique aqui.",
    "Shopee: sua compra de R$ 1.850 será entregue amanhã. Para cancelar, ligue agora para 0800-XXX-XXXX.",
    "Magazine Luiza alerta: compra de R$ 4.200 em eletrodomésticos aprovada em seu CPF.",
    "Americanas: débito de R$ 3.600 realizado. Se não autorizou, regularize seus dados.",

    # Serviços públicos - ameaças
    "Receita Federal: você tem pendências fiscais. Multa de R$ 5.000. Regularize imediatamente seus dados.",
    "INSS: seu benefício será suspenso. Atualize seus dados cadastrais em até 48h.",
    "DETRAN: você tem multas pendentes. Para evitar suspensão da CNH, informe seus dados.",
    "Tribunal de Justiça: você está sendo intimado. Compareça ou envie seus dados para regularização.",
    "Prefeitura Municipal: IPTU atrasado resultará em negativação. Envie comprovante de pagamento.",

    # Utilidades - bloqueio
    "Vivo: sua linha será bloqueada por falta de pagamento. Evite suspensão enviando comprovante agora.",
    "Claro informa: sua internet será cortada. Regularize urgente com seus dados bancários.",
    "Enel: corte de energia programado para amanhã. Envie comprovante de pagamento para evitar.",
    "Correios: você tem uma encomenda parada. Taxa de R$ 50. Pague agora informando dados do cartão.",

    # Prêmios sem instituição clara
    "Você ganhou um iPhone 15 Pro Max! Parabéns! Para retirar, envie CPF, nome completo e endereço.",
    "Seu CPF foi sorteado! Ganhe R$ 25.000 agora mesmo. Responda com seus dados bancários.",
    "Parabéns! Você foi contemplado com um carro 0km. Confirme seus dados para retirada.",
    "Sua linha telefônica foi premiada com R$ 100.000! Informe seus dados para receber.",

    # Golpes de empréstimo
    "Empréstimo aprovado de R$ 50.000 sem consulta ao SPC. Envie RG, CPF e comprovante de renda.",
    "Crédito pré-aprovado de até R$ 100 mil. Liberação em 1 hora. Confirme seus dados pessoais.",
    "Banco Central libera empréstimo emergencial. Você tem R$ 30.000 disponíveis. Cadastre-se agora.",

    # WhatsApp/Telegram golpes
    "WhatsApp: sua conta será desativada por violar termos. Evite bloqueio confirmando seus dados.",
    "Telegram Premium: você ganhou 1 ano grátis! Cadastre email e senha para ativar.",

    # Cartão de crédito
    "Seu cartão de crédito foi clonado. Confirme os dados do cartão para bloqueio imediato.",
    "Limite do cartão aumentado para R$ 50.000. Confirme nome impresso e CVV para ativação.",

    # Familiar em perigo (muito comum)
    "Mãe, preciso de dinheiro urgente. Faz um PIX de R$ 2.000 agora por favor. Meu celular quebrou.",
    "Filho, sofri um acidente. Preciso de R$ 5.000 para o hospital. Transfere agora pelo meu CPF.",
    "Oi pai, troquei de número. Me manda R$ 1.500 urgente, vou te explicar depois.",

    # Promoções impossíveis
    "Netflix grátis por 5 anos! Confirme seus dados de pagamento para garantir.",
    "Spotify Premium vitalício. Envie email e senha do cartão para ativar.",
    "Ifood: R$ 500 em créditos grátis! Cadastre dados do cartão agora.",

    # Ameaças jurídicas
    "Você está sendo processado. Evite penhora de bens enviando seus dados para acordo.",
    "Notificação extrajudicial: dívida de R$ 12.000. Regularize com dados bancários urgente.",
    "Escritório de advocacia: você deve R$ 8.500. Evite execução fiscal com pagamento imediato.",
]

# Golpes com pedidos de PIX/dinheiro sem ser de instituição
money_request_scams = [
    "Oi filho, acessa esse link pra ganhar 5000 no pix agora",
    "Você ganhou R$ 10.000 no pix! Confirme seus dados para receber.",
    "Faça um PIX de R$ 100 e receba R$ 10.000 de volta. Promoção relâmpago!",
    "Ganhe R$ 5.000 agora! Basta fazer um PIX de R$ 50 para ativar.",
    "Invista R$ 200 e receba R$ 50.000 em 24 horas. Garantido!",
    "Oportunidade única! Envie R$ 300 e ganhe R$ 100.000 em bitcoins.",
    "Multiplique seu dinheiro! PIX de R$ 500 vira R$ 250.000.",
    "Preciso que você faça um PIX urgente de R$ 2.000 para mim. É emergência!",
    "Me empresta R$ 5.000 urgente? Devolvo amanhã com R$ 10.000.",
    "Faz um PIX pra mim agora de R$ 1.500. Preciso muito, depois explico.",
    "Transfere R$ 3.000 urgente. Estou numa situação difícil, por favor!",
    "Envia R$ 800 agora que eu te devolvo R$ 2.000 depois.",
]

# Mensagens que combinam múltiplas táticas
combined_scams = [
    "Bradesco URGENTE: sua conta será bloqueada em 2 horas. Você tem dívida de R$ 15.000. Evite negativação enviando CPF e senha agora!",
    "Banco Santander: parabéns! Você ganhou R$ 1 milhão. Para sacar, confirme dados do cartão, CVV e senha em 24 horas ou perderá o prêmio.",
    "Receita Federal alerta: multa de R$ 50.000 por irregularidades. Evite penhora enviando CPF, RG e comprovante de endereço urgente.",
    "DETRAN/INSS: sua CNH e benefício serão suspensos. Regularize com PIX de R$ 800 em taxa administrativa.",
    "Promoção Mercado Livre + Magazine Luiza: ganhe R$ 20.000 em compras! Cadastre dados do cartão de crédito para participar.",
    "WhatsApp + Governo: sua conta e CPF foram selecionados para auxílio emergencial de R$ 5.000. Confirme dados bancários.",
]

print("="*80)
print("ENRIQUECENDO DATASET COM GOLPES DE IMPERSONATION")
print("="*80)

# Carregar dataset existente
df = pd.read_csv('data/spam_ptbr_v4.tsv', sep='\t', encoding='utf-8', on_bad_lines='skip')
print(f"Dataset atual: {len(df)} mensagens")
print(f"  - Ham: {len(df[df['label'] == 'ham'])}")
print(f"  - Spam: {len(df[df['label'] == 'spam'])}")

# Criar DataFrame com novos golpes
all_scams = impersonation_scams + money_request_scams + combined_scams
new_spam_df = pd.DataFrame({
    'label': ['spam'] * len(all_scams),
    'message': all_scams
})

print(f"\nAdicionando {len(new_spam_df)} novos golpes:")
print(f"  - Impersonation: {len(impersonation_scams)}")
print(f"  - Money requests: {len(money_request_scams)}")
print(f"  - Combined tactics: {len(combined_scams)}")

# Combinar com dataset existente
df_enriched = pd.concat([df, new_spam_df], ignore_index=True)

# Embaralhar
df_enriched = df_enriched.sample(frac=1, random_state=42).reset_index(drop=True)

print(f"\nDataset enriquecido: {len(df_enriched)} mensagens")
print(f"  - Ham: {len(df_enriched[df_enriched['label'] == 'ham'])}")
print(f"  - Spam: {len(df_enriched[df_enriched['label'] == 'spam'])}")

# Salvar novo dataset
output_file = 'data/spam_ptbr_v5.tsv'
df_enriched.to_csv(output_file, sep='\t', index=False, encoding='utf-8')

print(f"\n✓ Dataset salvo em: {output_file}")
print("="*80)
