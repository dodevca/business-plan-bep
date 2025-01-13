import streamlit as st

# Title
st.title("Aplikasi Perhitungan Break Even Point (BEP)")

# Input dari user
st.header("Masukkan Data")
fixed_costs = st.number_input("Biaya Tetap (Rp)", min_value=0.0, step=100.0)
variable_cost_per_unit = st.number_input("Biaya Variabel per Unit (Rp)", min_value=0.0, step=10.0)
selling_price_per_unit = st.number_input("Harga Jual per Unit (Rp)", min_value=0.0, step=10.0)
sales_per_month = st.number_input("Penjualan per Bulan (Unit)", min_value=1, step=1)

# Perhitungan BEP
if variable_cost_per_unit < selling_price_per_unit:
    bep_units = fixed_costs / (selling_price_per_unit - variable_cost_per_unit)
    bep_revenue = bep_units * selling_price_per_unit
    time_to_bep = bep_units / sales_per_month
    
    # Output hasil perhitungan
    st.subheader("Hasil Perhitungan")
    st.write(f"Break Even Point (BEP) dalam Unit: {bep_units:.2f} unit")
    st.write(f"Break Even Point (BEP) dalam Rupiah: Rp {bep_revenue:,.2f}")
    st.write(f"Perkiraan Waktu Pencapaian BEP: {time_to_bep:.2f} bulan")
else:
    st.error("Biaya variabel per unit harus lebih kecil dari harga jual per unit!")
