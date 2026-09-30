"""Aynı hastanın iki kartını birleştirir (v6.215).

Kullanım:
    python3 hasta_birlestir.py <yanlış no> <doğru no>          ne olacak -- yalnızca listeler
    python3 hasta_birlestir.py <yanlış no> <doğru no> uygula   birleştirir ("BIRLESTIR" yazmanız istenir)

Kullanıcı (2026-09-29): "... ile ... dosya numaralı hasta aynı. Doğru numara
.... Bu iki hasta kayıtlarını birleştirir misin?" (numaralar buraya yazılmadı).
Aynı hasta iki dosya numarasıyla iki kez kaydedilmişse (Access'te numara
yanlış yazılmış, aktarım ikinci bir kart açmış) `dosya_no_degistir.py`
yetmiyor: o doğru numara kayıtlıysa bilerek duruyor.

Doğru numaralı kart KALIR, yanlış numaralı kart silinir; yanlışın her şeyi
doğrunun olur, tek işlemde:
  1. tedavileri (`cycle.hasta_id`) ve sperm dondurmaları
     (`sperm_dondurma.hasta_id`) -- tedaviye bağlı her şey (örnekler,
     olaylar, tüpler, fotoğraflar, bulgular) onlarla birlikte gidiyor;
  2. fotoğraf ve onam ekinin yolu (`<yanlış>/...` -> `<doğru>/...`) ve
     veritabanı yazıldıktan sonra arşiv klasörünün içindekiler doğrunun
     klasörüne taşınıyor (aynı adlı dosya varsa araç baştan durur);
  3. başka hastaların "eşin dosya no"sunda yanlış numara yazıyorsa doğrusu;
  4. doğru kartta BOŞ olan alanlar (doğum tarihi, eş adı, telefon, ...)
     yanlış karttan doluyor; iki kartta da dolu ve farklıysa doğrununki
     kalıyor, önizleme söylüyor; notlar alt alta birleşiyor. Kartın açılış
     günü ikisinin erkeni (Bakanlık verisinin "yeni hasta" ölçüsü, v6.201);
     biri aktifse kart aktif;
  5. yanlış numara geçiciyse (9000000001…, `cryo_esle.py` açtı) sperm
     tüplerinin `<yanlış>-SP-SSDD` etiketi `<doğru>-SP-SSDD` oluyor
     (`dosya_no_degistir.py`'nin kuralı); gerçek numaralı tüpün etiketine
     dokunulmuyor -- tankta tüpün üstünde yazıyor olabilir;
  6. tedaviler tarih sırasıyla yeniden numaralanıyor (`db.tedavileri_sirala()`);
  7. her değişiklik `degisiklik_log`'a; silinen kartın bütün alanları
     "BIRLESTIRME" satırında duruyor.

Önce veritabanının tamamı `lab_ONCEKI_<zaman>.db` diye kopyalanıyor (yedek
klasörü bu bilgisayarda varsa oraya -- Yedekleme ekranının "geri yükle"
listesinde görünür --, yoksa veri klasörüne). Lab kayıt no (`cycle_no`),
embriyo tüpünün etiketi ve örnek kodu (`specimen.id`) dosya numarasını
içermiyor, değişmiyor. Hastayı KULLANICI söylüyor: araç adların, doğum
tarihlerinin tutup tutmadığını gösteriyor, karar vermiyor. Çıktıda hasta adı
yok.
"""

import json
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path

import db as _db          # veritabanının yeri tek yerde: db.py (tuzak #8)
import dosya_no_degistir as _dnd     # geçici numaralı sperm etiketleri, kullanıcı
import geri_yukle
import goruntuler
import yedek

# Doğru kartta boşsa yanlış karttan doldurulan alanlar (ekrandaki adıyla).
# `notlar` ayrı: ikisinde de varsa alt alta birleşiyor.
ALANLAR = {"dogum_tarihi": "doğum tarihi", "es_adi": "eş adı",
           "es_dogum_tarihi": "eşin doğum tarihi", "telefon": "telefon",
           "es_telefon": "eşin telefonu", "es_dosya_no": "eşin dosya no"}
_ISARET = re.compile(r"\[Access kaydı\s+([^\]#\s]*)#([^\]\s]+)\]")


def _kelimeler(metin) -> frozenset:
    """Adın kelime kümesi (sıra önemsiz), Türkçe büyük harfle."""
    m = str(metin or "").strip().replace("i", "İ").upper()
    return frozenset(k for k in re.split(r"[^\wİIŞĞÜÖÇ]+", m) if k)


def _ad_karsilastir(a, b) -> str:
    ka, kb = _kelimeler(a), _kelimeler(b)
    if not ka or not kb:
        return "biri boş"
    if ka == kb:
        return "aynı"
    ortak = ka & kb
    return "farklı yazılmış" if ortak else "FARKLI"


def _deger_karsilastir(silinecek, kalacak) -> str:
    if _bos(silinecek) and _bos(kalacak):
        return "ikisinde de yok"
    if _bos(kalacak):
        return "yalnızca silinecek kartta"
    if _bos(silinecek):
        return "yalnızca kalacak kartta"
    return "aynı" if str(silinecek).strip() == str(kalacak).strip() else "FARKLI"


def _hasta(b, no):
    return b.execute("SELECT * FROM hasta WHERE lab_id=? AND dosya_no=?",
                     (_db.LAB_ID, no)).fetchone()


def _bos(v) -> bool:
    return v is None or str(v).strip() == ""


def _arsiv(eski, yeni):
    kok = goruntuler.arsiv_klasor()
    return kok / goruntuler.guvenli_ad(eski), kok / goruntuler.guvenli_ad(yeni)


def _yol_tablolari():
    return [t for t in ("goruntu", "sperm_dondurma_dosya", "pgt_sonuc")
            if _db.tablo_var(t)]


def _yol_kolonu(tablo):
    return "rapor_dosya_yolu" if tablo == "pgt_sonuc" else "dosya_yolu"


def _mutlak_yollar(b, eski_k, y_id) -> list:
    """Yanlış kartın fotoğraf / onam kayıtlarından yolu MUTLAK yazılmış olanlar
    (v6.4 öncesi) ve arşivde yanlışın klasörüne düşenler:
    [(tablo, id, yeni göreli yol)]. Göreli yollar önek değişikliğiyle."""
    sonuc = []
    satirlar = [("goruntu", r[0], r[1]) for r in b.execute(
        "SELECT g.id, g.dosya_yolu FROM goruntu g JOIN cycle c ON c.id=g.cycle_id "
        "WHERE c.hasta_id=?", (y_id,))]
    if _db.tablo_var("sperm_dondurma_dosya"):
        satirlar += [("sperm_dondurma_dosya", r[0], r[1]) for r in b.execute(
            "SELECT d.id, d.dosya_yolu FROM sperm_dondurma_dosya d "
            "JOIN sperm_dondurma s ON s.id=d.sperm_dondurma_id WHERE s.hasta_id=?",
            (y_id,))]
    for tablo, rid, yol in satirlar:
        if not yol or not Path(yol).is_absolute():
            continue
        tam = goruntuler.tam_yol(yol)
        try:
            ic = tam.relative_to(eski_k)
        except ValueError:
            continue                         # yanlışın klasöründe değil: dokunma
        sonuc.append((tablo, rid, ic.as_posix()))
    return sonuc


def plan(eski, yeni) -> dict:
    """Ne olacağını hesaplar, hiçbir şey yazmaz. `engel` doluysa uygulanmaz."""
    b = _db.baglan()
    try:
        return _plan(b, eski, yeni)
    finally:
        b.close()


def _plan(b, eski, yeni) -> dict:
    y, d = _hasta(b, eski), _hasta(b, yeni)
    if not y:
        sys.exit(f"Dosya no {eski} kayıtlı değil.")
    if not d:
        sys.exit(f"Dosya no {yeni} kayıtlı değil. Yalnızca numara yanlışsa "
                 f"birleştirme değil numara değişikliği: python3 dosya_no_degistir.py "
                 f"{eski} {yeni}")
    p = {"y": y, "d": d, "engel": [], "uyari": []}
    say = lambda sql, *a: b.execute(sql, a).fetchone()[0]
    for k, h in (("y", y), ("d", d)):
        p[k + "_tedavi"] = say("SELECT COUNT(*) FROM cycle WHERE hasta_id=?", h["id"])
        p[k + "_sperm"] = say("SELECT COUNT(*) FROM sperm_dondurma WHERE hasta_id=?", h["id"])
        p[k + "_foto"] = say("SELECT COUNT(*) FROM goruntu g JOIN cycle c ON c.id=g.cycle_id "
                             "WHERE c.hasta_id=?", h["id"])
    # Kart alanları
    p["ad"] = _ad_karsilastir(y["ad_soyad"], d["ad_soyad"])
    p["es"] = _ad_karsilastir(y["es_adi"], d["es_adi"])
    if _kelimeler(y["ad_soyad"]) and _kelimeler(y["ad_soyad"]) == _kelimeler(d["es_adi"]):
        p["uyari"].append("Yanlış kartın adı doğru kartın EŞ adıyla aynı: bu, eşin kendi "
                          "kartı olabilir (sperm dondurma). O zaman birleştirilmez, "
                          "eşin kartında \"Eşine bağla\" kullanılır.")
    kolonlar = [r[1] for r in b.execute("PRAGMA table_info(hasta)")]
    p["doldur"], p["farkli"] = {}, []
    for alan, ad in ALANLAR.items():
        if alan not in kolonlar or _bos(y[alan]):
            continue
        if alan == "es_dosya_no" and y[alan] in (eski, yeni):
            continue                         # kartın kendisini gösterirdi
        if _bos(d[alan]):
            p["doldur"][alan] = y[alan]
        elif str(y[alan]).strip() != str(d[alan]).strip():
            if alan in ("es_adi",) and _kelimeler(y[alan]) == _kelimeler(d[alan]):
                continue
            p["farkli"].append(ad)
    if p["ad"] == "FARKLI":
        p["uyari"].append("Adlar birbirini hiç tutmuyor: gerçekten aynı hasta mı? Kartları "
                          "ekranda karşılaştırın.")
    if "doğum tarihi" in p["farkli"]:
        p["uyari"].append("Doğum tarihleri farklı: gerçekten aynı hasta mı? Kartları "
                          "ekranda karşılaştırın.")
    p["notlar"] = None
    if "notlar" in kolonlar and not _bos(y["notlar"]):
        yn, dn = str(y["notlar"]).strip(), str(d["notlar"] or "").strip()
        if not dn:
            p["notlar"] = yn
        elif yn not in dn:
            p["notlar"] = f"{dn}\n({eski} kartından) {yn}"
    p["durum"] = "aktif" if "aktif" in (y["durum"], d["durum"]) else d["durum"]
    p["acilis"] = min(y["olusturma_zamani"], d["olusturma_zamani"])
    # Eş numarası olarak yanlış numarayı taşıyan kartlar (kendisi hariç)
    p["esler"] = [r[0] for r in b.execute(
        "SELECT id FROM hasta WHERE lab_id=? AND es_dosya_no=? AND id NOT IN (?, ?)",
        (_db.LAB_ID, eski, y["id"], d["id"]))] if "es_dosya_no" in kolonlar else []
    p["es_kendisi"] = "es_dosya_no" in kolonlar and d["es_dosya_no"] in (eski, yeni)
    if p["es_kendisi"]:
        p["uyari"].append("Doğru kartın \"eşin dosya no\"su bu iki numaradan biri: "
                          "birleşince kartın kendisini gösterirdi, boşaltılıyor.")
    # Sperm tüpü etiketleri (yalnızca geçici numarada, dosya_no_degistir'in kuralı)
    p["etiketler"] = _dnd._sperm_etiketleri(b, y["id"], eski, yeni)
    cakisan = [e for _t, _e, e in p["etiketler"] if b.execute(
        "SELECT 1 FROM tasiyici WHERE lab_id=? AND etiket=?", (_db.LAB_ID, e)).fetchone()]
    if cakisan:
        p["engel"].append("Tüp etiketi zaten var: " + ", ".join(cakisan))
    # Fotoğraf yolları ve arşiv
    eski_k, yeni_k = _arsiv(eski, yeni)
    p["arsiv"] = (eski_k, yeni_k)
    p["yollar"] = {t: b.execute(f"SELECT COUNT(*) FROM {t} WHERE lab_id=? AND "
                                f"{_yol_kolonu(t)} LIKE ?", (_db.LAB_ID, f"{eski}/%")
                                ).fetchone()[0] for t in _yol_tablolari()}
    p["mutlak"] = _mutlak_yollar(b, eski_k, y["id"])
    p["dosyalar"] = ([x for x in eski_k.rglob("*") if x.is_file()]
                     if eski_k.is_dir() else [])
    cakisan = [x for x in p["dosyalar"] if (yeni_k / x.relative_to(eski_k)).exists()]
    if cakisan:
        p["engel"].append(f"Arşivde aynı adlı {len(cakisan)} dosya iki kartın klasöründe "
                          f"de var (ilki: {cakisan[0].relative_to(eski_k)}) -- fotoğraflar "
                          "karışırdı, elle bakın.")
    # Aynı gün, aynı tipte iki tedavi: aynı tedavi iki kez girilmiş olabilir.
    gun = _db.tedavi_tarihi(b, "c")
    tedaviler = {k: b.execute(f"SELECT c.id, c.cycle_no, c.cycle_tipi, substr({gun},1,10) g "
                              "FROM cycle c WHERE c.hasta_id=?", (h["id"],)).fetchall()
                 for k, h in (("y", y), ("d", d))}
    p["ayni_gun"] = [(a["cycle_no"], c["cycle_no"], a["g"]) for a in tedaviler["y"]
                     for c in tedaviler["d"]
                     if a["g"] and a["g"] == c["g"] and a["cycle_tipi"] == c["cycle_tipi"]]
    # Access'ten gelen kayıtlar: aynı CSV yeniden aktarılırsa yanlış numara
    # "başka hastanın tedavisi" diye çakışır (`aktar_access._carpismalar()`).
    p["access"] = []
    for (notu,) in b.execute("SELECT protokol_notu FROM cycle WHERE hasta_id=?", (y["id"],)):
        for kaynak, kayit in _ISARET.findall((notu or "").replace("\n", " ")):
            p["access"].append((kaynak, kayit))
    # Birleşince yapılabilecekler
    fet = ",".join("?" * len(_db.FET_TIPLERI))
    p["bagsiz_fet"] = b.execute(
        "SELECT COUNT(DISTINCT c.id) FROM cycle c JOIN olay o ON o.thaw_cycle_id=c.id "
        "AND o.tip='thaw' AND o.iptal_mi=0 JOIN specimen s ON s.id=o.specimen_id "
        f"AND s.cycle_id=c.id WHERE c.hasta_id IN (?, ?) AND c.cycle_tipi IN ({fet}) "
        "AND c.protokol_notu LIKE '%[Access kayd%'",
        (y["id"], d["id"], *_db.FET_TIPLERI)).fetchone()[0]
    p["konumsuz"] = b.execute(
        "SELECT COUNT(DISTINCT t.id) FROM tasiyici t JOIN olay o ON o.vit_tasiyici_id=t.id "
        "JOIN specimen s ON s.id=o.specimen_id JOIN cycle c ON c.id=s.cycle_id "
        "WHERE c.hasta_id IN (?, ?) AND o.tip='vitrifikasyon' AND o.iptal_mi=0 "
        "AND t.durum='dolu' AND t.kategori='embriyo' AND t.konum_id IS NULL",
        (y["id"], d["id"])).fetchone()[0]
    return p


def ozet_yaz(eski, yeni, p):
    y, d = p["y"], p["d"]
    print(f"Kalacak kart   : dosya no {yeni} -- {p['d_tedavi']} tedavi, "
          f"{p['d_sperm']} sperm dondurma, {p['d_foto']} fotoğraf")
    print(f"Silinecek kart : dosya no {eski} -- {p['y_tedavi']} tedavi, "
          f"{p['y_sperm']} sperm dondurma, {p['y_foto']} fotoğraf")
    print(f"Ad: {p['ad']} · eş adı: {p['es']} · doğum tarihi: "
          f"{_deger_karsilastir(y['dogum_tarihi'], d['dogum_tarihi'])}")
    for u in p["uyari"]:
        print(f"DİKKAT: {u}")
    if p["doldur"]:
        print("Kalacak kartta boş, silinecekten yazılacak: "
              + ", ".join(ALANLAR[a] for a in p["doldur"]))
    if p["farkli"]:
        print("İki kartta da dolu ve farklı (kalacak kartınki kalıyor, silinecek kartınki "
              "değişiklik geçmişinde): " + ", ".join(p["farkli"]))
    if p["notlar"]:
        print("Notlar: silinecek kartın notu kalacak kartın notuna eklenecek.")
    if p["durum"] != d["durum"]:
        print(f"Kart durumu: {d['durum']} -> {p['durum']} (silinecek kart aktif).")
    yol = sum(p["yollar"].values()) + len(p["mutlak"])
    print(f"Taşınacak: {p['y_tedavi']} tedavi, {p['y_sperm']} sperm dondurma, "
          f"{yol} fotoğraf/ek yolu, arşivde {len(p['dosyalar'])} dosya "
          f"({p['arsiv'][0]} -> {p['arsiv'][1]})")
    if p["etiketler"]:
        print(f"Sperm tüpü etiketi (geçici numara): {len(p['etiketler'])} tüp "
              f"{eski}-SP-... -> {yeni}-SP-...")
    if p["esler"]:
        print(f"\"Eşin dosya no\"su {eski} olan {len(p['esler'])} kart -> {yeni}")
    for yno, dno, g in p["ayni_gun"]:
        print(f"DİKKAT: aynı gün ({g}) aynı tipte iki tedavi: {yno} (silinecek kart) ve "
              f"{dno} (kalacak kart). Aynı tedavi iki kez girilmiş olabilir -- birleştirme "
              "ikisini de korur; fazlası varsa tedavi ekranından silinir.")
    for e in p["engel"]:
        print(f"ENGEL: {e}")


def _logla(b, tablo, kayit, alan, eski, yeni, kid, simdi):
    b.execute("INSERT INTO degisiklik_log (lab_id, tablo_adi, kayit_id, alan, "
              "eski_deger, yeni_deger, kullanici_id, zaman) VALUES (?,?,?,?,?,?,?,?)",
              (_db.LAB_ID, tablo, str(kayit), alan,
               None if eski is None else str(eski), None if yeni is None else str(yeni),
               kid, simdi))


def onceki_kopya() -> Path:
    """Birleştirmeden önce veritabanının tamamı (SQLite yedek API'si,
    doğrulanmış). Yedek klasörü bu bilgisayarda varsa oraya: Yedekleme
    ekranının "geri yükle" listesi `lab_ONCEKI_*`'yı da gösteriyor
    (`geri_yukle.yedekleri_listele()`); yoksa veri klasörüne (`tasi.py`'nin
    yeri). Günlük temizlik bu adı silmiyor (`yedek.eskileri_temizle()`)."""
    hedef = _db.ayar("yedek_klasor", "")
    klasor = (Path(hedef) if hedef and yedek.bu_makineye_uygun_mu(hedef)
              and Path(hedef).is_dir() else _db.VERI_KOK)
    yol = klasor / f"lab_ONCEKI_{datetime.now():%Y%m%d_%H%M%S}.db"
    geri_yukle._tutarli_kopya(_db.DB_YOLU, yol)
    return yol


def uygula(eski, yeni) -> dict:
    kid = _dnd._kullanici_id()
    simdi = datetime.now().isoformat(" ", "seconds")
    with _db.yazma_islemi() as b:
        p = _plan(b, eski, yeni)             # kilidin içinde yeniden
        if p["engel"]:
            sys.exit("Birleştirilmedi: " + "; ".join(p["engel"]))
        y, d = p["y"], p["d"]
        tedaviler = [r[0] for r in b.execute("SELECT id FROM cycle WHERE hasta_id=?",
                                             (y["id"],))]
        spermler = [r[0] for r in b.execute(
            "SELECT id FROM sperm_dondurma WHERE hasta_id=?", (y["id"],))]
        b.execute("UPDATE cycle SET hasta_id=? WHERE hasta_id=?", (d["id"], y["id"]))
        b.execute("UPDATE sperm_dondurma SET hasta_id=? WHERE hasta_id=?", (d["id"], y["id"]))
        for cid in tedaviler:
            _logla(b, "cycle", cid, "hasta_id", y["id"], d["id"], kid, simdi)
        for sid in spermler:
            _logla(b, "sperm_dondurma", sid, "hasta_id", y["id"], d["id"], kid, simdi)
        for tablo in _yol_tablolari():
            k = _yol_kolonu(tablo)
            b.execute(f"UPDATE {tablo} SET {k} = ? || substr({k}, ?) "
                      f"WHERE lab_id=? AND {k} LIKE ?",
                      (f"{yeni}/", len(f"{eski}/") + 1, _db.LAB_ID, f"{eski}/%"))
        yeni_ad = goruntuler.guvenli_ad(yeni)
        for tablo, rid, ic in p["mutlak"]:
            b.execute(f"UPDATE {tablo} SET dosya_yolu=? WHERE id=?", (f"{yeni_ad}/{ic}", rid))
        for eid in p["esler"]:
            b.execute("UPDATE hasta SET es_dosya_no=? WHERE id=?", (yeni, eid))
            _logla(b, "hasta", eid, "es_dosya_no", eski, yeni, kid, simdi)
        for tid, e, yeni_etiket in p["etiketler"]:
            b.execute("UPDATE tasiyici SET etiket=? WHERE id=?", (yeni_etiket, tid))
            _logla(b, "tasiyici", tid, "etiket", e, yeni_etiket, kid, simdi)
        # Silinen kartın bütün alanları günlükte (denetim izi): farklı olduğu
        # için kalmayan telefon, doğum tarihi burada okunabilir.
        _logla(b, "hasta", y["id"], "BIRLESTIRME",
               json.dumps({k: y[k] for k in y.keys()}, ensure_ascii=False),
               f"dosya {yeni} kartına birleştirildi", kid, simdi)
        b.execute("DELETE FROM hasta WHERE id=?", (y["id"],))
        guncel = dict(p["doldur"])
        if p["notlar"]:
            guncel["notlar"] = p["notlar"]
        if p["durum"] != d["durum"]:
            guncel["durum"] = p["durum"]
        if p["acilis"] != d["olusturma_zamani"]:
            guncel["olusturma_zamani"] = p["acilis"]
        if p["es_kendisi"] and "es_dosya_no" not in guncel:
            guncel["es_dosya_no"] = None
        for alan, deger in guncel.items():
            b.execute(f"UPDATE hasta SET {alan}=? WHERE id=?", (deger, d["id"]))
            _logla(b, "hasta", d["id"], alan, d[alan], deger, kid, simdi)
        degisen = _db.tedavileri_sirala(b, d["id"])
        for cid, _no, e, yn in degisen:
            _logla(b, "cycle", cid, "hasta_cycle_no", e, yn, kid, simdi)
    hatalar = _arsivi_tasi(*p["arsiv"])
    p["hatalar"] = hatalar
    p["sira"] = degisen
    return p


def _klasor_birlestir(kaynak: Path, hedef: Path, hatalar: list):
    """`kaynak`'ın içindekileri `hedef`'e taşır; ikisinde de olan klasörün
    içine iner. Aynı adlı dosyanın üzerine yazmaz (plan onu baştan
    yakalıyor; arada biri eklediyse hata listesine)."""
    hedef.mkdir(parents=True, exist_ok=True)
    for oge in sorted(kaynak.iterdir()):
        h = hedef / oge.name
        if oge.is_dir() and h.is_dir():
            _klasor_birlestir(oge, h, hatalar)
            continue
        if h.exists():
            hatalar.append(f"{oge}: {h} zaten var")
            continue
        try:
            shutil.move(str(oge), str(h))
        except OSError as e:
            hatalar.append(f"{oge}: {e}")
    try:
        kaynak.rmdir()                       # boş kaldıysa
    except OSError:
        pass


def _arsivi_tasi(eski_k: Path, yeni_k: Path) -> list:
    if not eski_k.is_dir():
        return []
    hatalar = []
    try:
        if not yeni_k.exists():
            shutil.move(str(eski_k), str(yeni_k))
        else:
            _klasor_birlestir(eski_k, yeni_k, hatalar)
    except OSError as e:
        hatalar.append(f"{eski_k}: {e}")
    return hatalar


def sonraki_adimlar(eski, yeni, p):
    if p["access"]:
        print("\nAccess'ten gelen kayıtlar: aynı CSV yeniden aktarılırsa yanlış numara "
              "\"başka hastanın tedavisi\" diye çakışır. O dosyayı yeniden aktaracaksanız "
              "düzeltme dosyanıza (duzelt=...) şu satırlar:")
        for kaynak, kayit in p["access"]:
            if kaynak:
                print(f"    {kaynak}#{kayit}  DOSYA  {eski}  {yeni}")
            else:
                print(f"    (#{kayit}: etiketsiz ağustos 2026 kaydı -- düzeltme satırı "
                      "yazılamıyor, o dosyayı yeniden aktarmayın)")
    if p["bagsiz_fet"]:
        print(f"\nBu hastanın {p['bagsiz_fet']} aktarılmış FET'i kaynak tüpüne bağlı değil; "
              "tüp öteki kartta olabilir. Bağlamayı yeniden denemek için:\n"
              "    python3 aktar_access.py bagla")
    if p["konumsuz"]:
        print(f"\nBu hastanın {p['konumsuz']} tüpünün konumu girilmemiş (Cryo Haritası'nda "
              "görünmüyor, v6.233): Cryo Haritası -> Haritadan yer tamamla, ya da tüpün "
              "sayfasında karar (yeri, taşındı, imha).")


def main():
    args = [a for a in sys.argv[1:] if a]
    if len(args) not in (2, 3) or not all(a.isdigit() for a in args[:2]) \
            or (len(args) == 3 and args[2] != "uygula"):
        sys.exit(__doc__)
    eski, yeni = int(args[0]), int(args[1])
    if eski == yeni:
        sys.exit("İki numara aynı.")
    p = plan(eski, yeni)
    ozet_yaz(eski, yeni, p)
    if p["engel"]:
        sys.exit("\nBirleştirilemez: önce ENGEL satırlarına bakın.")
    if len(args) == 2:
        print(f"\nHiçbir şey yazılmadı. Birleştirmek için:\n"
              f"    python3 hasta_birlestir.py {eski} {yeni} uygula")
        return
    print(f"\nDosya no {eski} kartı SİLİNECEK, her şeyi {yeni} kartına geçecek.")
    if input('Birleştirmek için "BIRLESTIR" yazın: ').strip() != "BIRLESTIR":
        sys.exit("Vazgeçildi.")
    kopya = onceki_kopya()
    print(f"Önceki hal kopyalandı: {kopya}")
    p = uygula(eski, yeni)
    print(f"\nBirleştirildi: dosya no {yeni} -- {p['y_tedavi'] + p['d_tedavi']} tedavi, "
          f"{p['y_sperm'] + p['d_sperm']} sperm dondurma.")
    if p["sira"]:
        print("Tedavi sırası (tarih sırasıyla): "
              + ", ".join(f"{no} {e}.→{yn}." for _c, no, e, yn in p["sira"]))
    if p["dosyalar"] and not p["hatalar"]:
        print(f"Arşiv: {len(p['dosyalar'])} dosya {p['arsiv'][1]} klasörüne taşındı.")
    for h in p["hatalar"]:
        print(f"UYARI: arşivde taşınamadı -- {h}. Veritabanı yeni yolu gösteriyor; "
              "dosyayı elle taşıyın, yoksa fotoğraf görünmez.")
    sonraki_adimlar(eski, yeni, p)
    print("\nProgram açıksa sayfayı yenileyin; kapatıp açmaya gerek yok.")


if __name__ == "__main__":
    main()
