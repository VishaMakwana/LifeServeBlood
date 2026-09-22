(function () {
    var minimumDisplayTime = 500;
    var startedAt = Date.now();

    function hideSkeleton() {
        var skeleton = document.querySelector('.site-skeleton');
        if (skeleton) {
            var remainingTime = Math.max(0, minimumDisplayTime - (Date.now() - startedAt));
            window.setTimeout(function () {
                skeleton.classList.add('is-hidden');
            }, remainingTime);
        }
    }

    function showSkeleton() {
        var skeleton = document.querySelector('.site-skeleton');
        if (skeleton) {
            skeleton.classList.remove('is-hidden');
        }
    }

    document.addEventListener('DOMContentLoaded', hideSkeleton);
    window.addEventListener('pageshow', hideSkeleton);

    document.addEventListener('click', function (event) {
        var link = event.target.closest('a[href]');
        if (
            !link
            || link.target === '_blank'
            || link.hasAttribute('download')
            || link.getAttribute('href') === '#'
            || link.hasAttribute('data-bs-toggle')
        ) {
            return;
        }

        var url = new URL(link.href, window.location.href);
        if (url.origin === window.location.origin && url.href !== window.location.href) {
            showSkeleton();
        }
    });
})();
