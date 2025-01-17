import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def hitung_margin_profit(harga_per_unit, biaya_variabel_per_unit):
    if harga_per_unit <= 0:
        return "Tidak terdefinisi (harga per unit <= 0)"
    if harga_per_unit <= biaya_variabel_per_unit:
        return "Tidak ada margin (harga <= biaya variabel)"
    
    margin_profit = ((harga_per_unit - biaya_variabel_per_unit) / harga_per_unit) * 100
    return round(margin_profit, 2)

def hitung_laba_kotor_dan_bersih(total_pendapatan, total_biaya_variabel, biaya_tetap, pajak_persen):
    laba_kotor = total_pendapatan - total_biaya_variabel
    laba_bersih = laba_kotor - biaya_tetap
    laba_bersih_setelah_pajak = laba_bersih * (1 - pajak_persen / 100)
    return round(laba_kotor, 2), round(laba_bersih_setelah_pajak, 2)


def hitung_pendapatan_tambahan(laba_saat_ini, target_laba):
    return max(0, target_laba - laba_saat_ini)

def tampilkan_grafik(pendapatan, biaya, laba_saat_ini):
    labels = ['Pendapatan', 'Biaya', 'Laba Saat Ini']
    values = [pendapatan, biaya, laba_saat_ini]

    fig, ax = plt.subplots()
    ax.bar(labels, values, color=['blue', 'red', 'green'])
    ax.set_title('Perbandingan Pendapatan, Biaya, dan Laba')
    ax.set_ylabel('Jumlah (Rp)')
    st.pyplot(fig)

def hitung_margin_kontribusi(harga_per_unit, biaya_variabel_per_unit):
    return harga_per_unit - biaya_variabel_per_unit

def analisis_sensitivitas(jangkauan_harga, biaya_tetap, biaya_variabel_per_unit):
    hasil_sensitivitas = []

    for harga in jangkauan_harga:
        harga = harga * 1000

        if harga > biaya_variabel_per_unit:
            bep_unit = biaya_tetap / (harga - biaya_variabel_per_unit)
            hasil_sensitivitas.append({"Harga (RP)": harga, "BEP Unit (RP)": round(bep_unit, 2)})
        else:
            hasil_sensitivitas.append({"Harga (RP)": harga, "BEP Unit (RP)": "Tidak terdefinisi (harga <= biaya variabel)"})

    df_hasil = pd.DataFrame(hasil_sensitivitas)

    return df_hasil

def simulasi_target_laba(target_laba, biaya_tetap, margin_kontribusi):
    if margin_kontribusi > 0:
        unit_dibutuhkan = (target_laba + biaya_tetap) / margin_kontribusi
        return unit_dibutuhkan
    else:
        return "Tidak terdefinisi (margin kontribusi <= 0)"

def hitung_roi(investasi_awal, laba):
    if investasi_awal > 0:
        return (laba / investasi_awal) * 100
    else:
        return "Tidak terdefinisi (investasi awal <= 0)"

def hitung_periode_pengembalian(investasi_awal, laba_tahunan):
    if laba_tahunan > 0:
        return investasi_awal / laba_tahunan
    else:
        return "Tidak terdefinisi (laba tahunan <= 0)"

def plot_bep(biaya_tetap, biaya_variabel_per_unit, harga_per_unit, initial_units=100, tolerance=0.001):
    def newton_raphson(f, f_prime, x0, tolerance, max_iter=100):
        x = x0
        for _ in range(max_iter):
            fx = f(x)
            if abs(fx) < tolerance:
                return x
            f_prime_x = f_prime(x)
            if f_prime_x == 0:
                raise ValueError("Turunan mendekati nol, metode gagal.")
            x -= fx / f_prime_x
        raise ValueError("Metode Newton-Raphson tidak konvergen.")
    
    def total_cost(units):
        return biaya_tetap + (biaya_variabel_per_unit * units)

    def total_revenue(units):
        return harga_per_unit * units

    f = lambda units: total_cost(units) - total_revenue(units)
    f_prime = lambda units: biaya_variabel_per_unit - harga_per_unit

    try:
        bep_units = newton_raphson(f, f_prime, initial_units, tolerance)
        bep_revenue = total_revenue(bep_units)
        
        st.write(f"Titik Impas dalam Unit: {bep_units:.2f} unit")
        st.write(f"Titik Impas dalam Pendapatan: Rp {bep_revenue:,.2f}")
        
        max_units = int(bep_units * 1.5)
        units = np.linspace(0, max_units, 500)
        costs = total_cost(units)
        revenues = total_revenue(units)

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(units, costs, label="Total Biaya", color="red")
        ax.plot(units, revenues, label="Total Pendapatan", color="green")
        ax.axvline(bep_units, linestyle="--", color="blue", label="Titik Impas")
        ax.scatter([bep_units], [bep_revenue], color="blue", zorder=5)
        ax.set_title("Grafik Titik Impas (BEP)", fontsize=16)
        ax.set_xlabel("Jumlah Unit", fontsize=12)
        ax.set_ylabel("Biaya / Pendapatan (Rp)", fontsize=12)
        ax.legend()
        ax.grid(True)

        st.pyplot(fig)

    except ValueError as e:
        st.error(f"Perhitungan Gagal: {e}")

st.markdown("<h1 style='text-align: center;'>Business Break-Even Calculator</h1>", unsafe_allow_html=True)
st.markdown(
    """
    <p style='text-align: center;'>
    Aplikasi ini membantu anda untuk menghitung titik impas (break-even point) sebelum anda memulai usaha, 
    yaitu saat pendapatan bisnis sama dengan total biaya.
    </p>
    """, unsafe_allow_html=True
)

with st.sidebar:
    st.header("Input Data Bisnis Anda")

    try:
        harga_per_unit = st.number_input("Harga per Unit (Rp)", min_value=0.0, step=0.01, help="Harga penjualan untuk setiap unit produk.\nContoh: Jika Anda menjual sebuah produk dengan harga Rp50.000, maka masukkan angka 50000.")
        biaya_variabel_per_unit = st.number_input("Biaya Variabel per Unit (Rp)", min_value=0.0, step=0.01, help="Biaya yang berubah sesuai dengan jumlah unit yang diproduksi atau terjual (misalnya bahan baku).\nContoh: Jika biaya bahan baku dan produksi untuk satu unit adalah Rp30.000, maka masukkan angka 30000.")
        total_pendapatan = st.number_input("Total Pendapatan (Rp)", min_value=0.0, step=0.01, help="Total uang yang diperoleh dari penjualan semua unit produk.\nContoh: Jika Anda menjual 1.000 unit dengan harga per unit Rp50.000, maka total pendapatan adalah Rp50.000.000.")
        total_biaya_variabel = st.number_input("Total Biaya Variabel (Rp)", min_value=0.0, step=0.01, help="Total biaya variabel untuk seluruh unit yang diproduksi atau terjual.\nContoh: Jika biaya variabel per unit Rp30.000 dan Anda menjual 1.000 unit, maka total biaya variabel adalah Rp30.000.000.")
        biaya_tetap = st.number_input("Biaya Tetap (Rp)", min_value=0.0, step=0.01, help="Biaya yang tetap dan tidak dipengaruhi oleh jumlah unit yang terjual (misalnya sewa gedung atau gaji staf tetap).\nContoh: Jika biaya tetap Anda Rp10.000.000, maka masukkan angka 10000000.")
        pajak_persen = st.number_input("Pajak (%)", min_value=0.0, step=0.1, help="Persentase pajak yang dikenakan pada laba kotor.\nContoh: Jika pajak adalah 10%, masukkan angka 10.")
        investasi_awal = st.number_input("Investasi Awal (Rp)", min_value=0.0, step=0.01, help="Total uang yang Anda investasikan untuk memulai bisnis.\nContoh: Jika investasi awal Anda Rp100.000.000, maka masukkan angka 100000000.")
        laba_tahunan = st.number_input("Laba Tahunan (Rp)", min_value=0.0, step=0.01, help="Laba bersih yang Anda hasilkan dalam satu tahun.\nContoh: Jika laba bersih tahunan Anda Rp20.000.000, masukkan angka 20000000.")
        target_laba = st.number_input("Target Laba (Rp)", min_value=0.0, step=0.01, help="Jumlah laba yang ingin Anda capai dalam suatu periode tertentu.\nContoh: Jika target laba Anda adalah Rp50.000.000, maka masukkan angka 50000000.")
        jangkauan_harga = st.slider("Jangkauan Harga untuk Analisis Sensitivitas (Rp)", min_value=1.0, max_value=500.0, value=(10.0, 100.0), step=1.0, help="Rentang harga produk yang ingin Anda gunakan untuk menganalisis sensitivitas BEP.\nContoh: Jika Anda ingin menganalisis harga dari Rp10.000 hingga Rp100.000, pilih rentang ini.")
        kirim = st.button("Hitung")
    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")

if kirim:
    try:
        margin_profit = hitung_margin_profit(harga_per_unit, biaya_variabel_per_unit)
        st.subheader("Margin Laba")
        st.write(f"Margin laba per unit: {margin_profit}%")

        laba_kotor, laba_bersih = hitung_laba_kotor_dan_bersih(total_pendapatan, total_biaya_variabel, biaya_tetap, pajak_persen)
        st.subheader("Laba Kotor dan Laba Bersih")
        st.write(f"Laba kotor: Rp{laba_kotor:,}")
        st.write(f"Laba bersih: Rp{laba_bersih:,}")

        pendapatan_tambahan = hitung_pendapatan_tambahan(laba_bersih, target_laba)
        st.subheader("Pendapatan Tambahan")
        st.write(f"Untuk mencapai target laba, Anda memerlukan pendapatan tambahan sebesar Rp{pendapatan_tambahan:,}.")

        st.subheader("Visualisasi Grafik Laba")
        tampilkan_grafik(total_pendapatan, (total_biaya_variabel + biaya_tetap), laba_bersih)

        margin_kontribusi = hitung_margin_kontribusi(harga_per_unit, biaya_variabel_per_unit)
        st.subheader("Margin Kontribusi")
        st.write(f"Margin kontribusi per unit: Rp{margin_kontribusi:,}")

        hasil_sensitivitas = analisis_sensitivitas(range(int(jangkauan_harga[0]), int(jangkauan_harga[1] + 1)), biaya_tetap, biaya_variabel_per_unit)
        st.subheader("Analisis Sensitivitas")
        st.write(hasil_sensitivitas)

        unit_untuk_target_laba = simulasi_target_laba(target_laba, biaya_tetap, margin_kontribusi)
        st.subheader("Simulasi Target Laba")
        st.write(f"Unit yang dibutuhkan untuk mencapai target laba: {unit_untuk_target_laba}")

        roi = hitung_roi(investasi_awal, laba_bersih)
        st.subheader("Return on Investment (ROI)")
        st.write(f"ROI: {roi}%")

        periode_pengembalian = hitung_periode_pengembalian(investasi_awal, laba_tahunan)
        st.subheader("Periode Pengembalian Modal")
        st.write(f"Periode pengembalian: {periode_pengembalian} tahun")

        st.subheader("Visualisasi Break-Even Point (BEP)")
        plot_bep(biaya_tetap, biaya_variabel_per_unit, harga_per_unit)
    except Exception as e:
        st.error(f"Perhitungan Gagal: {e}")