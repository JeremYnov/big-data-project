# big-data-project

## Premier lancement du projet

```bash
# Créer le .env (linux)
cp .env-example .env

# Build l'image python
docker-compose build

# Start l'env
docker-compose up
```

## Éteindre entièrement les containers 

```bash
# Éteindre l'env
docker-compose down
```

## Relancer le projet (si il a déjà été build)

```bash
# Start l'env
docker-compose up
```
