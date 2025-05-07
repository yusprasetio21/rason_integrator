#!/bin/bash

# === Path dan Metadata ===
BINARY_DIR="/ftp/rasonftp/sent/"
OUTPUT_DIR="/home/bmkgsatu/rason_integrator/checkfile/"
TODAY=$(date +%Y-%m-%d)
OUTPUT_CSV="$OUTPUT_DIR/check_file_ftp_$(date +%Y%m%d).csv"

# Metadata stasiun
read -r -d '' METADATA << EOM
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

# === 2. Load metadata ke associative array ===
declare -A STATIONS
while IFS='|' read -r id name; do
    STATIONS["$id"]="$name"
done <<< "$METADATA"

# === 3. Cek folder dan file yang dimodifikasi hari ini ===
if [[ ! -d "$BINARY_DIR" ]] || [[ ! -d "$OUTPUT_DIR" ]]; then
    echo "Folder tidak ditemukan: $BINARY_DIR atau $OUTPUT_DIR"
    exit 1
fi

FILES=()
while IFS= read -r -d $'\0' file; do
    FILES+=("$file")
done < <(find "$BINARY_DIR" -type f -newermt "$TODAY" ! -newermt "$TODAY +1 day" -print0)

if [[ ${#FILES[@]} -eq 0 ]]; then
    echo "Tidak ada file yang dimodifikasi hari ini ($TODAY)"
    exit 0
fi

echo "file_name,tanggal_data,wmo_id,station_name,status" > "$OUTPUT_CSV"

# === 4. Loop untuk memproses file-file hari ini ===
for FILE_PATH in "${FILES[@]}"; do
    FILE_NAME=$(basename "$FILE_PATH")
    WMO_ID="-"
    TANGGAL_DATA="-"
    STATION_NAME="-"
    STATUS="Tidak Dikenali"

    # Format: P/T20xxxxx[A-D]YYYYMMDDhhmmGTS.X
    if [[ "$FILE_NAME" =~ ^[PT]20([0-9]{5})([A-D])([0-9]{10})GTS\.X$ ]]; then
        WMO_ID="${BASH_REMATCH[1]}"
        TANGGAL_DATA="${BASH_REMATCH[3]:0:4}-${BASH_REMATCH[3]:4:2}-${BASH_REMATCH[3]:6:2} ${BASH_REMATCH[3]:8:2}:${BASH_REMATCH[3]:10:2}"

    # Format: P/T20xxxxx[A-D]YYYYMMDDhhmm.DAT
    elif [[ "$FILE_NAME" =~ ^[PT]20([0-9]{5})([A-D])([0-9]{10})\.DAT$ ]]; then
        WMO_ID="${BASH_REMATCH[1]}"
        TANGGAL_DATA="${BASH_REMATCH[3]:0:4}-${BASH_REMATCH[3]:4:2}-${BASH_REMATCH[3]:6:2} ${BASH_REMATCH[3]:8:2}:${BASH_REMATCH[3]:10:2}"

    
    # Format: P/T20xxxxx[A-D]YYYYMMDDhhmm.X
    elif [[ "$FILE_NAME" =~ ^[PT]20([0-9]{5})([A-D])([0-9]{10})\.X$ ]]; then
        WMO_ID="${BASH_REMATCH[1]}"
        TANGGAL_DATA="${BASH_REMATCH[3]:0:4}-${BASH_REMATCH[3]:4:2}-${BASH_REMATCH[3]:6:2} ${BASH_REMATCH[3]:8:2}:${BASH_REMATCH[3]:10:2}"

    # Format: P/T20xxxxx[A-D]YYYYMMDDhhmm.X (versi lama)
    elif [[ "$FILE_NAME" =~ ^[PT]20([0-9]{5})([A-D])([0-9]{8})\.X$ ]]; then
        WMO_ID="${BASH_REMATCH[1]}"
        part="${BASH_REMATCH[3]}"
        TANGGAL_DATA="20${part:4:2}-${part:2:2}-${part:0:2} ${part:6:2}:00"

    # Format: P2096509D2025041500.X
    elif [[ "$FILE_NAME" =~ ^P([0-9]{7})([A-D])([0-9]{12})\.X$ ]]; then
        WMO_ID="${BASH_REMATCH[1]:2}"
        TANGGAL_DATA="${BASH_REMATCH[2]:0:4}-${BASH_REMATCH[2]:4:2}-${BASH_REMATCH[2]:6:2} ${BASH_REMATCH[2]:8:2}:${BASH_REMATCH[2]:10:2}"

    # Format: T2096805B2025041500.X
    elif [[ "$FILE_NAME" =~ ^T([0-9]{7})([A-D])([0-9]{12})\.X$ ]]; then
        WMO_ID="${BASH_REMATCH[1]:2}"
        TANGGAL_DATA="${BASH_REMATCH[2]:0:4}-${BASH_REMATCH[2]:4:2}-${BASH_REMATCH[2]:6:2} ${BASH_REMATCH[2]:8:2}:${BASH_REMATCH[2]:10:2}"

    # Format: P2096805D2025041500GTS.X
    elif [[ "$FILE_NAME" =~ ^P([0-9]{7})([A-D])([0-9]{12})GTS\.X$ ]]; then
        WMO_ID="${BASH_REMATCH[1]}"
        TANGGAL_DATA="${BASH_REMATCH[3]:0:4}-${BASH_REMATCH[3]:4:2}-${BASH_REMATCH[3]:6:2} ${BASH_REMATCH[3]:8:2}:${BASH_REMATCH[3]:10:2}"

    # Format: T2096805C2025041500GTS.X
    elif [[ "$FILE_NAME" =~ ^T([0-9]{7})([A-D])([0-9]{12})GTS\.X$ ]]; then
        WMO_ID="${BASH_REMATCH[1]}"
        TANGGAL_DATA="${BASH_REMATCH[3]:0:4}-${BASH_REMATCH[3]:4:2}-${BASH_REMATCH[3]:6:2} ${BASH_REMATCH[3]:8:2}:${BASH_REMATCH[3]:10:2}"

    # Format: Dxxxxx_YYYYMMDDHH.(BIN|bfh|bfr|bin)
    elif [[ "$FILE_NAME" =~ ^D([0-9]{5})_([0-9]{10})(.*\.(BIN|bfh|bfr|bin))$ ]]; then
        WMO_ID="${BASH_REMATCH[1]}"
        TANGGAL_DATA="${BASH_REMATCH[2]:0:4}-${BASH_REMATCH[2]:4:2}-${BASH_REMATCH[2]:6:2} ${BASH_REMATCH[2]:8:2}:00"

    # Format: Dxxxxx_YYYYMMDDhh.X
    elif [[ "$FILE_NAME" =~ ^D([0-9]{5})_([0-9]{10})\.X$ ]]; then
        WMO_ID="${BASH_REMATCH[1]}"
        TANGGAL_DATA="${BASH_REMATCH[2]:0:4}-${BASH_REMATCH[2]:4:2}-${BASH_REMATCH[2]:6:2} ${BASH_REMATCH[2]:8:2}:00"

    # Format: A_IUSG01WIMM170000_C_WIXX_20250417005451.BIN
    elif [[ "$FILE_NAME" =~ ^A_IUSG01([A-Z0-9]{4})[0-9]{6}_C_[A-Z0-9]{4}_([0-9]{14})\.BIN$ ]]; then
        ICAO="${BASH_REMATCH[1]}"
        DATETIME="${BASH_REMATCH[2]}"
        TANGGAL_DATA="${DATETIME:0:4}-${DATETIME:4:2}-${DATETIME:6:2} ${DATETIME:8:2}:${DATETIME:10:2}"
        
        # Cari WMO_ID berdasarkan ICAO
        for key in "${!STATIONS[@]}"; do
            VALUE="${STATIONS[$key]}"
            ICAO_FROM_METADATA="${VALUE%%_*}"  # ambil bagian sebelum _
            if [[ "$ICAO_FROM_METADATA" == "$ICAO" ]]; then
                WMO_ID="$key"
                STATION_NAME="$VALUE"
                STATUS="Dikenali"
                break
            fi
        done

        if [[ "$STATUS" != "Dikenali" ]]; then
            echo "File $FILE_NAME => Format dikenali tapi ICAO $ICAO tidak ditemukan di metadata"
            echo "$FILE_NAME,-,-,-,Format dikenali tapi ICAO $ICAO tidak ditemukan" >> "$OUTPUT_CSV"
            continue
        fi

    # Format: A_IUSG01WIMM1700_C_WIXX_202504170000.bin
    elif [[ "$FILE_NAME" =~ ^A_IUSG[0-9]{2}([A-Z0-9]{4})[0-9]{4}_C_([A-Z0-9]{4})([0-9]{10})\.bin$ ]]; then
        ICAO="${BASH_REMATCH[1]}"
        DATETIME="${BASH_REMATCH[3]}"
        TANGGAL_DATA="${DATETIME:0:4}-${DATETIME:4:2}-${DATETIME:6:2} ${DATETIME:8:2}:${DATETIME:10:2}"
        
        # Cari WMO_ID berdasarkan ICAO
        for key in "${!STATIONS[@]}"; do
            VALUE="${STATIONS[$key]}"
            ICAO_FROM_METADATA="${VALUE%%_*}"  # ambil bagian sebelum _
            if [[ "$ICAO_FROM_METADATA" == "$ICAO" ]]; then
                WMO_ID="$key"
                STATION_NAME="$VALUE"
                STATUS="Dikenali"
                break
            fi
        done

        if [[ "$STATUS" != "Dikenali" ]]; then
            echo "File $FILE_NAME => Format dikenali tapi ICAO $ICAO tidak ditemukan di metadata"
            echo "$FILE_NAME,-,-,-,Format dikenali tapi ICAO $ICAO tidak ditemukan" >> "$OUTPUT_CSV"
            continue
        fi    
    # Format bfr pertama: A_IUKG51WION1700_C_WION2025170000.bfr
        elif [[ "$FILE_NAME" =~ ^A_IUKG[0-9]{2}([A-Z0-9]{4})[0-9]{4}_C_([A-Z0-9]{4})([0-9]{10})\.bfr$ ]]; then
        ICAO="${BASH_REMATCH[1]}"
        DATETIME="${BASH_REMATCH[3]}"
        TANGGAL_DATA="${DATETIME:0:4}-${DATETIME:4:2}-${DATETIME:6:2} ${DATETIME:8:2}:${DATETIME:10:2}"
        
        # Cari WMO_ID berdasarkan ICAO
        for key in "${!STATIONS[@]}"; do
            VALUE="${STATIONS[$key]}"
            ICAO_FROM_METADATA="${VALUE%%_*}"  # ambil bagian sebelum _
            if [[ "$ICAO_FROM_METADATA" == "$ICAO" ]]; then
                WMO_ID="$key"
                STATION_NAME="$VALUE"
                STATUS="Dikenali"
                break
            fi
        done

        if [[ "$STATUS" != "Dikenali" ]]; then
            echo "File $FILE_NAME => Format dikenali tapi ICAO $ICAO tidak ditemukan di metadata"
            echo "$FILE_NAME,-,-,-,Format dikenali tapi ICAO $ICAO tidak ditemukan" >> "$OUTPUT_CSV"
            continue
        fi    
    # Format bfr kedua: A_IUKG51WION1700_C_WION2025170000.bfr
        elif [[ "$FILE_NAME" =~ ^A_IUKG[0-9]{2}([A-Z0-9]{4})[0-9]{4}_C_([A-Z0-9]{4})([0-9]{12})\.bfr$ ]]; then
        ICAO="${BASH_REMATCH[1]}"
        DATETIME="${BASH_REMATCH[3]}"
        TANGGAL_DATA="${DATETIME:0:4}-${DATETIME:4:2}-${DATETIME:6:2} ${DATETIME:8:2}:${DATETIME:10:2}"
        
        # Cari WMO_ID berdasarkan ICAO
        for key in "${!STATIONS[@]}"; do
            VALUE="${STATIONS[$key]}"
            ICAO_FROM_METADATA="${VALUE%%_*}"  # ambil bagian sebelum _
            if [[ "$ICAO_FROM_METADATA" == "$ICAO" ]]; then
                WMO_ID="$key"
                STATION_NAME="$VALUE"
                STATUS="Dikenali"
                break
            fi
        done

        if [[ "$STATUS" != "Dikenali" ]]; then
            echo "File $FILE_NAME => Format dikenali tapi ICAO $ICAO tidak ditemukan di metadata"
            echo "$FILE_NAME,-,-,-,Format dikenali tapi ICAO $ICAO tidak ditemukan" >> "$OUTPUT_CSV"
            continue
        fi 

    # Format pertama dan kedua disatukan
    elif [[ "$FILE_NAME" =~ ^A_IUKG[0-9]{2}([A-Z0-9]{4})[0-9]{4}_C_([A-Z0-9]{4})([0-9]{10,12})\.bfr$ ]]; then
    ICAO="${BASH_REMATCH[1]}"
    DATETIME="${BASH_REMATCH[3]}"
    TANGGAL_DATA="${DATETIME:0:4}-${DATETIME:4:2}-${DATETIME:6:2} ${DATETIME:8:2}:${DATETIME:10:2}"

    echo "Mencocokkan ICAO: $ICAO dengan metadata..."

    # Cari WMO_ID berdasarkan ICAO
    for key in "${!STATIONS[@]}"; do
        VALUE="${STATIONS[$key]}"
        ICAO_FROM_METADATA="${VALUE%%_*}"  # ambil bagian sebelum _
        
        echo "Mencocokkan ICAO $ICAO dari file dengan ICAO $ICAO_FROM_METADATA dari metadata..."

        if [[ "$ICAO_FROM_METADATA" == "$ICAO" ]]; then
            WMO_ID="$key"
            STATION_NAME="$VALUE"
            STATUS="Dikenali"
            break
        fi
    done

    if [[ "$STATUS" != "Dikenali" ]]; then
        echo "File $FILE_NAME => Format dikenali tapi ICAO $ICAO tidak ditemukan di metadata"
        echo "$FILE_NAME,-,-,-,Format dikenali tapi ICAO $ICAO tidak ditemukan" >> "$OUTPUT_CSV"
        continue
    fi

    else
        echo "File $FILE_NAME => Format tidak dikenali"
        echo "$FILE_NAME,-,-,-,Format tidak dikenali" >> "$OUTPUT_CSV"
        continue
    fi

    # Mengecek apakah ada nama stasiun terkait dengan WMO_ID
    if [[ -n "${STATIONS[$WMO_ID]}" ]]; then
        STATION_NAME="${STATIONS[$WMO_ID]}"
        STATUS="Dikenali"
    fi

    # Output ke konsol dan CSV
    echo "File $FILE_NAME => $STATUS: ID $WMO_ID ($STATION_NAME), Tanggal: $TANGGAL_DATA"
    echo "$FILE_NAME,$TANGGAL_DATA,$WMO_ID,$STATION_NAME,$STATUS" >> "$OUTPUT_CSV"
done


