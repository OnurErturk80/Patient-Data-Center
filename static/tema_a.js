/* "Klinik Koyu" açılır pencereleri (v6.254). Yalnızca tasarım açıkken
   yüklenir (base.html). Şablonlara DOKUNMAZ: seçili bağlantılara (aşağıdaki
   YOLLAR) tıklanınca hedef ekran getirilir, içeriği (`.kap`) pencerede
   gösterilir -- telefonda alttan açılan pencere, masaüstünde ortada.
   Form pencerenin içinden gönderilir; başarıyla biterse (yönlendirme) ana
   sayfa yenilenir ya da yeni ekrana gidilir, hata dönerse hata pencerede
   görünür, yazılanlar silinmez. Betik hata verirse bağlantı eskisi gibi
   sayfa olarak açılır: pencere yalnızca kolaylık, işlev ona bağlı değil.
   `data-pencere-icerik` olan bir öğe hedef ekranda varsa yalnızca o(lar)
   gösterilir (toplu maturasyon kartı gibi). */
(function () {
  'use strict';
  if (window.pdcPencereKuruldu) return;
  window.pdcPencereKuruldu = true;

  var YOLLAR = [
    /^\/hasta\/yeni$/,
    /^\/hasta\/\d+\/(duzenle|cycle\/yeni|sperm-dondurma\/yeni|sil)$/,
    /^\/cycle\/\d+\/(duzenle|bitir|foto-ekle|sil|arsiv-sil)$/,
    /^\/specimen\/\d+\/[a-z]+-sil$/,
    /^\/specimen\/\d+\/sil$/,
    /^\/goruntu\/\d+\/sil$/,
    /^\/sperm-dondurma\/yeni-hasta$/,
    /^\/cryo\/tasima(\/hasta\/\d+)?$/
  ];

  function pencereMi(a) {
    if (!a || a.target === '_blank' || a.hasAttribute('download') ||
        a.hasAttribute('data-pencere-yok')) return false;
    var u;
    try { u = new URL(a.href, location.href); } catch (e) { return false; }
    if (u.origin !== location.origin) return false;
    if (u.pathname === location.pathname && u.search === location.search) return false;
    if (/[?&]duzenle=toplu(&|$)/.test(u.search)) return true;
    for (var i = 0; i < YOLLAR.length; i++) if (YOLLAR[i].test(u.pathname)) return true;
    return false;
  }

  /* ---- işlem sürerken gösterge (v6.260, kullanıcının isteği: "Programda bir
     işlem sürerken kullanıcı programın ilgilendiğini gösteren belirteç olsun").
     Sayfa geçişlerinin üst çizgisini base.html'in gezinti betiği zaten çiziyor
     (`.yukleniyor`, 150 ms); burada eksik olanlar: basılan düğmenin "İşleniyor…"
     olması, aynı formun ikinci kez gönderilmesinin engellenmesi, pencere içi
     formlar ve yanıt gelmezse uyarı. Hızlı işlemde (BEKLE_SURESI altında)
     hiçbir şey değişmez. Sunucuya hiçbir şey gönderilmez, yalnızca görünüm. */
  var BEKLE_SURESI = 400, KILIT_SURESI = 8000, YANIT_SURESI = 120000;
  var etiket = function () { return (document.getElementById('asamaetiket') || {}).dataset || {}; };
  var bekleyenler = [];

  function bildir(metin) {
    var n = document.getElementById('pdcBildirim');
    if (!n) {
      n = document.createElement('div');
      n.id = 'pdcBildirim';
      n.className = 'pdcbildirim';
      n.setAttribute('role', 'alert');
      document.body.appendChild(n);
    }
    n.textContent = metin;
    n.hidden = false;
    clearTimeout(n._z);
    n._z = setTimeout(function () { n.hidden = true; }, 7000);
  }

  function formunDugmesi(form, dugme) {
    return dugme || form.querySelector('button[type=submit], button:not([type]), input[type=submit]');
  }

  // Düğmeyi "İşleniyor…" yapar (BEKLE_SURESI sonra); dönen işlev eski haline getirir.
  function bekleBasla(form, dugme, yanitYokta) {
    var d = formunDugmesi(form, dugme);
    var durum = { form: form, d: d, bitti: false, eski: null };
    form.dataset.pdcGonderildi = String(Date.now());
    durum.z1 = setTimeout(function () {
      if (durum.bitti) return;
      form.classList.add('pdc-bekliyor');
      form.setAttribute('aria-busy', 'true');
      if (d) {
        durum.eski = d.tagName === 'INPUT' ? d.value : d.innerHTML;
        var yazi = etiket().bekle || '\u0130\u015fleniyor\u2026';
        if (d.tagName === 'INPUT') d.value = yazi;
        else d.innerHTML = '<span class="pdcdonus" aria-hidden="true"></span><span>' + yazi.replace(/</g, '&lt;') + '</span>';
        d.disabled = true;
        d.classList.add('pdc-bekliyor');
      }
    }, BEKLE_SURESI);
    // Çok uzun süren bilinen işlerde (yedek, geri yükleme, taşıma) uyarı yok:
    // yeniden basılması yanıt gelmemesinden daha tehlikeli.
    var uzunIs = /\/(yedekleme|tasi|kurulum)/.test(form.getAttribute('action') || '');
    if (!uzunIs) durum.z2 = setTimeout(function () {
      if (durum.bitti) return;
      bitir();
      bildir(etiket().yanitYok || 'Sunucudan yan\u0131t gelmedi. Ba\u011flant\u0131y\u0131 kontrol edip yeniden deneyin.');
    }, yanitYokta || YANIT_SURESI);
    function bitir() {
      if (durum.bitti) return;
      durum.bitti = true;
      clearTimeout(durum.z1); clearTimeout(durum.z2);
      form.classList.remove('pdc-bekliyor');
      form.removeAttribute('aria-busy');
      delete form.dataset.pdcGonderildi;
      if (d && durum.eski !== null) {
        if (d.tagName === 'INPUT') d.value = durum.eski; else d.innerHTML = durum.eski;
        d.disabled = false;
        d.classList.remove('pdc-bekliyor');
      }
    }
    durum.bitir = bitir;
    bekleyenler.push(durum);
    return bitir;
  }
  window.pdcBekleBasla = bekleBasla;

  function sessizMi(form) {
    var hedef = (form.getAttribute('target') || '').toLowerCase();
    var yol = form.getAttribute('action') || '';
    return hedef === '_blank' || yol.indexOf('/disari/') !== -1 ||
      form.hasAttribute('data-pdc-sessiz');
  }

  // İkinci gönderim (çift tık, yavaş yanıtta tekrar basma) engellenir.
  document.addEventListener('submit', function (e) {
    var f = e.target;
    if (!f || f.tagName !== 'FORM' || sessizMi(f)) return;
    var onceki = Number(f.dataset.pdcGonderildi || 0);
    if (onceki && Date.now() - onceki < KILIT_SURESI) {
      e.preventDefault(); e.stopImmediatePropagation();
    }
  }, true);
  // Başka bir işlev göndermeyi iptal etmediyse (onay penceresi, doğrulama) bekleme başlar.
  document.addEventListener('submit', function (e) {
    var f = e.target;
    if (!f || f.tagName !== 'FORM' || e.defaultPrevented || sessizMi(f)) return;
    if (f.dataset.pdcGonderildi) return;
    bekleBasla(f, e.submitter);
    // Kilit yalnızca birkaç saniye: sayfa yerinde kalırsa (indirme) yeniden basılabilsin.
    setTimeout(function () { delete f.dataset.pdcGonderildi; }, KILIT_SURESI);
  });
  // Önbellekten geri dönülen sayfada kilitli düğme kalmasın.
  window.addEventListener('pageshow', function (e) {
    if (!e.persisted) return;
    bekleyenler.forEach(function (b) { b.bitir(); });
    bekleyenler = [];
  });

  /* Aşama ekranları: aşama listesi (`nav.yanmenu`) taslaktaki adım şeridine
     çevrilir, yerine ana menü konur (base.html'deki şablon). Menü zaten
     sayfada; bu yalnızca görünümünü değiştirir, bağlantılar aynı. */
  function asamaSeridi() {
    var baslik = document.querySelector('nav.yanmenu a.baslik');
    var nav = baslik && baslik.closest('nav');
    var kap = document.querySelector('.kap');
    if (!nav || !kap || document.querySelector('.asamaseridi')) return;
    var ogeler = Array.prototype.slice.call(nav.querySelectorAll('a.oge'));
    if (!ogeler.length) return;
    var aktif = -1;
    ogeler.forEach(function (o, i) { if (o.classList.contains('aktif')) aktif = i; });
    var D = (document.getElementById('asamaetiket') || {}).dataset || {};
    var toplam = ogeler.length;
    // Sunucu "veri kaydedilmiş mi" söylüyorsa (data-tamam) ✓ ona göre; söylemiyorsa
    // (yeniden başlatılmamış program) eski gibi geçerli aşamadan öncekiler.
    var veriVar = ogeler.some(function (o) { return o.hasAttribute('data-tamam'); });
    function tamamMi(o, i) {
      return veriVar ? o.getAttribute('data-tamam') === '1' : (aktif > -1 && i < aktif);
    }
    var tamamSayisi = ogeler.filter(tamamMi).length;
    var kutu_ = document.createElement('div');
    kutu_.className = 'asamakap';
    var ust_ = document.createElement('div');
    ust_.className = 'asamaust';
    var et = document.createElement('span');
    et.className = 'et';
    et.appendChild(document.createTextNode((D.baslik || 'Tedavi aşamaları')));
    if (veriVar || aktif > -1) {
      var b = document.createElement('b');
      b.textContent = ' \u00b7 ' + (veriVar ? tamamSayisi : aktif + 1) + ' / ' + toplam;
      et.appendChild(b);
    }
    ust_.appendChild(et);
    var alan = document.createElement('div');
    alan.className = 'asamaalan';
    var ser = document.createElement('nav');
    ser.className = 'asamaseridi';
    ser.setAttribute('aria-label', nav.getAttribute('aria-label') || '');
    ogeler.forEach(function (o, i) {
      var a = document.createElement('a');
      a.href = o.getAttribute('href');
      var kayitli = tamamMi(o, i);
      var durum = i === aktif ? 'simdi' : (kayitli ? 'bitti' : 'bekle');
      a.className = 'adim ' + durum + (kayitli ? ' kayitli' : '') +
        (i === 0 ? ' pri' : '') + (i === toplam - 1 ? ' son' : '');
      if (i === aktif) a.setAttribute('aria-current', 'step');
      var n = document.createElement('span');
      n.className = 'no';
      n.textContent = durum === 'bitti' ? (D.tamam || 'Tamam')
        : durum === 'simdi' ? (D.simdi || 'Şimdi')
        : (D.asama || 'Aşama {n}').replace('{n}', i + 1);
      var t = document.createElement('span');
      t.className = 'ad';
      t.textContent = o.textContent.trim();
      a.appendChild(n); a.appendChild(t);
      if (durum === 'simdi') {
        var h = document.createElement('div');   // gölge clip-path'e kırpılmasın
        h.className = 'halka';
        h.appendChild(a);
        ser.appendChild(h);
      } else ser.appendChild(a);
    });
    alan.appendChild(ser);
    var ilr = document.createElement('div');
    ilr.className = 'ilerleme';
    var dolu = document.createElement('i');
    dolu.style.width = Math.round((veriVar ? tamamSayisi : (aktif > -1 ? aktif + 1 : 0)) * 100 / toplam) + '%';
    ilr.appendChild(dolu);
    kutu_.appendChild(ust_); kutu_.appendChild(alan); kutu_.appendChild(ilr);
    function kenarlar() {
      alan.classList.toggle('sol', ser.scrollLeft > 4);
      alan.classList.toggle('sag', ser.scrollLeft + ser.clientWidth < ser.scrollWidth - 4);
    }
    ser.addEventListener('scroll', kenarlar, { passive: true });
    window.addEventListener('resize', kenarlar);
    var ustCubuk = document.querySelector('.ust');
    if (ustCubuk) document.documentElement.style.setProperty('--ust-h', ustCubuk.offsetHeight + 'px');
    kap.insertBefore(kutu_, kap.firstChild);
    var sablon = document.getElementById('anamenusablon');
    // Ana menü gövdede, `.kap`'ın KARDEŞİ olmalı (CSS `.yanmenu ~ .kap`):
    // aşama listesi başka bir kabın içinde duruyor olabilir.
    if (sablon && sablon.content && sablon.parentNode) {
      nav.parentNode.removeChild(nav);
      sablon.parentNode.insertBefore(sablon.content.cloneNode(true), sablon);
    } else nav.hidden = true;
    var simdi = ser.querySelector('.simdi');
    // Geçerli bölmeyi ortala (yalnızca şerit kayıyorsa); kenar solmaları.
    if (simdi && ser.scrollWidth > ser.clientWidth + 2) {
      var hedef = simdi.parentNode.classList.contains('halka') ? simdi.parentNode : simdi;
      try { ser.scrollLeft = Math.max(0, hedef.offsetLeft - (ser.clientWidth - hedef.offsetWidth) / 2); } catch (e) {}
    }
    kenarlar();
    // Fotoğraflı aşama ekranı: taslaktaki gibi iki sütun (fotoğraf | bilgi).
    if (kap.querySelector(':scope > .foto')) kap.classList.add('asamaekrani');
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', asamaSeridi);
  else asamaSeridi();

  var perde, kutu, govde, baslikEl, acik = false, sonOdak = null;

  function kur() {
    if (perde) return;
    perde = document.createElement('div');
    perde.className = 'pencereperde';
    perde.hidden = true;
    perde.innerHTML =
      '<div class="pencere" role="dialog" aria-modal="true" aria-labelledby="pencerebaslik" tabindex="-1">' +
      '<div class="pencere-tutac" aria-hidden="true"></div>' +
      '<div class="pencere-ust"><h2 id="pencerebaslik"></h2>' +
      '<button type="button" class="pencere-kapat" aria-label="Kapat">&#10005;</button></div>' +
      '<div class="pencere-govde"></div></div>';
    document.body.appendChild(perde);
    kutu = perde.querySelector('.pencere');
    govde = perde.querySelector('.pencere-govde');
    baslikEl = perde.querySelector('#pencerebaslik');
    perde.addEventListener('mousedown', function (e) { if (e.target === perde) kapat(); });
    perde.querySelector('.pencere-kapat').addEventListener('click', kapat);
    document.addEventListener('keydown', function (e) {
      if (!acik) return;
      if (e.key === 'Escape') { e.preventDefault(); kapat(); }
      else if (e.key === 'Tab') odakTuzagi(e);
    });
    // Aşağı sürükleyerek kapatma (telefon): tutacaktan.
    var y0 = null;
    var tutac = perde.querySelector('.pencere-tutac'), ust = perde.querySelector('.pencere-ust');
    [tutac, ust].forEach(function (el) {
      el.addEventListener('touchstart', function (e) { y0 = e.touches[0].clientY; }, { passive: true });
      el.addEventListener('touchmove', function (e) {
        if (y0 === null) return;
        var d = e.touches[0].clientY - y0;
        if (d > 0) kutu.style.transform = 'translateY(' + d + 'px)';
      }, { passive: true });
      el.addEventListener('touchend', function (e) {
        if (y0 === null) return;
        var d = (e.changedTouches[0].clientY - y0);
        y0 = null; kutu.style.transform = '';
        if (d > 110) kapat();
      });
    });
  }

  function odaklanabilirler() {
    return kutu.querySelectorAll('a[href],button:not([disabled]),input:not([disabled]):not([type=hidden]),select:not([disabled]),textarea:not([disabled]),[tabindex]:not([tabindex="-1"])');
  }
  function odakTuzagi(e) {
    var l = Array.prototype.filter.call(odaklanabilirler(), function (x) { return x.offsetParent !== null; });
    if (!l.length) { e.preventDefault(); return; }
    var ilk = l[0], son = l[l.length - 1];
    if (e.shiftKey && document.activeElement === ilk) { e.preventDefault(); son.focus(); }
    else if (!e.shiftKey && document.activeElement === son) { e.preventDefault(); ilk.focus(); }
  }

  function kapat() {
    if (!acik) return;
    acik = false;
    perde.hidden = true;
    document.documentElement.classList.remove('pencere-acik');
    govde.innerHTML = '';
    if (sonOdak && sonOdak.focus) { try { sonOdak.focus(); } catch (e) {} }
  }

  // Pencere açıkken ana sayfa kendiliğinden yenilenmesin (tazeleme, v6.54).
  var eskiGeziniyor = window.pdcGeziniyor;
  window.pdcGeziniyor = function () { return acik || (eskiGeziniyor ? eskiGeziniyor() : false); };

  function icerikCikar(doc) {
    var secili = doc.querySelectorAll('[data-pencere-icerik]');
    var kap = doc.querySelector('.kap');
    var kutuEl = document.createElement('div');
    if (secili.length) {
      var uy = doc.querySelectorAll('.kap > .uyari');
      Array.prototype.forEach.call(uy, function (n) { kutuEl.appendChild(n.cloneNode(true)); });
      Array.prototype.forEach.call(secili, function (n) { kutuEl.appendChild(n.cloneNode(true)); });
      if (kap) Array.prototype.forEach.call(kap.querySelectorAll('script'), function (s) { kutuEl.appendChild(s.cloneNode(true)); });
    } else if (kap) {
      kutuEl.innerHTML = kap.innerHTML;
    } else {
      return null;
    }
    // Pencerede ayrıca bir başlık var: içeriğin ilk kart başlığı tekrar etmesin.
    return kutuEl;
  }

  function baslikBul(doc, kok, yedek) {
    if (yedek) return yedek;
    var h = kok.querySelector('h2');
    if (h && h.textContent.trim()) { var t = h.textContent.trim(); return t.length > 60 ? yedek : t; }
    var ust = doc.querySelector('.ust h1');
    return (yedek || (ust && ust.textContent.trim()) || '');
  }

  function doldur(html, yedekBaslik) {
    var doc = new DOMParser().parseFromString(html, 'text/html');
    var kok = icerikCikar(doc);
    if (!kok) return false;
    baslikEl.textContent = baslikBul(doc, kok, yedekBaslik);
    govde.innerHTML = '';
    // Betikler DOMParser'da çalışmaz; yeniden yaratılıp çalıştırılır.
    var betikler = [];
    Array.prototype.forEach.call(kok.querySelectorAll('script'), function (s) {
      var y = document.createElement('script');
      if (s.src) y.src = s.src; else y.text = s.textContent;
      betikler.push(y); s.parentNode.removeChild(s);
    });
    while (kok.firstChild) govde.appendChild(kok.firstChild);
    betikler.forEach(function (y) { try { govde.appendChild(y); } catch (e) {} });
    // İçerik başlığı pencerenin başlığıyla aynıysa tekrar etme.
    var ic = govde.querySelector('[data-pencere-icerik] > h2');
    if (ic) { baslikEl.textContent = ic.textContent.trim(); ic.hidden = true; }
    var h = govde.querySelector('h2');
    if (h && h.textContent.trim() === baslikEl.textContent.trim()) h.hidden = true;
    bagla();
    return true;
  }

  function bagla() {
    Array.prototype.forEach.call(govde.querySelectorAll('form'), function (f) {
      if (f.method && f.method.toLowerCase() !== 'post') {
        // GET formları (arama gibi) pencerede anlamsız: normal gönderim.
        return;
      }
      f.addEventListener('submit', function (e) {
        if (e.defaultPrevented) return;
        e.preventDefault();
        gonder(f, e.submitter);
      });
    });
    Array.prototype.forEach.call(govde.querySelectorAll('a[href]'), function (a) {
      a.addEventListener('click', function (e) {
        if (e.defaultPrevented || e.ctrlKey || e.metaKey || e.shiftKey || e.button) return;
        var u; try { u = new URL(a.href, location.href); } catch (x) { return; }
        if (a.getAttribute('href').charAt(0) === '#') return;
        // Aynı ekrana dönen bağlantı ("Vazgeç") pencereyi kapatır.
        if (u.origin === location.origin && u.pathname === location.pathname) {
          e.preventDefault(); kapat();
        }
      });
    });
    var ilk = govde.querySelector('input:not([type=hidden]):not([type=radio]):not([type=checkbox]),select,textarea');
    (ilk || kutu).focus({ preventScroll: true });
  }

  function mesgul(a) { kutu.classList.toggle('mesgul', a); }

  function gonder(form, dugme) {
    var veri = new FormData(form);
    if (dugme && dugme.name) veri.append(dugme.name, dugme.value);
    mesgul(true);
    var bekleBitir = bekleBasla(form, dugme);
    fetch(form.getAttribute('action') || location.href, {
      method: 'POST', body: veri, credentials: 'same-origin',
      headers: { 'X-Pencere': '1' }
    }).then(function (r) {
      return r.text().then(function (t) { return { r: r, t: t }; });
    }).then(function (s) {
      mesgul(false);
      var u = new URL(s.r.url, location.href);
      var basari = s.r.ok && !(/[?&]hata=/.test(u.search) || !s.r.redirected);
      if (!basari) bekleBitir();   // başarıda sayfa değişiyor, düğme kilitli kalsın
      var hataVar = /[?&]hata=/.test(u.search) || !s.r.redirected;
      if (s.r.ok && !hataVar) {
        // Başarı: aynı ekransa yenile, başka ekransa oraya git.
        if (u.pathname === location.pathname) location.reload();
        else location.href = u.pathname + u.search;
        return;
      }
      if (!doldur(s.t, baslikEl.textContent)) location.href = u.pathname + u.search;
    }).catch(function () { mesgul(false); bekleBitir(); form.submit(); });
  }

  function ac(a) {
    kur();
    sonOdak = a;
    var yedek = (a.getAttribute('data-baslik') || a.textContent || '').replace(/\s+/g, ' ').trim();
    return fetch(a.href, { credentials: 'same-origin', headers: { 'X-Pencere': '1' } })
      .then(function (r) {
        if (!r.ok || r.redirected && new URL(r.url).pathname.indexOf('/giris') === 0) throw new Error('x');
        return r.text();
      })
      .then(function (t) {
        if (!doldur(t, yedek.length > 40 ? '' : yedek)) throw new Error('x');
        acik = true; perde.hidden = false;
        document.documentElement.classList.add('pencere-acik');
        kutu.scrollTop = 0; govde.scrollTop = 0;
        var ilk = govde.querySelector('input:not([type=hidden]):not([type=radio]):not([type=checkbox]),select,textarea');
        (ilk || kutu).focus({ preventScroll: true });
      });
  }

  document.addEventListener('click', function (e) {
    if (e.defaultPrevented || e.ctrlKey || e.metaKey || e.shiftKey || e.altKey || e.button) return;
    var a = e.target.closest ? e.target.closest('a[href]') : null;
    if (!a || (perde && perde.contains(a)) || !pencereMi(a)) return;
    e.preventDefault();
    ac(a).catch(function () { location.href = a.href; });
  }, true);
})();
