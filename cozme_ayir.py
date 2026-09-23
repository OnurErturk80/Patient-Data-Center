"""IVF/ICSI tedavisine yazılmış çözmeleri ayrı bir FET tedavisine taşır (v6.155).

Kullanım:
    python3 cozme_ayir.py            neler taşınacak -- yalnızca listeler
    python3 cozme_ayir.py uygula     taşır (önce "AYIR" yazmanız istenir)

Kullanıcının kararı (v6.155): "ivf/icsi tedavisi içinde çözme bölümü
olmamalıydı ... Embriyoloji özet formu ve art lab formuna iki tedaviyi
birleştirip yazıyor." v6.155'ten önce IVF/ICSI tedavisinin kendi çözme
ekranı vardı ve Cryo Haritası'ndan açılan çözme ekranı "hangi tedavi için"
seçimini embriyonun kaynak tedavisine bırakıyordu. O yoldan kaydedilen
çözme -- ve ondan sonraki transfer, yeniden dondurma -- IVF/ICSI'nin
kaydı sayıldı; iki tedavi tek formda birleşti.

Ne yapar, çözme grubu başına (aynı tedavi, aynı gün):
  1. Hedef FET'i seçer: bu embriyoların transferi zaten bir FET'e
     yazılmışsa o (çözme yanlış yere düşmüş, transfer doğru yerde); yoksa
     hastanın o gün planlanmış/açılmış, hiç kaydı olmayan tek bir FET'i;
     o da yoksa YENİ bir FET açar (lab kayıt no programın verdiği, yıl
     çözmenin yılı). Aday birden çoksa grubu atlar ve söyler.
  2. Çözmenin "hangi tedavi için"ini (`thaw_cycle_id`) FET yapar.
  3. Çözmeden sonra -- bir sonraki çözmeye kadar -- IVF/ICSI'ye yazılmış
     transferi ve yeniden dondurmayı FET'e taşır (`tr_cycle_id`,
     `vit_cycle_id`). Değerlendirmeler (FET 3->5'in blastokisti gibi)
     taşınmaz, taşınmaları gerekmiyor: bir değerlendirmenin tedavisi ondan
     önceki çözmeden türetiliyor (`db.olay_tedavisi()`).
  4. "İşlemi yapan"ın çözme satırını (ve taşınan transfer/dondurmanınkini)
     FET'e kopyalar; IVF/ICSI'de o işlem kalmadıysa oradan kaldırır.
  5. Gebelik sonucu, beta hCG ve doğan bebek tedaviye bağlı: IVF/ICSI'de
     hiç transfer kalmadıysa ve FET'te henüz yoksa taşınır; yoksa
     dokunulmaz, rapor söyler (taze transfer + FET birlikte -- hangi
     gebeliğin hangisi olduğuna kullanıcı karar verir).
  6. Yeni FET'in durumu: transfer taşındıysa "transfer ile bitti", yeniden
     dondurma taşındıysa "dondurma ile bitti", ikisi de yoksa devam ediyor.
  7. Hastanın tedavilerini tarih sırasıyla yeniden numaralar
     (`db.tedavileri_sirala()`), her değişikliği değişiklik geçmişine yazar.

Kural: hiçbir şey silinmez, embriyo kopyalanmaz; yalnızca "hangi tedavide
yapıldı" alanları değişir. İkinci çalıştırma hiçbir şey bulmaz -- taşınan
çözmenin tedavisi artık FET.

Önce yedek alın (Yönetici → Yedekleme → Şimdi yedekle). Çıktıda hasta adı
yok, yalnızca dosya no ve tedavi no.
"""

import datetime as _dt
import sqlite3
import sys

import db as _db          # veritabanının yeri tek yerde: db.py (tuzak #8)

DB = _db.DB_YOLU
if not DB.exists():
    sys.exit("lab.db bulunamadi: " + str(DB))

# Değerlendirme türleri: FET (3->5 kültür) mü düz FET mi.
_KULTUR_OLAYLARI = ("cleavage_degerlendirme", "blastokist_degerlendirme")


def _baglan():
    b = sqlite3.connect(DB, timeout=15)
    b.row_factory = sqlite3.Row
    b.execute("PRAGMA foreign_keys = ON")
    return b


def _kolonlar(b, tablo):
    return {r[1] for r in b.execute(f"PRAGMA table_info({tablo})")}


def _hazir_mi(b):
    eksik = [k for k in ("thaw_cycle_id", "tr_cycle_id")
             if k not in _kolonlar(b, "olay")]
    if eksik:
        sys.exit("Gocler calismamis, kolon yok: " + ", ".join(eksik)
                 + "\nProgrami bir kez acip kapatin, sonra tekrar deneyin.")


def _cozmesiz_tipler():
    """Çözme aşaması OLMAYAN tedavi tipleri -- v6.155'ten beri IVF/ICSI.
    Tip adı elle yazılmıyor, `TIP_ASAMALARI`'ndan soruluyor."""
    return [t for t in _db.TIP_ASAMALARI if not _db.cozme_tedavisi_mi(t)]


def gruplari_bul(b):
    """Çözme aşaması olmayan bir tedaviye yazılmış çözmeler, (tedavi, gün)
    başına bir grup. Aynı gün aynı tedaviden çözülen tüpler tek FET'tir."""
    tipler = _cozmesiz_tipler()
    if not tipler:
        return []
    yer = ",".join("?" * len(tipler))
    satirlar = b.execute(
        "SELECT o.id, o.specimen_id, o.zaman, s.cycle_id AS kaynak, "
        "  COALESCE(o.thaw_cycle_id, s.cycle_id) AS yazildigi, "
        "  c.cycle_no, c.cycle_tipi, c.hasta_id, h.dosya_no, "
        "  kc.cycle_tipi AS kaynak_tipi "
        "FROM olay o JOIN specimen s ON s.id = o.specimen_id "
        "JOIN cycle kc ON kc.id = s.cycle_id "
        "JOIN cycle c ON c.id = COALESCE(o.thaw_cycle_id, s.cycle_id) "
        "JOIN hasta h ON h.id = c.hasta_id "
        f"WHERE o.tip = 'thaw' AND o.iptal_mi = 0 AND c.cycle_tipi IN ({yer}) "
        "ORDER BY c.id, date(o.zaman), o.id", tipler).fetchall()
    gruplar = {}
    for r in satirlar:
        anahtar = (r["yazildigi"], (r["zaman"] or "")[:10])
        gruplar.setdefault(anahtar, []).append(r)
    return list(gruplar.values())


def _sonraki_cozme(b, specimen_id, cozme_id):
    r = b.execute("SELECT MIN(id) FROM olay WHERE specimen_id = ? "
                  "AND tip = 'thaw' AND iptal_mi = 0 AND id > ?",
                  (specimen_id, cozme_id)).fetchone()
    return r[0]


def _sonraki_olaylar(b, cozme, tip):
    """Bu çözmeden sonra, bir sonraki çözmeye kadar, `tip` türündeki olaylar
    (kimlik sırası -- saatler elle geri tarihlenebilir, v6.143)."""
    ust = _sonraki_cozme(b, cozme["specimen_id"], cozme["id"])
    kosul = " AND id < ?" if ust else ""
    arg = (cozme["specimen_id"], tip, cozme["id"]) + ((ust,) if ust else ())
    return b.execute(
        "SELECT * FROM olay WHERE specimen_id = ? AND tip = ? AND iptal_mi = 0 "
        f"AND id > ?{kosul} ORDER BY id", arg).fetchall()


def plan_kur(b, grup):
    """Bir grubun ne olacağı -- yazmadan. Sözlük döner."""
    ilk = grup[0]
    yanlis = ilk["yazildigi"]
    vit_var = "vit_cycle_id" in _kolonlar(b, "olay")
    transferler, dondurmalar = [], []
    for cz in grup:
        for t in _sonraki_olaylar(b, cz, "transfer"):
            transferler.append(t)
        if vit_var:
            for v in _sonraki_olaylar(b, cz, "vitrifikasyon"):
                dondurmalar.append(v)
    # Taşınacaklar: yalnızca hâlâ yanlış tedaviye yazılmış olanlar.
    tr_tasi = [t for t in transferler
               if (t["tr_cycle_id"] or t["cycle_id"]) == yanlis]
    vit_tasi = [v for v in dondurmalar
                if (v["vit_cycle_id"] or v["cycle_id"]) == yanlis]

    # Hedef: transferi zaten başka bir çözme tedavisine yazılmışsa o.
    hedefler = {t["tr_cycle_id"] for t in transferler
                if t["tr_cycle_id"] and t["tr_cycle_id"] != yanlis}
    hedefler = {h for h in hedefler if _db.cozme_tedavisi_mi(b.execute(
        "SELECT cycle_tipi FROM cycle WHERE id = ?", (h,)).fetchone()[0])}
    sorun = None
    hedef = None
    neden = ""
    if len(hedefler) > 1:
        sorun = "transferler birden cok tedaviye yazilmis"
    elif hedefler:
        hedef = hedefler.pop()
        neden = "transferi zaten bu tedavide"
    else:
        hedef, neden, sorun = _bos_fet(b, ilk)

    yumurta = _db.yumurta_mi(ilk["kaynak_tipi"], "thaw")
    if yumurta:
        tip = "yumurta_cozme"
    else:
        # Çözmeden sonra değerlendirme girilmişse embriyo kültüre alınmış:
        # FET (3->5 kültür).
        kultur = any(
            b.execute("SELECT 1 FROM olay WHERE specimen_id = ? AND iptal_mi = 0 "
                      f"AND tip IN ({','.join('?' * len(_KULTUR_OLAYLARI))}) "
                      "AND zaman >= ? LIMIT 1",
                      (cz["specimen_id"], *_KULTUR_OLAYLARI, cz["zaman"])).fetchone()
            for cz in grup)
        tip = "fet_kultur" if kultur else "fet"
    if hedef:
        tip = b.execute("SELECT cycle_tipi FROM cycle WHERE id = ?",
                        (hedef,)).fetchone()[0]
    return {"grup": grup, "yanlis": yanlis, "hedef": hedef, "neden": neden,
            "tip": tip, "sorun": sorun, "tr": tr_tasi, "vit": vit_tasi}


def _bos_fet(b, ilk):
    """Hastanın o gün planlanmış ya da açılmış, hiç kaydı olmayan çözme
    tedavisi. Kullanıcı FET'i açmış ama çözmeyi yanlış tedaviye yazmış
    olabilir; yeni bir FET açmak onu boş bırakırdı."""
    gun = (ilk["zaman"] or "")[:10]
    plan = "planlanan_tarih" in _kolonlar(b, "cycle")
    adaylar = []
    for c in b.execute("SELECT * FROM cycle WHERE hasta_id = ? AND id <> ?",
                       (ilk["hasta_id"], ilk["yazildigi"])).fetchall():
        if not _db.cozme_tedavisi_mi(c["cycle_tipi"]):
            continue
        gunler = {(c["olusturma_zamani"] or "")[:10]}
        if plan:
            gunler.add((c["planlanan_tarih"] or "")[:10])
        if gun not in gunler:
            continue
        dolu = b.execute(
            "SELECT 1 FROM olay WHERE iptal_mi = 0 AND (thaw_cycle_id = ? "
            "OR tr_cycle_id = ? OR cycle_id = ?) LIMIT 1",
            (c["id"], c["id"], c["id"])).fetchone()
        if not dolu:
            adaylar.append(c["id"])
    if len(adaylar) > 1:
        return None, "", "o gun acilmis birden cok bos FET var"
    if adaylar:
        return adaylar[0], "o gun acilmis bos tedavi", None
    return None, "yeni tedavi acilacak", None


def _log(b, kid, tablo, kayit_id, alan, eski, yeni):
    # `guvenlik.degisiklikleri_yaz()` kendi bağlantısını açar; burası
    # `yazma_islemi()`'nin kilidi içinde, aynı bağlantıdan yazılıyor
    # (aktar_access'in gerekçesi).
    if str(eski or "") == str(yeni or ""):
        return
    b.execute("INSERT INTO degisiklik_log (lab_id, tablo_adi, kayit_id, alan, "
              "eski_deger, yeni_deger, kullanici_id, zaman) "
              "VALUES (?,?,?,?,?,?,?,?)",
              (_db.LAB_ID, tablo, str(kayit_id), alan,
               None if eski is None else str(eski),
               None if yeni is None else str(yeni), kid,
               _dt.datetime.now().isoformat(" ", "seconds")))


def _islem_yapan_kopyala(b, kaynak, hedef, asama):
    b.execute("INSERT OR IGNORE INTO islem_yapan (lab_id, cycle_id, asama, "
              "yapan_ad, zaman, kullanici_id) SELECT lab_id, ?, asama, yapan_ad, "
              "zaman, kullanici_id FROM islem_yapan WHERE cycle_id = ? "
              "AND asama = ?", (hedef, kaynak, asama))


def plan_uygula(b, p, kid, rapor):
    from aktar_access import _lab_no     # programın numara kuralı, tek kopya
    grup, yanlis = p["grup"], p["yanlis"]
    ilk = grup[0]
    hedef = p["hedef"]
    if not hedef:
        zaman = ilk["zaman"] or _dt.datetime.now().isoformat(" ", "seconds")
        # Açılış anı çözmenin anı: ay listesi ve "Bugün bitenler" tedaviyi
        # bugüne değil çözmenin gününe koysun (aktar_access'in yaptığı).
        hedef = b.execute(
            "INSERT INTO cycle (lab_id, hasta_id, cycle_no, cycle_tipi, "
            "olusturma_zamani) VALUES (?, ?, ?, ?, ?)",
            (_db.LAB_ID, ilk["hasta_id"], _lab_no(b, zaman[:4]), p["tip"],
             zaman)).lastrowid
        _log(b, kid, "cycle", hedef, "cozme_ayir",
             None, f"acildi ({p['tip']})")
    for cz in grup:
        b.execute("UPDATE olay SET thaw_cycle_id = ? WHERE id = ?",
                  (hedef, cz["id"]))
        _log(b, kid, "olay", cz["id"], "thaw_cycle_id", yanlis, hedef)
    for t in p["tr"]:
        b.execute("UPDATE olay SET tr_cycle_id = ? WHERE id = ?", (hedef, t["id"]))
        _log(b, kid, "olay", t["id"], "tr_cycle_id", yanlis, hedef)
    for v in p["vit"]:
        b.execute("UPDATE olay SET vit_cycle_id = ? WHERE id = ?", (hedef, v["id"]))
        _log(b, kid, "olay", v["id"], "vit_cycle_id", yanlis, hedef)

    # İşlemi yapan: FET'e kopya; IVF/ICSI'de o işlem kalmadıysa oradan kalkar.
    _islem_yapan_kopyala(b, yanlis, hedef, "thaw")
    if p["tr"]:
        _islem_yapan_kopyala(b, yanlis, hedef, "transfer")
    if p["vit"]:
        _islem_yapan_kopyala(b, yanlis, hedef, "vitrifikasyon")
    kalan_cozme = b.execute(
        "SELECT 1 FROM olay o JOIN specimen s ON s.id = o.specimen_id "
        "WHERE o.tip = 'thaw' AND o.iptal_mi = 0 "
        "AND COALESCE(o.thaw_cycle_id, s.cycle_id) = ? LIMIT 1",
        (yanlis,)).fetchone()
    if not kalan_cozme:
        b.execute("DELETE FROM islem_yapan WHERE cycle_id = ? AND asama = 'thaw'",
                  (yanlis,))
    kalan_tr = b.execute(
        "SELECT 1 FROM olay o JOIN specimen s ON s.id = o.specimen_id "
        "WHERE o.tip = 'transfer' AND o.iptal_mi = 0 "
        "AND COALESCE(o.tr_cycle_id, s.cycle_id) = ? LIMIT 1",
        (yanlis,)).fetchone()
    if p["tr"] and not kalan_tr:
        b.execute("DELETE FROM islem_yapan WHERE cycle_id = ? "
                  "AND asama = 'transfer'", (yanlis,))

    # Gebelik: tedaviye bağlı. Yalnızca belirsizlik yoksa taşınır.
    gebelik_tablolari = [t for t in ("gebelik_sonucu", "beta_hcg", "dogan_bebek")
                         if _kolonlar(b, t)]
    gebelik = {t: b.execute(f"SELECT COUNT(*) FROM {t} WHERE cycle_id = ?",
                            (yanlis,)).fetchone()[0] for t in gebelik_tablolari}
    if any(gebelik.values()) and p["tr"]:
        hedefte = any(b.execute(f"SELECT 1 FROM {t} WHERE cycle_id = ? LIMIT 1",
                                (hedef,)).fetchone() for t in gebelik_tablolari)
        if kalan_tr or hedefte:
            rapor.append("    GEBELIK SONUCU TASINMADI: " + (
                "tedavide taze transfer de var" if kalan_tr
                else "FET'te zaten gebelik kaydi var")
                + " -- hangisinin oldugunu ekrandan kontrol edin")
        else:
            for t in gebelik_tablolari:
                b.execute(f"UPDATE {t} SET cycle_id = ? WHERE cycle_id = ?",
                          (hedef, yanlis))
            _log(b, kid, "cycle", hedef, "gebelik", yanlis, hedef)
            rapor.append("    gebelik sonucu FET'e tasindi")

    # Yeni FET'in bitişi (var olan hedefe dokunulmaz -- kullanıcı ekrandan
    # bitirmiş ya da bitirecek).
    if not p["hedef"]:
        if p["tr"]:
            son = max(t["zaman"] or "" for t in p["tr"])
            durum = ("tamamlandi", "transfer", son)
        elif p["vit"]:
            son = max(v["zaman"] or "" for v in p["vit"])
            durum = ("tamamlandi", "dondurma", son)
        else:
            durum = None
            rapor.append("    FET devam ediyor olarak kaldi (transfer ya da "
                         "dondurma yok) -- ekrandan bitirin")
        if durum:
            b.execute("UPDATE cycle SET durum = ?, bitis_sebebi = ?, "
                      "bitis_zamani = ? WHERE id = ?", (*durum, hedef))
            _log(b, kid, "cycle", hedef, "bitis_sebebi", None, durum[1])

    kaynak = b.execute("SELECT durum, bitis_sebebi FROM cycle WHERE id = ?",
                       (yanlis,)).fetchone()
    if kaynak["bitis_sebebi"] == "transfer" and not kalan_tr:
        rapor.append("    DIKKAT: IVF/ICSI tedavisinin bitis sebebi 'transfer' "
                     "ama artik transferi yok -- ekrandan 'dondurma' yapin")

    for cid, no, eski, yeni in _db.tedavileri_sirala(b, ilk["hasta_id"]):
        _log(b, kid, "cycle", cid, "hasta_cycle_no", eski, yeni)
        rapor.append(f"    tedavi sirasi: {no} {eski}. -> {yeni}.")
    return hedef


def goster(b, p):
    ilk = p["grup"][0]
    print(f"Dosya {ilk['dosya_no']} · {ilk['cycle_no']} ({ilk['cycle_tipi']}) · "
          f"cozme {(ilk['zaman'] or '')[:16]}")
    print("   cozulen   : " + ", ".join(r["specimen_id"] for r in p["grup"]))
    if p["sorun"]:
        print(f"   ATLANACAK : {p['sorun']} -- elle bakin")
        return
    if p["hedef"]:
        no = b.execute("SELECT cycle_no FROM cycle WHERE id = ?",
                       (p["hedef"],)).fetchone()[0]
        print(f"   hedef     : {no} ({p['tip']}) -- {p['neden']}")
    else:
        print(f"   hedef     : YENI {p['tip']} tedavisi")
    print(f"   tasinacak : cozme {len(p['grup'])}, transfer {len(p['tr'])}, "
          f"yeniden dondurma {len(p['vit'])}")


def main():
    uygula = len(sys.argv) > 1 and sys.argv[1] == "uygula"
    b = _baglan()
    _hazir_mi(b)
    print(f"Veritabani : {DB}\n")
    planlar = [plan_kur(b, g) for g in gruplari_bul(b)]
    if not planlar:
        print("IVF/ICSI tedavisine yazilmis cozme yok -- yapilacak bir sey yok.")
        return
    for p in planlar:
        goster(b, p)
    yapilacak = [p for p in planlar if not p["sorun"]]
    print(f"\n{len(planlar)} grup, {len(yapilacak)} tanesi tasinabilir.")
    if not uygula:
        print("Tasimak icin: python3 cozme_ayir.py uygula "
              "(once programdan yedek alin)")
        return
    if not yapilacak:
        return
    if input('\nOnaylamak icin AYIR yazin: ').strip() != "AYIR":
        print("Vazgecildi, hicbir sey degismedi.")
        return
    b.close()
    from aktar_access import _kullanici_id
    kid = _kullanici_id()
    # Her grup kendi işleminde: biri patlarsa öncekiler yerinde kalır, sonrakiler
    # tekrar çalıştırmada bulunur (grup yeniden aranıyor, kayıtlı plan değil).
    for p in yapilacak:
        rapor = []
        with _db.yazma_islemi() as yb:
            yb.row_factory = sqlite3.Row
            taze = plan_kur(yb, [yb.execute(
                "SELECT o.id, o.specimen_id, o.zaman, s.cycle_id AS kaynak, "
                "  COALESCE(o.thaw_cycle_id, s.cycle_id) AS yazildigi, "
                "  c.cycle_no, c.cycle_tipi, c.hasta_id, h.dosya_no, "
                "  kc.cycle_tipi AS kaynak_tipi "
                "FROM olay o JOIN specimen s ON s.id = o.specimen_id "
                "JOIN cycle kc ON kc.id = s.cycle_id "
                "JOIN cycle c ON c.id = COALESCE(o.thaw_cycle_id, s.cycle_id) "
                "JOIN hasta h ON h.id = c.hasta_id WHERE o.id = ?",
                (r["id"],)).fetchone() for r in p["grup"]])
            if taze["yanlis"] != p["yanlis"] or taze["sorun"]:
                print(f"Atlandi (bu arada degismis): {p['grup'][0]['cycle_no']}")
                continue
            hedef = plan_uygula(yb, taze, kid, rapor)
            no = yb.execute("SELECT cycle_no FROM cycle WHERE id = ?",
                            (hedef,)).fetchone()[0]
        print(f"{p['grup'][0]['cycle_no']} -> {no}: tamam")
        for s in rapor:
            print(s)
    print("\nBitti. Programi yeniden baslatmaniza gerek yok; ekrani tazeleyin.")


if __name__ == "__main__":
    main()
