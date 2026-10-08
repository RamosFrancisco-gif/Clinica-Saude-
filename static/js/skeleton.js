/* Skeleton loading — atua SOMENTE dentro de <main>. O <header> nunca é tocado. */
(function () {
  function initSkeleton(scope) {
    if (!scope) return;

    // 1. Imagens: shimmer + fade-in ao carregar (sem deslocar o layout)
    var imgs = scope.querySelectorAll('img:not([data-skl])');
    imgs.forEach(function (img) {
      img.setAttribute('data-skl', '');
      function done() { img.classList.add('skl-done'); }
      if (img.complete && img.naturalWidth > 0) {
        done();
      } else {
        img.addEventListener('load', done, { once: true });
        img.addEventListener('error', done, { once: true });
        setTimeout(done, 5000); // trava de segurança
      }
    });

    // 2. Blocos marcados com data-skeleton: shimmer até a página terminar de carregar
    var blocks = scope.querySelectorAll('[data-skeleton]:not(.skl)');
    blocks.forEach(function (el) { el.classList.add('skl'); });
    function clearBlocks() {
      blocks.forEach(function (el) { el.classList.remove('skl'); });
    }
    if (document.readyState === 'complete') {
      setTimeout(clearBlocks, 300);
    } else {
      window.addEventListener('load', function () { setTimeout(clearBlocks, 300); }, { once: true });
      setTimeout(clearBlocks, 2000); // trava de segurança
    }
  }

  window.__skl = true;
  document.addEventListener('DOMContentLoaded', function () {
    initSkeleton(document.querySelector('main'));
  });
})();
