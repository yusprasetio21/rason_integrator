#!/bin/bash

# Metadata dimasukkan langsung di sini (format: WMO_ID|ICAO_Stasiun)
metadata=$(cat << 'EOM'
97810|WAPF_Stasiun Meteorologi Karel Sadsuitubun
97900|WAPS_Stasiun Meteorologi Mathilda Batlayeri
97722|WAPA_Stasiun Meteorologi Amahai
97790|WAPC_Stasiun Meteorologi Bandaneira
97700|WAPR_Stasiun Meteorologi Namlea
97724|WAPP_Stasiun Meteorologi Pattimura
97072|WAFF_Stasiun Meteorologi Mutiara Sis-Al Jufri
97086|WAFW_Stasiun Meteorologi Syukuran Aminudin Amir
97028|WAFL_Stasiun Meteorologi Sultan Bantilan
97096|WAFP_Stasiun Meteorologi Kasiguncu
97008|WAMH_Stasiun Meteorologi Naha
97014|WAMM_Stasiun Meteorologi Sam Ratulangi
97048|WAMG_Stasiun Meteorologi Djalaluddin
97192|WAWB_Stasiun Meteorologi Beto Ambari
97148|WAWW_Stasiun Geofisika Kendari
97142|WAWP_Stasiun Meteorologi Sangia Ni Bandera
97404|WAEW_LEOWATIMENA TNIAU
97460|WAEL_Stasiun Meteorologi Oesman Sadik
97410|WAEK_Pos Meteorologi Kao
97406|WAEG_Stasiun Meteorologi Gamar Malamo
97600|WAES_Stasiun Meteorologi Emalamo
97430|WAEE_Stasiun Meteorologi Sultan Babullah
97180|WAAA_Stasiun Meteorologi Sultan Hasanuddin
97124|WAFB_Stasiun Meteorologi Toraja
97126|WAFM_Stasiun Meteorologi Andi Jemma
97116|WAFJ_Stasiun Meteorologi Tampa Padang
96001|WITN_Stasiun Meteorologi Maimun Saleh
96011|WITT_Stasiun Meteorologi Sultan Iskandar Muda
96015|WITC_Stasiun Meteorologi Cut Nyak Dhien Nagan Raya
96009|WIMA_Stasiun Meteorologi Malikussaleh
96163|WIEE_Stasiun Meteorologi Minangkabau
96109|WIBB_Stasiun Meteorologi Sultan Syarif Kasim II
96171|WIBJ_Stasiun Meteorologi Japura
96043|WIMN_Stasiun Meteorologi Silangit
96035|WIMM_Stasiun Meteorologi Kualanamu
96075|WIMB_Stasiun Meteorologi Binaka
96071|WIME_Stasiun Meteorologi Aek Godang
96073|WIMS_Stasiun Meteorologi FL Tobing
96087|WIDD_Stasiun Meteorologi Hang Nadim
96145|WIDM_Stasiun Meteorologi Tarempa
96089|WIDT_Stasiun Meteorologi Raja Haji Abdullah
96179|WIDS_Stasiun Meteorologi Dabo
96091|WIDN_Stasiun Meteorologi Raja Haji Fisabilillah
96147|WION_Stasiun Meteorologi Maritim Natuna
97690|WAJJ_Stasiun Meteorologi Sentani
97980|WAKK_Stasiun Meteorologi Mopah
97580|WAJI_Stasiun Meteorologi Mararena
97570|WABO_Stasiun Meteorologi Sudjarwo Tjondronegoro
97686|WAVV_Stasiun Meteorologi Wamena
97796|WAYY_Stasiun Meteorologi Mozez Kilangin
97780|WAYE_Stasiun Meteorologi Enarotali
97682|WABI_Stasiun Meteorologi Nabire
97560|WABB_Stasiun Meteorologi Frans Kaisiepo
97876|WAKT_Stasiun Meteorologi Tanah Merah
97530|WAUU_Stasiun Meteorologi Rendani
97630|WASF_Stasiun Meteorologi Torea
97760|WASK_Stasiun Meteorologi Utarom
97502|WASS_Stasiun Meteorologi Domine Eduard Osok
96859|WAHI_Stasiun Meteorologi Yogyakarta
96853|WAHH_ADI SUTJIPTO TNIAU
96855|WARY_Stasiun Geofisika Sleman
0|WIHH_Halim Perdana Kusuma Jakarta
96559|WIOS_Stasiun Meteorologi Tebelian
96557|WIOG_Stasiun Meteorologi Nangapinoh
96533|WIOI_HARRY DADISUMANTRY TNIAU
96581|WIOO_Stasiun Meteorologi Supadio
96535|WIOH_Stasiun Meteorologi Paloh
96615|WIOK_Stasiun Meteorologi Rahadi Oesman
96565|WIOP_Stasiun Meteorologi Pangsuma
96221|WIPP_Stasiun Meteorologi Sultan Mahmud Badaruddin II
96749|WIII_Stasiun Meteorologi Soekarno Hatta
96739|WIRR_Stasiun Meteorologi Budiarto
96839|WAHS_Stasiun Meteorologi Ahmad Yani
96805|WIIL_Stasiun Meteorologi Tunggul Wulung
96755|WIHJ_ATANG SANDJAJA TNIAU
96793|WICD_Pos Meteorologi Penggung
96781|WICC_HUSEIN SASTRA NEGARA TNIAU
96791|WICA_Stasiun Meteorologi Kertajati
96249|WIKT_Stasiun Meteorologi H. AS. Hananjoeddin
96237|WIKK_Stasiun Meteorologi Depati Amir
96207|WIJI_Stasiun Meteorologi Depati Parbo
96195|WIJJ_Stasiun Meteorologi Sultan Thaha
96295|WILL_Stasiun Meteorologi Radin Inten II
96253|WIGG_Stasiun Meteorologi Fatmawati Soekarno
96525|WAQD_Stasiun Meteorologi Tanjung Harapan
96509|WAQQ_Stasiun Meteorologi Juwata
96503|WAQA_Stasiun Meteorologi Nunukan
96505|WAQJ_Stasiun Meteorologi Yuvai Semaring
96695|WAOK_Stasiun Meteorologi Gusti Syamsir Alam
99991|TEST_upt testing
96685|WAOO_Stasiun Meteorologi Syamsudin Noor
96925|WARW_Stasiun Meteorologi Sangkapura
96933|WRSP_Stasiun Meteorologi Perak I
96987|WADY_Stasiun Meteorologi Banyuwangi
96935|WARR_Stasiun Meteorologi Juanda
96947|WARA_ABDUL RAHMAN SALEH TNIAU
96973|WART_Stasiun Meteorologi Trunojoyo
96881|WARI_ISWAHYUDI TNIAU
96929|WARD_Stasiun Meteorologi Dhoho
96607|WALS_Stasiun Meteorologi Aji Pangeran Tumenggung Pranoto
96529|WAQT_Stasiun Meteorologi Kalimarau
96633|WALL_Stasiun Meteorologi Sultan Aji Muhammad Sulaiman Sepinggan
97230|WADD_Stasiun Meteorologi I Gusti Ngurah Rai
97270|WADB_Stasiun Meteorologi Sultan Muhammad Salahuddin
97240|WADL_Stasiun Meteorologi Zainuddin Abdul Madjid
97260|WADS_Stasiun Meteorologi Sultan Muhammad Kaharuddin
96651|WAGS_Stasiun Meteorologi H. Asan
96653|WAGM_Stasiun Meteorologi Sanggu
96595|WAGB_Stasiun Meteorologi Beringin
96645|WAGI_Stasiun Meteorologi Iskandar
96655|WAGG_Stasiun Meteorologi Tjilik Riwut
97380|WATS_Stasiun Meteorologi Tardamu
97284|WATG_Stasiun Meteorologi Frans Sales Lega
97300|WATC_Stasiun Meteorologi Fransiskus Xaverius Seda
97378|WATR_Stasiun Meteorologi David Constatijn Saudale
97340|WATU_Stasiun Meteorologi Umbu Mehang Kunda
97372|WATT_Stasiun Meteorologi Eltari
97310|WATL_Stasiun Meteorologi Gewayantana
97320|WATM_Stasiun Meteorologi Mali
97282|WATO_Stasiun Meteorologi Komodo
99924|WICN_AWOS Nusawiru
99927|WARE_Pos Meteorologi Bandara Notohadinegoro - Jember
99928|WIPB_AWOS Silampari - Sumatera
97004|WAMN_Pos Meteorologi Melonguane
99930|WAEH_AWOS Weda Bay
96801|WICM_Wiriadinata TNI AU
99934|WIOD_Pos Meteorologi Singkawang
99957|WATK_AWOS Lede Kalumbang
99935|WATE_AWOS H. Hasan Aroeboesman
96149|WIDO_Raden Sadjad TNIAU
99909|WAOC_AWOS Bersujud
EOM
)

# Tanggal hari ini (format YYYYMMDD)
today=$(date +%Y%m%d)

# Path file binary
binary_dir="/home/bmkgsatu/rason_integrator/rasonfile-bucket/sent/binary"

# Cetak header
echo "no,filename,icao,station_name"

# Counter
n=1

# Loop file yang ketemu
find "$binary_dir" -type f \( -iname "*.bin" -o -iname "*.bfr" \) | grep "$today" | while read -r filepath; do
    filename=$(basename "$filepath")
    icao=$(echo "$filename" | cut -c9-12)

    # Ambil stasiun yang persis cocok ICAO nya
    station=$(echo "$metadata" | grep -E "\|${icao}_" | head -n1 | cut -d'|' -f2)

    echo "$n,$filename,$icao,$station"
    n=$((n+1))
done







