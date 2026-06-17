#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

source venv/bin/activate

KEYWORD="${1:-Lego}"

check_reddit() {
    python -c "from src.config import RedditConfig; exit(0) if RedditConfig().is_valid() else exit(1)" 2>/dev/null
}

reddit_ok() {
    if check_reddit; then
        return 0
    else
        echo "  ⚠ Reddit no configurado. Ejecuta: python -m src.cli setup"
        echo ""
        return 1
    fi
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
    echo " 0) Salir"
    echo "------------------------------"
    read -rp "Opcion: " opt
    echo ""
    case $opt in
        1)
            if reddit_ok; then
                echo ">>> Hot posts de r/$KEYWORD (top 10):"
                python -m src.cli hot "$KEYWORD" --limit 10
            fi
            menu
            ;;
        2)
            if reddit_ok; then
                echo ">>> Top posts de r/$KEYWORD esta semana (top 5):"
                python -m src.cli top "$KEYWORD" --limit 5 --time week
            fi
            menu
            ;;
        3)
            if reddit_ok; then
                echo ">>> Buscar '$KEYWORD' en Reddit:"
                python -m src.cli search "$KEYWORD" --limit 5
            fi
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
        6)
            if reddit_ok; then
                read -rp "Post ID: " post_id
                echo ">>> Detalle del post $post_id:"
                python -m src.cli details "$post_id"
            fi
            menu
            ;;
        7)
            read -rp "Nueva palabra clave: " KEYWORD && KEYWORD="${KEYWORD//\"/}"
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
        echo "  ⚠ Reddit no configurado. Para activar: python -m src.cli setup"
    fi
else
    menu
fi
