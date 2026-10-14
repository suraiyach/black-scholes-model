from .bs import price, greeks

def compute_row(row, S: float, r: float, T: float):
    sigma = max(1e-6, float(row.get("impliedVolatility", 0)))
    K = float(row["strikePrice"]) if isinstance(row["strikePrice"], (int, float)) else float(row["strikePrice"])
    kind = "C" if row.get("optionType", "CE").upper() in ("C", "CE") else "P"

    p = price(S, K, T, r, sigma, kind)
    g = greeks(S, K, T, r, sigma)

    out = {
        **row,
        "bsPrice": round(p, 2),
    }
    for k, v in g.items():
        if abs(v) < 1:
            out[k] = round(v, 6)
        else:
            out[k] = round(v, 4)
    return out
