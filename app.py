import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from datetime import datetime
# ============================================
# CONFIGURACIÓN
# ============================================
st.set_page_config(
    page_title="Business Automation Pack",
    page_icon="📦",
    layout="wide"
)

# ============================================
# ESTILOS
# ============================================
st.markdown("""
    <style>
    .main { background-color: #0F172A; }
    .stApp { background-color: #0F172A; }
    h1, h2, h3, p, label { color: white !important; }
    .metric-card {
        background: #1E293B;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        border-top: 4px solid #3B82F6;
    }
    </style>
""", unsafe_allow_html=True)

# ============================================
# HEADER
# ============================================
st.markdown("""
    <div style='background: linear-gradient(135deg, #1E293B, #334155); 
    padding: 30px; border-radius: 12px; margin-bottom: 20px;'>
        <h1 style='color: white; margin: 0;'>📦 Business Automation Pack</h1>
        <p style='color: #93C5FD; margin: 5px 0 0;'>
        Powered by Python 🐍
        </p>
    </div>
""", unsafe_allow_html=True)

# ============================================
# MENÚ LATERAL
# ============================================
st.sidebar.title("🗂️ Módulos")
modulo = st.sidebar.selectbox(
    "Seleccioná un módulo:",
    ["🏠 Inicio", 
     "📊 Sales Report", 
     "📦 Inventory Alert", 
     "💰 Income vs Expenses",
     "📄 Quote Generator"]
)

# ============================================
# MÓDULO: INICIO
# ============================================
if modulo == "🏠 Inicio":
    st.markdown("## Bienvenido al Business Automation Pack")
    st.markdown("Seleccioná un módulo del menú lateral para comenzar.")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("📊 **Sales Report**\n\nAnalizá tus ventas por producto con gráficos automáticos.")
    with col2:
        st.warning("📦 **Inventory Alert**\n\nDetectá productos con stock bajo automáticamente.")
    with col3:
        st.success("💰 **Income vs Expenses**\n\nVisualizá tu balance financiero en segundos.")

# ============================================
# MÓDULO: SALES REPORT
# ============================================
elif modulo == "📊 Sales Report":
    st.markdown("## 📊 Sales Report")
    st.markdown("Subí tu archivo Excel con columnas: **Product, Quantity, Price**")

    archivo = st.file_uploader("Subir archivo Excel", type=["xlsx", "csv"])

    if archivo:
        df = pd.read_excel(archivo) if archivo.name.endswith("xlsx") else pd.read_csv(archivo)
        df["Total"] = df["Quantity"] * df["Price"]
        ventas = df.groupby("Product")["Total"].sum().sort_values(ascending=False)
        total = ventas.sum()
        porcentajes = (ventas / total * 100).round(2)

        st.markdown("### 📋 Resumen")
        col1, col2, col3 = st.columns(3)
        col1.metric("💰 Total Revenue", f"${total:,.2f}")
        col2.metric("🏆 Best Seller", ventas.idxmax())
        col3.metric("📉 Worst Seller", ventas.idxmin())

        st.markdown("### 📊 Ventas por Producto")
        fig, ax = plt.subplots(figsize=(10, 4))
        fig.patch.set_facecolor("#1E293B")
        ax.set_facecolor("#1E293B")
        ventas.plot(kind="bar", ax=ax, color="#3B82F6", edgecolor="black")
        ax.set_title("Sales by Product", color="white")
        ax.tick_params(colors="white")
        ax.spines["bottom"].set_color("white")
        ax.spines["left"].set_color("white")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        st.pyplot(fig)

        st.markdown("### 📄 Datos completos")
        st.dataframe(df)

        output = io.BytesIO()
        df.to_excel(output, index=False)
        st.download_button(
            "⬇️ Descargar reporte Excel",
            data=output.getvalue(),
            file_name="sales_report.xlsx"
        )

# ============================================
# MÓDULO: INVENTORY ALERT
# ============================================
elif modulo == "📦 Inventory Alert":
    st.markdown("## 📦 Inventory Alert")
    st.markdown("Subí tu archivo Excel con columnas: **Product, Category, Stock**")

    stock_minimo = st.slider("Stock mínimo para alertas", 1, 50, 10)
    archivo = st.file_uploader("Subir archivo Excel", type=["xlsx", "csv"])

    if archivo:
        df = pd.read_excel(archivo) if archivo.name.endswith("xlsx") else pd.read_csv(archivo)
        stock_bajo = df[df["Stock"] <= stock_minimo].sort_values("Stock")
        stock_ok = df[df["Stock"] > stock_minimo]

        col1, col2, col3 = st.columns(3)
        col1.metric("📦 Total Products", len(df))
        col2.metric("✅ Stock OK", len(stock_ok))
        col3.metric("🚨 Low Stock", len(stock_bajo))

        if len(stock_bajo) > 0:
          st.error(f"🚨 {len(stock_bajo)} producto(s) necesitan reposición inmediata!")
          st.markdown("### 🔴 Productos a reponer")
          st.dataframe(
             stock_bajo,
             use_container_width=True,
             hide_index=False
    )
        else:
            st.success("✅ Todos los productos tienen stock suficiente!")

        st.markdown("### ✅ Productos con stock OK")
        st.dataframe(
    stock_ok,
    use_container_width=True,
    hide_index=False
)

# ============================================
# MÓDULO: INCOME VS EXPENSES
# ============================================
elif modulo == "💰 Income vs Expenses":
    st.markdown("## 💰 Income vs Expenses")
    st.markdown("Subí tu archivo Excel con columnas: **Date, Type, Category, Amount**")

    archivo = st.file_uploader("Subir archivo Excel", type=["xlsx", "csv"])

    if archivo:
        df = pd.read_excel(archivo) if archivo.name.endswith("xlsx") else pd.read_csv(archivo)
        df["Date"] = pd.to_datetime(df["Date"])
        df["Month"] = df["Date"].dt.strftime("%B")

        ingresos = df[df["Type"] == "Income"]["Amount"].sum()
        gastos = df[df["Type"] == "Expense"]["Amount"].sum()
        balance = ingresos - gastos
        margen = (balance / ingresos * 100).round(2) if ingresos > 0 else 0

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("💚 Total Income", f"${ingresos:,.2f}")
        col2.metric("🔴 Total Expenses", f"${gastos:,.2f}")
        col3.metric("💰 Balance", f"${balance:,.2f}")
        col4.metric("📊 Margin", f"{margen}%")

        fig, axes = plt.subplots(1, 2, figsize=(12, 4))
        fig.patch.set_facecolor("#1E293B")

        gastos_cat = df[df["Type"] == "Expense"].groupby("Category")["Amount"].sum()
        gastos_cat.plot(kind="pie", ax=axes[0], autopct="%1.1f%%", startangle=90)
        axes[0].set_title("Expenses by Category", color="white")
        axes[0].set_facecolor("#1E293B")

        por_mes = df.groupby(["Month", "Type"])["Amount"].sum().unstack(fill_value=0)
        por_mes.plot(kind="bar", ax=axes[1], color=["#DC2626", "#16A34A"], edgecolor="black")
        axes[1].set_title("Monthly Breakdown", color="white")
        axes[1].set_facecolor("#1E293B")
        axes[1].tick_params(colors="white")
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(fig)

        st.markdown("### 📄 Datos completos")
        st.dataframe(df)
        # ============================================
# MÓDULO: QUOTE GENERATOR
# ============================================
elif modulo == "📄 Quote Generator":
    st.markdown("## 📄 Quote Generator")
    st.markdown("Completá los datos para generar un presupuesto profesional en PDF.")

    col1, col2 = st.columns(2)
    with col1:
        nombre_negocio = st.text_input("Nombre de tu negocio", "Mi Negocio")
        email_negocio = st.text_input("Email", "contacto@minegocio.com")
    with col2:
        tel_negocio = st.text_input("Teléfono", "+54 11 1234-5678")
        validez = st.number_input("Validez del presupuesto (días)", 1, 60, 15)

    st.markdown("### 📦 Productos / Servicios")
    st.markdown("Subí un Excel con columnas: **Product, Description, Quantity, Unit Price**")

    archivo = st.file_uploader("Subir archivo Excel", type=["xlsx", "csv"])

    if archivo:
        df = pd.read_excel(archivo) if archivo.name.endswith("xlsx") else pd.read_csv(archivo)
        df["Subtotal"] = df["Quantity"] * df["Unit Price"]
        subtotal = df["Subtotal"].sum()
        iva = (subtotal * 0.21).round(2)
        total = (subtotal + iva).round(2)
        numero = datetime.now().strftime("%Y%m%d%H%M")
        fecha = datetime.now().strftime("%B %d, %Y")

        col1, col2, col3 = st.columns(3)
        col1.metric("Subtotal", f"${subtotal:,.2f}")
        col2.metric("IVA 21%", f"${iva:,.2f}")
        col3.metric("TOTAL", f"${total:,.2f}")

        st.dataframe(df, use_container_width=True)

        if st.button("📄 Generar PDF"):
            buffer = io.BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=A4,
                rightMargin=15*mm, leftMargin=15*mm,
                topMargin=12*mm, bottomMargin=12*mm)

            DARK = colors.HexColor("#1E293B")
            ACCENT = colors.HexColor("#3B82F6")
            WHITE = colors.white
            GRAY = colors.HexColor("#F1F5F9")

            styles = getSampleStyleSheet()
            story = []

            title_s = ParagraphStyle("t", fontSize=22, textColor=WHITE, fontName="Helvetica-Bold", alignment=TA_LEFT)
            sub_s = ParagraphStyle("s", fontSize=10, textColor=colors.HexColor("#93C5FD"), fontName="Helvetica", alignment=TA_LEFT)
            body_s = ParagraphStyle("b", fontSize=9, textColor=DARK, fontName="Helvetica", alignment=TA_LEFT)

            header = Table([[
                Table([[Paragraph(nombre_negocio, title_s)],
                [Spacer(1, 6)],
                [Paragraph("Professional Quote", sub_s)],
                       [Paragraph(email_negocio, sub_s)],
                       [Paragraph(tel_negocio, sub_s)]], colWidths=[100*mm]),
                Table([[Paragraph("QUOTE", ParagraphStyle("q", fontSize=28, textColor=ACCENT, fontName="Helvetica-Bold", alignment=TA_RIGHT))],
                       [Paragraph(f"# {numero}", ParagraphStyle("qn", fontSize=9, textColor=colors.HexColor("#93C5FD"), fontName="Helvetica", alignment=TA_RIGHT))],
                       [Spacer(1,8)],
                       [Paragraph(f"Date: {fecha}", ParagraphStyle("qd", fontSize=9, textColor=WHITE, fontName="Helvetica", alignment=TA_RIGHT))],
                       [Paragraph(f"Valid: {validez} days", ParagraphStyle("qv", fontSize=9, textColor=WHITE, fontName="Helvetica", alignment=TA_RIGHT))]], colWidths=[70*mm])
            ]], colWidths=[100*mm, 75*mm])
            header.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),DARK),("PADDING",(0,0),(-1,-1),14)]))
            story.append(header)
            story.append(Spacer(1,10))

            headers_row = [["#","Product","Description","Qty","Unit Price","Subtotal"]]
            rows = [[str(i+1), str(row["Product"]), str(row.get("Description","")),
                     str(int(row["Quantity"])), f"${row['Unit Price']:,.2f}", f"${row['Subtotal']:,.2f}"]
                    for i, (_, row) in enumerate(df.iterrows())]

            pt = Table(headers_row + rows, colWidths=[10*mm,35*mm,55*mm,12*mm,22*mm,22*mm])
            pt.setStyle(TableStyle([
                ("BACKGROUND",(0,0),(-1,0),ACCENT),
                ("TEXTCOLOR",(0,0),(-1,0),WHITE),
                ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),
                ("FONTSIZE",(0,0),(-1,-1),9),
                ("ALIGN",(0,0),(-1,-1),"CENTER"),
                ("ALIGN",(1,1),(2,-1),"LEFT"),
                ("ROWBACKGROUNDS",(0,1),(-1,-1),[GRAY,WHITE]),
                ("GRID",(0,0),(-1,-1),0.5,colors.HexColor("#E2E8F0")),
                ("PADDING",(0,0),(-1,-1),6),
            ]))
            story.append(pt)
            story.append(Spacer(1,8))

            totals = Table([
                ["","","","","Subtotal:", f"${subtotal:,.2f}"],
                ["","","","","IVA 21%:", f"${iva:,.2f}"],
            ], colWidths=[10*mm,35*mm,55*mm,12*mm,22*mm,22*mm])
            totals.setStyle(TableStyle([("ALIGN",(4,0),(-1,-1),"RIGHT"),("FONTSIZE",(0,0),(-1,-1),9)]))
            story.append(totals)

            total_t = Table([["","","","","TOTAL:", f"${total:,.2f}"]],
                colWidths=[10*mm,35*mm,55*mm,12*mm,22*mm,22*mm])
            total_t.setStyle(TableStyle([
                ("BACKGROUND",(4,0),(-1,-1),DARK),
                ("TEXTCOLOR",(4,0),(-1,-1),WHITE),
                ("FONTNAME",(4,0),(-1,-1),"Helvetica-Bold"),
                ("FONTSIZE",(4,0),(-1,-1),11),
                ("ALIGN",(4,0),(-1,-1),"RIGHT"),
                ("PADDING",(0,0),(-1,-1),6),
            ]))
            story.append(total_t)

            doc.build(story)
            buffer.seek(0)

            st.download_button(
                "⬇️ Descargar presupuesto PDF",
                data=buffer,
                file_name=f"quote_{numero}.pdf",
                mime="application/pdf"
            )
            st.success("✅ PDF generado correctamente!")