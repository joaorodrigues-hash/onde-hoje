import hashlib
import os

def gerar_hash_senha(senha_pura: str) -> str:
    """Gera um salt aleatório e calcula o hash PBKDF2 da senha."""
    salt = os.urandom(16).hex()
    hash_bytes = hashlib.pbkdf2_hmac(
        'sha256',
        senha_pura.encode('utf-8'),
        salt.encode('utf-8'),
        100_000
    )
    return f"{salt}${hash_bytes.hex()}"

def verificar_senha(senha_pura: str, senha_salva: str) -> bool:
    """Valida a senha digitada contra o hash ou contra legado em texto puro."""
    if not senha_salva:
        return False

    # Suporte a senhas antigas em texto simples
    if "$" not in senha_salva:
        return senha_pura == senha_salva

    try:
        salt, hash_esperado = senha_salva.split("$", 1)
        hash_bytes = hashlib.pbkdf2_hmac(
            'sha256',
            senha_pura.encode('utf-8'),
            salt.encode('utf-8'),
            100_000
        )
        return hash_bytes.hex() == hash_esperado
    except Exception:
        return False