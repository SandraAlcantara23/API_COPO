from flask import Flask, render_template, send_file, request
import matplotlib.pyplot as plt
import io
import math

app = Flask(__name__)

def koch_curve(order, length=1.0, start=(0, 0), angle=0):
    if order == 0:
        rad = math.radians(angle)
        x_end = start[0] + length * math.cos(rad)
        y_end = start[1] + length * math.sin(rad)
        return [start, (x_end, y_end)]
    
    length /= 3.0
    p1 = start
    rad = math.radians(angle)
    p2 = (p1[0] + length * math.cos(rad), p1[1] + length * math.sin(rad))
    
    rad60 = math.radians(angle + 60)
    p3 = (p2[0] + length * math.cos(rad60), p2[1] + length * math.sin(rad60))
    
    rad_60 = math.radians(angle - 60)
    p4 = (p3[0] + length * math.cos(rad_60), p3[1] + length * math.sin(rad_60))
    
    rad = math.radians(angle)
    p5 = (p4[0] + length * math.cos(rad), p4[1] + length * math.sin(rad))
    
    points = []
    points += koch_curve(order - 1, length, p1, angle)[:-1]
    points += koch_curve(order - 1, length, p2, angle + 60)[:-1]
    points += koch_curve(order - 1, length, p3, angle - 60)[:-1]
    points += koch_curve(order - 1, length, p4, angle)
    
    return points

def draw_half_koch(order=4):
    points = koch_curve(order, length=1.0)
    x, y = zip(*points)
    plt.figure(figsize=(8,4))
    plt.plot(x, y, color="blue")
    plt.axis("equal")
    plt.axis("off")
    plt.title(f"Copo de Nieve - Curva de Koch (orden {order})")
    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight", dpi=150)
    buf.seek(0)
    plt.close()
    return buf

# --------- RUTAS ---------
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        order = int(request.form.get("orden", 5))  # valor por defecto 5
        img_buf = draw_half_koch(order)
        return send_file(img_buf, mimetype="image/png")
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
