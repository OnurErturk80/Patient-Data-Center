-- Güncel şema (tüm göçler uygulanmış hali)
PRAGMA foreign_keys = ON;

CREATE TABLE ayarlar (
    id       INTEGER PRIMARY KEY,
    lab_id   INTEGER NOT NULL REFERENCES lab(id),
    anahtar  TEXT NOT NULL,
    deger    TEXT NOT NULL,
    aciklama TEXT,
    UNIQUE (lab_id, anahtar)
);

CREATE TABLE beta_hcg (
    id       INTEGER PRIMARY KEY,
    cycle_id INTEGER NOT NULL REFERENCES cycle(id),
    zaman    TEXT NOT NULL,
    deger    REAL NOT NULL
);

CREATE TABLE cycle (
    id                INTEGER PRIMARY KEY,
    lab_id            INTEGER NOT NULL REFERENCES lab(id),
    hasta_id          INTEGER NOT NULL REFERENCES hasta(id),
    cycle_no          TEXT NOT NULL,
    cycle_tipi        TEXT NOT NULL CHECK (cycle_tipi IN ('taze','fet')),
    endikasyon        TEXT,
    protokol_tipi     TEXT,
    gonadotropin_tipi TEXT,
    baslangic_doz     REAL,
    toplam_doz        REAL,
    stim_gun_sayisi   INTEGER,
    trigger_tipi      TEXT,
    hcg_gunu_e2       REAL,
    hcg_gunu_p4       REAL,
    endometrium_mm    REAL,
    folikul_sayisi    INTEGER,
    amh               REAL,
    afc               INTEGER,
    protokol_notu     TEXT,
    hcg_zamani        TEXT,
    opu_zamani        TEXT,
    denudasyon_zamani TEXT,
    opu_sag_oosit     INTEGER,
    opu_sol_oosit     INTEGER,
    durum             TEXT NOT NULL DEFAULT 'aktif',
    olusturma_zamani  TEXT NOT NULL DEFAULT (datetime('now')), hasta_cycle_no INTEGER,
    UNIQUE (lab_id, cycle_no)
);

CREATE TABLE degisiklik_log (
    id           INTEGER PRIMARY KEY,
    lab_id       INTEGER NOT NULL REFERENCES lab(id),
    tablo_adi    TEXT NOT NULL,
    kayit_id     TEXT NOT NULL,
    alan         TEXT NOT NULL,
    eski_deger   TEXT,
    yeni_deger   TEXT,
    kullanici_id INTEGER NOT NULL REFERENCES kullanici(id),
    zaman        TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE gebelik_sonucu (
    id                    INTEGER PRIMARY KEY,
    lab_id                INTEGER NOT NULL REFERENCES lab(id),
    cycle_id              INTEGER NOT NULL REFERENCES cycle(id),
    klinik_gebelik        TEXT,
    gebelik_kesesi_sayisi INTEGER,
    fk_pozitif            TEXT,
    fk_kontrol_zamani     TEXT,
    sonlanma              TEXT,
    dogum_zamani          TEXT,
    bebek_sayisi          INTEGER,
    guncelleme_zamani     TEXT
);

CREATE TABLE goruntu (
    id                 INTEGER PRIMARY KEY,
    lab_id             INTEGER NOT NULL REFERENCES lab(id),
    cycle_id           INTEGER NOT NULL REFERENCES cycle(id),
    specimen_id        TEXT REFERENCES specimen(id),
    asama              TEXT NOT NULL,
    zaman              TEXT NOT NULL,
    dosya_yolu         TEXT NOT NULL,
    orijinal_dosya_adi TEXT,
    kullanici_id       INTEGER REFERENCES kullanici(id),
    olusturma_zamani   TEXT NOT NULL DEFAULT (datetime('now'))
, kaynak_imza TEXT, kaynak TEXT NOT NULL DEFAULT 'kamera');

CREATE TABLE hasta (
    id               INTEGER PRIMARY KEY,
    lab_id           INTEGER NOT NULL REFERENCES lab(id),
    dosya_no         INTEGER NOT NULL,
    ad_soyad         TEXT NOT NULL,
    dogum_tarihi     TEXT,
    es_adi           TEXT,
    es_dogum_tarihi  TEXT,
    notlar           TEXT,
    olusturma_zamani TEXT NOT NULL DEFAULT (datetime('now')), durum TEXT NOT NULL DEFAULT 'aktif',
    UNIQUE (lab_id, dosya_no)
);

CREATE TABLE kaynak_dosya (
    imza       TEXT PRIMARY KEY,
    dosya_adi  TEXT NOT NULL,
    cycle_id   INTEGER REFERENCES cycle(id),
    goruntu_id INTEGER REFERENCES goruntu(id),
    durum      TEXT NOT NULL,          -- eslesti / atlandi
    zaman      TEXT NOT NULL
);

CREATE TABLE konum (
    id       INTEGER PRIMARY KEY,
    lab_id   INTEGER NOT NULL REFERENCES lab(id),
    seviye1  TEXT,
    seviye2  TEXT,
    seviye3  TEXT,
    seviye4  TEXT,
    tam_yol  TEXT NOT NULL,
    durum    TEXT NOT NULL DEFAULT 'bos',
    UNIQUE (lab_id, tam_yol)
);

CREATE TABLE konum_semasi (
    id            INTEGER PRIMARY KEY,
    lab_id        INTEGER NOT NULL REFERENCES lab(id),
    seviye_sirasi INTEGER NOT NULL,
    seviye_adi    TEXT NOT NULL,
    deger_tipi    TEXT NOT NULL,
    UNIQUE (lab_id, seviye_sirasi)
);

CREATE TABLE kullanici (
    id               INTEGER PRIMARY KEY,
    lab_id           INTEGER NOT NULL REFERENCES lab(id),
    ad_soyad         TEXT NOT NULL,
    kisa_kod         TEXT NOT NULL,
    rol              TEXT NOT NULL,
    kullanici_adi    TEXT NOT NULL UNIQUE,
    sifre_hash       TEXT NOT NULL,
    aktif_mi         INTEGER NOT NULL DEFAULT 1,
    olusturma_zamani TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE lab (
    id               INTEGER PRIMARY KEY,
    ad               TEXT NOT NULL,
    aktif_mi         INTEGER NOT NULL DEFAULT 1,
    olusturma_zamani TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE liste_degeri (
    id        INTEGER PRIMARY KEY,
    lab_id    INTEGER NOT NULL REFERENCES lab(id),
    liste_adi TEXT NOT NULL,
    kod       TEXT NOT NULL,
    etiket    TEXT NOT NULL,
    sira      INTEGER NOT NULL DEFAULT 0,
    aktif_mi  INTEGER NOT NULL DEFAULT 1,
    UNIQUE (lab_id, liste_adi, kod)
);

CREATE TABLE olay (
    id                 INTEGER PRIMARY KEY,
    lab_id             INTEGER NOT NULL REFERENCES lab(id),
    specimen_id        TEXT REFERENCES specimen(id),
    cycle_id           INTEGER NOT NULL REFERENCES cycle(id),
    tip                TEXT NOT NULL,
    zaman              TEXT NOT NULL,
    kullanici_id       INTEGER NOT NULL REFERENCES kullanici(id),
    gun                INTEGER,
    notlar             TEXT,

    mat_deger          TEXT,
    icsi_gecis_zorlugu TEXT,
    icsi_sonuc         TEXT,
    fert_sonuc         TEXT,
    fert_pn_sayisi     TEXT,
    fert_pn_skoru      TEXT,
    cl_hucre_sayisi    INTEGER,
    cl_simetri         TEXT,
    cl_fragmentasyon   REAL,
    cl_skor            TEXT,
    cl_skor_kaynagi    TEXT,
    bl_genisleme       TEXT,
    bl_icm             TEXT,
    bl_te              TEXT,
    bl_skor            TEXT,
    bl_skor_kaynagi    TEXT,
    biy_tip            TEXT,
    biy_hucre_sayisi   INTEGER,
    biy_tup_etiketi    TEXT,
    biy_sonuc          TEXT,
    vit_tasiyici_id    INTEGER REFERENCES tasiyici(id),
    thaw_sagkalim      TEXT,
    thaw_re_expansion  REAL,
    thaw_cycle_id      INTEGER REFERENCES cycle(id),
    tr_cycle_id        INTEGER REFERENCES cycle(id),
    tr_tipi            TEXT,
    dis_sebep          TEXT,

    iptal_mi           INTEGER NOT NULL DEFAULT 0,
    iptal_kullanici_id INTEGER REFERENCES kullanici(id),
    iptal_zamani       TEXT,
    iptal_sebep        TEXT,
    olusturma_zamani   TEXT NOT NULL DEFAULT (datetime('now')), bl_derece TEXT,

    CHECK (tip IN ('denudasyon','maturasyon_kontrolu','icsi','fertilizasyon_kontrolu',
                   'cleavage_degerlendirme','blastokist_degerlendirme','biyopsi',
                   'vitrifikasyon','thaw','transfer','discard'))
);

CREATE TABLE oturum (
    jeton TEXT PRIMARY KEY,
    kullanici_id INTEGER NOT NULL REFERENCES kullanici(id),
    olusturma TEXT NOT NULL, son_erisim TEXT NOT NULL);

CREATE TABLE pgt_sonuc (
    id                    INTEGER PRIMARY KEY,
    lab_id                INTEGER NOT NULL REFERENCES lab(id),
    specimen_id           TEXT NOT NULL REFERENCES specimen(id),
    tup_etiketi           TEXT NOT NULL,
    gonderim_zamani       TEXT,
    laboratuvar           TEXT,
    test_tipi             TEXT,
    sonuc_zamani          TEXT,
    sonuc                 TEXT,
    mozaik_yuzde          REAL,
    detay                 TEXT,
    karar                 TEXT,
    rapor_dosya_yolu      TEXT,
    kaydeden_kullanici_id INTEGER REFERENCES kullanici(id),
    olusturma_zamani      TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE specimen (
    id               TEXT PRIMARY KEY,
    lab_id           INTEGER NOT NULL REFERENCES lab(id),
    cycle_id         INTEGER NOT NULL REFERENCES cycle(id),
    cycle_sira_no    INTEGER NOT NULL,
    durum            TEXT NOT NULL,
    olusturma_zamani TEXT NOT NULL DEFAULT (datetime('now')),
    UNIQUE (cycle_id, cycle_sira_no)
);

CREATE TABLE specimen_bulgu (
    id           INTEGER PRIMARY KEY,
    specimen_id  TEXT NOT NULL REFERENCES specimen(id),
    asama        TEXT NOT NULL,
    bulgu_kodu   TEXT NOT NULL,
    zaman        TEXT NOT NULL,
    kullanici_id INTEGER NOT NULL REFERENCES kullanici(id)
);

CREATE TABLE sperm_analiz (
    id                      INTEGER PRIMARY KEY,
    sperm_ornek_id          INTEGER NOT NULL REFERENCES sperm_ornek(id),
    asama                   TEXT NOT NULL CHECK (asama IN ('bazal','hazirlik_sonrasi')),
    zaman                   TEXT NOT NULL,
    kullanici_id            INTEGER REFERENCES kullanici(id),
    hacim_ml                REAL,
    konsantrasyon_milyon_ml REAL,
    pr_yuzde                REAL,
    np_yuzde                REAL,
    im_yuzde                REAL,
    toplam_motil_sayi       REAL,
    notlar                  TEXT
);

CREATE TABLE sperm_ornek (
    id                  INTEGER PRIMARY KEY,
    lab_id              INTEGER NOT NULL REFERENCES lab(id),
    cycle_id            INTEGER NOT NULL REFERENCES cycle(id),
    alinma_zamani       TEXT,
    alinma_yontemi      TEXT,
    abstinans_gun       INTEGER,
    likefaksiyon_zamani TEXT,
    hacim_ml            REAL,
    viskozite           TEXT,
    renk                TEXT,
    ph                  REAL,
    hazirlama_yontemi   TEXT,
    hazirlama_zamani    TEXT,
    kullanici_id        INTEGER REFERENCES kullanici(id),
    notlar              TEXT,
    olusturma_zamani    TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE tasiyici (
    id                   INTEGER PRIMARY KEY,
    lab_id               INTEGER NOT NULL REFERENCES lab(id),
    tip                  TEXT NOT NULL,
    etiket               TEXT NOT NULL,
    renk                 TEXT,
    konum_id             INTEGER REFERENCES konum(id),
    vitrifikasyon_zamani TEXT,
    kullanici_id         INTEGER REFERENCES kullanici(id),
    durum                TEXT NOT NULL DEFAULT 'dolu',
    UNIQUE (lab_id, etiket)
);

CREATE TABLE islem_yapan (
    id           INTEGER PRIMARY KEY,
    lab_id       INTEGER NOT NULL REFERENCES lab(id),
    cycle_id     INTEGER NOT NULL REFERENCES cycle(id),
    asama        TEXT NOT NULL,
    yapan_ad     TEXT,
    zaman        TEXT,
    kullanici_id INTEGER REFERENCES kullanici(id),
    UNIQUE (cycle_id, asama)
);

CREATE INDEX idx_bulgu_specimen   ON specimen_bulgu(specimen_id, asama);

CREATE INDEX idx_islem_yapan_cycle ON islem_yapan(cycle_id);

CREATE INDEX idx_cycle_hasta      ON cycle(hasta_id);

CREATE INDEX idx_cycle_opu        ON cycle(opu_zamani);

CREATE INDEX idx_goruntu_cycle    ON goruntu(cycle_id);

CREATE INDEX idx_goruntu_specimen ON goruntu(specimen_id, asama);

CREATE INDEX idx_olay_cycle_tip   ON olay(cycle_id, tip);

CREATE INDEX idx_olay_specimen    ON olay(specimen_id, tip);

CREATE INDEX idx_olay_zaman       ON olay(zaman);

CREATE INDEX idx_specimen_cycle   ON specimen(cycle_id);

CREATE INDEX idx_tasiyici_konum   ON tasiyici(konum_id);
