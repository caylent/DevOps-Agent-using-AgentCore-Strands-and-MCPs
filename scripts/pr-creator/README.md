# 🤖 AI-Powered PR Creator

Script inteligente para crear Pull Requests con descripciones generadas automáticamente usando AWS Bedrock.

## 🚀 Características

- ✅ Genera descripciones de PR automáticamente usando Claude 3 Sonnet
- ✅ Analiza diffs, commits y archivos modificados 
- ✅ Soporte para templates personalizados de PR
- ✅ Fallbacks automáticos si la IA no está disponible
- ✅ Configuración flexible mediante variables de entorno
- ✅ Validaciones de prerequisitos (gh CLI, AWS CLI, jq)

## 📋 Prerequisitos

1. **GitHub CLI** instalado y autenticado:
   ```bash
   # Instalar gh CLI
   # macOS: brew install gh
   # Ubuntu: apt install gh
   gh auth login
   ```

2. **AWS CLI** configurado con credenciales:
   ```bash
   aws configure
   # O usar variables de entorno AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
   ```

3. **jq** para parsear JSON:
   ```bash
   # macOS: brew install jq
   # Ubuntu: apt install jq
   ```

4. **Permisos de Bedrock**: Tu cuenta AWS debe tener acceso a Amazon Bedrock y el modelo Claude 3 Sonnet.

## 🛠 Uso

### Uso básico:
```bash
./scripts/pr-creator/create.sh
```

### Configuración mediante variables de entorno:

```bash
# Rama base (default: dev)
BASE_BRANCH=main ./scripts/pr-creator/create.sh

# Título personalizado del PR
PR_TITLE="Mi nueva característica increíble" ./scripts/pr-creator/create.sh

# Template personalizado
TEMPLATE_PATH=.github/PULL_REQUEST_TEMPLATE/feature.md ./scripts/pr-creator/create.sh


# Deshabilitar IA
USE_AI=false ./scripts/pr-creator/create.sh

# Modelo de IA personalizado
AI_MODEL="anthropic.claude-3-haiku-20240307-v1:0" ./scripts/pr-creator/create.sh

# Tokens máximos para respuesta de IA
AI_MAX_TOKENS=500 ./scripts/pr-creator/create.sh
```

### Configuración completa:
```bash
BASE_BRANCH=main \
PR_TITLE="Integración con Bedrock para PRs inteligentes" \
TEMPLATE_PATH=.github/PULL_REQUEST_TEMPLATE/feature.md \
USE_AI=true \
AI_MODEL="anthropic.claude-3-sonnet-20240229-v1:0" \
AI_MAX_TOKENS=1000 \
./scripts/pr-creator/create.sh
```

## ⚙️ Variables de Configuración

| Variable | Default | Descripción |
|----------|---------|-------------|
| `BASE_BRANCH` | `dev` | Rama base para el PR |
| `PR_TITLE` | Último commit | Título del PR |
| `TEMPLATE_PATH` | `.github/PULL_REQUEST_TEMPLATE.md` | Path al template |
| `USE_AI` | `true` | Habilitar/deshabilitar generación IA |
| `AI_MODEL` | `anthropic.claude-3-sonnet-20240229-v1:0` | Modelo de Bedrock |
| `AI_MAX_TOKENS` | `1000` | Tokens máximos para respuesta |

## 🧠 Modelos de IA Disponibles

- `anthropic.claude-3-sonnet-20240229-v1:0` (Recomendado - Balance entre calidad y velocidad)
- `anthropic.claude-3-haiku-20240307-v1:0` (Más rápido, menos detallado)
- `anthropic.claude-3-opus-20240229-v1:0` (Más detallado, más lento)

## 📝 Templates de PR

El script busca templates en el siguiente orden:
1. Variable `TEMPLATE_PATH` (si se especifica)
2. `.github/PULL_REQUEST_TEMPLATE.md` (default)
3. Template mínimo generado automáticamente

### Template de ejemplo:
```markdown
## Summary

<!-- Describe what this PR does and why -->

## Changes
- 

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Breaking changes documented

## Notes
<!-- Additional notes, deployment instructions, etc. -->
```

## 🔧 Solución de Problemas

### Error: "AWS CLI not authenticated"
```bash
aws configure
# o
aws sts get-caller-identity  # para verificar autenticación
```

### Error: "jq not found"
```bash
# macOS
brew install jq

# Ubuntu/Debian
sudo apt update && sudo apt install jq
```

### Error: "Model access denied"
- Verifica que tu cuenta AWS tenga acceso a Amazon Bedrock
- Solicita acceso al modelo Claude 3 Sonnet en la consola de AWS
- Verifica que estés en una región que soporte Bedrock (us-east-1, us-west-2, etc.)

### La IA no funciona pero el script continúa
- Esto es normal! El script tiene fallbacks automáticos
- Verifica los logs para entender por qué falló la generación IA
- Usa `USE_AI=false` si quieres deshabilitar la IA completamente

## 🎯 Cómo Funciona

1. **Análisis**: El script analiza los cambios git desde la rama base
2. **Generación IA**: Envía diffs, commits y archivos modificados a Bedrock
3. **Template**: Usa la descripción IA o fallback en el template
4. **PR Creation**: Crea el PR con `gh pr create`
5. **Feedback**: Proporciona feedback visual del proceso

## 🤝 Contribuir

Para mejorar este script:
1. Fork el repositorio
2. Crea tu rama: `git checkout -b feature/mejora-increible`
3. Commit tus cambios: `git commit -m 'Agrega mejora increíble'`
4. Push: `git push origin feature/mejora-increible`
5. Crea un PR (¡usando este mismo script! 🎉)