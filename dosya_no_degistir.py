"""Bir hastanın dosya numarasını değiştirir (v6.172).

Kullanım:
    python3 dosya_no_degistir.py <eski no> <yeni no>          ne olacak -- yalnızca listeler
    python3 dosya_no_degistir.py <eski no> <yeni no> uygula   değiştirir ("DEGISTIR" yazmanız istenir)

Hasta düzenleme ekranı dosya numarasını bilerek kilitliyor ("Dosya no
değiştirilemez. Yanlışsa kayıt silinip yeniden açılmalı."): numara arşiv
klasörünün adı (`arsiv/<dosya no>/...`) ve `goruntu.dosya_yolu`'nun ilk
parçası -- ekrandan değiştirilse fotoğraflar kaybolurdu. Silip yeniden açmak
ise Access'ten aktarılmış, tüpü tankta duran bir tedavide (aralık 2024'ün
yer tutucu "99" numaralı hastası; gerçek numarası 2019'un dosyalarında) hem
zahmetli hem riskli: çözülmüş tüpü olan kayıt silinemez.

Bu araç numarayı her yerde birlikte değiştiriyor, tek işlemde:
  1. `hasta.dosya_no`;
  2. `goruntu.dosya_yolu` ve `sperm_dondurma_dosya.dosya_yolu`'nun
     `<eski>/` ile başlayanları;
  3. başka hastaların `es_dosya_no`'sunda eski numara yazıyorsa o da;
  4. veritabanı yazıldıktan sonra `arsiv/<eski>/` klasörü `arsiv/<yeni>/`
     olarak yeniden adlandırılıyor (yoksa atlanıyor; adlandırma başarısız
     olursa söyleniyor -- veritabanı yeni numarada, klasör elle taşınır);
  5. her değişiklik `degisiklik_log`'a düşüyor;
  6. eski numara GEÇİCİYSE (9000000001…, `cryo_esle.py` açtı) hastanın sperm
     tüplerinin `<eski>-SP-SSDD` etiketi `<yeni>-SP-SSDD` oluyor (v6.180).
     Geçici numara hiçbir tüpün üstünde yazmıyor; gerçek numaralı tüpün
     etiketine dokunulmuyor -- o tankta tüpün üstünde yazıyor olabilir.

Yeni numara başka bir hastada kayıtlıysa araç durur: iki kartı birleştirmek
bu aracın işi değil -- aynı hastaysa `hasta_birlestir.py` (v6.215). Lab kayıt no (`cycle_no`), embriyo tüpünün etiketi ve
örnek kodu (`specimen.id`) dosya numarasını içermiyor, değişmiyor. Önce yedek alın
(Yönetici → Yedekleme → Şimdi yedekle). Çıktıda hasta adı yok.
"""

import shutil
import sys

import db as _db          # veritabanının yeri tek yerde: db.py (tuzak #8)
import goruntuler
import guvenlik

DB = _db.DB_YOLU
if not DB.exists():
    sys.exit("lab.db bulunamadi: " + str(DB))


def _hasta(no):
    return _db.tek("SELECT * FROM hasta WHERE lab_id=? AND dosya_no=?", (_db.LAB_ID, no))


def _kullanici_id():
    for kosul in ("AND rol='yonetici'", ""):
        r = _db.tek(f"SELECT id FROM kullanici WHERE lab_id=? AND aktif_mi=1 "
                    f"{kosul} ORDER BY id LIMIT 1", (_db.LAB_ID,))
        if r:
            return r["id"]
    sys.exit("Aktif kullanici yok -- once bir kullanici ac (kullanici.py).")


GECICI_DOSYA_TABANI = 9_000_000_000     # cryo_esle.py'nin tabanı


def _sperm_etiketleri(b, hid, eski, yeni):
    """[(taşıyıcı id, eski etiket, yeni etiket)] -- yalnızca geçici numarada."""
    if eski <= GECICI_DOSYA_TABANI:
        return []
    onek = f"{eski}-SP-"
    return [(r[0], r[1], f"{yeni}-SP-" + r[1][len(onek):]) for r in b.execute(
        "SELECT t.id, t.etiket FROM sperm_dondurma sd JOIN tasiyici t ON t.id=sd.tasiyici_id "
        "WHERE sd.hasta_id=? AND t.kategori='sperm' AND substr(t.etiket, 1, ?) = ?",
        (hid, len(onek), onek)).fetchall()]


def ozet(eski, yeni):
    h = _hasta(eski)
    if not h:
        sys.exit(f"Dosya no {eski} kayıtlı değil.")
    if _hasta(yeni):
        sys.exit(f"Dosya no {yeni} zaten başka bir hastada kayıtlı -- iki kart "
                 "birleştirilmez, araç durdu. İkisi aynı hastaysa (v6.215): "
                 f"python3 hasta_birlestir.py {eski} {yeni}")
    hid = h["id"]
    tedavi = _db.tek("SELECT COUNT(*) AS n FROM cycle WHERE hasta_id=?", (hid,))["n"]
    foto = _db.tek("SELECT COUNT(*) AS n FROM goruntu g JOIN cycle c ON c.id=g.cycle_id "
                   "WHERE c.hasta_id=? AND g.dosya_yolu LIKE ?", (hid, f"{eski}/%"))["n"]
    onam = _db.tek("SELECT COUNT(*) AS n FROM sperm_dondurma_dosya d "
                   "JOIN sperm_dondurma s ON s.id=d.sperm_dondurma_id "
                   "WHERE s.hasta_id=? AND d.dosya_yolu LIKE ?", (hid, f"{eski}/%"))["n"]
    es = _db.tek("SELECT COUNT(*) AS n FROM hasta WHERE lab_id=? AND es_dosya_no=?",
                 (_db.LAB_ID, eski))["n"]
    with _db.baglan() as b:
        etiket = _sperm_etiketleri(b, hid, eski, yeni)
        cakisan = [y for _t, _e, y in etiket if b.execute(
            "SELECT 1 FROM tasiyici WHERE lab_id=? AND etiket=?", (_db.LAB_ID, y)).fetchone()]
    if cakisan:
        sys.exit(f"Tüp etiketi zaten var: {', '.join(cakisan)} -- araç durdu.")
    klasor = goruntuler.arsiv_klasor() / goruntuler.guvenli_ad(eski)
    print(f"Hasta {eski} -> {yeni}: {tedavi} tedavi, {foto} fotoğraf yolu, "
          f"{onam} onam eki, {len(etiket)} sperm tüpü etiketi, "
          f"{es} hastada eş numarası olarak; "
          f"arşiv klasörü {'var' if klasor.is_dir() else 'yok'} ({klasor}).")
    return h, klasor


def uygula(eski, yeni, h, klasor):
    hid, kid = h["id"], _kullanici_id()
    with _db.yazma_islemi() as b:
        b.execute("UPDATE hasta SET dosya_no=? WHERE id=?", (yeni, hid))
        for tablo in ("goruntu", "sperm_dondurma_dosya"):
            b.execute(f"UPDATE {tablo} SET dosya_yolu = ? || substr(dosya_yolu, ?) "
                      f"WHERE lab_id=? AND dosya_yolu LIKE ?",
                      (f"{yeni}/", len(f"{eski}/") + 1, _db.LAB_ID, f"{eski}/%"))
        esler = [r["id"] for r in b.execute(
            "SELECT id FROM hasta WHERE lab_id=? AND es_dosya_no=?",
            (_db.LAB_ID, eski)).fetchall()]
        b.execute("UPDATE hasta SET es_dosya_no=? WHERE lab_id=? AND es_dosya_no=?",
                  (yeni, _db.LAB_ID, eski))
        etiketler = _sperm_etiketleri(b, hid, eski, yeni)
        for tid, _e, y in etiketler:
            b.execute("UPDATE tasiyici SET etiket=? WHERE id=?", (y, tid))
    guvenlik.degisiklikleri_yaz("hasta", hid, {"dosya_no": eski}, {"dosya_no": yeni}, kid)
    for tid, e, y in etiketler:
        guvenlik.degisiklikleri_yaz("tasiyici", tid, {"etiket": e}, {"etiket": y}, kid)
    for eid in esler:
        guvenlik.degisiklikleri_yaz("hasta", eid, {"es_dosya_no": eski},
                                    {"es_dosya_no": yeni}, kid)
    print(f"Veritabanı yazıldı: dosya no {yeni}.")
    if klasor.is_dir():
        hedef = klasor.parent / goruntuler.guvenli_ad(yeni)
        try:
            if hedef.exists():
                raise OSError(f"{hedef} zaten var")
            shutil.move(str(klasor), str(hedef))
            print(f"Arşiv klasörü taşındı: {klasor} -> {hedef}")
        except OSError as e:
            print(f"UYARI: arşiv klasörü taşınamadı ({e}). Veritabanı yeni numarada; "
                  f"klasörü elle {hedef} adına taşıyın, yoksa fotoğraflar görünmez.")


def main():
    args = [a for a in sys.argv[1:] if a]
    if len(args) not in (2, 3) or not all(a.isdigit() for a in args[:2]) \
            or (len(args) == 3 and args[2] != "uygula"):
        sys.exit(__doc__)
    eski, yeni = int(args[0]), int(args[1])
    if eski == yeni:
        sys.exit("Eski ve yeni numara aynı.")
    if len(args) == 2:
        ozet(eski, yeni)
        print("Değiştirmek için:  python3 dosya_no_degistir.py "
              f"{eski} {yeni} uygula")
        return
    h, klasor = ozet(eski, yeni)
    if input('Değiştirmek için "DEGISTIR" yazın: ').strip() != "DEGISTIR":
        sys.exit("Vazgeçildi.")
    uygula(eski, yeni, h, klasor)


if __name__ == "__main__":
    main()
