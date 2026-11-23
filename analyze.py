"""Dependency-free descriptive statistics and simple linear regression."""
import argparse
import csv
import math
from pathlib import Path

def load_pairs(path, x_name, y_name):
    pairs = []
    with path.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames or x_name not in reader.fieldnames or y_name not in reader.fieldnames:
            raise ValueError(f"CSV must include columns {x_name!r} and {y_name!r}")
        for line, row in enumerate(reader, start=2):
            try: x, y = float(row[x_name]), float(row[y_name])
            except (ValueError, TypeError): raise ValueError(f"row {line}: values must be numeric")
            if not (math.isfinite(x) and math.isfinite(y)):
                raise ValueError(f"row {line}: values must be finite")
            pairs.append((x, y))
    if len(pairs) < 2: raise ValueError("at least two observations are required")
    return pairs

def summarize(pairs):
    n = len(pairs); xs = [p[0] for p in pairs]; ys = [p[1] for p in pairs]
    mx = sum(xs)/n; my = sum(ys)/n
    vx = sum((x-mx)**2 for x in xs)/(n-1)
    vy = sum((y-my)**2 for y in ys)/(n-1)
    cov = sum((x-mx)*(y-my) for x,y in pairs)/(n-1)
    if vx == 0: raise ValueError("x column is constant; regression slope is undefined")
    slope = cov/vx; intercept = my-slope*mx
    predictions = [intercept+slope*x for x in xs]
    sse = sum((y-pred)**2 for y,pred in zip(ys,predictions))
    sst = sum((y-my)**2 for y in ys)
    return {"n":n,"mean_x":mx,"mean_y":my,"sd_x":math.sqrt(vx),"sd_y":math.sqrt(vy),
            "covariance":cov,"correlation":cov/math.sqrt(vx*vy) if vy else float("nan"),
            "slope":slope,"intercept":intercept,"rmse":math.sqrt(sse/n),
            "r_squared":1-sse/sst if sst else float("nan")}

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("csv_file", type=Path); p.add_argument("--x", required=True); p.add_argument("--y", required=True)
    a = p.parse_args()
    try:
        s = summarize(load_pairs(a.csv_file,a.x,a.y))
        print(f"Observations: {s['n']}")
        for label,key in [("Mean x","mean_x"),("Mean y","mean_y"),("Sample SD x","sd_x"),
                          ("Sample SD y","sd_y"),("Sample covariance","covariance"),
                          ("Pearson r","correlation"),("Regression slope","slope"),
                          ("Regression intercept","intercept"),("In-sample RMSE","rmse"),
                          ("In-sample R²","r_squared")]:
            print(f"{label:<20} {s[key]:.4f}")
        print(f"Model: {a.y} = {s['intercept']:.4f} + {s['slope']:.4f} * {a.x}")
    except (OSError, UnicodeError, ValueError) as e:
        p.error(str(e))

if __name__ == "__main__": main()
