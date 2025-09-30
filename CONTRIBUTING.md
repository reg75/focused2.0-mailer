# Contributing — FocusEd Mailer
**EN:** Thanks for helping improve the FocusEd mailer.  
**BR:** Obrigado por colaborar com o mailer do FocusEd.

## How to work locally
```bash
# EN: Build & run with Docker
# BR: Construir e executar com Docker
docker network create focused-net || true
docker build -t focused-mailer:0.1.0 .
docker run --name mailer --rm \
  --env-file .env \
  --network focused-net \
  -p 8001:8001 \
  focused-mailer:0.1.0
```

- **Docs:** http://localhost:8001/docs  
- **Health:** `GET /health`

## Branch & commit style
- Branches: `feat/<topic>`, `fix/<bug>`, `docs/<area>`
- Commits: Conventional Commits (`feat:`, `fix:`, `docs:`, etc.)

## Code style / Estilo de código
- Follow FastAPI conventions
- Keep routes simple and small
- Add EN/PT-BR comments where helpful

## Tests & checks
- Run container; POST to `/mail/observation` with a test payload
- Ensure it reaches SendGrid (or logs an error in dev mode)

## Security
- Protect `/mail/observation` with `X-API-KEY`
- Do not commit real API keys (`.env` is ignored, `.env.example` documents vars)

## Definition of done
- Builds & runs via Docker
- `/health` and `/docs` pass manual checks
- README updated if API changes
- Changelog updated