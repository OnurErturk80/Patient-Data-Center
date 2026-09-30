"""Aynı hastanın iki tedavisini birleştirir (v6.228).

Kullanım:
    python3 tedavi_birlestir.py <birleşen no> <esas no>          ne olacak -- yalnızca listeler
    python3 tedavi_birlestir.py <birleşen no> <esas no> uygula   birleştirir ("BIRLESTIR" yazmanız istenir)

Numaralar lab kayıt no (tedavi ekranının başlığındaki 2026-0xxx). Esas tedavi
KALIR, birleşen tedavi silinir; dondurulmuş örnekleri esas tedavinin olur.

Kullanıcı (2026-09-30): "... tedavisini ... tedavisine bağla. Esas tedavi ....
dondurulmuş örneklerini de tek tedaviye topla" (numaralar buraya yazılmadı).
Bir tedavi iki kaydı birden taşıyınca yumurtalar iki kez sayılırdı -- ekranın
özeti, resmî formun ızgarası, istatistik. O yüzden araç birleşen tedavinin ne
olduğuna bakıp üç yoldan birini seçiyor:

  1. "Excel kaydı": birleşen tedavi Cryo Haritası Excel'inden açılmış bir
     dondurma kaydı (`db.CRYO_EXCEL_ISARETI`: "Hastaya bağla", v6.213;
     `cryo_esle.py yeni_hasta`, v6.179). Tüpündeki embriyolar esas tedavide
     zaten kayıtlı: her tüp esas tedavinin eşleşen, dondurulmamış
     örneklerine geçer, Excel'in açtığı örnekler silinir. Esas tedavinin hiç
     örneği yoksa (ya da o da bir Excel kaydıysa) örnekler esas tedaviye
     taşınır, numaraları esas tedavinin numarasıyla.
  2. "Aynı işlemin ikinci kaydı": aynı tip, aynı OPU günü. Tüpler aynı
     kuralla esas tedaviye geçer; birleşen tedavinin öteki yumurtaları esas
     tedavide zaten kayıtlı, silinir. Aynı gün aynı transfer iki tedavide de
     yazılı olmalı; silinecek örnekte fotoğraf, bulgu ya da PGT varsa durur.
  3. "Kendi örneği yok" (iki FET, boş açılmış tedavi): çözme, transfer ve
     yeniden dondurma kayıtları esas tedavinin olur (`thaw_cycle_id`,
     `tr_cycle_id`, `vit_cycle_id`).

Tüpün esas tedavideki karşılığı:
  - aynı straw esas tedavide zaten bir tüp olarak varsa (dolu, aynı içerik,
    en çok bir gün farkla, konumu boş ya da aynı goblet, Excel kaydına bağlı
    değil): Excel kaydı o tüpe bağlanır (`cryo_esle.excel_kaydini_tupe_bagla()`,
    "bağı çöz" bildiği gibi geri alır), fazla tüp örnekleriyle silinir;
  - içerik tutmuyor ama esas tedavide aynı gün dondurulmuş, yeri girilmemiş
    aynı türden bir tüp varsa araç durur (v6.229): Excel aynı straw'ı başka
    bir yazımla gösteriyor olabilir; tüp esasın başka örneklerine yazılsaydı
    straw iki tüp olurdu. Excel kaydından açılmış tüpte yol programda:
    kaydın sayfasında "Açılan tüpü geri al", sonra "Tüpe bağla";
  - yoksa tüp esas tedavinin örneklerine geçer: aynı skor, yoksa esas
    tedavide hiç değerlendirilmemiş örnek (skoru tüpten yazılır), yoksa aynı
    evre ve sayı (cleavage'da hücre, blastokistte genişleme -- "yakın skor");
    birleşen örneğin skoru yoksa herhangi biri. Aynı skorlu embriyolar
    birbirinden ayırt edilemez, sıra no sırasıyla. Adaylar dondurulmamış,
    çözülmemiş, transfer edilmemiş, dejenere ve arrest olmayan örnekler.
    Dondurma ve sonrası (çözme, transfer, yeniden dondurma) yeni kimlikle
    esas tedavinin örneğine yazılıyor -- kimlik sırası işlem sırası kalsın
    (`db.olay_sirasini_duzelt()`'in gerekçesi). Tüp kalıyor: etiketi, yeri,
    rengi, Excel bağı; etiket programın ürettiği bir koddaysa (Excel ya da
    Access kaydı) esas tedavinin numarasına çevriliyor.

Hepsinde: tedavi düzeyindeki kayıtlar (işlemi yapan, androloji, gebelik,
beta hCG, doğan bebek, genel bulgular, belge ekleri) esas tedavide yoksa
geçer; varsa esasınki kalır (aynı işlemin ikinci kaydında birleşeninki düşer,
öbür yollarda araç durur); esas tedavinin boş alanları birleşenden dolar
(Excel kaydından değil: onun alanları üretilmiş); fotoğraflar esas tedavinin
arşiv klasörüne taşınır; birleşen tedavi silinir, bütün alanları günlükte
("BIRLESTIRME"); tedaviler tarih sırasıyla yeniden numaralanır.

Protokol notu: birleşenin notu esasınkinin altına eklenir. Access kaydında
(aynı işlemin ikinci kaydı ya da boş tedavi) yalnızca işareti: not esas
tedavide zaten kayıtlı işlemi anlatıyor, tamamı eklenseydi resmî formun
NOTLAR'ı embriyoları iki kez yazardı; işaret ise kalmalı -- aynı dosya
yeniden aktarılınca kayıt ikinci kez açılmasın (`aktar_access._zaten_var()`).
O zaman taşınan tüpün dondurma notu da "birleştirildi" olur
(`db.KAYNAK_DONDURMA_NOTU` taşıyan tüpü form "Dondurulan:"a yazmıyor).
Excel kaydının notu eklenmez (işareti esas tedaviyi istatistikten düşürürdü).

Durduğu yerler (hiçbir şey yazılmaz): iki tedavi farklı hastaların; esas
tedavi Excel kaydı, birleşen gerçek tedavi (ters yön); tipler farklı; OPU
günleri farklı (Excel kaydında bir gün; OPU'suz tedavide günler 1, Excel'de
8 günden uzak); tüpün içeriği esas tedavide karşılık bulmuyor ya da esasta
aynı straw olabilecek, farklı yazılmış bir tüp var (v6.229); silinecek
örnekte fotoğraf / bulgu / PGT ya da başka tedaviye yazılmış kayıt; iki
tedavide de gebelik sonucu (aynı işlemin ikinci kaydı değilse); arşivde iki
klasörde aynı adlı dosya. Boş bir tedavi (hiç kaydı yok) her tedaviye
birleşebilir -- birleştirmek onu silmek; tipi ya da günü farklıysa önizleme
uyarır, alanları yazılmaz.

Önce veritabanının tamamı `lab_ONCEKI_<zaman>.db` (hasta_birlestir.py'nin
yeri: yedek klasörü, yoksa veri klasörü). Hangi tedavinin esas olduğunu
KULLANICI söylüyor; araç ikisinde ne olduğunu gösteriyor. Çıktıda hasta adı
yok.
"""

import collections
import json
import re
import sys
from datetime import date, datetime, timedelta

import db as _db                 # veritabanının yeri tek yerde: db.py (tuzak #8)
import cryo_esle                 # içerik yazımının karşılaştırması, Excel kaydı bağlama
import dosya_no_degistir as _dnd
import goruntuler
import hasta_birlestir as _hb    # önceki halin kopyası, arşiv taşıma, günlük satırı
import metinler

ONAY = "BIRLESTIR"

# Birleşenden esas tedavinin BOŞ alanına yazılanlar (ekrandaki adıyla).
ALANLAR = {
    "endikasyon": "endikasyon", "protokol_tipi": "protokol", "gonadotropin_tipi":
    "gonadotropin", "baslangic_doz": "başlangıç dozu", "toplam_doz": "toplam doz",
    "stim_gun_sayisi": "stimülasyon günü", "trigger_tipi": "trigger",
    "hcg_gunu_e2": "hCG günü E2", "hcg_gunu_p4": "hCG günü P4",
    "endometrium_mm": "endometrium", "folikul_sayisi": "folikül sayısı", "amh": "AMH",
    "afc": "AFC", "hcg_zamani": "hCG zamanı", "opu_zamani": "OPU zamanı",
    "denudasyon_zamani": "denüdasyon zamanı", "opu_sag_oosit": "OPU sağ",
    "opu_sol_oosit": "OPU sol", "opu_hekim": "OPU hekimi",
    "transfer_hekim": "transfer hekimi",
    "planlanan_tarih": "planlanan tarih", "bulas_kadin": "bulaş (kadın)",
    "bulas_erkek": "bulaş (erkek)", "pgt_testleri": "PGT", "pgt_notu": "PGT notu"}

_DEGERLENDIRME = cryo_esle.DEGERLENDIRME_TIPLERI
_ACCESS = "[Access kayd"
# Programın ürettiği etiket: "<lab kayıt no>-<SSDD>" (vitrifikasyon ekranının
# önerisi, aktarım ve Excel kaydı da öyle açıyor).
_ETIKET = re.compile(r"^(?P<no>.+)-(?P<ss>\d{2})(?P<dd>\d{2})$")


# ------------------------------------------------------------------ okuma

def _tedavi(b, no):
    return b.execute("SELECT * FROM cycle WHERE lab_id=? AND cycle_no=?",
                     (_db.LAB_ID, no)).fetchone()


def _tur(c) -> str:
    notu = c["protokol_notu"] or ""
    if _db.CRYO_EXCEL_ISARETI in notu:
        return "excel"
    return "access" if _ACCESS in notu else "program"


def _tip_adi(b, kod) -> str:
    """Ekranın yazdığı ad (`metinler.py`'nin `tip_<kod>`'u), yoksa listenin etiketi."""
    m = metinler.METINLER.get(f"tip_{kod}", {}).get("tr")
    if m:
        return m
    r = b.execute("SELECT etiket FROM liste_degeri WHERE lab_id=? AND "
                  "liste_adi='cycle_tipi' AND kod=?", (_db.LAB_ID, kod)).fetchone()
    return r[0] if r else kod


_DURUM_ADI = {"aktif": "devam ediyor", "tamamlandi": "bitti", "iptal": "iptal"}


def _gun(iso) -> str:
    if not iso:
        return "—"
    try:
        return date.fromisoformat(str(iso)[:10]).strftime("%d.%m.%Y")
    except ValueError:
        return str(iso)


def _gun_farki(a, b) -> int:
    try:
        return abs((date.fromisoformat(a[:10]) - date.fromisoformat(b[:10])).days)
    except (TypeError, ValueError):
        return 999


def _say(b, sql, *a) -> int:
    return b.execute(sql, a).fetchone()[0]


# Örneğin kalitesi: v6.233'ten beri `cryo_esle`'de -- Excel kaydının
# "tedaviye bağla"sı (programın ekranı) aynı anahtarla karşılaştırıyor, iki
# kopya ayrı düşmesin. Adlar burada eskisi gibi.
_embriyo_izi = cryo_esle.ornek_izi
_son = cryo_esle.son_olay
_anahtar = cryo_esle.ornek_anahtari
_yazim = cryo_esle.ornek_yazimi
_evre_sayi = cryo_esle.evre_sayi


def _tup_yazimi(yazimlar, yumurta: bool) -> str:
    """Tüpün laboratuvar yazımı -- `formlar.tup_metni()`'nin biçimi:
    "3BA-1BB", yumurtada "4*MII-1*MI"."""
    if not yumurta:
        return "-".join(yazimlar)
    say = collections.Counter(yazimlar)
    sira = ["MII", "MI", "GV"] + sorted(k for k in say if k not in ("MII", "MI", "GV"))
    return "-".join(f"{say[k]}*{k}" for k in sira if say.get(k))


def _ornekler(b, cid) -> dict:
    """Tedavinin kendi örnekleri, olaylarıyla: {örnek id: bilgi}."""
    sonuc = {}
    for s in b.execute("SELECT * FROM specimen WHERE cycle_id=? ORDER BY cycle_sira_no",
                       (cid,)):
        sonuc[s["id"]] = {"id": s["id"], "s": s, "olaylar": [], "aktif": []}
    if not sonuc:
        return sonuc
    idler = list(sonuc)
    for i in range(0, len(idler), 500):
        parca = idler[i:i + 500]
        yer = ",".join("?" * len(parca))
        for o in b.execute(f"SELECT * FROM olay WHERE specimen_id IN ({yer}) ORDER BY id",
                           parca):
            x = sonuc[o["specimen_id"]]
            x["olaylar"].append(o)
            if not o["iptal_mi"]:
                x["aktif"].append(o)
    pgt = _db.tablo_var("pgt_sonuc")
    for sid, x in sonuc.items():
        ak = x["aktif"]
        x["foto"] = _say(b, "SELECT COUNT(*) FROM goruntu WHERE specimen_id=?", sid)
        x["bulgu"] = _say(b, "SELECT COUNT(*) FROM specimen_bulgu WHERE specimen_id=?", sid)
        x["pgt"] = _say(b, "SELECT COUNT(*) FROM pgt_sonuc WHERE specimen_id=?", sid) if pgt else 0
        x["vit"] = [o for o in ak if o["tip"] == "vitrifikasyon"]
        x["thaw"] = [o for o in ak if o["tip"] == "thaw"]
        x["transfer"] = [o for o in ak if o["tip"] == "transfer"]
        x["degenere"] = any((o["tip"] == "icsi" and o["icsi_sonuc"] == "degenere") or
                            (o["tip"] == "fertilizasyon_kontrolu" and o["fert_sonuc"] == "degenere")
                            for o in ak)
        x["iz"] = _embriyo_izi(ak)
        x["olgunluk"] = any(o["tip"] == "maturasyon_kontrolu" for o in ak)
        x["embriyo"] = x["iz"]
        x["anahtar"] = _anahtar(ak, x["iz"])
        x["yazim"] = _yazim(ak, x["iz"])
        # Başka bir tedaviye yazılmış kayıt: bu örnek o tedavide çözüldü /
        # transfer edildi / yeniden donduruldu.
        x["baska"] = sorted({v for o in ak for v in (
            o["thaw_cycle_id"], o["tr_cycle_id"],
            o["vit_cycle_id"] if "vit_cycle_id" in o.keys() else None)
            if v and v != x["s"]["cycle_id"]})
    return sonuc


def _ilk_dondurma(x, cid):
    """Örneğin bu tedavide yapılan ilk (aktif) dondurması -- tüpü bu
    tedavinin tüpü yapan kayıt."""
    for o in x["vit"]:
        vc = o["vit_cycle_id"] if "vit_cycle_id" in o.keys() else None
        if (vc or o["cycle_id"]) == cid:
            return o
    return None


def _tup(b, tid) -> dict:
    t = b.execute("SELECT t.*, k.tam_yol FROM tasiyici t LEFT JOIN konum k "
                  "ON k.id = t.konum_id WHERE t.id=?", (tid,)).fetchone()
    ekler = [dict(e) for e in b.execute(
        "SELECT * FROM excel_kaydi WHERE tasiyici_id=? ORDER BY id", (tid,))] \
        if _db.tablo_var("excel_kaydi") else []
    ornekler = [r[0] for r in b.execute(
        "SELECT DISTINCT specimen_id FROM olay WHERE vit_tasiyici_id=? "
        "AND tip='vitrifikasyon' AND iptal_mi=0", (tid,))]
    return {"t": t, "excel": ekler, "ornekler": ornekler}


def _tup_metni(t, yazim) -> str:
    return f"{t['etiket']} ({yazim}) · {t['tam_yol'] or 'konum girilmemiş'} · {t['durum']}"


def _tupler(b, ornekler, cid) -> dict:
    """Tedavide dondurulmuş tüpler: {tüp id: {"bilgi", "ornekler": [id],
    "gun"}} -- tedavinin kendi örneklerinin bu tedavideki ilk dondurması."""
    sonuc = {}
    for sid, x in ornekler.items():
        o = _ilk_dondurma(x, cid)
        if not o or not o["vit_tasiyici_id"]:
            continue
        g = sonuc.setdefault(o["vit_tasiyici_id"], {"ornekler": [], "gun": o["zaman"]})
        g["ornekler"].append(sid)
        g["gun"] = min(g["gun"] or o["zaman"], o["zaman"] or g["gun"])
    for tid, g in sonuc.items():
        g["bilgi"] = _tup(b, tid)
    return sonuc


# ------------------------------------------------------------------ eşleşme

def _adaylar(ornekler) -> list:
    """Esas tedavinin tüpe girebilecek örnekleri: dondurulmamış, çözülmemiş,
    transfer edilmemiş, dejenere ve arrest olmayan."""
    return [x for x in ornekler.values()
            if not x["vit"] and not x["thaw"] and not x["transfer"]
            and not x["degenere"] and x["anahtar"] not in ("arrest", "DEGENERE", "ATRETIK")]


def _eslestir(istenen, adaylar) -> dict:
    """istenen: [(örnek id, tür, anahtar)] -> {örnek id: (aday, katman)}.
    Katmanlar sırayla, her biri bütün istenenler için: aynı skor;
    değerlendirilmemiş aday; aynı evre ve sayı; birleşenin skoru yoksa
    herhangi biri (önce değerlendirilmemiş)."""
    atanan, kullanilan = {}, set()

    def al(tur, uygun):
        for a in adaylar:
            if a["id"] not in kullanilan and _tur_esit(a, tur) and uygun(a):
                kullanilan.add(a["id"])
                return a
        return None

    katmanlar = [
        ("aynı skor", lambda k: k != "?", lambda a, k: a["anahtar"] == k),
        ("değerlendirilmemiş örnek", lambda k: k != "?", lambda a, k: a["anahtar"] == "?"),
        ("yakın skor", lambda k: _evre_sayi(k) is not None,
         lambda a, k: _evre_sayi(a["anahtar"]) == _evre_sayi(k)),
        ("skorsuz", lambda k: k == "?", lambda a, k: a["anahtar"] == "?"),
        ("skorsuz", lambda k: k == "?", lambda a, k: True),
    ]
    for ad, ister, uygun in katmanlar:
        for sid, tur, k in istenen:
            if sid in atanan or not ister(k):
                continue
            a = al(tur, lambda a: uygun(a, k))
            if a:
                atanan[sid] = (a, ad)
    return atanan


def _tur_esit(a, tur) -> bool:
    if tur == "embriyo":
        return a["iz"]
    return not a["iz"]


def _tup_turu(g, B_orn, B) -> str:
    """Tüpteki örneklerin türü: biri embriyoysa embriyo; hiçbirinin izi yoksa
    olgunluğu yazılı olan yumurta; hiçbir şey yazılı değilse (skorsuz Excel
    embriyosu) tedavinin tipi."""
    xs = [B_orn[s] for s in g["ornekler"]]
    if any(x["iz"] for x in xs):
        return "embriyo"
    if any(x["olgunluk"] for x in xs):
        return "yumurta"
    return "yumurta" if B["cycle_tipi"] == "oosit_cryo" else "embriyo"


def _straw_olabilir(g, tid, h, kullanilan) -> bool:
    """Esas tedavinin `h` tüpü birleşenin `g` tüpüyle aynı straw olabilir mi,
    içeriğe bakmadan: ikisi de dolu, aynı kategori, esasınki Excel kaydına
    bağlı değil, en çok bir gün farkla, konumu boş ya da aynı yer."""
    t, ht = g["bilgi"]["t"], h["bilgi"]["t"]
    return not (t["durum"] != "dolu" or tid in kullanilan or ht["durum"] != "dolu"
                or h["bilgi"]["excel"] or ht["kategori"] != t["kategori"]
                or _gun_farki(h["gun"], g["gun"]) > 1
                or (ht["konum_id"] and t["konum_id"] and ht["konum_id"] != t["konum_id"]))


def _ayni_straw(g, B_orn, A_tupler, A_orn, kullanilan) -> dict:
    """Esas tedavide aynı straw: `_straw_olabilir()` ve aynı içerik."""
    istenen = sorted(B_orn[s]["anahtar"] for s in g["ornekler"])
    for tid, h in A_tupler.items():
        if not _straw_olabilir(g, tid, h, kullanilan):
            continue
        if sorted(A_orn[s]["anahtar"] for s in h["ornekler"] if s in A_orn) == istenen \
                and len(h["bilgi"]["ornekler"]) == len(g["ornekler"]):
            return {"tid": tid, **h}
    return None


def _benzer_tupler(g, tur, p, kullanilan) -> list:
    """Esas tedavide aynı straw OLABİLECEK, içeriği farklı yazılmış tüpler
    (v6.229): `_straw_olabilir()`, aynı tür (embriyo / yumurta) ve yeri
    girilmemiş. Excel, tedavide dondurulmuş bir tüpü başka bir yazımla
    gösterebiliyor ("3BA-1BB" / "3BB-1BB"); araç birleşenin tüpünü esas
    tedavinin başka örneklerine yazsaydı aynı straw iki tüp olurdu. Yeri
    girilmiş tüp gobletinde kendi straw'ı (Excel'de kendi satırı), aday değil.
    Hangisi olduğuna kullanıcı karar veriyor, araç durur (`_benzer_engeli()`)."""
    return [(tid, h) for tid, h in p["A_tupler"].items()
            if _straw_olabilir(g, tid, h, kullanilan) and not h["bilgi"]["t"]["konum_id"]
            and _tup_turu(h, p["A_orn"], p["A"]) == tur]


def _benzer_engeli(p, k) -> str:
    """Aynı straw olabilecek tüpün engeli: iki yazım ve ne yapılacağı. Excel
    kaydından açılmış tüpte yol programda var (v6.213): "Açılan tüpü geri
    al" o tüpü (ve boş kalan tedaviyi) siler, "Tüpe bağla" Excel kaydını esas
    tedavinin tüpüne bağlar -- straw tedavinin kaydıyla görünür."""
    eski = p["B"]["cycle_no"]
    g, t = k["g"], k["g"]["bilgi"]["t"]
    yumurta = k["tur"] == "yumurta"
    yazim = _tup_yazimi([p["B_orn"][s]["yazim"] for s in g["ornekler"]], yumurta)
    esasin, yazimlar = [], set()
    for _tid, h in k["benzer"]:
        ht = h["bilgi"]["t"]
        y = _tup_yazimi([p["A_orn"][s]["yazim"] for s in h["ornekler"] if s in p["A_orn"]],
                        yumurta)
        yazimlar.add(y)
        esasin.append(f"{ht['etiket']} ({y}; {_gun(h['gun'])}; "
                      f"{ht['tam_yol'] or 'yeri girilmemiş'})")
    metin = (f"{t['etiket']} ({yazim}; {_gun(g['gun'])}) tüpü esas tedavinin aynı gün "
             "dondurulmuş " + ("tüpüyle" if len(esasin) == 1 else "tüplerinden biriyle")
             + " aynı straw olabilir, yazımı farklı: " + ", ".join(esasin) + ". ")
    # Birebir aynı tüplerden hangisinin straw olduğu fark etmez (v6.148'in
    # "aynı tedavinin birebir aynı tüpleri" kuralı).
    if len(esasin) == 1:
        hedef, ayni_not = k["benzer"][0][1]["bilgi"]["t"]["etiket"], ""
    elif len(yazimlar) == 1:
        hedef, ayni_not = "bu tüplerden biri", " İçerikleri aynı: hangisi olduğu fark etmez."
    else:
        hedef, ayni_not = "doğru tüp", ""
    acilan = [e for e in g["bilgi"]["excel"]
              if (cryo_esle.acilan_bilgisi(e) or {}).get("tur") == "tedavi"]
    if len(g["bilgi"]["excel"]) == 1 and acilan:
        e = acilan[0]
        metin += (f"Aynı straw'sa birleştirme gerekmez: Cryo Haritası'nda Excel kaydı "
                  f"#{e['id']} sayfasında (/cryo/excel-kaydi/{e['id']}) önce \"Açılan tüpü "
                  f"geri al\" ({t['etiket']} tüpü silinir; {eski} tedavisi boş kalırsa o da), "
                  f"sonra \"Tüpe bağla\" ile {hedef} (listede yoksa etiketini yazın)."
                  f"{ayni_not} ")
    else:
        metin += "Aynı straw'sa elle bakılmalı. "
    return metin + ("Esas tedavinin kaydı doğruysa onu Excel'in yazısına göre değiştirmeyin. "
                    "Başka bir straw'sa elle bakılmalı.")


# ------------------------------------------------------------------ plan

def plan(eski, esas) -> dict:
    """Ne olacağını hesaplar, hiçbir şey yazmaz. `engel` doluysa uygulanmaz."""
    b = _db.baglan()
    try:
        return _plan(b, eski, esas)
    finally:
        b.close()


def _plan(b, eski, esas) -> dict:
    B, A = _tedavi(b, eski), _tedavi(b, esas)
    if not B:
        sys.exit(f"{eski} numaralı tedavi yok.")
    if not A:
        sys.exit(f"{esas} numaralı tedavi yok.")
    p = {"A": A, "B": B, "engel": [], "uyari": [], "bilgi": []}
    engel, uyari = p["engel"], p["uyari"]
    if A["hasta_id"] != B["hasta_id"]:
        dosya = {r[0]: r[1] for r in b.execute(
            "SELECT id, dosya_no FROM hasta WHERE id IN (?, ?)", (A["hasta_id"], B["hasta_id"]))}
        engel.append(f"İki tedavi farklı hastaların (dosya no {dosya.get(B['hasta_id'])} ve "
                     f"{dosya.get(A['hasta_id'])}). Aynı hastanın iki kartıysa önce kartlar "
                     "birleştirilir: python3 hasta_birlestir.py <yanlış no> <doğru no>")
        return p
    p["dosya_no"] = _say(b, "SELECT dosya_no FROM hasta WHERE id=?", A["hasta_id"])
    p["A_tur"], p["B_tur"] = _tur(A), _tur(B)
    A_orn, B_orn = _ornekler(b, A["id"]), _ornekler(b, B["id"])
    p["A_orn"], p["B_orn"] = A_orn, B_orn
    A_tupler, B_tupler = _tupler(b, A_orn, A["id"]), _tupler(b, B_orn, B["id"])
    p["A_tupler"], p["B_tupler"] = A_tupler, B_tupler
    fet_A = A["cycle_tipi"] in _db.FET_TIPLERI
    ters = f"python3 tedavi_birlestir.py {esas} {eski}"

    if p["A_tur"] == "excel" and p["B_tur"] != "excel":
        engel.append(f"Esas tedavi {esas} Cryo Haritası Excel'inden açılmış bir dondurma "
                     f"kaydı, {eski} gerçek bir tedavi: kalan tedavi gerçek olan olmalı. "
                     f"Ters yönde: {ters}")
        return p
    if not B_orn:
        p["yol"] = "bos"
    elif p["B_tur"] == "excel":
        p["yol"] = "excel"
    else:
        p["yol"] = "mukerrer"

    # Başka tedavilerin bu tedaviye yazılmış kayıtları (FET'in çözmesi,
    # transferi, yeniden dondurması; eski kayıtlarda olay.cycle_id).
    bagli = {}
    for kolon in ("thaw_cycle_id", "tr_cycle_id", "vit_cycle_id", "cycle_id"):
        if kolon == "vit_cycle_id" and not _db.kolon_var("olay", "vit_cycle_id"):
            continue
        bagli[kolon] = _say(b, f"SELECT COUNT(*) FROM olay o JOIN specimen s "
                               f"ON s.id=o.specimen_id WHERE o.{kolon}=? AND s.cycle_id<>?",
                            B["id"], B["id"])
    p["bagli"] = bagli
    p["sperm_bagi"] = [r[0] for r in b.execute(
        "SELECT id FROM sperm_dondurma WHERE kullanim_cycle_id=?", (B["id"],))]
    _kayitlar_plani(b, p)
    icerik_var = (B_orn or any(bagli.values()) or p["sperm_bagi"]
                  or any(k["satirlar"] for k in p["kayitlar"].values()))

    # Tedavilerin günü (`db.tedavi_tarihi()`: OPU, FET'te çözme / transfer,
    # yoksa açılış): iki ayrı günün işi tek tedavide toplanmaz.
    gun = _db.tedavi_tarihi(b, "c")
    p["gunler"] = {k: (b.execute(f"SELECT substr({gun},1,10) FROM cycle c WHERE c.id=?",
                                 (c["id"],)).fetchone()[0])
                   for k, c in (("A", A), ("B", B))}
    fark = _gun_farki(p["gunler"]["A"], p["gunler"]["B"])
    if p["yol"] == "bos":
        if icerik_var and A["cycle_tipi"] != B["cycle_tipi"]:
            engel.append(f"Tipler farklı ({_tip_adi(b, B['cycle_tipi'])} / "
                         f"{_tip_adi(b, A['cycle_tipi'])}): birleşen tedavinin kayıtları "
                         "esas tedavinin tipinde anlamını yitirir.")
        elif icerik_var and fark > 1:
            engel.append(f"Tedavilerin günleri farklı ({_gun(p['gunler']['B'])} / "
                         f"{_gun(p['gunler']['A'])}): iki ayrı tedavi, birleştirilmez.")
        if not icerik_var:
            p["bos_tedavi"] = True
            p["bilgi"].append(f"{eski} boş bir tedavi: birleştirmek onu silmek demek.")
            if A["cycle_tipi"] != B["cycle_tipi"] or fark > 1:
                uyari.append(f"Tipleri ya da günleri farklı ({_tip_adi(b, B['cycle_tipi'])} "
                             f"{_gun(p['gunler']['B'])} / {_tip_adi(b, A['cycle_tipi'])} "
                             f"{_gun(p['gunler']['A'])}): numaralar doğru mu? Birleşen "
                             "tedavinin alanları esas tedaviye yazılmaz.")
    elif p["yol"] == "excel":
        _excel_plani(b, p, fet_A)
    else:
        _mukerrer_plani(b, p, ters)

    if p["sperm_bagi"] and "androloji" not in _db.TIP_ASAMALARI.get(A["cycle_tipi"], ()):
        engel.append(f"{eski} tedavisine bağlanmış dondurulmuş sperm var; esas tedavinin tipinde "
                     "androloji yok.")
    if B["durum"] == "aktif" and A["durum"] != "aktif":
        p["uyari"].append(f"{eski} hâlâ devam ediyor, esas tedavi {esas} bitmiş görünüyor: "
                          "esasın durumu kalır (gerekirse ekrandan listeye geri alınır).")
    _alanlar_plani(b, p)
    _arsiv_plani(b, p)
    return p


def _excel_plani(b, p, fet_A):
    A, B, A_orn, B_orn = p["A"], p["B"], p["A_orn"], p["B_orn"]
    eski, esas = B["cycle_no"], A["cycle_no"]
    engel = p["engel"]
    if fet_A:
        engel.append(f"Esas tedavi {_tip_adi(b, A['cycle_tipi'])}: Excel kaydının "
                     "tüpü dondurmanın yapıldığı tedavinin (OPU'lu) olmalı.")
        return
    tupsuz = [sid for sid, x in B_orn.items() if not _ilk_dondurma(x, B["id"])]
    if tupsuz:
        engel.append(f"{eski} tedavisinde tüpte olmayan {len(tupsuz)} örnek var: bu tedavi yalnızca "
                     "dondurma kaydı değil, elle bakılmalı.")
        return
    if A["opu_zamani"] and B["opu_zamani"] and _gun_farki(A["opu_zamani"], B["opu_zamani"]) > 1:
        engel.append(f"Excel'in günü tutmuyor: {eski} tedavisinin OPU günü {_gun(B['opu_zamani'])} "
                     f"(Excel'deki gün sayısından), {esas} tedavisininki {_gun(A['opu_zamani'])}. "
                     "Tüp başka bir tedavinin olabilir.")
        return
    if A["opu_zamani"] and not B["opu_zamani"]:
        # Excel gün sayısını yazmamış: dondurma OPU'dan en çok 8 gün sonra.
        for g in p["B_tupler"].values():
            fark = (date.fromisoformat(g["gun"][:10]) - date.fromisoformat(A["opu_zamani"][:10])).days \
                if g["gun"] else None
            if fark is None or not 0 <= fark <= 8:
                engel.append(f"{g['bilgi']['t']['etiket']} tüpünün dondurma günü "
                             f"({_gun(g['gun'])}) esas tedavinin OPU'suyla "
                             f"({_gun(A['opu_zamani'])}) tutmuyor: tüp başka bir tedavinin "
                             "olabilir.")
                return
    if not A["opu_zamani"] and _gun_farki(p["gunler"]["A"], p["gunler"]["B"]) > 8:
        # Esas tedavinin OPU'su yok (o da bir Excel kaydı ya da OPU'su
        # yazılmamış): dondurma, tedavinin gününden en çok 8 gün uzakta olabilir.
        engel.append(f"Tedavilerin günleri farklı ({_gun(p['gunler']['B'])} / "
                     f"{_gun(p['gunler']['A'])}): tüp başka bir tedavinin olabilir.")
        return
    tasi = not A_orn or p["A_tur"] == "excel"
    _tup_plani(b, p, tasi=tasi)


def _mukerrer_plani(b, p, ters):
    A, B, A_orn, B_orn = p["A"], p["B"], p["A_orn"], p["B_orn"]
    eski, esas = B["cycle_no"], A["cycle_no"]
    engel = p["engel"]
    if B["cycle_tipi"] in _db.FET_TIPLERI:
        engel.append(f"{eski} bir {_tip_adi(b, B['cycle_tipi'])} ve kendi örnekleri var "
                     "(Access'ten aktarılmış, kaynak tüpüne bağlanmamış embriyolar): bu araç "
                     "onları birleştirmez, elle bakılmalı.")
        return
    if not A_orn:
        engel.append(f"Esas tedavi {esas} tedavisinin hiç örneği yok, bütün embriyoloji {eski} tedavisinde: "
                     f"örnek kodları ve tüp etiketleri onu taşıyor. Ters yönde: {ters}")
        return
    if A["cycle_tipi"] != B["cycle_tipi"]:
        engel.append(f"Tipler farklı ({_tip_adi(b, B['cycle_tipi'])} / "
                     f"{_tip_adi(b, A['cycle_tipi'])}): iki ayrı tedavi, birleştirilmez.")
        return
    if not (A["opu_zamani"] and B["opu_zamani"]) or A["opu_zamani"][:10] != B["opu_zamani"][:10]:
        engel.append(f"OPU günleri farklı ({_gun(B['opu_zamani'])} / {_gun(A['opu_zamani'])}): "
                     "iki ayrı yumurta toplama, birleştirilmez. İkisi de kendi tedavisinde "
                     "kalır; dondurulmuş örnekler de dondurulduğu tedavide görünür.")
        return
    if len(B_orn) > len(A_orn):
        engel.append(f"{eski} tedavisinde {len(B_orn)} yumurta var, esas tedavide ({esas}) {len(A_orn)}: "
                     "esas tedavi eksik olabilir. Hangisinin doğru olduğuna ekranda bakın.")
        return
    # Taze transfer: aynı gün, aynı sayı esas tedavide de yazılı olmalı.
    def taze(orn, cid):
        return [o for x in orn.values() for o in x["transfer"]
                if (o["tr_cycle_id"] or o["cycle_id"]) == cid]
    tb, ta = taze(B_orn, B["id"]), taze(A_orn, A["id"])
    if tb:
        gb = sorted(o["zaman"][:10] for o in tb)
        ga = sorted(o["zaman"][:10] for o in ta)
        if gb != ga:
            engel.append(f"{eski} tedavisindeki transfer ({len(tb)} embriyo, {_gun(gb[0])}) esas "
                         f"tedavide aynı değil ({len(ta)} embriyo): transfer silinirdi.")
            return
        p["bilgi"].append(f"Transfer ({len(tb)} embriyo, {_gun(gb[0])}) iki tedavide de "
                          f"yazılı: {eski} tedavisindeki silinecek.")
    _tup_plani(b, p, tasi=False)
    # Tüpte olmayan öteki örnekler: esas tedavide zaten kayıtlı, silinir.
    tuplu = {s for g in p["B_tupler"].values() for s in g["ornekler"]}
    p["sil_tupsuz"] = [sid for sid in B_orn if sid not in tuplu]
    _silinebilir_mi(p, p["sil_tupsuz"], "silinecek")


def _silinebilir_mi(p, idler, ne):
    B_orn = p["B_orn"]
    foto = sum(B_orn[s]["foto"] for s in idler)
    bulgu = sum(B_orn[s]["bulgu"] for s in idler)
    pgt = sum(B_orn[s]["pgt"] for s in idler)
    baska = sorted({c for s in idler for c in B_orn[s]["baska"]})
    eski, esas = p["B"]["cycle_no"], p["A"]["cycle_no"]
    if foto:
        p["engel"].append(f"{eski} tedavisinin {ne} örneklerinde {foto} fotoğraf var -- fotoğraflar "
                          f"silinirdi. Fotoğraflı tedavi esas olmalı: python3 "
                          f"tedavi_birlestir.py {esas} {eski}")
    if bulgu or pgt:
        p["engel"].append(f"{eski} tedavisinin {ne} örneklerinde bulgu ya da PGT kaydı var -- "
                          "silinirdi, elle bakılmalı.")
    if baska:
        p["engel"].append(f"{eski} tedavisinin {ne} örneklerinden biri başka bir tedavide çözülmüş / "
                          "transfer edilmiş: silinemez, elle bakılmalı.")


def _tup_plani(b, p, tasi):
    """Birleşen tedavinin her tüpü için karar: aynı straw esas tedavide var
    (`ayni`), esas tedavinin örneklerine geçer (`esle`), örnekler taşınır
    (`tasi`)."""
    A, B, A_orn, B_orn = p["A"], p["B"], p["A_orn"], p["B_orn"]
    eski, esas = B["cycle_no"], A["cycle_no"]
    p["tup_kararlari"] = []
    kullanilan = set()
    istenen = []
    for tid, g in sorted(p["B_tupler"].items(), key=lambda x: (x[1]["gun"] or "", x[0])):
        t = g["bilgi"]["t"]
        yabanci = [s for s in g["bilgi"]["ornekler"] if s not in B_orn]
        if yabanci:
            p["engel"].append(f"{t['etiket']} tüpünde başka bir tedavinin örneği de var: "
                              "elle bakılmalı.")
            continue
        k = {"tid": tid, "g": g, "tur": _tup_turu(g, B_orn, B),
             "anahtarlar": [B_orn[s]["anahtar"] for s in g["ornekler"]]}
        if tasi:
            k["karar"] = "tasi"
        else:
            ayni = _ayni_straw(g, B_orn, p["A_tupler"], A_orn, kullanilan)
            if ayni:
                kullanilan.add(ayni["tid"])
                k.update(karar="ayni", hedef=ayni)
        p["tup_kararlari"].append(k)
    # Birebir tutmayanlar: esasta aynı straw olabilecek bir tüp varsa durulur
    # (v6.229); yoksa esas tedavinin örneklerine. Birebir eşleşmeler önce --
    # sonraki bir tüpün birebir eşi öncekine "benzer" sayılmasın.
    for k in p["tup_kararlari"]:
        if "karar" in k:
            continue
        benzer = _benzer_tupler(k["g"], k["tur"], p, kullanilan)
        if benzer:
            k.update(karar="benzer", benzer=benzer)
            p["engel"].append(_benzer_engeli(p, k))
        else:
            k["karar"] = "esle"
            istenen += [(s, k["tur"], B_orn[s]["anahtar"]) for s in k["g"]["ornekler"]]
    atanan = _eslestir(istenen, _adaylar(A_orn)) if istenen else {}
    p["atanan"] = atanan
    # PGT'li örnek: sonuç biyopsi kaydına bağlı (`pgt_sonuc.biyopsi_id`), iki
    # tedavinin biyopsisini birleştirmek bu aracın işi değil.
    pgtli = [s for s, _t, _k in istenen
             if B_orn[s]["pgt"] or any(o["tip"] == "biyopsi" for o in B_orn[s]["aktif"])]
    if pgtli:
        p["engel"].append(f"{eski} tedavisinin tüpteki {len(pgtli)} örneğinde biyopsi / PGT kaydı var: "
                          "elle bakılmalı.")
    for k in p["tup_kararlari"]:
        if k["karar"] == "ayni":
            _silinebilir_mi(p, k["g"]["ornekler"], "fazla tüpteki")
        if k["karar"] != "esle":
            continue
        eksik = [s for s in k["g"]["ornekler"] if s not in atanan]
        if eksik:
            bos = [a for a in _adaylar(A_orn) if a["id"] not in {x[0]["id"] for x in atanan.values()}]
            t = k["g"]["bilgi"]["t"]
            yazim = _tup_yazimi([B_orn[s]["yazim"] for s in k["g"]["ornekler"]],
                                k["tur"] == "yumurta")
            p["engel"].append(
                f"{t['etiket']} ({yazim}) tüpünün {len(eksik)} örneği esas tedavide karşılık "
                "bulmadı. Esas tedavinin dondurulmamış "
                + ("embriyoları" if k["tur"] == "embriyo" else "yumurtaları") + ": "
                + (", ".join(f"{a['id']} ({a['yazim']})" for a in bos
                             if _tur_esit(a, k["tur"])) or "yok")
                + ". Esas tedavinin skoru yanlışsa orada düzeltip yeniden deneyin; Excel "
                "farklı yazdıysa (tedavinin kaydı doğru) elle bakılmalı.")
    for sid, (a, katman) in atanan.items():
        if katman == "aynı skor":
            continue
        ne = {"değerlendirilmemiş örnek": f"esas tedavide değerlendirmesi olmayan "
                                          f"{a['id']} tüpün skorunu ({B_orn[sid]['yazim']}) alacak",
              "yakın skor": f"skorlar farklı: tüpte {B_orn[sid]['yazim']}, esas tedavide "
                            f"{a['id']} {a['yazim']} (aynı evre ve sayı); esasınki kalır",
              "skorsuz": f"tüpte skor yok; {a['id']} ({a['yazim']}) seçildi"}[katman]
        p["uyari"].append(f"{ne} -- doğru embriyo mu, esas tedavinin ekranında bakın.")
    # Programın ürettiği etiket esas tedavinin numarasına (Excel / Access kaydı).
    p["etiketler"] = []
    if p["B_tur"] in ("excel", "access"):
        dolu = {r[0] for r in b.execute("SELECT etiket FROM tasiyici WHERE lab_id=?",
                                        (_db.LAB_ID,))}
        for k in p["tup_kararlari"]:
            if k["karar"] in ("ayni", "benzer"):
                continue
            eski_e = k["g"]["bilgi"]["t"]["etiket"]
            m = _ETIKET.match(eski_e)
            if not m or m.group("no") != eski:
                continue
            yeni_e = _yeni_etiket(esas, m, dolu)
            if yeni_e:
                dolu.add(yeni_e)
                p["etiketler"].append((k["tid"], eski_e, yeni_e))
    # Taşınacak örneklerin yeni numarası (esas tedavinin numarasıyla).
    p["yeni_idler"] = {}
    if tasi:
        sira = _say(b, "SELECT COALESCE(MAX(cycle_sira_no), 0) FROM specimen WHERE cycle_id=?",
                    A["id"])
        var = {r[0] for r in b.execute("SELECT id FROM specimen WHERE id LIKE ?",
                                       (f"{esas}-%",))}
        for sid in sorted(B_orn, key=lambda s: B_orn[s]["s"]["cycle_sira_no"]):
            sira += 1
            while f"{esas}-{sira:02d}" in var:
                sira += 1
            p["yeni_idler"][sid] = (f"{esas}-{sira:02d}", sira)


def _yeni_etiket(esas, m, dolu):
    try:
        t = datetime(2000, 1, 1, int(m.group("ss")), int(m.group("dd")))
    except ValueError:
        return None
    for _ in range(600):
        e = f"{esas}-{t:%H%M}"
        if e not in dolu:
            return e
        t += timedelta(minutes=1)
    return None


def _kayitlar_plani(b, p):
    """Tedavi düzeyindeki kayıtlar: {tablo: {"satirlar": [...], "gecer": [...],
    "duser": [...]}} -- esas tedavide yoksa geçer, varsa esasınki kalır."""
    A, B = p["A"], p["B"]
    k = {}

    def tablo(ad, kosul="cycle_id=?"):
        if not _db.tablo_var(ad):
            return None
        return ([dict(r) for r in b.execute(f"SELECT * FROM {ad} WHERE {kosul}", (B["id"],))],
                [dict(r) for r in b.execute(f"SELECT * FROM {ad} WHERE {kosul}", (A["id"],))])
    iy = tablo("islem_yapan")
    if iy:
        asamalar = {r["asama"] for r in iy[1]}
        k["islem_yapan"] = {"satirlar": iy[0],
                            "gecer": [r for r in iy[0] if r["asama"] not in asamalar],
                            "duser": [r for r in iy[0] if r["asama"] in asamalar]}
    for ad in ("sperm_ornek", "gebelik_sonucu", "beta_hcg", "dogan_bebek"):
        t = tablo(ad)
        if t is None:
            continue
        k[ad] = {"satirlar": t[0], "gecer": t[0] if not t[1] else [],
                 "duser": t[0] if t[1] else []}
    tb = tablo("tedavi_bulgu")
    if tb:
        # Genel bulgular aşama başına bir küme (v6.200): esas tedavide o aşamanın
        # kümesi varsa o kalır, iki küme karıştırılmaz.
        var = {r["asama"] for r in tb[1]}
        k["tedavi_bulgu"] = {"satirlar": tb[0],
                             "gecer": [r for r in tb[0] if r["asama"] not in var],
                             "duser": [r for r in tb[0] if r["asama"] in var]}
    belge = [dict(r) for r in b.execute(
        "SELECT * FROM goruntu WHERE cycle_id=? AND specimen_id IS NULL", (B["id"],))]
    k["goruntu"] = {"satirlar": belge, "gecer": belge, "duser": []}
    kd = [dict(r) for r in b.execute("SELECT * FROM kaynak_dosya WHERE cycle_id=?", (B["id"],))]
    k["kaynak_dosya"] = {"satirlar": kd, "gecer": kd, "duser": []}
    p["kayitlar"] = k


_KAYIT_ADI = {"islem_yapan": "işlemi yapan", "sperm_ornek": "androloji",
              "gebelik_sonucu": "gebelik sonucu", "beta_hcg": "beta hCG",
              "dogan_bebek": "doğan bebek", "tedavi_bulgu": "genel bulgu",
              "goruntu": "belge eki (Doktor Notu / PGT raporu)",
              "kaynak_dosya": "kamera kuyruğu işareti"}


def _alanlar_plani(b, p):
    A, B = p["A"], p["B"]
    p["doldur"], p["farkli"], p["not_eki"] = {}, [], None
    ilgisiz = p.get("bos_tedavi") and (
        A["cycle_tipi"] != B["cycle_tipi"]
        or _gun_farki(p["gunler"]["A"], p["gunler"]["B"]) > 1)
    if p["B_tur"] == "excel" or ilgisiz:
        # Excel kaydının alanları (OPU günü Excel'in gün sayısından, bitiş
        # "dondurma") ve notu ("OPU, ICSI ve döllenme kaydı yok", işareti)
        # üretilmiş: gerçek tedaviye yazılmaz, günlükte kalır. Başka tipte ya da
        # günde boş bir tedavinin alanları da esas tedavinin değil.
        pass
    else:
        kolonlar = set(A.keys())
        for alan, ad in ALANLAR.items():
            if alan not in kolonlar or _hb._bos(B[alan]):
                continue
            if _hb._bos(A[alan]):
                p["doldur"][alan] = B[alan]
            elif str(A[alan]).strip() != str(B[alan]).strip():
                p["farkli"].append(ad)
    p["yalniz_isaret"] = False
    if p["B_tur"] != "excel":
        bn = (B["protokol_notu"] or "").strip()
        an = (A["protokol_notu"] or "").strip()
        ek = None
        if p["B_tur"] == "access" and (p["yol"] == "mukerrer" or p.get("bos_tedavi")):
            # Aynı işlemin ikinci kaydında Access'in notu esas tedavide zaten
            # kayıtlı işlemi anlatıyor -- notun tamamı eklenseydi formun
            # NOTLAR'ı embriyoları iki kez yazardı; boş bir tedavinin notu da
            # esas tedaviyi anlatmıyor. Kalan yalnızca işaret: aynı dosya
            # yeniden aktarılınca kayıt ikinci kez açılmasın
            # (`aktar_access._zaten_var()`). Notun kendisi günlükte.
            isaretler = [f"[Access kaydı {k}#{n}]" if k else f"[Access kaydı #{n}]"
                         for k, n in _hb._ISARET.findall(bn.replace("\n", " "))]
            if isaretler:
                ek = f"({B['cycle_no']} ile birleştirildi)\n" + "\n".join(isaretler)
                p["yalniz_isaret"] = True
        elif bn:
            ek = f"({B['cycle_no']} tedavisinden)\n" + bn
        if ek and ek.split("\n", 1)[1] not in an:
            p["not_eki"] = (an + "\n" if an else "") + ek
    # Kayıtlar: esas tedavide olan birleşende de varsa ne olacağı yola bağlı.
    for ad, k in p["kayitlar"].items():
        if not k["duser"] or ad in ("islem_yapan", "tedavi_bulgu"):
            continue
        if p["yol"] != "mukerrer":
            p["engel"].append(f"İki tedavide de {_KAYIT_ADI[ad]} kaydı var: hangisinin "
                              "kalacağına ekranda bakın (birinden silin).")


def _arsiv_plani(b, p):
    kok = goruntuler.arsiv_klasor()
    klasor = kok / goruntuler.guvenli_ad(p.get("dosya_no") or "")
    ek, yk = klasor / goruntuler.guvenli_ad(p["B"]["cycle_no"]), \
        klasor / goruntuler.guvenli_ad(p["A"]["cycle_no"])
    p["arsiv"] = (ek, yk)
    p["dosyalar"] = [x for x in ek.rglob("*") if x.is_file()] if ek.is_dir() else []
    cakisan = [x for x in p["dosyalar"] if (yk / x.relative_to(ek)).exists()]
    if cakisan:
        p["engel"].append(f"Arşivde aynı adlı {len(cakisan)} dosya iki tedavinin klasöründe "
                          f"de var (ilki: {cakisan[0].relative_to(ek)}) -- elle bakın.")
    p["goreli"] = (f"{goruntuler.guvenli_ad(p.get('dosya_no') or '')}/"
                   f"{goruntuler.guvenli_ad(p['B']['cycle_no'])}/",
                   f"{goruntuler.guvenli_ad(p.get('dosya_no') or '')}/"
                   f"{goruntuler.guvenli_ad(p['A']['cycle_no'])}/")


# ------------------------------------------------------------------ yazdırma

_TUR_ADI = {"excel": "Cryo Haritası Excel'inden açılmış dondurma kaydı",
            "access": "Access kaydından aktarılmış", "program": "programdan girilmiş"}
_YOL_ADI = {"excel": "Excel kaydı -> tüpler esas tedavinin örneklerine geçer",
            "mukerrer": "aynı işlemin ikinci kaydı -> tüpler esas tedaviye geçer, "
                        "fazla yumurtalar silinir",
            "bos": "birleşen tedavinin kendi örneği yok -> kayıtları esas tedavinin olur"}


def _tedavi_satiri(b, c, tur, orn, tupler):
    ek = ""
    if c["cycle_tipi"] in _db.FET_TIPLERI:
        cozme = _say(b, "SELECT COUNT(*) FROM olay WHERE tip='thaw' AND iptal_mi=0 "
                        "AND thaw_cycle_id=?", c["id"])
        transfer = _say(b, "SELECT COUNT(*) FROM olay WHERE tip='transfer' AND iptal_mi=0 "
                           "AND tr_cycle_id=?", c["id"])
        ek = f" · bu tedavi için {cozme} çözme, {transfer} transfer"
    opu = f" · OPU {_gun(c['opu_zamani'])}" if c["opu_zamani"] else ""
    return (f"{c['cycle_no']} · {_tip_adi(b, c['cycle_tipi'])}{opu} · {len(orn)} örnek, "
            f"{len(tupler)} tüp{ek} · {_TUR_ADI[tur]} · "
            f"{_DURUM_ADI.get(c['durum'], c['durum'])}")


def ozet_yaz(p):
    b = _db.baglan()
    try:
        _ozet_yaz(b, p)
    finally:
        b.close()


def _ozet_yaz(b, p):
    A, B = p["A"], p["B"]
    eski = B["cycle_no"]
    if "A_tur" not in p:
        for e in p["engel"]:
            print(f"ENGEL: {e}")
        return
    print(f"Esas tedavi     : {_tedavi_satiri(b, A, p['A_tur'], p['A_orn'], p['A_tupler'])}")
    print(f"Birleşen tedavi : {_tedavi_satiri(b, B, p['B_tur'], p['B_orn'], p['B_tupler'])}")
    print(f"Hasta: dosya no {p['dosya_no']} (iki tedavi de)")
    if p["engel"]:
        # Birleştirilemiyorsa ne yapılacağını anlatmak yanıltır: yalnızca sebep.
        for e in p["engel"]:
            print(f"ENGEL: {e}")
        return
    print(f"Yol: {_YOL_ADI[p['yol']]}")
    for k in p.get("tup_kararlari", []):
        g, t = k["g"], k["g"]["bilgi"]["t"]
        yazim = _tup_yazimi([p["B_orn"][s]["yazim"] for s in g["ornekler"]],
                            k["tur"] == "yumurta")
        excel = "".join(f" · Excel kaydı #{e['id']}" for e in g["bilgi"]["excel"])
        print(f"  Tüp {_tup_metni(t, yazim)} · {_gun(g['gun'])}{excel}")
        if k["karar"] == "ayni":
            h = k["hedef"]["bilgi"]["t"]
            if g["bilgi"]["excel"]:
                ne = "Excel kaydı ona bağlanır"
            elif t["konum_id"] and not h["konum_id"]:
                ne = f"yeri ({t['tam_yol']}) ona geçer"
            else:
                ne = "tüp olduğu gibi kalır"
            print(f"     -> aynı straw esas tedavide zaten var: {h['etiket']} "
                  f"({h['tam_yol'] or 'konum girilmemiş'}); {ne}. Bu tüp ve "
                  f"{len(g['ornekler'])} örneği silinir.")
        elif k["karar"] == "tasi":
            yeni = ", ".join(p["yeni_idler"][s][0] for s in g["ornekler"])
            print(f"     -> örnekler esas tedaviye taşınır, yeni numaraları: {yeni}")
        else:
            satir = []
            for s in g["ornekler"]:
                a = p["atanan"].get(s)
                satir.append(f"{p['B_orn'][s]['yazim']} -> {a[0]['id']} ({a[0]['yazim']})"
                             if a else f"{p['B_orn'][s]['yazim']} -> KARŞILIK YOK")
            print("     -> tüp esas tedavinin embriyolarına geçer: " + "; ".join(satir))
    for tid, e, y in p.get("etiketler", []):
        print(f"  Etiket: {e} -> {y} (programın ürettiği kod, esas tedavinin numarasıyla)")
    if p.get("sil_tupsuz"):
        print(f"Silinecek: {eski} tedavisinin tüpte olmayan {len(p['sil_tupsuz'])} yumurtası "
              f"(esas tedavide {len(p['A_orn'])} yumurta kayıtlı).")
    bag = {k: v for k, v in p.get("bagli", {}).items() if v}
    if bag:
        adlar = {"thaw_cycle_id": "çözme", "tr_cycle_id": "transfer",
                 "vit_cycle_id": "yeniden dondurma", "cycle_id": "değerlendirme"}
        print("Başka tedavilerin örnekleri için bu tedavide yapılanlar esas tedaviye yazılacak: "
              + ", ".join(f"{v} {adlar[k]}" for k, v in bag.items()))
    if p.get("sperm_bagi"):
        print(f"Bağlanmış dondurulmuş sperm: {len(p['sperm_bagi'])} kayıt esas tedaviye.")
    gecer = [f"{len(k['gecer'])} {_KAYIT_ADI[ad]}" for ad, k in p.get("kayitlar", {}).items()
             if k["gecer"]]
    duser = [f"{len(k['duser'])} {_KAYIT_ADI[ad]}" for ad, k in p.get("kayitlar", {}).items()
             if k["duser"]]
    if gecer:
        print("Esas tedaviye geçecek: " + ", ".join(gecer))
    if duser:
        print("Esas tedavide zaten var, birleşeninki düşecek (günlükte kalır): "
              + ", ".join(duser))
    if p.get("doldur"):
        print("Esas tedavide boş, birleşenden yazılacak: "
              + ", ".join(ALANLAR[a] for a in p["doldur"]))
    if p.get("farkli"):
        print("İki tedavide de dolu ve farklı (esasınki kalıyor, birleşeninki günlükte): "
              + ", ".join(p["farkli"]))
    if p.get("not_eki") and p.get("yalniz_isaret"):
        print(f"Protokol notu: {eski} tedavisinin Access işareti esas tedavinin notuna "
              "eklenecek (aynı dosya yeniden aktarılınca kayıt ikinci kez açılmasın); notun "
              "kendisi günlükte kalır.")
    elif p.get("not_eki"):
        print(f"Protokol notu: {eski} tedavisinin notu esas tedavinin notunun altına eklenecek "
              "(resmî formun NOTLAR'ına da basılır).")
    if p.get("dosyalar"):
        print(f"Arşiv: {len(p['dosyalar'])} dosya {p['arsiv'][0]} -> {p['arsiv'][1]}")
    for x in p["bilgi"]:
        print(x)
    for u in p["uyari"]:
        print(f"DİKKAT: {u}")


# ------------------------------------------------------------------ yazma

def _tasinacak_olaylar(x, a, katman, B_id) -> list:
    """Birleşen örneğin esas tedavinin örneğine geçecek olayları, kimlik
    sırasıyla: tüpe konmasıyla başlayan her şey (dondurma, sonra çözme,
    transfer, yeniden dondurma; kültürdeki değerlendirmeler); esas tedavinin
    örneği hiç değerlendirilmemişse bu tüpün yazdığı değerlendirme (yumurtada
    olgunluk) de -- tüpün kalitesi görünsün. Öteki kayıtlar (ICSI, döllenme,
    aynı skorun ikinci yazımı) esas tedavide var, örnekle birlikte silinir."""
    ilk = _ilk_dondurma(x, B_id)
    kalite = katman in ("değerlendirilmemiş örnek", "skorsuz") and a["anahtar"] == "?"
    kalite_tipleri = _DEGERLENDIRME if a["iz"] else ("maturasyon_kontrolu",)
    sonuc = []
    for o in x["aktif"]:
        if o["id"] >= ilk["id"] and (o["tip"] in ("vitrifikasyon", "thaw", "transfer")
                                     or (o["zaman"] or "") >= (ilk["zaman"] or "")):
            sonuc.append(o)
        elif kalite and o["tip"] in kalite_tipleri:
            sonuc.append(o)
    return sonuc


def _olay_tasi(b, o, sid, A_id, B_id, dondurma_notu=None):
    """Olayı yeni kimlikle `sid` örneğine yazar (kimlik sırası = işlem sırası),
    eskisini siler; PGT sonucu ve günlüğün olay satırları yeni kimliğe.

    `dondurma_notu`: aktarımın dondurma notunun (`db.KAYNAK_DONDURMA_NOTU`)
    yerine yazılacak önek. Resmî form Access'ten aktarılmış tedavide o notu
    taşıyan tüpü "Dondurulan:" satırına yazmıyor (protokol notu anlatıyor,
    v6.159); esas tedavinin notu bu dondurmayı anlatmıyorsa tüp satırda
    görünmeli."""
    d = dict(o)
    eski_id = d.pop("id")
    d["specimen_id"], d["cycle_id"] = sid, A_id
    if (dondurma_notu and d["tip"] == "vitrifikasyon"
            and (d.get("notlar") or "").startswith(_db.KAYNAK_DONDURMA_NOTU)):
        d["notlar"] = dondurma_notu + d["notlar"][len(_db.KAYNAK_DONDURMA_NOTU):]
    for k in ("thaw_cycle_id", "tr_cycle_id", "vit_cycle_id"):
        if k in d and d[k] == B_id:
            d[k] = A_id
    kolonlar = list(d)
    yeni = b.execute(f"INSERT INTO olay ({','.join(kolonlar)}) VALUES "
                     f"({','.join('?' * len(kolonlar))})", [d[k] for k in kolonlar]).lastrowid
    if _db.tablo_var("pgt_sonuc") and _db.kolon_var("pgt_sonuc", "biyopsi_id"):
        b.execute("UPDATE pgt_sonuc SET biyopsi_id=? WHERE biyopsi_id=?", (yeni, eski_id))
    b.execute("UPDATE degisiklik_log SET kayit_id=? WHERE tablo_adi='olay' AND kayit_id=?",
              (str(yeni), str(eski_id)))
    b.execute("DELETE FROM olay WHERE id=?", (eski_id,))
    return yeni


def _ornegi_sil(b, sid, kid, simdi, sebep):
    olaylar = b.execute("SELECT COUNT(*) FROM olay WHERE specimen_id=?", (sid,)).fetchone()[0]
    b.execute("DELETE FROM olay WHERE specimen_id=?", (sid,))
    b.execute("DELETE FROM specimen WHERE id=?", (sid,))
    _hb._logla(b, "specimen", sid, "KALICI_SILME", f"{olaylar} kayıt", sebep, kid, simdi)


def uygula(eski, esas) -> dict:
    kid = _dnd._kullanici_id()
    simdi = datetime.now().isoformat(" ", "seconds")
    with _db.yazma_islemi() as b:
        p = _plan(b, eski, esas)              # kilidin içinde yeniden
        if p["engel"]:
            sys.exit("Birleştirilmedi: " + "; ".join(p["engel"]))
        A, B = p["A"], p["B"]
        A_id, B_id = A["id"], B["id"]
        B_orn = p["B_orn"]
        sebep = f"{eski} tedavisi {esas} ile birleştirildi"
        dondurma_notu = (f"{eski} tedavisinden birleştirildi (Access kaydının dondurma notundan)"
                         if p.get("yalniz_isaret") else None)
        # 1. Tüpler
        for k in p.get("tup_kararlari", []):
            g = k["g"]
            tid = k["tid"]
            if k["karar"] == "ayni":
                h = k["hedef"]
                ht = b.execute("SELECT t.*, k.tam_yol FROM tasiyici t LEFT JOIN konum k "
                               "ON k.id=t.konum_id WHERE t.id=?", (h["tid"],)).fetchone()
                t = g["bilgi"]["t"]
                if g["bilgi"]["excel"]:
                    for e in g["bilgi"]["excel"]:
                        er = b.execute("SELECT * FROM excel_kaydi WHERE id=?", (e["id"],)).fetchone()
                        cryo_esle.excel_kaydini_tupe_bagla(b, er, ht, kid, simdi)
                else:
                    if t["konum_id"] and not ht["konum_id"]:
                        b.execute("UPDATE tasiyici SET konum_id=? WHERE id=?",
                                  (t["konum_id"], ht["id"]))
                        _hb._logla(b, "tasiyici", ht["id"], "konum", None, t["tam_yol"], kid, simdi)
                    for alan in ("renk",):
                        if t[alan] and not ht[alan]:
                            b.execute(f"UPDATE tasiyici SET {alan}=? WHERE id=?", (t[alan], ht["id"]))
                            _hb._logla(b, "tasiyici", ht["id"], alan, None, t[alan], kid, simdi)
                for sid in g["ornekler"]:
                    _ornegi_sil(b, sid, kid, simdi, sebep + f" (aynı straw: {ht['etiket']})")
                kalan = [f"{tb}.{kl}" for tb, kl in cryo_esle._kolonlu_tablolar(
                             b, {"tasiyici_id", "vit_tasiyici_id", "thaw_tasiyici_id"})
                         if b.execute(f"SELECT 1 FROM {tb} WHERE {kl}=? LIMIT 1",
                                      (tid,)).fetchone()]
                if kalan:
                    sys.exit(f"Birleştirilmedi (hiçbir şey yazılmadı): {t['etiket']} tüpünü "
                             "gösteren kayıt kaldı -- " + ", ".join(kalan))
                b.execute("DELETE FROM tasiyici WHERE id=?", (tid,))
                _hb._logla(b, "tasiyici", tid, "KALICI_SILME",
                           json.dumps(dict(t), ensure_ascii=False, default=str),
                           f"{sebep}: aynı straw {ht['etiket']}", kid, simdi)
                if t["konum_id"] and t["konum_id"] != (b.execute(
                        "SELECT konum_id FROM tasiyici WHERE id=?", (ht["id"],)).fetchone()[0]):
                    if not b.execute("SELECT 1 FROM tasiyici WHERE konum_id=? AND durum='dolu'",
                                     (t["konum_id"],)).fetchone():
                        b.execute("UPDATE konum SET durum='bos' WHERE id=?", (t["konum_id"],))
                continue
            if k["karar"] == "tasi":
                for sid in g["ornekler"]:
                    yeni_id, sira = p["yeni_idler"][sid]
                    s = B_orn[sid]["s"]
                    kol = [c for c in s.keys()]
                    d = dict(s)
                    d.update(id=yeni_id, cycle_id=A_id, cycle_sira_no=sira)
                    b.execute(f"INSERT INTO specimen ({','.join(kol)}) VALUES "
                              f"({','.join('?' * len(kol))})", [d[c] for c in kol])
                    b.execute("UPDATE olay SET specimen_id=?, cycle_id=? WHERE specimen_id=?",
                              (yeni_id, A_id, sid))
                    b.execute("UPDATE goruntu SET specimen_id=?, cycle_id=? WHERE specimen_id=?",
                              (yeni_id, A_id, sid))
                    b.execute("UPDATE specimen_bulgu SET specimen_id=? WHERE specimen_id=?",
                              (yeni_id, sid))
                    if _db.tablo_var("pgt_sonuc"):
                        b.execute("UPDATE pgt_sonuc SET specimen_id=? WHERE specimen_id=?",
                                  (yeni_id, sid))
                    b.execute("DELETE FROM specimen WHERE id=?", (sid,))
                    _hb._logla(b, "specimen", sid, "id", sid, yeni_id, kid, simdi)
                for e in g["bilgi"]["excel"]:
                    a = cryo_esle.acilan_bilgisi(e)
                    if a and a["tur"] == "tedavi" and a["id"] == B_id:
                        yeni = f"{cryo_esle.ACILAN}tüp {tid}, tedavi {A_id}"
                        b.execute("UPDATE excel_kaydi SET islem_notu=? WHERE id=?", (yeni, e["id"]))
                        _hb._logla(b, "excel_kaydi", e["id"], "islem_notu", e["islem_notu"],
                                   yeni, kid, simdi)
                continue
            # esle: tüp esas tedavinin örneklerine
            for sid in g["ornekler"]:
                a, katman = p["atanan"][sid]
                x = B_orn[sid]
                for o in _tasinacak_olaylar(x, a, katman, B_id):
                    _olay_tasi(b, o, a["id"], A_id, B_id, dondurma_notu=dondurma_notu)
                b.execute("UPDATE goruntu SET specimen_id=?, cycle_id=? WHERE specimen_id=?",
                          (a["id"], A_id, sid))
                b.execute("UPDATE specimen_bulgu SET specimen_id=? WHERE specimen_id=?",
                          (a["id"], sid))
                if _db.tablo_var("pgt_sonuc"):
                    b.execute("UPDATE pgt_sonuc SET specimen_id=? WHERE specimen_id=?",
                              (a["id"], sid))
                b.execute("UPDATE specimen SET durum=? WHERE id=?", (x["s"]["durum"], a["id"]))
                _hb._logla(b, "specimen", a["id"], "durum", a["s"]["durum"], x["s"]["durum"],
                           kid, simdi)
                _ornegi_sil(b, sid, kid, simdi, sebep + f" (tüpü {a['id']} örneğine geçti)")
            for e in g["bilgi"]["excel"]:
                if cryo_esle.acilan_bilgisi(e):
                    # Tüp artık esas tedavinin örneklerini taşıyor: "bağı çöz"
                    # onu silmesin, sıradan bağ gibi (tüp konumsuz kalır) çözsün.
                    b.execute("UPDATE excel_kaydi SET islem_notu=NULL, onceki_konum_id=NULL "
                              "WHERE id=?", (e["id"],))
                    _hb._logla(b, "excel_kaydi", e["id"], "islem_notu", e["islem_notu"], None,
                               kid, simdi)
        for tid, e, y in p.get("etiketler", []):
            b.execute("UPDATE tasiyici SET etiket=? WHERE id=?", (y, tid))
            _hb._logla(b, "tasiyici", tid, "etiket", e, y, kid, simdi)
        # 2. Aynı işlemin ikinci kaydında tüpte olmayan yumurtalar
        for sid in p.get("sil_tupsuz", []):
            _ornegi_sil(b, sid, kid, simdi, sebep + " (esas tedavide kayıtlı)")
        # 3. Başka tedavilerin bu tedaviye yazılmış kayıtları
        for kolon in ("thaw_cycle_id", "tr_cycle_id", "vit_cycle_id", "cycle_id"):
            if kolon == "vit_cycle_id" and not _db.kolon_var("olay", "vit_cycle_id"):
                continue
            for (oid,) in b.execute(f"SELECT id FROM olay WHERE {kolon}=?", (B_id,)).fetchall():
                b.execute(f"UPDATE olay SET {kolon}=? WHERE id=?", (A_id, oid))
                _hb._logla(b, "olay", oid, kolon, B_id, A_id, kid, simdi)
        for sd in p.get("sperm_bagi", []):
            b.execute("UPDATE sperm_dondurma SET kullanim_cycle_id=? WHERE id=?", (A_id, sd))
            _hb._logla(b, "sperm_dondurma", sd, "kullanim_cycle_id", B_id, A_id, kid, simdi)
        # 4. Tedavi düzeyindeki kayıtlar
        for ad, k in p["kayitlar"].items():
            for r in k["gecer"]:
                anahtar = "imza" if ad == "kaynak_dosya" else "id"
                b.execute(f"UPDATE {ad} SET cycle_id=? WHERE {anahtar}=?", (A_id, r[anahtar]))
                _hb._logla(b, ad, r[anahtar], "cycle_id", B_id, A_id, kid, simdi)
            for r in k["duser"]:
                if ad == "sperm_ornek":
                    b.execute("DELETE FROM sperm_analiz WHERE sperm_ornek_id=?", (r["id"],))
                b.execute(f"DELETE FROM {ad} WHERE id=?", (r["id"],))
                _hb._logla(b, ad, r["id"], "KALICI_SILME",
                           json.dumps(r, ensure_ascii=False, default=str),
                           sebep + " (esas tedavide var)", kid, simdi)
        # 5. Fotoğrafların yolu (arşiv klasörü esas tedavinin)
        b.execute("UPDATE goruntu SET cycle_id=? WHERE cycle_id=?", (A_id, B_id))
        eski_g, yeni_g = p["goreli"]
        for tablo, kolon in (("goruntu", "dosya_yolu"), ("pgt_sonuc", "rapor_dosya_yolu")):
            if not _db.tablo_var(tablo) or not _db.kolon_var(tablo, kolon):
                continue
            b.execute(f"UPDATE {tablo} SET {kolon} = ? || substr({kolon}, ?) "
                      f"WHERE {kolon} LIKE ?", (yeni_g, len(eski_g) + 1, eski_g + "%"))
        # 6. Alanlar ve protokol notu
        for alan, deger in p["doldur"].items():
            b.execute(f"UPDATE cycle SET {alan}=? WHERE id=?", (deger, A_id))
            _hb._logla(b, "cycle", A_id, alan, None, deger, kid, simdi)
        if p["not_eki"]:
            b.execute("UPDATE cycle SET protokol_notu=? WHERE id=?", (p["not_eki"], A_id))
            _hb._logla(b, "cycle", A_id, "protokol_notu", A["protokol_notu"], p["not_eki"],
                       kid, simdi)
        if _db.tablo_var("excel_kaydi"):
            for e in b.execute("SELECT * FROM excel_kaydi WHERE durum='baglandi' "
                               "AND islem_notu LIKE ?", (f"{cryo_esle.ACILAN}%",)).fetchall():
                a = cryo_esle.acilan_bilgisi(e)
                if a and a["tur"] == "tedavi" and a["id"] == B_id:
                    b.execute("UPDATE excel_kaydi SET islem_notu=NULL WHERE id=?", (e["id"],))
                    _hb._logla(b, "excel_kaydi", e["id"], "islem_notu", e["islem_notu"], None,
                               kid, simdi)
        # 7. Birleşen tedaviyi gösteren bir şey kaldı mı (tuzak #4)
        kalan = [f"{t}.{k}" for t, k in cryo_esle._kolonlu_tablolar(
                     b, {"cycle_id", "thaw_cycle_id", "tr_cycle_id", "vit_cycle_id",
                         "kullanim_cycle_id"})
                 if t != "degisiklik_log" and b.execute(
                     f"SELECT 1 FROM {t} WHERE {k}=? LIMIT 1", (B_id,)).fetchone()]
        if kalan:
            sys.exit("Birleştirilmedi (hiçbir şey yazılmadı): birleşen tedaviyi gösteren kayıt "
                     "kaldı -- " + ", ".join(kalan))
        _hb._logla(b, "cycle", B_id, "BIRLESTIRME",
                   json.dumps({k: B[k] for k in B.keys()}, ensure_ascii=False, default=str),
                   f"{esas} tedavisine birleştirildi", kid, simdi)
        b.execute("DELETE FROM cycle WHERE id=?", (B_id,))
        degisen = _db.tedavileri_sirala(b, A["hasta_id"])
        for cid, _no, e, yn in degisen:
            _hb._logla(b, "cycle", cid, "hasta_cycle_no", e, yn, kid, simdi)
    p["hatalar"] = _hb._arsivi_tasi(*p["arsiv"]) if p["dosyalar"] else []
    p["sira"] = degisen
    return p


def main():
    args = [a for a in sys.argv[1:] if a]
    if len(args) not in (2, 3) or (len(args) == 3 and args[2] != "uygula"):
        sys.exit(__doc__)
    eski, esas = args[0], args[1]
    if eski == esas:
        sys.exit("İki numara aynı.")
    p = plan(eski, esas)
    ozet_yaz(p)
    if p["engel"]:
        sys.exit("\nBirleştirilemez: önce ENGEL satırlarına bakın.")
    if len(args) == 2:
        print(f"\nHiçbir şey yazılmadı. Birleştirmek için:\n"
              f"    python3 tedavi_birlestir.py {eski} {esas} uygula")
        return
    print(f"\n{eski} tedavisi SİLİNECEK, dondurulmuş örnekleri ve kayıtları {esas} "
          "tedavisinin olacak.")
    if input(f'Birleştirmek için "{ONAY}" yazın: ').strip() != ONAY:
        sys.exit("Vazgeçildi.")
    kopya = _hb.onceki_kopya()
    print(f"Önceki hal kopyalandı: {kopya}")
    p = uygula(eski, esas)
    print(f"\nBirleştirildi: {eski} -> {esas}.")
    if p["sira"]:
        print("Tedavi sırası (tarih sırasıyla): "
              + ", ".join(f"{no} {e}.→{yn}." for _c, no, e, yn in p["sira"]))
    if p["dosyalar"] and not p["hatalar"]:
        print(f"Arşiv: {len(p['dosyalar'])} dosya {p['arsiv'][1]} klasörüne taşındı.")
    for h in p["hatalar"]:
        print(f"UYARI: arşivde taşınamadı -- {h}. Veritabanı yeni yolu gösteriyor; "
              "dosyayı elle taşıyın, yoksa fotoğraf görünmez.")
    print("\nProgram açıksa sayfayı yenileyin; kapatıp açmaya gerek yok. Tedavinin "
          "Embriyoloji Özet ve ART Lab formlarına bir bakın.")


if __name__ == "__main__":
    main()
