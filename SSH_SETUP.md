# Настройка SSH для AWS EC2 деплоя

## Проблема
```
Permission denied (publickey)
```

Это означает, что GitHub Actions пытается подключиться к EC2 с ключом, который не авторизован на сервере.

## Решение

### Вариант 1: Использовать существующий ключ с EC2 (Рекомендуется)

На вашем EC2 сервере уже есть ключ `id_ed25519`. Нужно добавить его в GitHub Secrets.

**Шаг 1:** На EC2 сервере получите **приватный** ключ:
```bash
ssh ubuntu@YOUR_EC2_IP
cat ~/.ssh/id_ed25519
```

**Важно:** Это приватный ключ, храните его в секрете!

**Шаг 2:** Скопируйте весь вывод (включая `-----BEGIN OPENSSH PRIVATE KEY-----` и `-----END OPENSSH PRIVATE KEY-----`)

**Шаг 3:** Добавьте в GitHub Secrets:
1. Откройте: https://github.com/loguntsovae-teachmeskills/TeachMeCiCd/settings/secrets/actions
2. Нажмите `New repository secret`
3. Name: `EC2_SSH_KEY`
4. Value: вставьте скопированный приватный ключ
5. Нажмите `Add secret`

### Вариант 2: Создать новый SSH ключ для деплоя

**На вашей локальной машине:**

```bash
# Создать новый SSH ключ
ssh-keygen -t ed25519 -C "github-actions-deploy" -f ~/.ssh/github_deploy_key -N ""

# Показать приватный ключ (для GitHub Secret)
cat ~/.ssh/github_deploy_key

# Показать публичный ключ (для EC2)
cat ~/.ssh/github_deploy_key.pub
```

**На EC2 сервере:**

```bash
# Добавить публичный ключ в authorized_keys
ssh ubuntu@YOUR_EC2_IP
echo "ВАШ_ПУБЛИЧНЫЙ_КЛЮЧ" >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
```

**В GitHub:**
1. Добавьте **приватный** ключ в Secret `EC2_SSH_KEY`

### Вариант 3: Использовать ключ от EC2 instance

Если вы создавали EC2 instance с key pair, используйте этот ключ:

1. Найдите ваш `.pem` файл (например, `my-key-pair.pem`)
2. Конвертируйте его если нужно:
```bash
# Если это .pem формат, он уже подходит
cat your-key.pem
```
3. Добавьте содержимое в GitHub Secret `EC2_SSH_KEY`

## Проверка настройки

После настройки проверьте подключение:

```bash
# С вашей локальной машины (используя тот же ключ)
ssh -i ~/.ssh/your_key ubuntu@YOUR_EC2_IP
```

Если подключение успешно - GitHub Actions тоже сможет подключиться!

## Текущие GitHub Secrets

Убедитесь что все три секрета настроены:

| Secret Name | Описание | Пример значения |
|-------------|----------|-----------------|
| `EC2_SSH_KEY` | Приватный SSH ключ | Содержимое `id_ed25519` или `.pem` файла |
| `EC2_HOST` | IP адрес EC2 | `54.123.45.67` или DNS |
| `EC2_USER` | Пользователь SSH | `ubuntu` (для Ubuntu AMI) |

## Безопасность

⚠️ **Важно:**
- Никогда не коммитьте приватные ключи в Git
- Используйте GitHub Secrets для хранения ключей
- Ограничьте доступ к EC2 Security Group (только необходимые IP)
- Регулярно ротируйте SSH ключи

## Troubleshooting

### Ошибка: "Too open permissions"
```bash
chmod 600 ~/.ssh/authorized_keys
chmod 700 ~/.ssh
```

### Ошибка: "No such file or directory"
```bash
# На EC2 создайте директорию для деплоя
mkdir -p /home/ubuntu/app
```

### Проверка authorized_keys
```bash
# На EC2 сервере
cat ~/.ssh/authorized_keys
```

Должен содержать публичный ключ, соответствующий приватному ключу в GitHub Secret.
