from pytrends.request import TrendReq


def interest_over_time(keyword: str, timeframe: str = "now 7-d", geo: str = ""):
    pytrends = TrendReq(hl="es", tz=360)
    pytrends.build_payload([keyword], timeframe=timeframe, geo=geo)
    df = pytrends.interest_over_time()
    if df.empty:
        return f"No hay datos para '{keyword}' en el periodo '{timeframe}'"
    if "isPartial" in df.columns:
        df = df.drop(columns=["isPartial"])
    lines = [f"Tendencias para: {keyword} ({timeframe})", ""]
    lines.append(f"{'Fecha':<20} {'Interés':>8}")
    lines.append("-" * 30)
    for date, row in df.iterrows():
        lines.append(f"{date.strftime('%Y-%m-%d'):<20} {int(row[keyword]):>8}")
    return "\n".join(lines)


def related_queries(keyword: str, geo: str = ""):
    pytrends = TrendReq(hl="es", tz=360)
    pytrends.build_payload([keyword], geo=geo)
    related = pytrends.related_queries()
    lines = [f"Consultas relacionadas con: {keyword}", ""]
    if keyword in related:
        queries = related[keyword]
        if "top" in queries and queries["top"] is not None:
            lines.append("  Top consultas:")
            for _, row in queries["top"].head(10).iterrows():
                lines.append(f"    {row['query']} ({row['value']})")
        if "rising" in queries and queries["rising"] is not None:
            lines.append("  En aumento:")
            for _, row in queries["rising"].head(10).iterrows():
                lines.append(f"    {row['query']} ({row['value']})")
    return "\n".join(lines) if len(lines) > 2 else "No hay consultas relacionadas."
