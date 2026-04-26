(function () {
    var btn = document.querySelector('.nav-toggle');
    var links = document.querySelector('.nav-links');
    if (!btn || !links) return;

    function close() {
        btn.classList.remove('is-open');
        links.classList.remove('is-open');
        btn.setAttribute('aria-expanded', 'false');
    }
    function toggle() {
        var open = btn.classList.toggle('is-open');
        links.classList.toggle('is-open');
        btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    }

    btn.addEventListener('click', toggle);
    links.addEventListener('click', function (e) {
        if (e.target.tagName === 'A') close();
    });
    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') close();
    });
})();
