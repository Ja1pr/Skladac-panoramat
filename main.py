import  streamlit as st
import numpy as np
import cv2

st.set_page_config(page_title="Panorama", page_icon="📷", layout="wide")


st.title("Spojovač obrázků")
uploaded_files = st.file_uploader("Vyber fotky pro panorama", accept_multiple_files=True)
sliderdata = ["720P","HD","UHD","4K"]
pixels_dict = {
    "720P": 720,
    "HD": 1080,
    "UHD": 2160,
    "4K": 2160  # UHD a 4K se v TV světě často zaměňují, obojí je 2160p
}
posuvnik = st.select_slider(label="Kvalita?", options=sliderdata)



if st.button("Vytvořit panoramu"):
    with st.spinner("Zpracovávám"):
        zpracovane_obrazky = []



        for nahrany_soubor in uploaded_files:
            file_bytes = np.asarray(bytearray(nahrany_soubor.read()), dtype=np.uint8)
            img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

            if img is not None:
                pixels = pixels_dict[posuvnik]
                target_h = pixels
                pomer = target_h / img.shape[0]
                sirka = int(img.shape[1] * pomer)
                zmenseny = cv2.resize(img, (sirka, target_h))

                zpracovane_obrazky.append(zmenseny)


        if len(zpracovane_obrazky) >= 2:
            stitcher = cv2.Stitcher_create()

            # 2. Samotný proces skládání
            # Předáš mu celý seznam obrázků najednou
            status, panorama = stitcher.stitch(zpracovane_obrazky)

            # 3. Vyhodnocení výsledku
            if status == cv2.Stitcher_OK:
                # Opět převod na RGB pro web
                st.divider()
                final_rgb = cv2.cvtColor(panorama, cv2.COLOR_BGR2RGB)
                _, buffer = cv2.imencode('.jpg', panorama)
                st.download_button(
                    label="Stáhnout",
                    data=buffer.tobytes(),
                    file_name="moje_panorama.jpg",
                    mime="image/jpeg",
                )
                st.image(final_rgb, caption="")

                # 2. Vytvoříme tlačítko
            else:
                # Pokud se to nepovede (málo společných bodů)
                st.error(f"Chyba při skládání. Kód chyby: {status}")
                st.info("Zkus nahrát fotky, které se více překrývají.")

