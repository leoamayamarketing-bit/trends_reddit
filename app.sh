#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

source venv/bin/activate

if [ $# -eq 0 ]; then
    read -rp "Palabra a buscar: " KEYWORD
else
    KEYWORD="$1"
fi
KEYWORD="${KEYWORD//\"/}"

check_reddit() {
    python -c "from src.config import RedditConfig; exit(0) if RedditConfig().is_valid() else exit(1)" 2>/dev/null
}

setup_reddit() {
    echo ">>> Abriendo navegador para crear app en Reddit..."
    echo "  Ve a: https://www.reddit.com/prefs/apps"
    echo "  Clic en Create App -> tipo: script"
    echo "  Redirect URI: http://localhost:8080"
    echo ""
    read -rp "Presiona Enter cuando hayas creado la app..."
    echo ""

    read -rp "Client ID: " client_id
    read -rp "Client Secret: " client_secret
    read -rp "Username: " username
    read -rsp "Password: " password
    echo ""

    cat > .env <<-EOF
REDDIT_CLIENT_ID=$client_id
REDDIT_CLIENT_SECRET=$client_secret
REDDIT_USER_AGENT=mi-script-cli/1.0 (by /u/$username)
REDDIT_USERNAME=$username
REDDIT_PASSWORD=$password
EOF
    chmod 600 .env
    echo ""
    echo "✅ Reddit configurado correctamente"
}

reddit_oferta() {
    echo "  ⚠ Reddit no configurado."
    read -rp "  Configurar ahora? (s/N): " ans
    if [[ "$ans" =~ ^[sS] ]]; then
        setup_reddit
        return 0
    fi
    return 1
}

menu() {
    echo ""
    echo "=============================="
    echo "  mi-script-cli — Menu"
    echo "=============================="
    echo " Keyword: $KEYWORD"
    echo "------------------------------"
    echo " 1) Hot posts de r/\$KEYWORD"
    echo " 2) Top posts de r/\$KEYWORD (semana)"
    echo " 3) Buscar '\$KEYWORD' en Reddit"
    echo " 4) Google Trends para '\$KEYWORD'"
    echo " 5) Consultas relacionadas en Trends"
    echo " 6) Detalle de un post (por ID)"
    echo " 7) Usar otra palabra clave"
    echo " 8) Configurar Reddit API"
    echo " 0) Salir"
    echo "------------------------------"
    read -rp "Opcion: " opt
    echo ""
    case $opt in
        1|2|3|6)
            if ! check_reddit && ! reddit_oferta; then
                menu
                return
            fi
            case $opt in
                1)
                    echo ">>> Hot posts de r/$KEYWORD (top 10):"
                    python -m src.cli hot "$KEYWORD" --limit 10
                    ;;
                2)
                    echo ">>> Top posts de r/$KEYWORD esta semana (top 5):"
                    python -m src.cli top "$KEYWORD" --limit 5 --time week
                    ;;
                3)
                    echo ">>> Buscar '$KEYWORD' en Reddit:"
                    python -m src.cli search "$KEYWORD" --limit 5
                    ;;
                6)
                    read -rp "Post ID: " post_id
                    echo ">>> Detalle del post $post_id:"
                    python -m src.cli details "$post_id"
                    ;;
            esac
            menu
            ;;
        4)
            echo ">>> Google Trends: $KEYWORD (ultimos 7 dias):"
            python -m src.cli trends "$KEYWORD" --timeframe "now 7-d"
            menu
            ;;
        5)
            echo ">>> Consultas relacionadas con $KEYWORD:"
            python -m src.cli related "$KEYWORD"
            menu
            ;;
        7)
            read -rp "Nueva palabra clave: " KEYWORD && KEYWORD="${KEYWORD//\"/}"
            menu
            ;;
        8)
            setup_reddit
            menu
            ;;
        0) exit 0 ;;
        *)
            echo "Opcion invalida"
            menu
            ;;
    esac
}

if [ $# -ge 1 ]; then
    echo ">>> Google Trends para '$KEYWORD' (ultimos 7 dias):"
    python -m src.cli trends "$KEYWORD" --timeframe "now 7-d"
    echo ""
    echo ">>> Consultas relacionadas:"
    python -m src.cli related "$KEYWORD"
    if check_reddit; then
        echo ""
        echo ">>> Hot posts de r/$KEYWORD (top 5):"
        python -m src.cli hot "$KEYWORD" --limit 5
    else
        echo ""
        echo "  ⚠ Reddit no configurado."
        read -rp "  Configurar ahora? (s/N): " ans
        if [[ "$ans" =~ ^[sS] ]]; then
            setup_reddit
            echo ""
            echo ">>> Hot posts de r/$KEYWORD (top 5):"
            python -m src.cli hot "$KEYWORD" --limit 5
        fi
    fi
else
    menu
fi
