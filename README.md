# FocusEd Mailer (FastAPI + SendGrid)
**EN:** Receives requests to email an observation with a PDF attachment. Auth via `X-API-KEY`.  
**BR:** Recebe requisições para enviar observação com PDF em anexo. Autenticação via `X-API-KEY`.

## Quick Start (Docker)
```bash
# EN: 1) Create the shared Docker network (only once)
# BR: 1) Criar a rede Docker compartilhada (apenas uma vez)
docker network create focused-net || true

# EN: 2) Build the mailer image
# BR: 2) Construir a imagem do mailer
docker build -t focused-mailer:0.1.0 .

# EN: 3) Run the container on port 8001
# BR: 3) Executar o contêiner na porta 8001
docker run --name mailer --rm   --env-file .env   --network focused-net   -p 8001:8001   focused-mailer:0.1.0
```

- **Swagger:** <http://localhost:8001/docs>  
- **Health:** `GET /health`

## Environment
See `.env.example`. Key settings:
- `SENDGRID_API_KEY` (API key from SendGrid)
- `MAILER_FROM_EMAIL` (must be a **verified** sender in SendGrid)
- `MAILER_API_KEY` (shared secret with backend)
- `RENDERER_URL` (e.g., `http://renderer:8002`)
- Optional: `MAILER_TO_OVERRIDE` (route all emails to one inbox for tests)

## Architecture
```mermaid
graph TB
  FE[Frontend (Nginx :80)] -->|/api proxy (CRUD: GET/POST/PUT/DELETE)| BE[Backend (FastAPI :8000)]
  BE -->|X-API-KEY auth| M[Mailer (FastAPI :8001)]
  M -->|POST /render| R[Renderer (WeasyPrint :8002)]
  M -->|Send email| SG[(SendGrid API)]
  BE -->|SQLite file (app.db)| DB[(SQLite)]
```

## SendGrid Setup / Configuração do SendGrid
**EN:**
1) Create a SendGrid account and log in. (www.sendgrid.com)
2) Go to **Settings → Sender Authentication** and verify either a **Single Sender** (email) or a **Domain**.  
3) Go to **Settings → API Keys**, create an API key with **Mail Send** permission.  
4) Put the key in `.env` as `SENDGRID_API_KEY`.  
5) Set `MAILER_FROM_EMAIL` to the verified sender address (from step 2).

**BR:**
1) Crie uma conta no SendGrid e faça login.  
2) Vá em **Settings → Sender Authentication** e verifique um **Single Sender** (e-mail) ou um **Domínio**.  
3) Vá em **Settings → API Keys** e crie uma chave com permissão **Mail Send**.  
4) Coloque a chave no `.env` como `SENDGRID_API_KEY`.  
5) Defina `MAILER_FROM_EMAIL` para o endereço verificado (do passo 2).

## API Overview
| Method | Path              | Description                         | Auth        |
|-------:|-------------------|-------------------------------------|-------------|
| GET    | /health           | Health probe                        | none        |
| POST   | /mail/observation | Send observation email with PDF     | `X-API-KEY` |

**POST /mail/observation** (example)
```bash
curl -sS -X POST http://localhost:8001/mail/observation   -H "Content-Type: application/json"   -H "X-API-KEY: YOUR_SUPER_SECRET_MATCHING_KEY"   -d '{
    "observation_id": 1,
    "teacher_email": "teacher@example.com",
    "subject": "FocusEd Observation #1",
    "body": "Please find attached your observation.",
    "html": "<h1>FocusEd Observation</h1><p>…</p>"
  }'
```

**EN:** Mailer calls `renderer` to generate a PDF and attaches it in the email via SendGrid.  
**BR:** O mailer chama o `renderer` para gerar PDF e anexa no e-mail via SendGrid.

## Demo Emails / E-mails de demonstração
**EN:** The sample dataset includes demo users with **open inbox** addresses at `mailbox.cc` (e.g., `focused-app.user1@mailbox.cc`, `focused-app.user2@mailbox.cc`, ...). These are **public** inboxes for testing only; anything you send there is visible to anyone.  

**BR:** O conjunto de dados de exemplo inclui usuários de demonstração com **caixas de entrada públicas** em `mailbox.cc` (ex.: `focused-app.user1@mailbox.cc`, `focused-app.user2@mailbox.cc`, ...). Essas caixas são **públicas** e servem apenas para testes; qualquer e-mail enviado é visível a qualquer pessoa.  

## Troubleshooting
- **401/403:** Check `X-API-KEY` header matches `MAILER_API_KEY`.  
- **SendGrid errors:** Verify API key and sender verification status; check logs in SendGrid dashboard.  
- **Renderer timeouts:** Ensure `RENDERER_URL` is reachable on `focused-net`.

## Development Notes
- **EN:** Add brief EN/PT-BR comments around handlers.  
- **BR:** Inclua comentários EN/PT-BR nos handlers.

## License
MIT — see `LICENSE`.

## Contributing
See `CONTRIBUTING.md`.