import re
import numpy as np

# ==================== FEATURES ORIGINAIS ====================

def has_url(text_series):
    """Detecta se há URL na mensagem (binário)"""
    return text_series.apply(lambda t: 1 if re.search(r'(https?://\S+)|([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}', t) else 0).to_numpy().reshape(-1, 1)

def has_phone_number(text_series):
    """Detecta se há número de telefone (8+ dígitos)"""
    return text_series.apply(lambda t: 1 if re.search(r'\d{8,}', t) else 0).to_numpy().reshape(-1, 1)

def has_money_keywords(text_series):
    """Detecta palavras relacionadas a dinheiro"""
    money_keywords = ['R$', 'dinheiro', 'grátis', 'ganhe', 'prêmio', 'desconto', 'oferta', 'pix', 'transferir', 'envia', 'depósito', 'depositar', 'pagamento', 'pagar', 'fatura', 'boleto', 'investimento', 'emprestimo', 'cartão']
    return text_series.apply(lambda t: 1 if any(keyword in t.lower() for keyword in money_keywords) else 0).to_numpy().reshape(-1, 1)

def has_urgency_keywords(text_series):
    """Detecta palavras de urgência"""
    urgency_keywords = ['urgente', 'imediatamente', 'agora', 'última chance', 'prazo', 'expira', 'hoje', 'não perca', 'último aviso', 'restam poucas', 'só hoje', 'corra', 'aproveite', 'imediato', 'agora mesmo', 'sem demora', 'não espere', 'últimas horas', 'tempo limitado', 'vagas limitadas']
    return text_series.apply(lambda t: 1 if any(keyword in t.lower() for keyword in urgency_keywords) else 0).to_numpy().reshape(-1, 1)

# ==================== FEATURES AVANÇADAS DE URL ====================

def num_urls(text_series):
    """Conta quantas URLs existem na mensagem"""
    url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
    return text_series.apply(lambda t: len(re.findall(url_pattern, t))).to_numpy().reshape(-1, 1)

def has_ip_url(text_series):
    """Detecta URLs com endereço IP direto (ex: http://192.168.1.1)"""
    ip_pattern = r'https?://(?:\d{1,3}\.){3}\d{1,3}'
    return text_series.apply(lambda t: 1 if re.search(ip_pattern, t) else 0).to_numpy().reshape(-1, 1)

def has_shortened_url(text_series):
    """Detecta URLs encurtadas (bit.ly, tinyurl, etc)"""
    shortened_pattern = r'https?://(?:bit\.ly|tinyurl\.com|goo\.gl|t\.co|ow\.ly|short\.link|encurtador\.com\.br)/\S+'
    return text_series.apply(lambda t: 1 if re.search(shortened_pattern, t) else 0).to_numpy().reshape(-1, 1)

def avg_url_length(text_series):
    """Calcula o comprimento médio das URLs (URLs longas são suspeitas)"""
    url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'

    def calc_avg_length(text):
        urls = re.findall(url_pattern, text)
        if urls:
            return sum(len(u) for u in urls) / len(urls)
        return 0

    return text_series.apply(calc_avg_length).to_numpy().reshape(-1, 1)

def has_suspicious_tld(text_series):
    """Detecta TLDs suspeitos (domínios gratuitos/baratos)"""
    suspicious_tlds = ['.tk', '.ml', '.ga', '.cf', '.gq', '.xyz', '.top', '.work', '.click', '.link']

    def check_tld(text):
        for tld in suspicious_tlds:
            if tld in text.lower():
                return 1
        return 0

    return text_series.apply(check_tld).to_numpy().reshape(-1, 1)

def max_subdomain_depth(text_series):
    """Calcula profundidade máxima de subdomínios (ex: a.b.c.example.com = 3)"""
    url_pattern = r'https?://([^/\s]+)'

    def calc_depth(text):
        urls = re.findall(url_pattern, text)
        if not urls:
            return 0
        max_depth = 0
        for domain in urls:
            # Remove porta se existir
            domain = domain.split(':')[0]
            # Conta pontos e subtrai 1 (example.com tem 1 ponto mas 0 subdomínios)
            depth = max(0, domain.count('.') - 1)
            max_depth = max(max_depth, depth)
        return max_depth

    return text_series.apply(calc_depth).to_numpy().reshape(-1, 1)

def has_encoded_chars(text_series):
    """Detecta caracteres codificados em URLs (%XX) - comum em obfuscação"""
    url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'

    def check_encoding(text):
        urls = re.findall(url_pattern, text)
        return 1 if any('%' in url for url in urls) else 0

    return text_series.apply(check_encoding).to_numpy().reshape(-1, 1)

# ==================== FEATURES DE PHISHING ESPECÍFICAS ====================

def has_at_in_url(text_series):
    """Detecta @ em URLs (técnica de phishing: http://google.com@malicious.com)"""
    pattern = r'https?://[^/]*@'
    return text_series.apply(lambda t: 1 if re.search(pattern, t) else 0).to_numpy().reshape(-1, 1)

def max_hyphens_in_domain(text_series):
    """Conta hífens máximos em domínios (ex: paypal-secure-login-verify.com)"""
    url_pattern = r'https?://([^/\s]+)'

    def count_hyphens(text):
        domains = re.findall(url_pattern, text)
        if not domains:
            return 0
        return max(domain.count('-') for domain in domains)

    return text_series.apply(count_hyphens).to_numpy().reshape(-1, 1)

def has_numbers_in_domain(text_series):
    """Detecta números em domínios (ex: paypa1.com em vez de paypal.com)"""
    url_pattern = r'https?://([^/\s]+)'

    def check_numbers(text):
        domains = re.findall(url_pattern, text)
        return 1 if any(bool(re.search(r'\d', domain)) for domain in domains) else 0

    return text_series.apply(check_numbers).to_numpy().reshape(-1, 1)

def has_nonstandard_port(text_series):
    """Detecta portas não padrão em URLs (não 80/443)"""
    pattern = r'https?://[^/]+:(?!80\b|443\b)\d+'
    return text_series.apply(lambda t: 1 if re.search(pattern, t) else 0).to_numpy().reshape(-1, 1)

def url_entropy(text_series):
    """Calcula entropia da URL (alta entropia = URL aleatória/suspeita)"""
    import math
    from collections import Counter

    url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'

    def calc_entropy(text):
        urls = re.findall(url_pattern, text)
        if not urls:
            return 0

        # Calcula entropia da primeira URL
        url = urls[0]
        if len(url) == 0:
            return 0

        # Conta frequência de cada caractere
        counter = Counter(url)
        length = len(url)

        # Calcula entropia de Shannon
        entropy = 0
        for count in counter.values():
            probability = count / length
            entropy -= probability * math.log2(probability)

        return entropy

    return text_series.apply(calc_entropy).to_numpy().reshape(-1, 1)

# ==================== FEATURES DE IMPERSONATION E ENGENHARIA SOCIAL ====================

def has_institution_name(text_series):
    """Detecta nomes de instituições financeiras, empresas e órgãos públicos (comum em phishing)"""
    institutions = [
        # Bancos
        'banco', 'bradesco', 'itau', 'itaú', 'santander', 'caixa', 'caixa econômica',
        'nubank', 'inter', 'banco do brasil', 'bb', 'sicoob', 'sicredi', 'safra',
        'original', 'neon', 'c6 bank', 'picpay', 'mercado pago', 'pagseguro',
        # E-commerce e marketplaces
        'mercadolivre', 'mercado livre', 'amazon', 'shopee', 'magalu', 'magazine luiza',
        'americanas', 'submarino', 'casas bahia', 'extra', 'carrefour', 'aliexpress',
        # Serviços e utilidades
        'correios', 'eletrobras', 'light', 'enel', 'copel', 'cemig', 'sabesp',
        'vivo', 'claro', 'tim', 'oi', 'nextel', 'algar', 'netflix', 'spotify',
        # Órgãos públicos
        'receita federal', 'governo', 'inss', 'detran', 'polícia federal', 'pf',
        'tribunal', 'justiça', 'ministério', 'prefeitura', 'sus', 'anvisa',
        # Transportes
        'uber', 'cabify', '99', 'latam', 'gol', 'azul', 'viajanet', 'decolar',
        # Outros serviços
        'ifood', 'rappi', 'whatsapp', 'telegram', 'facebook', 'instagram',
        'google', 'microsoft', 'apple', 'samsung'
    ]

    def check_institution(text):
        text_lower = text.lower()
        for inst in institutions:
            if inst in text_lower:
                return 1
        return 0

    return text_series.apply(check_institution).to_numpy().reshape(-1, 1)

def has_data_request(text_series):
    """Detecta pedidos de dados sensíveis ou ações suspeitas"""
    data_requests = [
        # Dados do cartão
        'dados do cartão', 'dados do cartao', 'número do cartão', 'numero do cartao',
        'cvv', 'código de segurança', 'codigo de seguranca', 'validade do cartão',
        'data de validade', 'bandeira do cartão', 'nome impresso',
        # Senhas e códigos
        'senha', 'sua senha', 'digite sua senha', 'informe sua senha',
        'código', 'codigo', 'token', 'código de verificação', 'codigo de verificacao',
        'código sms', 'codigo sms', 'código de confirmação', 'codigo de confirmacao',
        # Dados pessoais
        'cpf', 'seu cpf', 'digite seu cpf', 'informe seu cpf', 'número do cpf',
        'rg', 'identidade', 'data de nascimento', 'nome da mãe', 'nome da mae',
        'endereço completo', 'endereco completo', 'comprovante de residência',
        # Ações de atualização
        'atualize seus dados', 'confirme seus dados', 'verifique seus dados',
        'cadastre seus dados', 'envie seus dados', 'informe seus dados',
        'complete seu cadastro', 'regularize seu cadastro',
        # Acesso a contas
        'acesse sua conta', 'faça login', 'faca login', 'entre na sua conta',
        'desbloqueie sua conta', 'recupere sua conta', 'ative sua conta',
        # Solicitações diretas
        'envie', 'mande', 'repasse', 'encaminhe', 'compartilhe'
    ]

    def check_data_request(text):
        text_lower = text.lower()
        for request in data_requests:
            if request in text_lower:
                return 1
        return 0

    return text_series.apply(check_data_request).to_numpy().reshape(-1, 1)

def has_prize_claim(text_series):
    """Detecta mensagens de prêmios/ganhos (muito comum em golpes)"""
    prize_keywords = [
        'você ganhou', 'voce ganhou', 'foi sorteado', 'foi sorteada',
        'você é o ganhador', 'voce e o ganhador', 'parabéns você ganhou',
        'parabens voce ganhou', 'seu cpf foi sorteado', 'seu número foi sorteado',
        'numero foi sorteado', 'você foi premiado', 'voce foi premiado',
        'resgate seu prêmio', 'resgate seu premio', 'retire seu prêmio',
        'retire seu premio', 'receba seu prêmio', 'receba seu premio',
        'você tem um prêmio', 'voce tem um premio', 'prêmio pendente',
        'premio pendente', 'você foi contemplado', 'voce foi contemplado'
    ]

    return text_series.apply(
        lambda t: 1 if any(kw in t.lower() for kw in prize_keywords) else 0
    ).to_numpy().reshape(-1, 1)

def has_threat_language(text_series):
    """Detecta linguagem de ameaça/coerção (comum em golpes)"""
    threat_keywords = [
        'sua conta será bloqueada', 'sua conta sera bloqueada',
        'conta bloqueada', 'bloqueio de conta', 'suspensão', 'suspensao',
        'será cancelado', 'sera cancelado', 'será suspenso', 'sera suspenso',
        'pendência', 'pendencia', 'irregularidade', 'problema com seu',
        'atividade suspeita', 'tentativa de acesso', 'acesso não autorizado',
        'acesso nao autorizado', 'detectamos', 'identificamos um problema',
        'evite bloqueio', 'evite suspensão', 'evite suspensao',
        'prazo expira', 'expira em', 'vence hoje', 'último dia', 'ultimo dia',
        'multa', 'penalidade', 'cobrança', 'cobranca', 'dívida', 'divida',
        'negativação', 'negativacao', 'restrição', 'restricao'
    ]

    return text_series.apply(
        lambda t: 1 if any(kw in t.lower() for kw in threat_keywords) else 0
    ).to_numpy().reshape(-1, 1)

def has_large_money_amount(text_series):
    """Detecta valores monetários altos ou suspeitos (comum em golpes de prêmio)"""
    import re

    def check_money(text):
        # Procura por valores em R$
        money_patterns = [
            r'r\$\s*(\d+\.?\d*)',  # R$ 1000 ou R$ 1.000
            r'(\d+\.?\d*)\s*reais',  # 1000 reais
            r'(\d+\.?\d*)\s*mil',  # 100 mil
            r'(\d+)\s*milhão',  # 1 milhão
            r'(\d+)\s*milhao',  # 1 milhao
        ]

        text_lower = text.lower()

        # Verifica milhões/milhares
        if 'milhão' in text_lower or 'milhao' in text_lower or 'milhões' in text_lower or 'milhoes' in text_lower:
            return 1

        if 'mil reais' in text_lower and not 'milhas' in text_lower:
            # Pega o número antes de "mil reais"
            match = re.search(r'(\d+)\s*mil\s*reais', text_lower)
            if match and int(match.group(1)) >= 5:  # >= 5 mil reais
                return 1

        # Procura valores específicos
        for pattern in money_patterns[:2]:  # R$ e reais
            matches = re.findall(pattern, text_lower)
            for match in matches:
                try:
                    value = float(match.replace('.', '').replace(',', '.'))
                    if value >= 1000:  # Valores >= R$ 1.000
                        return 1
                except:
                    pass

        return 0

    return text_series.apply(check_money).to_numpy().reshape(-1, 1)

def has_action_required(text_series):
    """Detecta chamadas para ação imediata (CTA suspeitas)"""
    action_keywords = [
        'clique aqui', 'clique no link', 'acesse o link', 'acesse agora',
        'entre agora', 'cadastre-se', 'cadastre agora', 'registre-se',
        'confirme agora', 'verifique agora', 'atualize agora',
        'responda sim', 'responda agora', 'ligue agora', 'entre em contato',
        'não perca', 'nao perca', 'aproveite', 'garanta', 'garanta já',
        'garanta ja', 'saiba mais', 'descubra como', 'veja como',
        'baixe o app', 'instale o app', 'baixe agora'
    ]

    return text_series.apply(
        lambda t: 1 if any(kw in t.lower() for kw in action_keywords) else 0
    ).to_numpy().reshape(-1, 1)
