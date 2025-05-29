# Django Payment Service

![](https://img.shields.io/badge/Python-v3.9-green) ![](https://img.shields.io/badge/Django-v4.2.17-1a780c) 
![](https://img.shields.io/badge/MySQL-v8.0-blue) ![](https://img.shields.io/badge/Nginx-1a780c) 
![](https://img.shields.io/badge/Docker-blue) ![](https://img.shields.io/badge/Poetry-6900C6)

## About
Django payment сервис, чистая (hexagonal) архитектура


## Install
1. Отредактировать `SECRET_KEY` в файле .env
     
2. `$ cd deploy && docker compose up -d`

## API
- POST `/api/webhook/bank/` принимает JSON следующего формата:

```json
{
  "operation_id": "ccf0a86d-041b-4991-bcf7-e2352f7b8a4a",
  "amount": 145000,
  "payer_inn": "1234567890",
  "document_number": "PAY-328",
  "document_date": "2024-04-27T21:00:00Z"
}
```
Ответы:  
**200** {"status": "OK"} если `operation_id` уже существует в БД  
**201** {"status": "success"} если новая `operation_id`:  
    - создаёт `Payment`  
    - начисляет сумму на баланс организации с `payer_inn`  
    - логирует изменение баланса  
___
- GET `/api/organizations/<inn>/balance/` возвращает текущий баланс организации по ИНН:

```json
{
  "inn": 1234567890,
  "balance": 1234567890
}
```

## Документация
- **Swagger** - будет доступна по адресу `/api/docs`
