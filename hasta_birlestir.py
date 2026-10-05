"""Aynı hastanın iki kartını birleştirir (v6.215, toplu kip v6.234).

Kullanım:
    python3 hasta_birlestir.py <yanlış no> <doğru no>          ne olacak -- yalnızca listeler
    python3 hasta_birlestir.py <yanlış no> <doğru no> uygula   birleştirir ("BIRLESTIR" yazmanız istenir)
    python3 hasta_birlestir.py benzer          aynı ad + eş adı, numarası 1-2 hane farklı kartlar -- listeler
    python3 hasta_birlestir.py benzer uygula   listedekileri birleştirir ("BIRLESTIR")
    ... benzer [uygula] atla=<no>,<no>         o numaraların grupları birleştirilmez

Toplu kip (v6.234, kullanıcı: "İsim soyad ve eş adı eşleşen ama dosya
numaralarında bir kaç yanlış veya eksik olan hastaları birleştir"): Access'ten
gelen kayıtlarda numara eksik ya da yanlış yazılmış, aynı hastanın iki kartı
var. Aday: adı ve eşinin adı aynı (kelime kümesi, sıra önemsiz; eş adı iki
kartta da dolu), numaraları en çok 2 hane farklı (eksik, fazla, yanlış ya da
yer değiştirmiş hane). Hangi numara kalır -- üç işaret, ikisi ya da üçü
birbirini tutmalı, hiçbiri yoksa ya da çelişiyorsa birleştirilmez, iki yönün
komutu yazılır (hastane sisteminden bakıp kullanıcı seçer):
  - programa EKRANDAN girilmiş kayıt (Access'ten ya da Cryo Excel'inden
    değil) yalnızca bir kartta: onun numarası;
  - kayıt (tedavi + sperm dondurma) sayısı: çok olan -- yanlış numara bir kez
    yazılmış;
  - numaranın biçimi (hane sayısı, ilk iki hane) programdaki numaraların
    çoğuna uyan (en az 3 kat yaygın): "10" ile başlayan 9 haneli numaralar
    arasında 10 hanelisi fazla, 8 hanelisi eksik yazılmış.
Birleştirme tek çiftin yolundan (aşağıdaki 1-7, her çift kendi işleminde,
önce bir kez `lab_ONCEKI_*.db`). Sonra birleşen hastaların aktarılmış FET'leri
tüpüne (`aktar_access.butun_fetleri_bagla()`) ve Cryo Haritası'ndaki Excel
kayıtları tüpüne (`cryo_esle.excel_kayitlarini_bagla()`) bağlanmayı yeniden
dener: iki kartta ayrı duran dondurma ile çözme artık aynı hastada. Eş adı
farklı ya da boş olanlar ve numarası çok farklı olanlar yalnızca listelenir.
Ekranda ad yok, `hasta_birlestir_rapor.txt` adlarla (depoya girmez).

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

import collections
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


class Birlestirilemez(Exception):
    """Birleştirme yapılamıyor (kart yok, ENGEL): tek çift çıkar, toplu kip
    o çifti atlayıp sonrakine geçer."""


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
        raise Birlestirilemez(f"Dosya no {eski} kayıtlı değil.")
    if not d:
        raise Birlestirilemez(
            f"Dosya no {yeni} kayıtlı değil. Yalnızca numara yanlışsa "
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
    doğrulanmış). Yeri bütün güvenlik kopyaları için tek yerden
    (`yedek.guvenlik_kopyasi_yolu()`, v6.248): yedek klasörü bu bilgisayarda
    varsa `veritabani/` -- Yedekleme ekranının "geri yükle" listesi
    `lab_ONCEKI_*`'yı da gösteriyor --, yoksa veri klasörü. Günlük temizlik
    bu adı silmiyor (`yedek.eskileri_temizle()`)."""
    yol = yedek.guvenlik_kopyasi_yolu()
    geri_yukle._tutarli_kopya(_db.DB_YOLU, yol)
    return yol


def uygula(eski, yeni) -> dict:
    kid = _dnd._kullanici_id()
    simdi = datetime.now().isoformat(" ", "seconds")
    with _db.yazma_islemi() as b:
        p = _plan(b, eski, yeni)             # kilidin içinde yeniden
        if p["engel"]:
            raise Birlestirilemez("Birleştirilmedi: " + "; ".join(p["engel"]))
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


# ------------------------------------------------ benzer kartlar (v6.234)
#
# Access'ten gelen kayıtlarda dosya numarası eksik ya da yanlış yazılmış:
# aynı hasta iki kartta. Aday kural kullanıcının: adı ve eşinin adı aynı,
# numaraları birkaç hane farklı. Hangi numaranın kalacağı üç işaretten
# (`_yon()`); işaretler birbirini tutmuyorsa birleştirilmez.

YAKIN_HANE = 2          # "bir kaç hane": en çok iki hane farkı
BICIM_ORAN = 3          # yaygın biçim öbüründen en az 3 kat çok numarada ...
BICIM_EN_AZ = 5         # ... ve en az 5 numarada
RAPOR = Path("hasta_birlestir_rapor.txt")


def hane_farki(a, b) -> int:
    """İki numara kaç hane farklı: eksik, fazla, yanlış ya da bitişik yer
    değiştirmiş hane birer fark (Damerau-Levenshtein, bitişik yer
    değiştirme). "123456789" / "12356789" -> 1, "123456789" / "124356789" -> 1."""
    a, b = str(a), str(b)
    onceki2, onceki = None, list(range(len(b) + 1))
    for i in range(1, len(a) + 1):
        simdi = [i] + [0] * len(b)
        for j in range(1, len(b) + 1):
            simdi[j] = min(onceki[j] + 1, simdi[j - 1] + 1,
                           onceki[j - 1] + (a[i - 1] != b[j - 1]))
            if (i > 1 and j > 1 and a[i - 1] == b[j - 2] and a[i - 2] == b[j - 1]):
                simdi[j] = min(simdi[j], onceki2[j - 2] + 1)
        onceki2, onceki = onceki, simdi
    return onceki[len(b)]


def _fark_turu(a, b) -> str:
    """Farkın ekrandaki adı: "1 hane eksik" / "1 hane fazla" / "1 hane farklı"
    / "iki hane yer değiştirmiş" (kalacak numaraya göre, `a` silinecek)."""
    a, b = str(a), str(b)
    if len(a) == len(b):
        farkli = [i for i in range(len(a)) if a[i] != b[i]]
        if (len(farkli) == 2 and farkli[1] == farkli[0] + 1
                and a[farkli[0]] == b[farkli[1]] and a[farkli[1]] == b[farkli[0]]):
            return "iki hane yer değiştirmiş"
        return f"{len(farkli)} hane farklı"
    k, u = (a, b) if len(a) < len(b) else (b, a)
    it = iter(u)
    alt = all(ch in it for ch in k)
    n = len(u) - len(k)
    if alt:
        return f"{n} hane {'eksik' if len(a) < len(b) else 'fazla'}"
    return f"{n} hane {'kısa' if len(a) < len(b) else 'uzun'}, başka hane de farklı"


def _gecici(no) -> bool:
    """`cryo_esle.py`'nin açtığı geçici numara (9000000001…): yazılmış bir
    numara değil, yakınlığı anlamsız (ardışık verildi)."""
    return int(no) >= _dnd.GECICI_DOSYA_TABANI


def _kart_kayitlari(b) -> dict:
    """Kart başına kayıt sayısı ve ekrandan girilmiş kaydı olup olmadığı.

    Kayıt = tedavi + sperm dondurma; silme ekranından iptal edilen tedavi
    (bitiş sebebi yok, `aktar_access._silinmis()`) ve iptal edilmiş sperm
    dondurma sayılmaz. Ekrandan girilmiş: notunda ne Access işareti ne
    `db.CRYO_EXCEL_ISARETI` var. Hiç kaydı olmayan kart da ekrandan açılmıştır
    (aktarım ve Cryo Excel kartı kaydıyla birlikte açıyor)."""
    k = {}
    for hid, notu, durum, bitis in b.execute(
            "SELECT hasta_id, protokol_notu, durum, bitis_sebebi FROM cycle "
            "WHERE lab_id=?", (_db.LAB_ID,)):
        s = k.setdefault(hid, {"sayi": 0, "ekran": False, "hic": False})
        s["hic"] = True
        if durum == "iptal" and not bitis:
            continue
        s["sayi"] += 1
        n = (notu or "").replace("\n", " ")
        if "[Access kayd" not in n and _db.CRYO_EXCEL_ISARETI not in n:
            s["ekran"] = True
    for hid, notu, iptal in b.execute(
            "SELECT hasta_id, notlar, iptal_mi FROM sperm_dondurma WHERE lab_id=?",
            (_db.LAB_ID,)):
        s = k.setdefault(hid, {"sayi": 0, "ekran": False, "hic": False})
        s["hic"] = True
        if iptal:
            continue
        s["sayi"] += 1
        if _db.CRYO_EXCEL_ISARETI not in (notu or ""):
            s["ekran"] = True
    return k


def _bicim_sayilari(b):
    """Programdaki gerçek numaraların biçimleri: (hane sayısı, ilk iki hane)
    ve yalnızca hane sayısı -> kaç numara. Geçici numaralar dışarıda."""
    sinif, uzunluk = collections.Counter(), collections.Counter()
    for (no,) in b.execute("SELECT dosya_no FROM hasta WHERE lab_id=?", (_db.LAB_ID,)):
        if no is None or _gecici(no):
            continue
        s = str(no)
        sinif[(len(s), s[:2])] += 1
        uzunluk[len(s)] += 1
    return sinif, uzunluk


def _bicim_isareti(uyeler, sinif, uzunluk):
    """Biçimi programdaki numaraların çoğuna uyan kart (-> (hasta id, açıklama))
    ya da None. Önce hane sayısı + ilk iki hane: "10" ile başlayan 9 haneli
    numaralar arasında 10 hanelisi fazla, 8 hanelisi eksik yazılmış. Sınıflar
    küçükse (az numara) yalnızca hane sayısı. Karar için en yaygını ötekilerin
    her birinden en az BICIM_ORAN kat, en az BICIM_EN_AZ numarada olmalı."""
    def dene(anahtar, sayac, ad):
        degerler = {h["id"]: sayac[anahtar(str(h["dosya_no"]))] for h in uyeler}
        if len({anahtar(str(h["dosya_no"])) for h in uyeler}) < 2:
            return None
        sirali = sorted(degerler.items(), key=lambda x: -x[1])
        en, ikinci = sirali[0][1], sirali[1][1]
        if en >= BICIM_EN_AZ and en >= BICIM_ORAN * max(ikinci, 1) and en > ikinci:
            enk = next(h for h in uyeler if h["id"] == sirali[0][0])
            return sirali[0][0], ad(str(enk["dosya_no"]), en, ikinci)
        return None
    return (dene(lambda s: (len(s), s[:2]), sinif,
                 lambda s, en, ik: f"numaranın biçimi ({len(s)} hane, \"{s[:2]}\" ile "
                                   f"başlayan: programda {en} numara, öteki {ik})")
            or dene(len, uzunluk,
                    lambda s, en, ik: f"numaranın biçimi ({len(s)} hane: programda "
                                      f"{en} numara, öteki {ik})"))


def _yon(uyeler, kayitlar, sinif, uzunluk):
    """Hangi kart kalır: (hasta id | None, işaretler {ad: (id, açıklama)},
    None | neden belirsiz). İşaretler birbirini tutmalı."""
    isaret = {}
    ekran = [h for h in uyeler if kayitlar.get(h["id"], {}).get("ekran")
             or not kayitlar.get(h["id"], {}).get("hic")]
    if len(ekran) == 1:
        h = ekran[0]
        isaret["ekran"] = (h["id"], "programa ekrandan girilmiş kayıt bu numarada"
                           if kayitlar.get(h["id"], {}).get("hic")
                           else "kart ekrandan açılmış (kaydı yok)")
    sayilar = sorted(((kayitlar.get(h["id"], {}).get("sayi", 0), h["id"]) for h in uyeler),
                     reverse=True)
    if sayilar[0][0] > sayilar[1][0]:
        isaret["sayi"] = (sayilar[0][1], "daha çok kayıt bu numarada ("
                          + " / ".join(str(s) for s, _ in sayilar) + ")")
    bicim = _bicim_isareti(uyeler, sinif, uzunluk)
    if bicim:
        isaret["bicim"] = bicim
    if not isaret:
        return None, isaret, "kayıt sayısı eşit, numaraların biçimi de ayırmıyor"
    if len({i for i, _a in isaret.values()}) > 1:
        return None, isaret, "işaretler çelişiyor"
    return next(iter(isaret.values()))[0], isaret, None


def benzer_kartlar(b) -> dict:
    """Hiçbir şey yazmaz. -> {"gruplar": [...], "es_farkli": [...],
    "uzak": [...]}

    Grup: adı ve eşinin adı aynı (kelime kümesi; eş adı dolu) kartlar,
    numaraları birbirine en çok YAKIN_HANE farkla zincirleniyor (üç kart
    olabilir). Her grupta `kalacak` (hasta satırı ya da None), `isaret`,
    `belirsiz`. `es_farkli`: adı aynı, numarası yakın ama eşinin adı farklı
    ya da boş olan çiftler -- kullanıcının kuralında değil, yalnızca
    listeleniyor. `uzak`: adı ve eşinin adı aynı ama numarası çok farklı."""
    kartlar = [h for h in b.execute("SELECT * FROM hasta WHERE lab_id=?", (_db.LAB_ID,))
               if h["dosya_no"] is not None and not _gecici(h["dosya_no"])]
    kayitlar = _kart_kayitlari(b)
    sinif, uzunluk = _bicim_sayilari(b)
    adlar = collections.defaultdict(list)
    for h in kartlar:
        if _kelimeler(h["ad_soyad"]):
            adlar[_kelimeler(h["ad_soyad"])].append(h)
    gruplar, es_farkli, uzak = [], [], []
    for liste in adlar.values():
        if len(liste) < 2:
            continue
        esler = collections.defaultdict(list)
        for h in liste:
            esler[_kelimeler(h["es_adi"])].append(h)
        for es, uyeler in esler.items():
            if not es or len(uyeler) < 2:
                continue
            # Numarası yakın olanları zincirle (birleşim-bul)
            ata = {h["id"]: h["id"] for h in uyeler}

            def bul(x):
                while ata[x] != x:
                    ata[x] = ata[ata[x]]
                    x = ata[x]
                return x
            for i, x in enumerate(uyeler):
                for y in uyeler[i + 1:]:
                    if hane_farki(x["dosya_no"], y["dosya_no"]) <= YAKIN_HANE:
                        ata[bul(x["id"])] = bul(y["id"])
            parca = collections.defaultdict(list)
            for h in uyeler:
                parca[bul(h["id"])].append(h)
            for p in parca.values():
                if len(p) < 2:
                    continue
                p.sort(key=lambda h: h["dosya_no"])
                kid, isaret, belirsiz = _yon(p, kayitlar, sinif, uzunluk)
                gruplar.append({"uyeler": p, "isaret": isaret, "belirsiz": belirsiz,
                                "kalacak": next((h for h in p if h["id"] == kid), None),
                                "kayit": {h["id"]: kayitlar.get(h["id"], {}).get("sayi", 0)
                                          for h in p}})
            if len(parca) >= 2:              # numarası uzak kalan kart(lar) var
                uzak.append(sorted(uyeler, key=lambda h: h["dosya_no"]))
        # Adı aynı, numarası yakın, eş adı tutmuyor ya da boş
        for i, x in enumerate(liste):
            for y in liste[i + 1:]:
                ex, ey = _kelimeler(x["es_adi"]), _kelimeler(y["es_adi"])
                if ex == ey and ex:
                    continue
                if hane_farki(x["dosya_no"], y["dosya_no"]) <= YAKIN_HANE:
                    es_farkli.append((x, y, "eş adı iki kartta da yok" if not ex and not ey
                                      else "eş adı bir kartta yok" if not ex or not ey
                                      else "eş adı farklı yazılmış"))
    gruplar.sort(key=lambda g: g["uyeler"][0]["dosya_no"])
    return {"gruplar": gruplar, "es_farkli": es_farkli, "uzak": uzak,
            "kayitlar": kayitlar}


def benzer_plani() -> dict:
    """`benzer_kartlar()` + birleşecek her çiftin `_plan()`'ı (ENGEL,
    uyarılar). Hiçbir şey yazmaz."""
    b = _db.baglan()
    try:
        s = benzer_kartlar(b)
        for g in s["gruplar"]:
            g["planlar"], g["engel"] = [], []
            if not g["kalacak"]:
                continue
            for h in g["uyeler"]:
                if h["id"] == g["kalacak"]["id"]:
                    continue
                try:
                    p = _plan(b, h["dosya_no"], g["kalacak"]["dosya_no"])
                except Birlestirilemez as e:
                    g["engel"].append(str(e))
                    continue
                g["planlar"].append((h, p))
                g["engel"] += p["engel"]
        return s
    finally:
        b.close()


def _kart_ozeti(h, g) -> str:
    return f"{h['dosya_no']} ({g['kayit'][h['id']]} kayıt)"


def benzer_yaz(s):
    """Ekran: adsız (dosya no, sayılar, sebep). Adlarla ayrıntı RAPOR'da."""
    gruplar = s["gruplar"]
    birlesecek = [g for g in gruplar if _birlesir(g)]
    belirsiz = [g for g in gruplar if not g["kalacak"] and not g.get("atlandi")]
    engelli = [g for g in gruplar if g["kalacak"] and g["engel"] and not g.get("atlandi")]
    atlanan = [g for g in gruplar if g.get("atlandi")]
    print(f"Adı ve eşinin adı aynı, dosya numarası en çok {YAKIN_HANE} hane farklı: "
          f"{len(gruplar)} grup ({sum(len(g['uyeler']) for g in gruplar)} kart)")
    print(f"  {len(birlesecek):4}  birleşecek (hangi numaranın kalacağı belli)")
    print(f"  {len(belirsiz):4}  hangi numara doğru belli değil -- birleştirilmedi")
    print(f"  {len(engelli):4}  birleştirilemez (ENGEL)")
    if atlanan:
        print(f"  {len(atlanan):4}  atla= ile dışarıda bırakıldı: " + ", ".join(
            " / ".join(str(h["dosya_no"]) for h in g["uyeler"]) for g in atlanan))
    for no in s.get("atla_yok") or []:
        print(f"  UYARI: atla={no} listedeki hiçbir grupta yok.")
    if birlesecek:
        print("\nBirleşecek (kalacak numara <- silinecek kart):")
    for g in birlesecek:
        k = g["kalacak"]
        silinecek = [h for h in g["uyeler"] if h["id"] != k["id"]]
        print(f"  {_kart_ozeti(k, g)}  <-  " + ", ".join(
            f"{_kart_ozeti(h, g)} [{_fark_turu(h['dosya_no'], k['dosya_no'])}]"
            for h in silinecek))
        print("      sebep: " + "; ".join(a for _i, a in g["isaret"].values()))
        for h, p in g["planlar"]:
            for u in p["uyari"]:
                print(f"      DİKKAT ({h['dosya_no']}): {u}")
            for yno, dno, gun in p["ayni_gun"]:
                print(f"      DİKKAT: aynı gün ({gun}) aynı tipte iki tedavi ({yno} ve {dno}) "
                      "-- aynı tedavi iki kez girilmiş olabilir; birleştirme ikisini de "
                      "korur (tedavi_birlestir.py)")
    if belirsiz:
        print("\nHangi numara doğru belli değil (hastane sisteminden bakın, doğru olanı "
              "seçip çalıştırın):")
    for g in belirsiz:
        print("  " + " / ".join(_kart_ozeti(h, g) for h in g["uyeler"])
              + f" -- {g['belirsiz']}")
        for a, ad in g["isaret"].items():
            print(f"      {ad[1]} -> {next(h['dosya_no'] for h in g['uyeler'] if h['id'] == ad[0])}")
        for dogru in g["uyeler"]:
            obur = [h for h in g["uyeler"] if h["id"] != dogru["id"]]
            print(f"      doğrusu {dogru['dosya_no']} ise: " + "; ".join(
                f"python3 hasta_birlestir.py {h['dosya_no']} {dogru['dosya_no']} uygula"
                for h in obur))
    for g in engelli:
        print("\nENGEL: " + " / ".join(str(h["dosya_no"]) for h in g["uyeler"])
              + ": " + "; ".join(g["engel"]))
    if s["es_farkli"] or s["uzak"]:
        print(f"\nBirleştirilmeyen benzerlikler (kural dışında, yalnızca bilgi -- "
              f"ayrıntı {RAPOR}):")
        print(f"  {len(s['es_farkli']):4}  adı aynı, numarası yakın, eşinin adı farklı ya da yok")
        print(f"  {len(s['uzak']):4}  adı ve eşinin adı aynı, numarası çok farklı")
        print("  Aynı hastaysa: python3 hasta_birlestir.py <yanlış no> <doğru no>")


def benzer_raporu(s):
    """Adlarla ayrıntı (depoya girmez: `.gitignore`)."""
    def kart(h, kayit):
        return (f"{h['dosya_no']} · {h['ad_soyad'] or '-'} / eş: {h['es_adi'] or '-'} · "
                f"doğum {h['dogum_tarihi'] or '-'} · {kayit} kayıt")
    satirlar = [f"Aynı hasta, iki kart (hasta_birlestir.py benzer, v6.234) -- "
                f"{datetime.now():%d.%m.%Y %H:%M}",
                "Hasta adı içerir: bu dosyayı paylaşma, depoya koyma.", ""]
    for baslik, liste in (("BİRLEŞECEK", [g for g in s["gruplar"] if _birlesir(g)]),
                          ("HANGİ NUMARA DOĞRU BELLİ DEĞİL", [g for g in s["gruplar"]
                                                              if not g["kalacak"]]),
                          ("ENGEL", [g for g in s["gruplar"] if g["kalacak"] and g["engel"]]),
                          ("ATLA= İLE DIŞARIDA", [g for g in s["gruplar"]
                                                  if g.get("atlandi")])):
        satirlar.append(f"{baslik} ({len(liste)})")
        for g in liste:
            for h in g["uyeler"]:
                isaret = ("        " if not _birlesir(g) else "kalır   "
                          if h["id"] == g["kalacak"]["id"] else "silinir ")
                satirlar.append(f"  {isaret}{kart(h, g['kayit'][h['id']])}")
            satirlar.append("      " + ("; ".join(a for _i, a in g["isaret"].values())
                                       or "işaret yok") + (f" -- {g['belirsiz']}"
                                                           if g["belirsiz"] else ""))
            for e in g.get("engel") or []:
                satirlar.append(f"      ENGEL: {e}")
        satirlar.append("")
    kayit = lambda h: s["kayitlar"].get(h["id"], {}).get("sayi", 0)
    satirlar.append(f"ADI AYNI, NUMARASI YAKIN, EŞİNİN ADI FARKLI YA DA YOK "
                    f"({len(s['es_farkli'])}) -- birleştirilmedi")
    for x, y, neden in s["es_farkli"]:
        satirlar += [f"  {kart(x, kayit(x))}", f"  {kart(y, kayit(y))}", f"      {neden}"]
    satirlar.append("")
    satirlar.append(f"ADI VE EŞİNİN ADI AYNI, NUMARASI ÇOK FARKLI ({len(s['uzak'])}) -- "
                    "birleştirilmedi")
    for uyeler in s["uzak"]:
        satirlar += [f"  {kart(h, kayit(h))}" for h in uyeler] + [""]
    RAPOR.write_text("\n".join(satirlar) + "\n", encoding="utf-8")


def benzerleri_birlestir(s) -> dict:
    """Listedeki (kalacağı belli, ENGEL'siz) grupları birleştirir: her çift
    kendi işleminde, `uygula()` (kilidin içinde yeniden plan). -> sonuç."""
    sonuc = {"birlesen": [], "hata": [], "arsiv": [], "sira": 0, "kalanlar": set(),
             "access": []}
    for g in s["gruplar"]:
        if not _birlesir(g):
            continue
        k = g["kalacak"]["dosya_no"]
        for h in g["uyeler"]:
            if h["dosya_no"] == k:
                continue
            try:
                p = uygula(h["dosya_no"], k)
            except Birlestirilemez as e:
                sonuc["hata"].append((h["dosya_no"], k, str(e)))
                continue
            sonuc["birlesen"].append((h["dosya_no"], k))
            sonuc["kalanlar"].add(p["d"]["id"])
            sonuc["arsiv"] += p["hatalar"]
            sonuc["sira"] += len(p["sira"])
            sonuc["access"] += [(kaynak, kayit, h["dosya_no"], k)
                                for kaynak, kayit in p["access"]]
    return sonuc


def _birlesir(g) -> bool:
    return bool(g["kalacak"]) and not g["engel"] and not g.get("atlandi")


def _benzer_kipi(yaz: bool, atla=()):
    s = benzer_plani()
    atla = set(atla)
    for g in s["gruplar"]:
        if atla & {h["dosya_no"] for h in g["uyeler"]}:
            g["atlandi"] = True
    s["atla_yok"] = sorted(atla - {h["dosya_no"] for g in s["gruplar"] for h in g["uyeler"]})
    benzer_yaz(s)
    benzer_raporu(s)
    print(f"\nAyrıntı (hasta adlarıyla): {RAPOR}")
    n = sum(len(g["uyeler"]) - 1 for g in s["gruplar"] if _birlesir(g))
    if not n:
        print("Birleştirilecek kart yok.")
        return
    if not yaz:
        ek = f" atla={','.join(str(x) for x in sorted(atla))}" if atla else ""
        print(f"\nHiçbir şey yazılmadı. {n} kartı birleştirmek için:\n"
              f"    python3 hasta_birlestir.py benzer uygula{ek}\n"
              "Listeden bir grubu dışarıda bırakmak için sonuna atla=<dosya no> "
              "(virgülle birden çok).")
        return
    print(f"\n{n} kart SİLİNECEK, her şeyi kalacak numaranın kartına geçecek.")
    if input('Birleştirmek için "BIRLESTIR" yazın: ').strip() != "BIRLESTIR":
        sys.exit("Vazgeçildi.")
    kopya = onceki_kopya()
    print(f"Önceki hal kopyalandı: {kopya}")
    sonuc = benzerleri_birlestir(s)
    print(f"\nBirleştirildi: {len(sonuc['birlesen'])} kart.")
    if sonuc["sira"]:
        print(f"Tedavi sırası tarih sırasıyla yeniden numaralandı: {sonuc['sira']} tedavi.")
    for eski, yeni, hata in sonuc["hata"]:
        print(f"BİRLEŞTİRİLMEDİ {eski} -> {yeni}: {hata}")
    for h in sonuc["arsiv"]:
        print(f"UYARI: arşivde taşınamadı -- {h}. Veritabanı yeni yolu gösteriyor; "
              "dosyayı elle taşıyın, yoksa fotoğraf görünmez.")
    if sonuc["access"]:
        with RAPOR.open("a", encoding="utf-8") as f:
            f.write("\nACCESS DÜZELTME SATIRLARI -- aynı CSV yeniden aktarılırsa "
                    "(duzelt=...), yoksa gerekmez:\n")
            for kaynak, kayit, eski, yeni in sonuc["access"]:
                f.write(f"    {kaynak}#{kayit}  DOSYA  {eski}  {yeni}\n" if kaynak else
                        f"    (#{kayit}: etiketsiz ağustos 2026 kaydı, {eski} -> {yeni} -- "
                        "o dosyayı yeniden aktarmayın)\n")
        print(f"Access'ten gelen {len(sonuc['access'])} kaydın düzeltme satırı "
              f"{RAPOR} sonunda (yalnızca aynı CSV yeniden aktarılırsa gerekir).")
    if not sonuc["kalanlar"]:
        return
    hidler = sorted(sonuc["kalanlar"])
    # İki kartta ayrı duran dondurma ve çözme artık aynı hastada: FET'ler
    # tüpüne, Cryo Haritası'ndaki Excel kayıtları tüpüne (aktarımın sonundaki
    # adımların aynısı, yalnızca birleşen hastalar).
    import aktar_access
    print("\nBirleşen hastaların aktarılmış FET'leri tüpüne bağlanıyor:")
    aktar_access.butun_fetleri_bagla(hidler=hidler)
    if _db.tablo_var("excel_kaydi"):
        import cryo_esle
        plan = cryo_esle.excel_kayitlarini_bagla(hidler=set(hidler))
        bagli = sum(1 for _s, k, _t, _e in plan if cryo_esle.excel_kaydi_baglanir(k))
        print(f"\nCryo Haritası: birleşen hastaların {bagli} Excel kaydı tüpüne bağlandı.")


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
    if args and args[0] == "benzer":
        atla, yaz = set(), False
        for a in args[1:]:
            if a == "uygula":
                yaz = True
            elif a.startswith("atla=") and all(
                    x.strip().isdigit() for x in a[5:].split(",") if x.strip()):
                atla |= {int(x) for x in a[5:].split(",") if x.strip()}
            else:
                sys.exit(__doc__)
        return _benzer_kipi(yaz, atla)
    if len(args) not in (2, 3) or not all(a.isdigit() for a in args[:2]) \
            or (len(args) == 3 and args[2] != "uygula"):
        sys.exit(__doc__)
    eski, yeni = int(args[0]), int(args[1])
    if eski == yeni:
        sys.exit("İki numara aynı.")
    try:
        p = plan(eski, yeni)
    except Birlestirilemez as e:
        sys.exit(str(e))
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
    try:
        p = uygula(eski, yeni)
    except Birlestirilemez as e:
        sys.exit(str(e))
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
